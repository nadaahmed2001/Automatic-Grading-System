from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm, TeacherRegistrationForm, StudentProfileForm, TeacherProfileForm
from .forms import ExamForm
from .models import Exam, ExamSubmission
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from AIGradingModel.grading import StartGrading, StartGradingOCR

from AIGradingModel.OCR_Model.OCR_Gemini_Model import OCR_Gemini_Model #Gemeni
from AIGradingModel.OCR_Model.OCR_Space_Model import OCR_Space_Model #OCR Space
from AIGradingModel.OCR_Model.OCR_Verify_Model import OCR_Verify_Model #Verify

from .models import ExamSubmissionOCR
from django.core.files.storage import FileSystemStorage
from AIGradingModel import generativeAI
from AIGradingModel.exportGrades import export_ocr_grades_to_excel
from django.http import JsonResponse
import json
import math
from django.db.models import F
import decimal
from django.conf import settings

def index(request):
    return render(request, 'myapp/index.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        print("Form data:", request.POST)  # Debugging
        if form.is_valid():
            user = form.save()
           
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Registration unsuccessful. Please enter valid data')
            print("Form errors:", form.errors)  # Debug form errors
    else:
        form = StudentRegistrationForm()
    return render(request, 'myapp/student/register_student2.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Instead of logging in the user, redirect to the login page
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Registration unsuccessful. Please enter valid data')
            print("Form errors:", form.errors)  # Debug form errors
    else:
        form = TeacherRegistrationForm()
    return render(request, 'myapp/teacher/register_teacher2.html', {'form': form})

def login_view(request):
    print("CSRF Token from form:", request.POST.get('csrfmiddlewaretoken'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Username:", username)
        print("Password:", password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.userType == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'myapp/login.html')


def logout_view(request):
    logout(request)
    # return to login page
    return redirect('login')

def student_dashboard(request):
    if not hasattr(request.user, 'student'): # Check if the user is a student
        return HttpResponseForbidden("You are not authorized to view this page.")
    student_submissions = ExamSubmission.objects.filter(student=request.user)
    return render(request, 'myapp/student/student_dashboard.html', {'student_submissions': student_submissions})

def teacher_dashboard(request):
    if not hasattr(request.user, 'teacher'): # Check if the user is a teacher
        return HttpResponseForbidden("You are not authorized to view this page.")
    exams = Exam.objects.filter(teacher=request.user)
    return render(request, 'myapp/teacher/teacher_dashboard.html', {'exams': exams})

@login_required
def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            print("Exam Form is valid")
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            messages.success(request, 'Exam created successfully.')
            return redirect('teacher_dashboard')
    else:
        form = ExamForm()
    return render(request, 'myapp/teacher/create_exam.html', {'form': form})

@login_required
def view_exam_teacher(request, exam_id): #this will redirect to the specific exam page where the teacher can view the exam details
    exam = Exam.objects.get(pk=exam_id)
    exam_submissions = ExamSubmission.objects.filter(exam=exam)
    if not (request.user == exam.teacher or hasattr(request.user, 'teacher')):
        return HttpResponseForbidden("You are not authorized to view this exam.")
    return render(request, 'myapp/teacher/view_exam.html', {'exam': exam, 'exam_submissions': exam_submissions})
    # sent exam submissions to determine if this exam is graded or not

@login_required
def view_exam_student(request, exam_id): 
    exam = get_object_or_404(Exam, pk=exam_id)
    print("Exam ID:", exam_id) #Debugging
    print("User ID:", request.user.id) #Debugging

    try:
        submission = ExamSubmission.objects.get(exam=exam, student=request.user)
        print("Submission found:", submission.id) #Debugging
    except ExamSubmission.DoesNotExist:
        submission = None
        print("Submission not found for user:", request.user.id, "and exam:", exam_id) #Debugging

    if not submission:
        print("No submission found") #Debugging
        return HttpResponseForbidden("You are not authorized to view this exam.")
    
    return render(request, 'myapp/student/view_exam.html', {
        'exam': exam,
        'submission': submission
    })


@login_required
def take_exam(request):
    search_query = request.GET.get('search', '')  # Get the search term from the URL
    # Filter the exams for which the student has not submitted answers
    submitted_exams = ExamSubmission.objects.filter(student=request.user).values_list('exam', flat=True) #Exams that the student has submitted
    if search_query:
        exams = Exam.objects.filter(is_active=True, name__icontains=search_query).exclude(pk__in=submitted_exams)
    else:
        exams = Exam.objects.filter(is_active=True).exclude(pk__in=submitted_exams)
    return render(request, 'myapp/student/take_exam.html', {'exams': exams})



@login_required
def enter_exam(request, exam_id): #this will redirect to the specific exam page where the student can take the exam
    exam = get_object_or_404(Exam, pk=exam_id, is_active=True)
    return render(request, 'myapp/student/enter_specific_exam.html', {'exam': exam})

@login_required
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    if request.method == 'POST':
        student_answer = request.POST.get('student_answer')
        # Save the submission
        ExamSubmission.objects.create(
            exam=exam,
            student=request.user,
            student_answer=student_answer,
            score=0, #Not graded yet
        )
        # Redirect to the student dashboard
        return redirect('student_dashboard')
    


@login_required
def view_profile_student(request):
    return render(request, 'myapp/student/view_profile2.html', {'user': request.user})

@login_required
def view_profile_teacher(request):
    return render(request, 'myapp/teacher/view_profile2.html', {'user': request.user})


@login_required
def edit_profile_teacher(request):
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                updated_user = authenticate(username=user.username, password=new_password)
                if updated_user:
                    login(request, updated_user)
                    messages.success(request, 'Profile updated successfully, including password change.')
                else:
                    messages.error(request, 'There was an error updating your profile. Please try again.')
            else:
                user.save()
                messages.success(request, 'Profile updated successfully.')
            return redirect('view_profile_teacher')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherProfileForm(instance=request.user)

    return render(request, 'myapp/teacher/view_profile2.html', {'form': form, 'user': request.user})



@login_required
def edit_profile_student(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.student.student_id = form.cleaned_data.get('student_id')
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                updated_user = authenticate(username=user.username, password=new_password)
                if updated_user:
                    login(request, updated_user)
                    messages.success(request, 'Profile updated successfully, including password change.')
                else:
                    messages.error(request, 'There was an error updating your profile. Please try again.')
            else:
                user.save()
                user.student.save()
                messages.success(request, 'Profile updated successfully.')
            return redirect('view_profile_student')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherProfileForm(instance=request.user)

    return render(request, 'myapp/student/view_profile2.html', {'form': form, 'user': request.user})



@login_required
def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user)  # Ensure that only the teacher who created the exam can edit it
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)  # Pass instance on POST to update the specific exam
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated successfully.')
            return redirect('view_exam_teacher', exam_id=exam.id)
    else:
        form = ExamForm(instance=exam)  # Initialize form with instance data on GET (to hold the current data in the form)
    return render(request, 'myapp/teacher/edit_exam.html', {'form': form, 'exam': exam})



@login_required
def publish_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user)  # Ensure that only the teacher who created the exam can publish it
    if request.method == 'POST':
        exam.is_active = True
        exam.save()
        messages.success(request, "Exam published successfully.")
        return redirect('view_exam_teacher', exam_id=exam.id)
    else:
        return HttpResponseForbidden("Invalid request")


@login_required
def unpublish_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user)
    if request.method == 'POST':
        exam.is_active = False
        exam.save()
        messages.success(request, "Exam unpublished successfully.")
        return redirect('view_exam_teacher', exam_id=exam.id)
    else:
        return HttpResponseForbidden("Invalid request")



@login_required
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, "Exam deleted successfully.")
        return HttpResponseRedirect(reverse('teacher_dashboard')) # Redirect to the teacher dashboard
    else:
        return HttpResponseForbidden("Invalid request")



@login_required
def view_submissions(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user)
    submissions = ExamSubmission.objects.filter(exam=exam)
    is_graded = all(submission.is_graded for submission in submissions)
    if not submissions.exists():
        messages.info(request, "No submissions found.")
        return render (request, 'myapp/teacher/view_submissions.html', {'submissions': submissions, 'exam': exam})
    if is_graded:
        print("All submissions are graded , so redirecting to view_grades")
        return render(request, 'myapp/teacher/view_grades.html', {'submissions': submissions, 'exam': exam})
    else:
        print("Submissions are not graded , so redirecting to view_submissions")
        return render(request, 'myapp/teacher/view_submissions.html', {'submissions': submissions, 'exam': exam})




@login_required
def view_grades(request, exam_id):
    # check if this exam is alraedy graded or not
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user)
    exam_submissions = ExamSubmission.objects.filter(exam=exam)
    is_graded = all(submission.is_graded for submission in exam_submissions)
    if not is_graded:
        graded_submissions = StartGrading(exam_id)  # This will update and return graded submissions
        for submission in graded_submissions:
            if submission.score < 0:
                submission.score = 0.000
        return render(request, 'myapp/teacher/view_grades.html', {'submissions': graded_submissions, 'exam': exam})
    else:
        return render(request, 'myapp/teacher/view_grades.html', {'submissions': exam_submissions, 'exam': exam})



@login_required
def modify_grade(request, submission_id):
    if request.method == 'POST':
        submission = get_object_or_404(ExamSubmission, id=submission_id, exam__teacher=request.user)
        exam = submission.exam
        submissions = ExamSubmission.objects.filter(exam=exam)
        new_grade = request.POST.get('new_grade')
        submission.score = decimal.Decimal(new_grade)
        print(f"Before saving: {submission.score}")
        submission.save()
        print(f"After saving: {submission.score}")
        messages.success(request, "Grade updated successfully.")
        return render(request, 'myapp/teacher/view_grades.html', {'submissions': submissions, 'exam': exam})
    return HttpResponseForbidden("Invalid request")


@login_required
def approve_grades(request, exam_id):
    if request.method == 'POST':
        exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user) # Ensure that only the teacher who created the exam can approve its grades
        submissions = ExamSubmission.objects.filter(exam=exam) # Retrieve all submissions for the exam
        print("Approving grades for exam:", exam.name)
        
        for submission in submissions:
            if submission.score < 0:
                submission.score = 0.000
            print(f"Now approving Submission with ID {submission.id} - Student {submission.student.username} - Score {submission.score}")
            submission.is_approved = True
            submission.save()
        messages.success(request, "Grades approved successfully and sent to students!.")
        return render(request, 'myapp/teacher/view_grades.html', {'submissions': submissions, 'exam': exam})
    else:
        return HttpResponseForbidden("Invalid request")




@login_required
def generate_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            constraints = data.get('constraints', '')

            if not question:
                return JsonResponse({'error': 'Question is required.'}, status=400)

            model_answer = generativeAI.generate_model_answer(question, constraints)
            
            if not model_answer:
                return JsonResponse({'error': 'Failed to generate model answer.'}, status=500)

            return JsonResponse({'model_answer': model_answer})
        
        except Exception as e:
            return JsonResponse({'error': 'This service is not available right now, maybe a problem with your internet connection, please try again in a few minutes.'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def upload_images(request, exam_id):
    if request.method == 'POST':
        # processor, model = load_model()
        model_choice = request.POST.get('model')
        # Choose moodel correct spelling mistakes or not
        edit = 'true' if model_choice == 'model1' else 'false'
        print("Edit:", edit)
        
        uploaded_files = request.FILES.getlist('images')
        max_files = getattr(settings, 'DATA_UPLOAD_MAX_NUMBER_FILES', 100)
        if len(uploaded_files) > max_files:
            messages.error(request, f'You can upload a maximum of {max_files} files at a time.')
            return redirect('upload_images', exam_id=exam_id)
        
        for uploaded_file in uploaded_files:
            if edit=='false':
                #### First, use verify model ####
                print("Now trying Verify model and edit= ",edit)
                try:
                    fs = FileSystemStorage()
                    filename = fs.save(uploaded_file.name, uploaded_file)
                    file_path = fs.path(filename)
                    print("FILE PATH", file_path)
                        
                    #Verify model
                    student_id, student_name, extracted_answer = OCR_Verify_Model(file_path)
                    print("Student ID:", student_id)
                    print("Student Name:", student_name)
                    print("Extracted Answer:", extracted_answer)

                    # Save the results
                    ExamSubmissionOCR.objects.create(
                        exam_id=exam_id,
                        teacher=request.user,
                        student_id=student_id,
                        student_name=student_name,
                        image=uploaded_file,
                        extracted_text=extracted_answer,
                        score=0, #Not graded yet
                    )
                except Exception as e:
                ##### Use OCR-Space model as a backup model if edit='false
                    print('Verify model failed, trying OCR Space model...')
                    try:
                        fs = FileSystemStorage()
                        filename = fs.save(uploaded_file.name, uploaded_file)
                        file_path = fs.path(filename)
                        print("FILE PATH", file_path)
                        #OCR Space model
                        print("Now trying OCR Space model and edit= ",edit)
                        student_id, student_name, extracted_answer = OCR_Space_Model(file_path)
                        print("Student ID:", student_id)
                        print("Student Name:", student_name)
                        print("Extracted Answer:", extracted_answer)

                        # Save the results
                        ExamSubmissionOCR.objects.create(
                            exam_id=exam_id,
                            teacher=request.user,
                            student_id=student_id,
                            student_name=student_name,
                            image=uploaded_file,
                            extracted_text=extracted_answer,
                            score=0, #Not graded yet
                        )

                    except Exception as e:
                        messages.error(request, 'This service is not available right now, maybe a problem with your internet connection, please try again in a few minutes.')
                        print(f"Error processing file {uploaded_file.name}: {e}")  # Debugging
                        return redirect('upload_images', exam_id=exam_id)
        
            else: #edit='true'
                #### Use Gemini model ####
                print("Now trying Gemini model and edit= ",edit)
                try:
                    fs = FileSystemStorage()
                    filename = fs.save(uploaded_file.name, uploaded_file)
                    file_path = fs.path(filename)
                    print("FILE PATH", file_path)
                    #Gemini model
                    student_id, student_name, extracted_answer = OCR_Gemini_Model(file_path,edit)
                    print("Hello from view upload_images from Gemini model")
                    print("Student ID:", student_id)
                    print("Student Name:", student_name)
                    print("Extracted Answer:", extracted_answer)

                    # Save the results
                    ExamSubmissionOCR.objects.create(
                        exam_id=exam_id,
                        teacher=request.user,
                        student_id=student_id,
                        student_name=student_name,
                        image=uploaded_file,
                        extracted_text=extracted_answer,
                        score=0, #Not graded yet
                    )
                except Exception as e:
                    messages.error(request, 'Model1 is not available right now, please try again later or use Model2.')
                    print(f"Error processing file {uploaded_file.name}: {e}")
                    return redirect('upload_images', exam_id=exam_id)


        messages.success(request, "Images uploaded and processed successfully.")
        return redirect('view_submissions_ocr', exam_id=exam_id)
    
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user)
    return render(request, 'myapp/teacher/upload_images.html', {'exam_id': exam_id, 'exam': exam})


@login_required
def view_submissions_ocr(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    submissions = ExamSubmissionOCR.objects.filter(exam=exam)
    return render(request, 'myapp/teacher/view_submissions_ocr.html', {
        'exam': exam,
        'submissions': submissions
    })




@login_required
def view_grades_ocr(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user)
    exam.ocr_graded = True
    exam.save()
    print("now set ocr_graded to", exam.ocr_graded)
    if not exam.ocr_graded:
        graded_submissions = StartGradingOCR(exam_id)  # This will update and return graded submissions
    else:
        graded_submissions = ExamSubmissionOCR.objects.filter(exam=exam)
    for submission in graded_submissions:
        if submission.score < 0:
            submission.score = 0.000
        print(f"Submission ID: {submission.id} - Student ID: {submission.student_id} - Score: {submission.score}")
    return render(request, 'myapp/teacher/view_grades_ocr.html', {'submissions': graded_submissions, 'exam': exam})


@login_required
def modify_grade_ocr(request, submission_id):
    if request.method == 'POST':
        new_grade = request.POST.get('new_grade')
        submissions=ExamSubmissionOCR.objects.filter(exam__teacher=request.user)
        submission = submissions.get(id=submission_id) #submission that will update grade
        print("Before saving: ", submission.score)
        submission.score = decimal.Decimal(new_grade)
        submission.save()
        print("After saving: ", submission.score)
        messages.success(request, "Grade updated successfully.")
        return render(request, 'myapp/teacher/view_grades_ocr.html', {'submissions': submissions})
    return HttpResponseForbidden("Invalid request")

@login_required
def export_grades_ocr(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    print("Exporting grades for exam:", exam.name ,"With ID:", exam_id)
    submissions = ExamSubmissionOCR.objects.filter(exam_id=exam_id).values('student_id', 'score')
    return export_ocr_grades_to_excel(exam_id)






@login_required
def increase_grades(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    increase_by = decimal.Decimal(request.POST.get('increase_by', 0))
    submissions = ExamSubmission.objects.filter(exam=exam)
    for submission in submissions:
        new_score = submission.score + increase_by
        if new_score > decimal.Decimal('10.000'):
            new_score = decimal.Decimal('10.000')
        submission.score = new_score
        submission.save()
    messages.success(request, "All grades increased successfully.")
    return redirect('view_grades', exam_id=exam_id)

@login_required
def round_grades(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    submissions = ExamSubmission.objects.filter(exam=exam)
    for submission in submissions:
        new_score = math.ceil(submission.score)
        if new_score > 10:
            new_score = 10
        submission.score = new_score
        submission.save()
    messages.success(request, "All grades rounded up successfully.")
    return redirect('view_grades', exam_id=exam_id)

@login_required
def increase_grades_ocr(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    increase_by = decimal.Decimal(request.POST.get('increase_by', 0))
    print("I'm now increasing all ocr grades by ", increase_by)
    submissions = ExamSubmissionOCR.objects.filter(exam=exam)
    for submission in submissions:
        new_score = submission.score + increase_by
        if new_score > decimal.Decimal('10.000'):
            new_score = decimal.Decimal('10.000')
        submission.score = new_score
        submission.save()
    messages.success(request, "All grades increased successfully.")
    return redirect('view_grades_ocr', exam_id=exam_id)

@login_required
def round_grades_ocr(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    submissions = ExamSubmissionOCR.objects.filter(exam=exam)
    for submission in submissions:
        new_score = math.ceil(submission.score)
        if new_score > 10:
            new_score = 10
        submission.score = new_score
        submission.save()
    messages.success(request, "All grades rounded up successfully.")
    return redirect('view_grades_ocr', exam_id=exam_id)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('logout/', views.logout_view, name='logout'),


    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),


    path('teacher/create_exam/', views.create_exam, name='create_exam'),
    path('student/take_exam/', views.take_exam, name='take_exam'),
    path('student/enter_exam/<int:exam_id>/', views.enter_exam, name='enter_exam'),
    path('student/submit_exam/<int:exam_id>/', views.submit_exam, name='submit_exam'),
    path('student/exam/<int:exam_id>/view/', views.view_exam_student, name='view_exam_student'),


    path('teacher/exam/<int:exam_id>/view/', views.view_exam_teacher, name='view_exam_teacher'),
    path('teacher/edit_exam/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('teacher/exam/<int:exam_id>/publish/', views.publish_exam, name='publish_exam'),
    path('teacher/exam/<int:exam_id>/unpublish/', views.unpublish_exam, name='unpublish_exam'),
    path('teacher/exam/<int:exam_id>/delete/', views.delete_exam, name='delete_exam'),
    path('generate_answer/', views.generate_answer, name='generate_answer'),
    # View submissions are submissions that are not graded yet
    path('teacher/exam/<int:exam_id>/view_submissions/', views.view_submissions, name='view_submissions'),
    path('teacher/exam/<int:exam_id>/view_grades/', views.view_grades, name='view_grades'),
    path('teacher/modify_grade/<int:submission_id>/', views.modify_grade, name='modify_grade'),
    path('teacher/approve_grades/<int:exam_id>/', views.approve_grades, name='approve_grades'),


    # OCR related paths
    path('teacher/exam/<int:exam_id>/upload_images/', views.upload_images, name='upload_images'),
    path('teacher/exam/<int:exam_id>/view_submissions_ocr/', views.view_submissions_ocr, name='view_submissions_ocr'),
    path('teacher/exam/<int:exam_id>/view_grades_ocr/', views.view_grades_ocr, name='view_grades_ocr'),
    path('teacher/modify_grade_ocr/<int:submission_id>/', views.modify_grade_ocr, name='modify_grade_ocr'),
    path('teacher/exam/<int:exam_id>/export_grades_ocr/', views.export_grades_ocr, name='export_grades_ocr'),
    


    
    path('view_profile/student/', views.view_profile_student, name='view_profile_student'),
    path('edit_profile/student/', views.edit_profile_student, name='edit_profile_student'),
    path('view_profile/teacher/', views.view_profile_teacher, name='view_profile_teacher'),
    path('edit_profile/teacher/', views.edit_profile_teacher, name='edit_profile_teacher'),



    path('exam/<int:exam_id>/increase_grades/', views.increase_grades, name='increase_grades'),
    path('exam/<int:exam_id>/round_grades/', views.round_grades, name='round_grades'),
    path('exam/<int:exam_id>/increase_grades_ocr/', views.increase_grades_ocr, name='increase_grades_ocr'),
    path('exam/<int:exam_id>/round_grades_ocr/', views.round_grades_ocr, name='round_grades_ocr'),


]
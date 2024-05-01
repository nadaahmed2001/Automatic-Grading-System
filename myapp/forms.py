from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Teacher
from .models import Exam
from django.core.exceptions import ValidationError


class StudentRegistrationForm(UserCreationForm):
    student_id = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = Student
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name','student_id')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.userType = 'student'  # or 'teacher' for the TeacherRegistrationForm
        if commit:
            user.save()
        return user


class TeacherRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = Teacher
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name','email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.userType = 'teacher'
        if commit:
            user.save()
        return user


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'question', 'model_answer', 'keywordsList']

    def save(self, commit=True):
        exam = super().save(commit=False)
        if commit:
            exam.save()
        return exam
    
    def clean(self):
        cleaned_data = super().clean()
        question = cleaned_data.get('question')
        model_answer = cleaned_data.get('model_answer')
        keywordsList = cleaned_data.get('keywordsList')
        if not question or not model_answer:
            raise ValidationError({'question': 'This field is required.'})
        return cleaned_data


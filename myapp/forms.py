from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Teacher
from .models import Exam
from django.core.exceptions import ValidationError
from myapp.models import User


class StudentRegistrationForm(UserCreationForm):
    student_id = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = Student
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name','student_id','email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.userType = 'student'
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


class ExamForm(forms.ModelForm): #Form for creating new exam
    class Meta:
        model = Exam
        fields = ['name', 'question', 'model_answer', 'keywordsList']

    def save(self, commit=True):
        exam = super().save(commit=False)
        if commit:
            exam.save()
        return exam

class StudentProfileForm(forms.ModelForm): #Form for student edit profile
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        min_length=8,
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )
    student_id = forms.CharField(max_length=20, required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'student_id']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # IF email is already in use by another user
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email address is already in use.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # IF username is already in use by another user
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This username is already in use.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Password mismatch.')
        return cleaned_data


class TeacherProfileForm(forms.ModelForm):
    # New password and confirm password fields are added
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        min_length=8,
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email address is already in use.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This username is already in use.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Password mismatch.')
        return cleaned_data

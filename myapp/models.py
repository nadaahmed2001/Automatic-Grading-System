from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    userType = models.CharField(max_length=10, choices=[('teacher', 'Teacher'), ('student', 'Student')])

class Student(User):
    student_id = models.CharField(max_length=20, unique=True)

class Teacher(User):
    classmethod
    pass
    


class Exam(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    question= models.TextField(max_length=10000)
    model_answer = models.TextField(max_length=10000)
    keywordsList = models.TextField(max_length=10000)
    is_active = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

class ExamSubmission(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='submissions') #related name is used to access the submissions of a particular exam
    student = models.ForeignKey(User, on_delete=models.CASCADE,related_name='submissions') #related name is used to access the submissions of a particular student
    student_answer = models.TextField(max_length=10000)
    score = models.IntegerField()
    time_submitted = models.DateTimeField(auto_now_add=True)
    is_graded = models.BooleanField(default=False)

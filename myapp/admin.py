from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher
from .models import Exam, ExamSubmission, ExamSubmissionOCR

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Student, UserAdmin)
admin.site.register(Teacher, UserAdmin)
admin.site.register(Exam)
admin.site.register(ExamSubmission)
admin.site.register(ExamSubmissionOCR)


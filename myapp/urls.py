from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),


    path('create_exam/', views.create_exam, name='create_exam'),
    path('exam/<int:exam_id>/', views.view_exam, name='view_exam'),
    path('take_exam/', views.take_exam, name='take_exam'),
    path('enter_exam/<int:exam_id>/', views.enter_exam, name='enter_exam'),
    path('submit_exam/<int:exam_id>/', views.submit_exam, name='submit_exam'),
    path('edit_exam/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('exam/<int:exam_id>/publish/', views.publish_exam, name='publish_exam'),
    path('exam/<int:exam_id>/unpublish/', views.unpublish_exam, name='unpublish_exam'),
    path('exam/<int:exam_id>/delete/', views.delete_exam, name='delete_exam'),
    # View submissions are submissions that are not graded yet
    path('exam/<int:exam_id>/view_submissions/', views.view_submissions, name='view_submissions'),
    path('exam/<int:exam_id>/view_grades/', views.view_grades, name='view_grades'),
    path('modify_grade/<int:submission_id>/', views.modify_grade, name='modify_grade'),

    
    path('view_profile/student/', views.view_profile_student, name='view_profile_student'),
    path('edit_profile/student/', views.edit_profile_student, name='edit_profile_student'),
    path('view_profile/teacher/', views.view_profile_teacher, name='view_profile_teacher'),
    path('edit_profile/teacher/', views.edit_profile_teacher, name='edit_profile_teacher'),

]
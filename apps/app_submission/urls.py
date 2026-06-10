from django.urls import path
from . import views

urlpatterns = [
   
    path('student/', views.StudentSubmissionAPIView.as_view(), name='student-submission'),
    path('teacher/', views.TeacherSubmissionAPIView.as_view(), name='teacher-submission-list'),
    path('teacher/<int:pk>/', views.TeacherSubmissionDetailAPIView.as_view(), name='teacher-submission-detail'),
]
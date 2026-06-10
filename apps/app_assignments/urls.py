from django.urls import path
from .import views




urlpatterns = [
    path('groups/', views.GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('groups/<int:id>/', views.GroupDetailAPIView.as_view(), name='group-detail'),

   
    path('assignments/', views.AssignmentListCreateAPIView.as_view(), name='assignment-list-create'),
    path('assignments/<int:id>/', views.AssignmentDetailAPIView.as_view(), name='assignment-detail'),
]


 
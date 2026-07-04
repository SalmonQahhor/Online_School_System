from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    InviteAPIView, ProfileAPIView, RegisterAPIView, LoginAPIView, 
    LogoutAPIView, MeAPIView, ProfileAPIView, ChangePasswordAPIView,
    ValidateTokenAPIView
)


urlpatterns = [
    path('invite/', InviteAPIView.as_view()),
    path('invite/validate/', ValidateTokenAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('me/', MeAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
 
from .models import User, InviteToken
from .serializers import (
    RegisterSerializer, LoginSerializer, ChangePasswordSerializer,
    ProfileUpdateSerializer, UserSerializer
)
 
logger = logging.getLogger(__name__)
 
 
class InviteAPIView(APIView):
    """Admin users to invite"""
    permission_classes = [IsAdminUser]
 
    def post(self, request):
        email = request.data.get('email', '').lower().strip()
        role = request.data.get('role', 'student')
 
        if not email:
            return Response({'error': 'Email kiritilishi kerak.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if role not in ['teacher', 'student']:
            return Response({'error': 'Role noto\'g\'ri.'}, status=status.HTTP_400_BAD_REQUEST)
 
        if User.objects.filter(email=email).exists():
            logger.warning(f'Invite failed: {email} already registered')
            return Response({'error': 'Bu email allaqachon ro\'yxatdan o\'tgan.'}, status=status.HTTP_400_BAD_REQUEST)
 
        if InviteToken.objects.filter(email=email).exists():
            logger.warning(f'Invite exists: {email}')
            return Response({'error': 'Bu email uchun taklif allaqachon yuborilgan.'}, status=status.HTTP_400_BAD_REQUEST)
 
        invite = InviteToken.objects.create(email=email, role=role)
        logger.info(f'Invite created: {email} ({role}) - Token: {invite.token}')
 
        print(f"[EMAIL SIMULATION] {email} => Invite Token: {invite.token}")
 
        return Response({
            'message': f'Taklif {email} ga yuborildi.',
            'token': str(invite.token),
            'role': role
        }, status=status.HTTP_201_CREATED)
 
 
class ValidateTokenAPIView(APIView):
    """Validate invite token"""
    permission_classes = [AllowAny]
 
    def get(self, request):
        token = request.query_params.get('token')
 
        if not token:
            return Response({'error': 'Token kiritilishi kerak.'}, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            invite = InviteToken.objects.get(token=token)
 
            if not invite.is_valid():
                if invite.is_used:
                    return Response({'error': 'Bu taklif allaqachon ishlatilgan.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Taklif muddati tugagan.'}, status=status.HTTP_400_BAD_REQUEST)
 
            return Response({
                'email': invite.email,
                'role': invite.role,
                'valid': True
            }, status=status.HTTP_200_OK)
 
        except InviteToken.DoesNotExist:
            logger.warning(f'Invalid token: {token}')
            return Response({'error': 'Taklif topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
 
 
class RegisterAPIView(APIView):
    """Register with invite token"""
    permission_classes = [AllowAny]
 
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f'User registered: {user.email} ({user.role})')
            
            return Response({
                'message': 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz!',
                'email': user.email,
                'role': user.role
            }, status=status.HTTP_201_CREATED)
 
        logger.warning(f'Register failed: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
class LoginAPIView(APIView):
    """User login"""
    permission_classes = [AllowAny]
 
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
 
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(f'Login failed: User not found - {email}')
            return Response({'error': 'Email yoki parol noto\'g\'ri.'}, status=status.HTTP_401_UNAUTHORIZED)
 
        if not user.check_password(password):
            logger.warning(f'Login failed: Wrong password - {email}')
            return Response({'error': 'Email yoki parol noto\'g\'ri.'}, status=status.HTTP_401_UNAUTHORIZED)
 
        if not user.is_active:
            logger.warning(f'Login failed: User inactive - {email}')
            return Response({'error': 'Foydalanuvchi deaktivatsiya qilingan.'}, status=status.HTTP_401_UNAUTHORIZED)
 
        refresh = RefreshToken.for_user(user)
        logger.info(f'Login successful: {email}')
 
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'email': user.email,
            'username': user.username,
            'role': user.role
        }, status=status.HTTP_200_OK)
 
 
class LogoutAPIView(APIView):
    """Logout user"""
    permission_classes = [IsAuthenticated]
 
    def post(self, request):
        try:
            refresh = request.data.get('refresh')
            
            if not refresh:
                return Response({'error': 'Refresh token kiritilishi kerak.'}, status=status.HTTP_400_BAD_REQUEST)
 
            from rest_framework_simplejwt.tokens import RefreshToken as RT
            token = RT(refresh)
            token.blacklist()
 
            logger.info(f'Logout: {request.user.email}')
            return Response({'message': 'Muvaffaqiyatli chiqildi.'})
 
        except Exception as e:
            logger.error(f'Logout error: {request.user.email} - {str(e)}')
            return Response({'error': 'Chiqishda xato.'}, status=status.HTTP_400_BAD_REQUEST)
 
 
class MeAPIView(APIView):
    """Get current user info"""
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
 
 
class ProfileAPIView(APIView):
    """Get/Update profile"""
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
 
    def patch(self, request):
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
 
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Profile updated: {request.user.email}')
            return Response({
                'message': 'Profil yangilandi.',
                'user': serializer.data
            })
 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
class ChangePasswordAPIView(APIView):
    """Change password"""
    permission_classes = [IsAuthenticated]
 
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
 
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
 
        if not user.check_password(old_password):
            logger.warning(f'Password change failed: Wrong password - {user.email}')
            return Response({'error': 'Eski parol noto\'g\'ri.'}, status=status.HTTP_401_UNAUTHORIZED)
 
        user.set_password(new_password)
        user.save()
 
        logger.info(f'Password changed: {user.email}')
        return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi.'})

from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

import logging

from .models import InviteToken
from .serializers import InviteSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()
logger = logging.getLogger(__name__)



class InviteAPIView(APIView):
    permission_classes = [IsAdminUser]  # faqat admin

    def post(self, request):
        serializer = InviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        role = serializer.validated_data['role']

        # Allaqachon ro'yxatdan o'tgan
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Bu email allaqachon ro\'yxatdan o\'tgan.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Eski invite o'chirib, yangi yaratish
        InviteToken.objects.filter(email=email).delete()
        invite = InviteToken.objects.create(email=email, role=role)

        invite_link = f"{settings.FRONTEND_URL}/register?token={invite.token}"

        try:
            send_mail(
                subject='Online School — Taklif',
                message=f'Siz tizimga taklif qilindingiz.\n\nRol: {role}\nLink: {invite_link}\n\nLink 24 soat amal qiladi.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            logger.info(f'Invite sent: {email} ({role})')
        except Exception as e:
            logger.error(f'Invite email failed: {email} — {e}')
            # Email yuborilmasa ham token yaratilgan — adminга ko'rsatamiz
            return Response({
                'message': 'Invite yaratildi, lekin email yuborilmadi.',
                'invite_link': invite_link,  # admin o'zi yuborishi mumkin
                'token': str(invite.token),
            }, status=status.HTTP_201_CREATED)

        return Response(
            {'message': f'Invite {email} ga yuborildi.'},
            status=status.HTTP_201_CREATED
        )
    


class ValidateTokenAPIView(APIView):
    permission_classes = []

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Token kiritilmadi.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invite = InviteToken.objects.get(token=token)
        except InviteToken.DoesNotExist:
            return Response({'error': 'Token mavjud emas.'}, status=status.HTTP_404_NOT_FOUND)

        if not invite.is_valid():
            return Response({'error': 'Token muddati tugagan yoki ishlatilgan.'}, status=status.HTTP_400_BAD_REQUEST)

        # Frontend token valid bo'lsa email va roleni ko'rsatadi
        return Response({
            'email': invite.email,
            'role': invite.role,
        })



class RegisterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        invite = InviteToken.objects.get(token=token)

        user = User.objects.create_user(
            email=invite.email,
            username=username,
            password=password,
            role=invite.role,
            is_active=True,
            is_verified=True,
        )

        # Token ishlatilgan deb belgilanadi
        invite.is_used = True
        invite.save()

        logger.info(f'User registered: {user.email} ({user.role})')

        return Response(
            {'message': 'Ro\'yxatdan o\'tdingiz. Endi login qilishingiz mumkin.'},
            status=status.HTTP_201_CREATED
        )



class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)

        if user is None:
            logger.warning(f'Failed login: {email}')
            return Response(
                {'error': 'Email yoki parol noto\'g\'ri.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Akkaunt faol emas.'},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)
        logger.info(f'Login: {email}')

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role,
            'email': user.email,
        })
    






class LogoutAPIView(APIView):
    """Foydalanuvchini chiqarish — token blacklist qilish"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token kiritilmadi.'}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f'Logout: {request.user.email}')
            return Response({'message': 'Muvaffaqiyatli chiqildi.'})
        except Exception as e:
            logger.error(f'Logout error: {request.user.email} — {e}')
            return Response({'error': 'Chiqishda xato.'}, status=status.HTTP_400_BAD_REQUEST)


class MeAPIView(APIView):
    """Kirgan foydalanuvchi ma'lumotlari"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'is_verified': user.is_verified,
            'is_active': user.is_active,
        })


class ProfileEditAPIView(APIView):
    """Profil tahrir — nickname, parol o'zgartirish"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Profil ma'lumotlarini olish"""
        user = request.user
        return Response({
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
        })

    def patch(self, request):
        """Profil tahrir"""
        user = request.user
        
        # Username o'zgartirish
        if 'username' in request.data:
            new_username = request.data['username']
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                return Response(
                    {'error': 'Bu username band.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.username = new_username

        # First name
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']

        # Last name
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']

        user.save()
        logger.info(f'Profile updated: {user.email}')

        return Response({
            'message': 'Profil yangilandi.',
            'user': {
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })


class ChangePasswordAPIView(APIView):
    """Parol o'zgartirish"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return Response(
                {'error': 'Barcha maydonlar kiritilishi kerak.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Eski parol tekshirish
        if not user.check_password(old_password):
            logger.warning(f'Failed password change: {user.email}')
            return Response(
                {'error': 'Eski parol noto\'g\'ri.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Yangi parol match tekshirish
        if new_password != confirm_password:
            return Response(
                {'error': 'Yangi parollar mos emas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Yangi parol validatsiyasi
        if len(new_password) < 8:
            return Response(
                {'error': 'Parol kamida 8 belgi bo\'lishi kerak.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password == old_password:
            return Response(
                {'error': 'Yangi parol eskilikdan farq qilishi kerak.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        logger.info(f'Password changed: {user.email}')

        return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi.'})
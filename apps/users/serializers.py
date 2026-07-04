from rest_framework import serializers
from django.utils import timezone
from .models import User, InviteToken
from .validators import validate_email_format, validate_password_strength, validate_username
 
 
class UserSerializer(serializers.ModelSerializer):
    """User info serializer"""
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'avatar']
        read_only_fields = ['id']
 
 
class RegisterSerializer(serializers.Serializer):
    """Register with invite token"""
    token = serializers.CharField()
    username = serializers.CharField(validators=[validate_username])
    email = serializers.EmailField(validators=[validate_email_format])
    password = serializers.CharField(
        min_length=8,
        validators=[validate_password_strength],
        write_only=True
    )
 
    def validate_token(self, value):
        try:
            invite = InviteToken.objects.get(token=value)
            if invite.is_used:
                raise serializers.ValidationError('Bu taklif allaqachon ishlatilgan.')
            if not invite.is_valid():
                raise serializers.ValidationError('Taklif muddati tugagan.')
            return value
        except InviteToken.DoesNotExist:
            raise serializers.ValidationError('Taklif topilmadi.')
 
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Bu username band.')
        return value
 
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Bu email band.')
        return value
 
    def create(self, validated_data):
        invite = InviteToken.objects.get(token=validated_data['token'])
        
        user = User.objects.create_user(
            email=invite.email,
            username=validated_data['username'],
            password=validated_data['password'],
            role=invite.role
        )
        
        invite.is_used = True
        invite.used_at = timezone.now()
        invite.save()
        
        return user
 
 
class LoginSerializer(serializers.Serializer):
    """Login - role avtomatik beriladi"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError('Email yoki parol noto\'g\'ri.')
        except User.DoesNotExist:
            raise serializers.ValidationError('Email yoki parol noto\'g\'ri.')
        
        return attrs
 
 
class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer"""
    old_password = serializers.CharField(write_only=True, min_length=8)
    new_password = serializers.CharField(write_only=True, validators=[validate_password_strength])
    confirm_password = serializers.CharField(write_only=True, min_length=8)
 
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Parollar mos emas.'})
        return attrs
 
 
class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Profile update serializer"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'bio', 'avatar']
        read_only_fields = ['email']
 
    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError('Bu username band.')
        return value
 

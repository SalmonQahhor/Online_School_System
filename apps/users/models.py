import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),  
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='admin',  
        verbose_name="Rol"
    )
    is_verified = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
    )

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"



class InviteToken(models.Model):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=User.ROLE_CHOICES)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Taklif"
        verbose_name_plural = "Takliflar"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['email']),
        ]

    def is_valid(self):
        """Token valiflikni tekshiring"""
        if self.is_used:
            return False
        expiry_time = (timezone.now() - self.created_at).total_seconds()
        return expiry_time < 86400  # 24 soat

    def __str__(self):
        return f'{self.email} ({self.role}) - {"✓ Used" if self.is_used else "⏳ Pending"}'

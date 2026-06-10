from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, InviteToken




@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'role', 'is_active', 'is_verified']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'is_verified')}),
    )


@admin.register(InviteToken)
class InviteTokenAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'token', 'is_used', 'created_at']
    list_filter = ['role', 'is_used']
    readonly_fields = ['token', 'created_at']
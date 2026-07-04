from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import User, InviteToken
 
 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'username', 'role_badge', 'is_active',
        'is_staff', 'date_joined'
    )
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login', 'password_hash')
 
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('email', 'username', 'password', 'role')
        }),
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'phone', 'bio', 'avatar'),
            'classes': ('collapse',)
        }),
        ('Ruxsatlar', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Vaqtlar', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )
 
    def role_badge(self, obj):
        colors = {
            'teacher': '#FF6B6B',
            'student': '#4ECDC4'
        }
        color = colors.get(obj.role, '#95E1D3')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_badge.short_description = 'Role'
 
    def password_hash(self, obj):
        return '***' if obj.password else 'None'
    password_hash.short_description = 'Parol hash'
 
 
@admin.register(InviteToken)
class InviteTokenAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'role_badge', 'status_badge',
        'created_at', 'expiry_status'
    )
    list_filter = ('role', 'is_used', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('token', 'created_at', 'used_at')
 
    fieldsets = (
        ('Taklif ma\'lumoti', {
            'fields': ('email', 'role', 'token')
        }),
        ('Status', {
            'fields': ('is_used', 'used_at', 'created_at')
        }),
    )
 
    def role_badge(self, obj):
        colors = {
            'teacher': '#FF6B6B',
            'student': '#4ECDC4'
        }
        color = colors.get(obj.role, '#95E1D3')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_badge.short_description = 'Role'
 
    def status_badge(self, obj):
        if obj.is_used:
            return format_html(
                '<span style="background-color: #95E1D3; color: white; padding: 3px 10px; border-radius: 3px;">✓ Ishlatilgan</span>'
            )
        elif obj.is_valid():
            return format_html(
                '<span style="background-color: #4ECDC4; color: white; padding: 3px 10px; border-radius: 3px;">⏳ Faol</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #FF6B6B; color: white; padding: 3px 10px; border-radius: 3px;">✕ Muddati tugagan</span>'
            )
    status_badge.short_description = 'Status'
 
    def expiry_status(self, obj):
        from datetime import timedelta
        created = obj.created_at
        delta = timezone.now() - created
        remaining = timedelta(days=1) - delta
        hours = remaining.total_seconds() / 3600
 
        if obj.is_used:
            return 'Ishlatilgan'
        elif hours > 0:
            return f'{int(hours)} soat qoldi'
        else:
            return 'Muddati tugagan'
    expiry_status.short_description = 'Muddati'
 

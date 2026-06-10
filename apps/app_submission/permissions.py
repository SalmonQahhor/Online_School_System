from rest_framework import permissions




class IsTeacherOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role == "student":
            return False
        return request.user.role == "teacher"
    
    
class IsStudentOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role == "teacher":
            return False
        return request.user.role == "student"
    
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user
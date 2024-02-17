from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
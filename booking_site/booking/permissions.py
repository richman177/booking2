from rest_framework import permissions


class CheckCreateHotel(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'ownerUser':
            return True
        return False

class CheckCreateRoom(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'ownerUser':
            return True
        return False


class CheckCreateHotel(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'ownerUser':
            return False
        return True
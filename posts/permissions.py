# from rest_framework import permissions


# class IsCustomer(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user and request.user.groups.filter(name='customers'):
#             return True
#         return False


# class IsStaff(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user and request.user.groups.filter(name='staff'):
#             return True
#         return False

# from rest_framework import permissions

def IsProductRead(user):
    if user and user.user_role.role.permissions.filter(name='Product', read=True):
        return True
    return False
# class IsProductRead(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user and request.user.user_role.role.permissions.filter(name='Product'):
#             print(request.user.user_role.role.permissions.filter(name='product'))
#             return True
#         return False

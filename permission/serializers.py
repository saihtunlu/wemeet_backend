from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Role, UserRole, Permission
from account.serializers import UserSerializer


class PermissionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id', 'name', 'create', 'update', 'delete', 'read']


class RoleSerializers(serializers.ModelSerializer):
    permissions = PermissionSerializers(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'shop', 'name', 'permissions']


class UserRoleSerializers(serializers.ModelSerializer):
    role = RoleSerializers(many=False, read_only=True)

    class Meta:
        model = UserRole
        fields = ['user', 'id', 'role']

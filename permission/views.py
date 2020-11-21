from .models import Role, UserRole, Permission
from account.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics, pagination
from rest_framework.response import Response
from .serializers import RoleSerializers, UserRoleSerializers, PermissionSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .permissions import IsProductRead
# Create your views here.

# Roles


class Roles(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.order_by('created_at').reverse()
    serializer_class = RoleSerializers
    pagination_class = pagination.PageNumberPagination


class SingleRole(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        role_serializer = RoleSerializers(data=data)
        if role_serializer.is_valid():
            role_serializer.save()
            return Response(role_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        id = kwargs['id']
        role = get_object_or_404(
            Role, id=id)
        role_serializer = RoleSerializers(role, data=data)
        if role_serializer.is_valid():
            role_serializer.save()
            return Response(role_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        role = get_object_or_404(
            Role, id=id)
        role_serializer = RoleSerializers(role, many=False)
        return Response(role_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        role = get_object_or_404(
            Role, id=id)
        role.delete()
        return Response('Success', status=status.HTTP_201_CREATED)

# UserRoles


class UserRoles(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserRole.objects.order_by('created_at').reverse()
    serializer_class = UserRoleSerializers
    pagination_class = pagination.PageNumberPagination


class SingleUserRole(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        role = Role.objects.get(id=request.data['role_id'])
        user = User.objects.get(id=request.data['user_id'])
        userRole = UserRole(user=user, role=role)  # add foreign key
        userRole_serializer = UserRoleSerializers(userRole, data=data)
        if userRole_serializer.is_valid():
            userRole_serializer.save()
            return Response(userRole_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(userRole_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        role = Role.objects.get(id=request.data['role_id'])
        userRole = get_object_or_404(
            UserRole, id=request.data['id'])
        userRole.role = role
        userRole_serializer = UserRoleSerializers(userRole, data=data)
        if userRole_serializer.is_valid():
            userRole_serializer.save()
            return Response(userRole_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(userRole_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        if IsProductRead(request.user):
            userRole = get_object_or_404(
                UserRole, user=request.user.id)
            userRole_serializer = UserRoleSerializers(userRole, many=False)
            return Response(userRole_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response([{"deatil": "You don't have permission to read this content!"}], status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        userRole = get_object_or_404(
            UserRole, id=id)
        userRole.delete()
        return Response('Success', status=status.HTTP_201_CREATED)

# Permissions


class MyPermissions(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.order_by('created_at').reverse()
    serializer_class = PermissionSerializers
    pagination_class = pagination.PageNumberPagination


class SingleMyPermission(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        role = Role.objects.get(id=request.data['role_id'])
        permission = Permission(role=role)  # add foreign key
        permission_serializer = PermissionSerializers(permission, data=data)
        if permission_serializer.is_valid():
            permission_serializer.save()
            return Response(permission_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(permission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        permission = get_object_or_404(
            Permission, id=request.data['id'])
        permission_serializer = PermissionSerializers(permission, data=data)
        if permission_serializer.is_valid():
            permission_serializer.save()
            return Response(permission_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(permission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        permission = get_object_or_404(
            Permission, id=id)
        permission_serializer = PermissionSerializers(permission, many=False)
        return Response(permission_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        permission = get_object_or_404(
            Permission, id=id)
        permission.delete()
        return Response('Success', status=status.HTTP_201_CREATED)

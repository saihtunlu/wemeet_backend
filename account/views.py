from .models import User
from rest_framework import status
from rest_framework import generics, pagination
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

# Create your views here.


class Users(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.order_by('id').reverse()
    serializer_class = UserSerializer
    pagination_class = pagination.PageNumberPagination


class Auth(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        data = request.data
        data['email'] = request.user.email
        data['is_superuser'] = request.user.is_superuser
        user_serializer = UserSerializer(request.user, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user_serializer = UserSerializer(request.user, many=False)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

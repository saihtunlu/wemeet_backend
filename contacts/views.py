from .models import Friendship, FriendshipRequest, UserBlocks
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .serializers import FriendshipSerializers, FriendshipRequestSerializers, UserBlocksSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

# Create your views here.


class FriendRequests(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        User = get_user_model()
        to_user = User.objects.get(id=request.data['request_to'])
        FriendshipRequest.objects.create(
            from_user=request.user,
            to_user=to_user,
            message=data['message'],
        )
        return Response({"message": 'Successfully sent request!'}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        id = kwargs['id']
        action = kwargs['action']
        print(kwargs)
        if action == "decline":
            get_object_or_404(FriendshipRequest, id=id).decline()
            return Response({"message": 'Successfully declined request!'}, status=status.HTTP_201_CREATED)
        elif action == "accept":
            get_object_or_404(FriendshipRequest, id=id).accept()
            return Response({"message": 'Successfully accepted request!'}, status=status.HTTP_201_CREATED)
        elif action == "cancel":
            get_object_or_404(FriendshipRequest, id=id).cancel()
            return Response({"message": 'Successfully cancelled request!'}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        requestedUsers = FriendshipRequest.objects.filter(to_user=request.user)
        FriendshipRequest_serializers = FriendshipRequestSerializers(
            requestedUsers, many=True)
        return Response(FriendshipRequest_serializers.data, status=status.HTTP_201_CREATED)


class FriendLists(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        friends = Friendship.objects.filter(owner=request.user)
        Friendship_serializers = FriendshipSerializers(
            friends, many=True)
        return Response(Friendship_serializers.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        User = get_user_model()
        target_user = User.objects.get(id=id)
        Friendship.objects.unfriend(
            request.user, target_user)

        return Response('Success', status=status.HTTP_201_CREATED)

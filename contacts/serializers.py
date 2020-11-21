from rest_framework import serializers
from account.serializers import UserSerializer
from .models import FriendshipRequest, UserBlocks, Friendship


class FriendshipSerializers(serializers.ModelSerializer):

    friend = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'owner', 'friend', 'created_at', 'updated_at']


class FriendshipRequestSerializers(serializers.ModelSerializer):
    from_user = UserSerializer(many=False, read_only=True)
    to_user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ['id', 'from_user', 'to_user', 'message',
                  'accepted', 'created_at', 'updated_at']


class UserBlocksSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    blocks = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserBlocks
        fields = ['id', 'user', 'blocks', 'created_at', 'updated_at']

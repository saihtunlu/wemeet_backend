from rest_framework import serializers
from .models import Post, Like, Comment, CommentReplies, CommentLike
from account.serializers import UserSerializer
from django.contrib.auth.models import User


# Comment-Replies


class CommentRepliesSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    # post = PostSerializers(many=False, read_only=True)

    class Meta:
        model = CommentReplies
        fields = ['user',  'image', 'text', 'id', 'created_at', 'comment']
# Comments


class CountCommentLikeSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = CommentLike
        fields = ['comment', 'user']


class CommentSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    commentReplies = CommentRepliesSerializers(many=True, read_only=True)
    commentlikes = CountCommentLikeSerializers(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['user',  'image', 'text', 'id', 'created_at',
                  'commentlikes', 'commentReplies']


class CountLikeSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Like
        fields = ['post', 'user']
# comment-likes


class CommentLikeSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    comment = CommentSerializers(many=False, read_only=True)

    class Meta:
        model = CommentLike
        fields = ['user', 'comment']

# Posts


class PostSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    likes = CountLikeSerializers(many=True, read_only=True)
    comments = CommentSerializers(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['comments', 'id', 'content', 'created_at',
                  'image', 'user', 'likes']

# Like


class LikeSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    post = PostSerializers(many=False, read_only=True)

    class Meta:
        model = Like
        fields = ['user', 'post']

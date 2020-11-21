from .models import Post, Like, Comment, CommentReplies, CommentLike
from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import generics, pagination
from .serializers import (PostSerializers, LikeSerializers,
                          CommentSerializers, CommentRepliesSerializers, CommentLikeSerializers)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import json
# from .permissions import IsStaff
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework_tracking.mixins import LoggingMixin
from django.http import HttpResponse
from tablib import Dataset
from .resource import PostResource


# Create your views here.


class PostsView(LoggingMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.order_by('created_at').reverse()
    serializer_class = PostSerializers
    pagination_class = pagination.PageNumberPagination


class ExportPost(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Get selected option from form
        file_format = request.POST['file-format']
        post_resource = PostResource()
        dataset = post_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(
                dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(
                dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response


class ImportPost(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        post_resource = PostResource()
        dataset = Dataset()
        new_posts = request.FILES['importData']
        dataset.load(
            new_posts.read().decode('utf-8'), format='json')
        result = post_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            # Import now
            post_resource.import_data(dataset, dry_run=False)
            return Response(result.has_errors(), status=status.HTTP_201_CREATED)


class FilterPosts(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['content', 'user__username']


class SendEmail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        send_mail(
            'Subject here',
            'Here is the message.',
            'venomarcer@gmail.com',
            ['venomarcer14996@gmail.com'],
            fail_silently=False,
        )
        return Response('Success', status=status.HTTP_201_CREATED)


class Post_Detail(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        post = Post(user=self.request.user)
        post_serializer = PostSerializers(post, data=data)
        if post_serializer.is_valid():
            post_serializer.save()
            if data['type'] == "has_comments":
                for comment in data['comments']:
                    print(comment)
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        id = kwargs['id']
        post = Post.objects.get(user=self.request.user, id=id)
        post_serializer = PostSerializers(post, data=data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        post = get_object_or_404(
            Post, id=id)
        post_serializer = PostSerializers(post, many=False)
        return Response(post_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        post = Post.objects.get(user=self.request.user, id=id)
        post.delete()
        return Response('Success', status=status.HTTP_201_CREATED)


class AuthPost(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = Post.objects.filter(user=user_id)
        serializer = PostSerializers(queryset, many=True)
        return Response(serializer.data)


class RemovePost(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        Post.objects.get(user=self.request.user,
                         id=request.data['post_id']).delete()
        return Response('Success', status=status.HTTP_201_CREATED)


# Like
class AddLike(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        LikedPost = Post.objects.get(id=request.data['post_id'])
        like = Like(user=self.request.user,
                    post=LikedPost)  # add foreign key
        like_serializer = LikeSerializers(like, data=data)
        if like_serializer.is_valid():
            like_serializer.save()
            return Response('Success', status=status.HTTP_201_CREATED)
        else:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)


class RemoveLike(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        Like.objects.get(user=self.request.user,
                         post=request.data['post_id']).delete()
        return Response('Success', status=status.HTTP_201_CREATED)

# Comments


class AddComment(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        LikedPost = Post.objects.get(id=request.data['post_id'])
        comment = Comment(user=self.request.user,
                          post=LikedPost)  # add foreign key
        comment_serializer = CommentSerializers(comment, data=data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveComment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        Comment.objects.get(user=self.request.user,
                            id=request.data['comment_id']).delete()
        return Response('Success', status=status.HTTP_201_CREATED)

# Comment-replies


class AddCommentReply(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        RepliedComment = Comment.objects.get(id=request.data['comment_id'])
        commentReply = CommentReplies(user=self.request.user,
                                      comment=RepliedComment)  # add foreign key
        comment_reply_serializer = CommentRepliesSerializers(
            commentReply, data=data)
        if comment_reply_serializer.is_valid():
            comment_reply_serializer.save()
            return Response(comment_reply_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(comment_reply_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCommentReply(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        CommentReplies.objects.get(user=self.request.user,
                                   id=request.data['reply_id']).delete()
        return Response('Success', status=status.HTTP_201_CREATED)

# comment-likes


class AddCommentLike(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        LikedComment = get_object_or_404(
            Comment, id=request.data['comment_id'])
        like = CommentLike(user=self.request.user,
                           comment=LikedComment)  # add foreign key
        like_serializer = CommentLikeSerializers(like, data=data)
        if like_serializer.is_valid():
            like_serializer.save()
            return Response(like_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCommentLike(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        CommentLike.objects.get(user=self.request.user,
                                comment=request.data['comment_id']).delete()
        return Response('Success', status=status.HTTP_201_CREATED)

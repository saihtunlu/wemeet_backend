from django.urls import path
from .views import (PostsView, ImportPost, ExportPost, FilterPosts, Post_Detail, AuthPost, RemovePost, AddComment, RemoveComment, SendEmail,
                    AddLike, RemoveLike, AddCommentReply, RemoveCommentReply, AddCommentLike, RemoveCommentLike)

urlpatterns = [
    path('posts/', PostsView.as_view(), name='posts_view'),
    path('search-posts', FilterPosts.as_view()),
    path('post/<id>', Post_Detail.as_view()),
    path('post/', Post_Detail.as_view()),
    path('delete-post/', RemovePost.as_view(), name='remove_post'),
    path('my-posts/', AuthPost.as_view(), name='my_posts'),
    path('comment/', AddComment.as_view()),
    path('remove-comment/', RemoveComment.as_view()),
    path('like/', AddLike.as_view()),
    path('unlike/', RemoveLike.as_view()),
    path('comment-reply/', AddCommentReply.as_view()),
    path('remove-comment-reply/', RemoveCommentReply.as_view()),
    path('like-comment/', AddCommentLike.as_view()),
    path('unlike-comment/', RemoveCommentLike.as_view()),
    path('send-email/', SendEmail.as_view()),
    path('import-posts/', ImportPost.as_view()),
    path('export-posts/', ExportPost.as_view()),

]

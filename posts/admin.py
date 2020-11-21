from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Post, CommentLike, Comment, CommentReplies, Like
from .resource import PostResource
# Register your models here.
Models = [CommentLike, Comment, CommentReplies, Like]
admin.site.register(Models)


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    pass

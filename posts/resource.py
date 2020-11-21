from import_export import widgets, fields, resources
from .models import Post
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PostResource(resources.ModelResource):

    class Meta:
        model = Post

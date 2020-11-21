from django.contrib import admin
from .models import FriendshipRequest, Friendship, UserBlocks
# Register your models here.
models = [FriendshipRequest, Friendship, UserBlocks]
admin.site.register(models)

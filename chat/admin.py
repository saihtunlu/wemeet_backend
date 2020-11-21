from django.contrib import admin
from .models import ChatSession, ChatSessionMessage
# Register your models here.
Models = [ChatSession,
          ChatSessionMessage]
admin.site.register(Models)

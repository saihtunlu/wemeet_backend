"""Models for the chat app."""

from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from account.serializers import UserSerializer

User = get_user_model()


def deserialize_user(queryset):
    serializer = UserSerializer(queryset, many=False)
    return serializer.data


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def _generate_unique_uri():
    """Generates a unique uri for the chat session."""
    return str(uuid4()).replace('-', '')[:15]


class ChatSession(TrackableDateModel):
    """ A Chat Session. The uri's are generated by taking the first 15 characters from a UUID """

    creator = models.ForeignKey(
        User, related_name='creator', null=True, on_delete=models.PROTECT)
    uri = models.URLField(default=_generate_unique_uri)
    invited_user = models.ForeignKey(
        User, related_name='invited_user', null=True, on_delete=models.PROTECT)


class ChatSessionMessage(TrackableDateModel):
    """Store messages for a session."""

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    chat_session = models.ForeignKey(
        ChatSession, related_name='messages', on_delete=models.PROTECT
    )
    text = models.TextField(max_length=2000, null=True)
    image = models.ImageField(
        upload_to='chat/', null=True)
    audio = models.FileField(upload_to='audio/', null=True)
    received = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

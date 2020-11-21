"""Views for the chat app."""

from django.http import Http404
from django.contrib.auth import get_user_model
from .models import (
    ChatSession, ChatSessionMessage, deserialize_user
)
from .serializers import ChatSessionSerializers, ChatMessageSerializers
from rest_framework import permissions, status, generics, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from mypusher import channels
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import wikipedia
from rest_framework.response import Response


class ChatBot(APIView):
    """Manage Chat sessions."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        query = request.data['query']
        print(request.data)
        try:
            return Response(wikipedia.summary(query))
        except:
            pass
        for new_query in wikipedia.search(query):
            try:
                return Response(wikipedia.summary(new_query))
            except:
                pass
        return Response("I don't know about " + query)


class ChatSessionView(APIView):
    """Manage Chat sessions."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """create a new chat session."""
        user = request.user
        check1 = ChatSession.objects.filter(
            creator=user.id, invited_user=request.data['user_id']).first()
        check2 = ChatSession.objects.filter(
            invited_user=user.id, creator=request.data['user_id']).first()
        if check1:
            return Response({
                'status': 'SUCCESS', 'uri': check1.uri,
                'creator': deserialize_user(check1.creator),
                'invited_user': deserialize_user(check1.invited_user),
                'create_date': check1.create_date
            })
        elif check2:
            return Response({
                'status': 'SUCCESS', 'uri': check2.uri,
                'creator': deserialize_user(check2.creator),
                'invited_user': deserialize_user(check2.invited_user),
                'create_date': check2.create_date
            })
        else:
            User = get_user_model()
            invited_user = User.objects.get(id=request.data['user_id'])
            chat_session = ChatSession.objects.create(
                creator=user, invited_user=invited_user)

            return Response({
                'status': 'SUCCESS', 'uri': chat_session.uri,
                'title': 'New chat session created',
                'creator': deserialize_user(chat_session.creator),
                'invited_user': deserialize_user(chat_session.invited_user),
                'create_date': chat_session.create_date
            })

    def get(self, request, *args, **kwargs):
        """create a new chat session."""
        check = ChatSession.objects.filter(uri=kwargs['uri']).first()
        return Response({
            'status': 'SUCCESS', 'uri': check.uri,
            'creator': deserialize_user(check.creator),
            'invited_user': deserialize_user(check.invited_user),
            'create_date': check.create_date
        })


class MyChatSessionsView(APIView):
    """Manage Chat sessions."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """create a new chat session."""
        ChatSessions = ChatSession.objects.filter(
            Q(creator=request.user) | Q(invited_user=request.user))
        ChatSerializers = ChatSessionSerializers(ChatSessions, many=True)
        Chats = []
        for Chat in ChatSerializers.data:
            try:
                messageObject = ChatSessionMessage.objects.filter(
                    chat_session=Chat['id']).latest('create_date')
                message = ChatMessageSerializers(messageObject, many=False)
                Chat['message'] = message.data
            except:
                Chat['message'] = {}
            Chats.append(Chat)
        return Response(Chats)


class ChatSessionMessageView(generics.GenericAPIView):
    """Create/Get Chat session messages."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """return all messages in a chat session."""
        number = int(request.GET.get('number'))
        uri = kwargs['uri']
        chat_session = ChatSession.objects.get(uri=uri)
        ChatSession_Message = reversed(ChatSessionMessage.objects.filter(
            chat_session=chat_session).order_by('-id')[:number:1])
        messages = ChatMessageSerializers(ChatSession_Message, many=True).data
        data = {
            'id': chat_session.id, 'uri': chat_session.uri,
            'messages': messages,
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        """create a new message in a chat session."""
        uri = kwargs['uri']
        chat_to = request.data['chat_to']
        data = request.data

        chat_session = ChatSession.objects.get(uri=uri)
        chat_session_message = ChatSessionMessage(
            user=self.request.user, chat_session=chat_session)

        ChatMessage_Serializers = ChatMessageSerializers(
            chat_session_message, data=data)
        if ChatMessage_Serializers.is_valid():
            ChatMessage_Serializers.save()
            channels.Chat(chat_to, ChatMessage_Serializers.data)
            return Response(ChatMessage_Serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ChatMessage_Serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageReceived(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        channels.Received(request.data['chat_session'], request.data['sender'])
        messages = ChatSessionMessage.objects.filter(
            Q(chat_session=request.data['chat_session']) | Q(received=False))
        for message in messages:
            message.received = True
            message.save()
        return Response('success', status=status.HTTP_201_CREATED)


class MessageSeen(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        channels.Seen(request.data['chat_session'], request.data['sender'])

        messages = ChatSessionMessage.objects.filter(
            Q(chat_session=request.data['chat_session']) | Q(seen=False))
        for message in messages:
            message.received = True
            message.seen = True
            message.save()
        return Response('success', status=status.HTTP_201_CREATED)


class VideoChat(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        channels.Video(
            request.data['uri'], request.data['userId'], request.data['peerId'])
        return Response('success', status=status.HTTP_201_CREATED)


def raise_404(request):
    """Raise a 404 Error."""
    raise Http404

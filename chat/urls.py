"""URL's for the chat app."""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('chats/', views.ChatSessionView.as_view()),
    path('chats/<uri>/', views.ChatSessionView.as_view()),
    path('my-chats/', views.MyChatSessionsView.as_view()),
    path('received/', views.MessageReceived.as_view()),
    path('seen/', views.MessageSeen.as_view()),
    path('test-chat/', views.ChatBot.as_view()),
    path('chats/<uri>/messages/', views.ChatSessionMessageView.as_view()),
    path('start-video-chat/', views.VideoChat.as_view()),
]

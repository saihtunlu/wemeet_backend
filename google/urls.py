
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("google-login/", views.GoogleView.as_view()),
]

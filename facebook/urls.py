
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("fb-login/", views.SignInView.as_view()),
]

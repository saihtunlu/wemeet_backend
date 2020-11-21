from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.Auth.as_view()),
    path('users/', views.Users.as_view()),
]

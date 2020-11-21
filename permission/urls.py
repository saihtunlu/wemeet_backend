"""URL's for the chat app."""
from django.urls import path

from . import views

urlpatterns = [
    path('roles/', views.Roles.as_view()),
    path('role/<int:id>/', views.SingleRole.as_view()),
    path('role/', views.SingleRole.as_view()),
    path('user-roles/', views.UserRoles.as_view()),
    path('user-role/<int:id>/', views.SingleUserRole.as_view()),
    path('user-role/', views.SingleUserRole.as_view()),
    path('permissions/', views.MyPermissions.as_view()),
    path('permission/', views.SingleMyPermission.as_view()),
    path('permission/<int:id>/', views.SingleMyPermission.as_view()),
]

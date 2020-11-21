from django.urls import path
from .views import FriendRequests, FriendLists

urlpatterns = [
    path('request/', FriendRequests.as_view()),
    path('request/<int:id>/<str:action>', FriendRequests.as_view()),
    path('friends/', FriendLists.as_view()),
    path('friend/<int:id>', FriendLists.as_view()),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.chatbot.views import web_hook
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("webhook/", web_hook, name="webhook"),
    path('', include('rest_registration.api.urls')),
    path('', include('facebook.urls')),
    path('', include('chat.urls')),
    path('', include('posts.urls')),
    path('', include('google.urls')),
    path('', include('account.urls')),
    path('', include('permission.urls')),
    path('', include('contacts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

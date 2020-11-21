from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

FACEBOOK_DEBUG_TOKEN_URL = "https://graph.facebook.com/debug_token"
FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/v8.0/oauth/access_token"
FACEBOOK_URL = "https://graph.facebook.com/me"


class SignInView(APIView):
    def post(self, request):
        User = get_user_model()
        user_access_token = request.data['access_token']
        # get users email
        # https://graph.facebook.com/{your-user-id}?fields=id,name,email&access_token={your-user-access-token}
        user_info_url = FACEBOOK_URL
        user_info_payload = {
            "fields": "id,name,email",
            "access_token": user_access_token,
        }

        user_info_request = requests.get(
            user_info_url, params=user_info_payload)
        user_info_response = json.loads(user_info_request.text)
        print(user_info_response)
        # create user if not exist
        try:
            user = User.objects.get(email=user_info_response["email"])
        except User.DoesNotExist:
            user = User()
            user.username = user_info_response["email"]
            # provider random default password
            user.password = make_password(
                BaseUserManager().make_random_password())
            user.email = user_info_response["email"]
            user.save()

        token = RefreshToken.for_user(
            user
        )  # generate token without username & password
        response = {}
        response["username"] = user.username
        response["access"] = str(token.access_token)
        response["refresh"] = str(token)
        return Response(response)

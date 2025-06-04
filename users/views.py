from .models import CustomUser, UsersProfile
from .serializers import UsersProfileSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics, permissions

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:8000/api/auth/social/google/callback/'
    client_class = OAuth2Client


class Profile(generics.RetrieveUpdateAPIView):
    serializer_class = UsersProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
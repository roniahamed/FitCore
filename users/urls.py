from django.urls import path, include
from dj_rest_auth.registration.views import VerifyEmailView
from .views import GoogleLogin

urlpatterns = [
    # Authentications
    # dj-rest-auth
    path('oauth/', include('dj_rest_auth.urls')),
    path('registration/',include('dj_rest_auth.registration.urls')),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('password-reset-confirm/<uidb64>/<token>/', lambda request, uidb64, token:None, name='password_reset_confirm'),

    # Social Authentications
    path('social/', include('allauth.socialaccount.urls')),
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
]


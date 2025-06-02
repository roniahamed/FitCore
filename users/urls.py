from django.urls import path, include
from .views import UserDelete, UserUpdate, LogoutView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    # Authentications

    # jwt Authentication 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), 

    path('update/', UserUpdate.as_view(), name='user_update'),
    path('delete/', UserDelete.as_view(), name='user_delete'),
    path('logout/', LogoutView.as_view(), name='logout'),


    # dj-rest-auth
    path('oauth/', include('dj_rest_auth.urls')),
    path('registration/',include('dj_rest_auth.registration.urls')),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent')
]


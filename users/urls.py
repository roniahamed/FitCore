from django.urls import path
from .views import UserRegister, UserDelete, UserUpdate

urlpatterns = [
    path('register/', UserRegister.as_view(), name='user_register'),
    path('update/', UserUpdate.as_view(), name='user_update'),
    path('delete/', UserDelete.as_view(), name='user_delete'),
]
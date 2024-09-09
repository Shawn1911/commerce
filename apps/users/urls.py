from django.urls import path
from users.views import (ConfirmEmailAPIView, ForgotPasswordAPIView,
                         SingUpCreateAPIView, UpdatePasswordAPIView,
                         UserUpdateAPIView,)


app_name = 'users'

urlpatterns = [
    path('reset-link', ForgotPasswordAPIView.as_view(), name='reset-link'),
    path('reset-password', UpdatePasswordAPIView.as_view(), name='reset-password'),
    path('sign-up', SingUpCreateAPIView.as_view(), name='sign-up'),
    path('confirm-email', ConfirmEmailAPIView.as_view(), name='confirm-email'),
    path('user', UserUpdateAPIView.as_view(), name='user-update'),
]

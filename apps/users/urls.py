
from django.urls import path

from users.views import (PasswordResetConfirmView, RegisterUserView,
                         ResetPasswordView, UserLoginView, UserLogoutView, EmailConfirmationView, )
app_name = 'users'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('email-confirm/<uidb64>/<token>/', EmailConfirmationView.as_view(), name='email-confirm'),
]

from django.urls import include, path
from users.views import (AuthLogoutAPIView, AuthRetrieveAPIView,
                         ConfirmEmailAPIView, LoginAPIView,)


urlpatterns = [
    path('users/', include('users.urls')),
    path('shop/', include('shops.urls')),
    path('confirm-email/<str:token>', ConfirmEmailAPIView.as_view(), name='confirm-email'),
    path('token', LoginAPIView.as_view({'post': 'post'}), name='token'),
    path('auth', AuthRetrieveAPIView.as_view()),
    path('auth/signout', AuthLogoutAPIView.as_view()),
]

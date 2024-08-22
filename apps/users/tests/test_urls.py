from django.test import SimpleTestCase
from django.urls import reverse_lazy


class TestUsersUrls(SimpleTestCase):

    def test_user_url(self):
        sign_up_url = reverse_lazy('users:register_user')
        assert sign_up_url == '/api/v1/users/register/'

        login_url = reverse_lazy('users:user_login')
        assert login_url == '/api/v1/users/login/'

        sign_out_url = reverse_lazy('users:user_logout')
        assert sign_out_url == '/api/v1/users/logout/'

        confirm_email_url = reverse_lazy('users:email-confirm', kwargs={'uidb64': 'uidb64', 'token': 'token'})
        assert confirm_email_url == '/api/v1/users/email-confirm/uidb64/token/'

        reset_link_url = reverse_lazy('users:reset-password')
        assert reset_link_url == '/api/v1/users/reset-password/'

        reset_password_url = reverse_lazy('users:reset-password-confirm', kwargs={'uidb64': 'uidb64', 'token': 'token'})
        assert reset_password_url == '/api/v1/users/reset-password-confirm/uidb64/token/'

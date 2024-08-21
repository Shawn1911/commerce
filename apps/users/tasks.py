import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from root.settings import EMAIL_HOST_USER
from users.tokens import account_activation_token

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, user_id, is_reset_password=False, base_url='http://localhost:8000'):
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        if is_reset_password:
            url = reverse('reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})
            subject = "Reset Your Password"
            text_content = f"Hello {user.username},\n\nPlease reset your password by clicking the following link:\n{base_url}{url}\n\nThank you!"
        else:
            url = reverse('email-confirm', kwargs={'uidb64': uidb64, 'token': token})
            subject = "Confirm Your Email"
            text_content = f"Hello {user.username},\n\nPlease confirm your email by clicking the following link:\n{base_url}{url}\n\nThank you!"

        confirmation_url = f"{base_url}{url}"

        context = {
            'username': user.username,
            'confirmation_url': confirmation_url,
            'is_reset_password': is_reset_password
        }

        from_email = EMAIL_HOST_USER
        to_email = [user.email]

        html_content = render_to_string('apps/users/emails/confirmation_or_reset_email.html', context)

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()

    except AttributeError as exc:
        logger.error(f"AttributeError occurred: {str(exc)}")
        self.retry(exc=exc)
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist.")
    except Exception as exc:
        logger.error(f"An unexpected error occurred: {str(exc)}")
        self.retry(exc=exc)

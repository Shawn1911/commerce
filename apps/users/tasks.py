from celery import shared_task
from django.core.mail import send_mail

from root.settings import EMAIL_HOST_USER


@shared_task
def send_email(email, message, subject):
    send_mail(
        subject,
        '',
        EMAIL_HOST_USER,
        [email],
        html_message=message,
    )

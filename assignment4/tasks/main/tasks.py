from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True, max_retries=3)
def send_email_task(self, recipient, subject, body):
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient]
        )
        return 'Email sent successfully!'
    except Exception as exc:
        self.retry(exc=exc, countdown=60) 
from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from lms.models import Subscription


@shared_task
def update_message():
    status = True
    if Subscription.objects.filter(status=status).exists():
        print('Сообщение о обновлении материала курса')

        recipient_list = Subscription.objects.filter(status=status).values_list('user__email', flat=True)

        send_mail(
            subject='Сообщение о обновлении материала курса',
            message='Материалы курса обновились',
            from_email=EMAIL_HOST_USER,
            recipient_list=list(recipient_list)
        )

from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config.settings import EMAIL_HOST_USER
from lms.models import Subscription, Course


@shared_task
def update_message(id):

    recipient_list = Subscription.objects.filter(status=True, course=id).values_list('user__email', flat=True)

    send_mail(
        subject='Сообщение о обновлении материала курса',
        message='Материалы курса обновились',
        from_email=EMAIL_HOST_USER,
        recipient_list=list(recipient_list)
    )

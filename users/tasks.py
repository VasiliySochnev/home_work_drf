from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def exam_user():
    """Задача для проверки активности пользователя."""

    User = get_user_model()
    count_days = timezone.now() - timedelta(days=30)
    active_users = User.objects.filter(last_login__lt=count_days)

    for user in active_users:
        if user.is_active:
            user.is_active = False
            user.save()
            print(f"{user.email} переведен в статус:{user.is_active}")

    return None

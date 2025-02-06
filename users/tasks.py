from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()
def exam_user(User):

    count_days = timezone.now() - timedelta(days=7)
    active_users = User.objects.filter(last_login__gte=count_days)

    for user in active_users:
        if user.is_active:
            user.is_active = False
        return print(f"{user.username} переведен в статус:{user.is_active}")

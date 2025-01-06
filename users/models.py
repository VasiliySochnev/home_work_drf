from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course


class User(AbstractUser):
    """Модель пользователя."""
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(
        max_length=35, verbose_name="телефон", blank=True, null=True
    )
    city = models.CharField(max_length=100, verbose_name="город", blank=True, null=True)
    avatar = models.ImageField(
        upload_to="photo/avatars/", verbose_name="Аватар", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email}"


class Payments(models.Model):
    """Модель платежи."""

    CASH = "Наличные"
    TRANSFER = "Перевод на счет"

    WAY_PAY_CHOICES = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True, related_name='user')
    date_pay = models.DateTimeField(verbose_name='Дата платежа', blank=True, null=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', blank=True, null=True, related_name='paid_course')
    amount_pay = models.PositiveIntegerField(verbose_name='Сумма оплаты', blank=True, null=True)
    way_pay = models.CharField(max_length=50, choices=WAY_PAY_CHOICES, verbose_name='Способ оплаты', blank=True, null=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.amount_pay}"
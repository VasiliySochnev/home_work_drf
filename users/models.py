from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=35, verbose_name="телефон", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="город", blank=True, null=True)
    avatar = models.ImageField(upload_to="photo/avatars/", verbose_name="Аватар", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
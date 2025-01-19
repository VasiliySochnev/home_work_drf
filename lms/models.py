from django.db import models

from config import settings
from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    """Модель курса."""

    title = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(max_length=250, verbose_name="Описание курса")
    image = models.ImageField(
        upload_to="img/img_course/", verbose_name="превью", blank=True, null=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.title}"


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(max_length=250, verbose_name="Описание урока")
    image = models.ImageField(
        upload_to="img/img_lesson/", verbose_name="превью", blank=True, null=True
    )
    url = models.URLField(
        max_length=200, blank=True, null=True, verbose_name="Ссылка на видео"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.title}"


class Subscription(models.Model):
    """Модель подписка на обновление курса"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    status = models.BooleanField(default=True, verbose_name="Активна", null=True, blank=True)
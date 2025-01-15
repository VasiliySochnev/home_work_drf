from django.contrib import admin

from lms.models import Course, Lesson
from users.models import Payments, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "avatar",
        "email",
        "first_name",
        "last_name",
        "phone",
        "city",
    )
    search_fields = ("email",)
    list_filter = ("email",)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "date_pay",
        "paid_course",
        "amount_pay",
        "way_pay",
    )
    search_fields = ("user",)
    list_filter = ("paid_course",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "image",
    )
    search_fields = ("title",)
    list_filter = ("title",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "url",
        "course",
    )
    search_fields = ("title",)
    list_filter = ("course",)

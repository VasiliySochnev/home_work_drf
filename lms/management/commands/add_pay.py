from django.core.management.base import BaseCommand

from lms.models import Course
from users.models import Payments, User


class Command(BaseCommand):
    help = "Adding payments"

    def handle(self, *args, **options):
        User.objects.all()
        Course.objects.all()
        Payments.objects.all()

        course, _ = Course.objects.get_or_create(title="C1", description="good C1")

        user, _ = User.objects.get_or_create(
            email="student1@mail.ru", first_name="Ivan", last_name="Ivanov"
        )

        payments = [
            {
                "user": user,
                "paid_course": course,
                "amount_pay": 115000,
                "way_pay": "Перевод на счет",
            }
        ]

        for payment_data in payments:
            payment, created = Payments.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added payment: {payment.paid_course} {payment.way_pay}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Payment already exists: {payment.paid_course} {payment.way_pay}"
                    )
                )

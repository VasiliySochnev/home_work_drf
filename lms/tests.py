from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """Тест-кейс для тестирования CRUD-операций уроков."""

    def setUp(self):
        # Создаем пользователей
        self.owner = User.objects.create(
            email="owner@mail.ru", password="ownerpassword"
        )
        self.moderator = User.objects.create(
            email="moderator@mail.ru", password="moderatorpassword"
        )
        self.regular_user = User.objects.create(
            email="regular@mail.ru", password="regularpassword"
        )

        # Создаем группы
        self.moderator_group = Group.objects.create(name="Модераторы")
        self.regular_user_group = Group.objects.create(name="Пользователи")

        # Добавляем пользователей в группы
        self.moderator.groups.add(self.moderator_group)
        self.regular_user.groups.add(self.regular_user_group)

        # Создаем курс для тестирования, владелец курса будет 'owner'
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.owner
        )

        # Создаем уроки для этого курса, владелец уроков будет 'owner'
        self.lesson1 = Lesson.objects.create(
            title="Lesson 1",
            description="Lesson 1",
            course=self.course,
            owner=self.owner,
        )
        self.lesson2 = Lesson.objects.create(
            title="Lesson 2",
            description="Lesson 2",
            course=self.course,
            owner=self.owner,
        )

    def test_regular_user_can_list_lessons(self):
        """Тестирование списка уроков для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get("/lesson/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_moderator_can_list_and_edit_lessons(self):
        """Тестирование списка и редактирования уроков для модератора."""
        self.client.force_authenticate(user=self.moderator)

        # Проверка списка уроков
        response = self.client.get("/lesson/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

        # Попытка редактирования урока
        data = {"title": "Updated Lesson 1", "description": "Updated Lesson 1"}
        response = self.client.patch(f"/lesson/update/{self.lesson1.id}/", data)
        self.assertEqual(response.status_code, 200)

    def test_owner_can_edit_lessons(self):
        """Тестирование редактирования уроков для владельца."""
        self.client.force_authenticate(user=self.owner)

        data = {"title": "Updated Lesson 1", "description": "Updated Lesson 1"}
        response = self.client.patch(f"/lesson/update/{self.lesson1.id}/", data)
        self.assertEqual(response.status_code, 200)

        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.title, "Updated Lesson 1")  # Проверяем обновление

    def test_regular_user_cannot_edit_lessons(self):
        """Тестирование, что обычный пользователь не может редактировать уроки."""
        self.client.force_authenticate(user=self.regular_user)

        data = {
            "title": "Attempt to Update Lesson",
            "description": "Attempt to Update Lesson",
        }
        response = self.client.patch(f"/lesson/update/{self.lesson1.id}/", data)
        self.assertEqual(response.status_code, 403)

    def test_owner_can_destroy_lessons(self):
        """Тестирование удаления уроков для владельца."""
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(f"/lesson/delete/{self.lesson1.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_regular_user_cannot_destroy_lessons(self):
        """Тестирование, что обычный пользователь не может удалить уроки."""
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.delete(f"/lesson/delete/{self.lesson1.id}/")
        self.assertEqual(response.status_code, 403)

    def tearDown(self):
        # Очищаем данные после теста
        self.owner.delete()
        self.moderator.delete()
        self.regular_user.delete()
        self.course.delete()
        self.lesson1.delete()
        self.lesson2.delete()
        self.moderator_group.delete()
        self.regular_user_group.delete()


class SubscriptionTestCase(APITestCase):
    """Тестирование функционала подписки."""

    def setUp(self):
        # Создаем тестового пользователя и курс
        self.user = User.objects.create(email="test@mail.ru", password="password123")
        self.course = Course.objects.create(
            title="Test Course", description="Test Description"
        )

    def test_create_subscription(self):
        # Создаем подписку
        subscription = Subscription.objects.create(user=self.user, course=self.course)

        # Проверяем, что подписка создана
        self.assertIsNotNone(subscription.id)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)
        self.assertTrue(subscription.status)  # По умолчанию статус True

    def test_subscription_status_default(self):
        # Создаем подписку без указания статуса
        subscription = Subscription.objects.create(user=self.user, course=self.course)

        # Проверяем, что статус по умолчанию True
        self.assertTrue(subscription.status)

    def test_subscription_status_change(self):
        # Создаем подписку
        subscription = Subscription.objects.create(user=self.user, course=self.course)

        # Меняем статус подписки
        subscription.status = False
        subscription.save()

        # Проверяем, что статус изменился
        self.assertFalse(subscription.status)

    def tearDown(self):
        # Очищаем данные после теста
        self.user.delete()
        self.course.delete()

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.serializers import (CourseSerializer, LessonSerializer,
                             PaymentsSerializer)
from users.models import Payments
from users.permissions import Is_Users, Owner, Staff


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self, permission_classes=None):
        if self.action in ("destroy", "update"):
            permission_classes = [Owner]
        elif self.action in ("update", "retrieve"):
            permission_classes = [Staff]
        elif self.action == "create":
            permission_classes = [Is_Users, IsAuthenticated, ~Staff]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~Staff]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [Staff | Owner]


class LessonDestroyAPIView(generics.DestroyAPIView):

    queryset = Lesson.objects.all()
    permission_classes = [Owner]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "way_pay")
    ordering_fields = ("date_pay",)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее

        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        # Возвращаем ответ в API

        return Response({"message": message}, status=status.HTTP_200_OK)
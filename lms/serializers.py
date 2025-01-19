from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import UrlValidator
from users.models import Payments


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field='url')]



class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, instans):
        return instans.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return Subscription.objects.filter(user=user, course=obj).exists()


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"

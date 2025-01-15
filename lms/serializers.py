from rest_framework import serializers

from lms.models import Course, Lesson
from users.models import Payments


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    # course_lessons = serializers.CharField(
    #     source="lesson_set.all.lesson", read_only=True
    # )
    lessons = LessonSerializer(many=True)

    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, instans):

        return instans.lessons.count()


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"

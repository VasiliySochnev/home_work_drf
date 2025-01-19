from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import UrlValidator
from users.models import Payments


class LessonSerializer(serializers.ModelSerializer):
    # url = serializers.CharField(validators=[UrlValidator(field='url')])

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field='url')]



class CourseSerializer(serializers.ModelSerializer):
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

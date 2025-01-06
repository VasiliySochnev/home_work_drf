from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    lesson_count = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, instans):
        if instans.lessons.all().count():
            return instans.lessons.all().count()
        return 0


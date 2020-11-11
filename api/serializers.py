from rest_framework import serializers

from api.models import Course, Student, CourseParticipant


class CourseSerializer(serializers.ModelSerializer):
    students_amount = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class CourseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseParticipant
        fields = '__all__'

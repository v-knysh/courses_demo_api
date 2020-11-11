from rest_framework import serializers

from api.models import Course, Student, CourseParticipant


class CourseSerializer(serializers.ModelSerializer):
    students_amount = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({"end_date": "finish must occur after start"})
        return data


class CourseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseParticipant
        fields = '__all__'

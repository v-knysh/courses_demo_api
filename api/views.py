# Create your views here.
import csv

from django.db.models import Count, F, Subquery, OuterRef, Value
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import viewsets

from api.models import Course, Student, CourseParticipant
from api.serializers import CourseSerializer, StudentSerializer, CourseParticipantSerializer


def index(request):
    return redirect('/api')


def report(request):
    report_columns = ['full_name', 'courses_amount', 'completed_amount']

    students_data = student_report_qs().values(*report_columns)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'
    writer = csv.DictWriter(response, fieldnames=report_columns)
    writer.writeheader()
    for row in students_data:
        writer.writerow(row)
    return response


def student_report_qs():
    return Student.objects.annotate(
        full_name=Concat('first_name', Value(" "), 'last_name'),
        completed_amount=Subquery(
            Student.objects.filter(
                id=OuterRef('id'),
                courseparticipant__completed=True
            ).annotate(c=Count('courseparticipant')).values('c')
        ),
        courses_amount=Count(F('courseparticipant__id')),
    )


class CoursesViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all().annotate(students_amount=Count(F('courseparticipant__id')))
    serializer_class = CourseSerializer


class StudentsViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseParticipantsViewset(viewsets.ModelViewSet):
    queryset = CourseParticipant.objects.all()
    serializer_class = CourseParticipantSerializer

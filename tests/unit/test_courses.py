import datetime

from django.test import TestCase

from api.models import Student, Course, CourseParticipant
from api.views import student_report_qs


class AggregationTestCase(TestCase):
    def setUp(self):
        course_a = Course(
            name=f'Course A',
            description='',
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=1),
        )
        course_b = Course(
            name=f'Course B',
            description='',
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=1),
        )
        course_a.save()
        course_b.save()

        student_a = Student(first_name="Student A", last_name= "aaa", email="a@gail.com")
        student_b = Student(first_name="Student B", last_name= "bbb", email="b@gail.com")
        student_a.save()
        student_b.save()

        participants = [
            CourseParticipant(course=course_a, student=student_a, completed=True),
            CourseParticipant(course=course_b, student=student_b, completed=False),
            CourseParticipant(course=course_a, student=student_b, completed=True),
        ]
        CourseParticipant.objects.bulk_create(participants)

    def test_report_data_a_correct(self):
        report_data = (student_report_qs().values())
        student_a = Student.objects.filter(first_name='Student A').first()
        report_data_a = [r for r in report_data if r['id'] == student_a.id][0]
        self.assertEqual(report_data_a['full_name'], f"Student A aaa")
        self.assertEqual(report_data_a['full_name'], f"{student_a.first_name} {student_a.last_name}")

        self.assertEqual(report_data_a['courses_amount'], 1)
        self.assertEqual(report_data_a['completed_amount'], 1)

    def test_report_data_b_correct(self):
        report_data = (student_report_qs().values())
        student_b = Student.objects.filter(first_name='Student B').first()
        report_data_b = [r for r in report_data if r['id'] == student_b.id][0]
        self.assertEqual(report_data_b['full_name'], f"Student B bbb")
        self.assertEqual(report_data_b['full_name'], f"{student_b.first_name} {student_b.last_name}")

        self.assertEqual(report_data_b['courses_amount'], 2)
        self.assertEqual(report_data_b['completed_amount'], 1)
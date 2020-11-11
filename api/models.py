from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()


class CourseParticipant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    completed = models.BooleanField()

from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'courses', views.CoursesViewset, 'courses')
router.register(r'students', views.StudentsViewset, 'students')
router.register(r'course_participants', views.CourseParticipantsViewset, 'course_participants')

urlpatterns = [
    path('', views.index, name='index'),
    path('report', views.report, name='report'),
    path('api/', include(router.urls), name='api'),
]
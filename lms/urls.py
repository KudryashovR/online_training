from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView, SubscriptionView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
]

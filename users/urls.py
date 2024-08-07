from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import PaymentViewSet, UserProfileRetrieveUpdateAPIView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileRetrieveUpdateAPIView.as_view(), name='user-profile'),
]

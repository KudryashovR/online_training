from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.serializers import UserCreate, UserList, UserDetail
from users.views import PaymentViewSet, UserProfileRetrieveUpdateAPIView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileRetrieveUpdateAPIView.as_view(), name='user-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreate.as_view(), name='create_user'),
    path('users/', UserList.as_view(), name='list_users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='detail_user'),
]

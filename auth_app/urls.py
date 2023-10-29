
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth_app.apps import AuthAppConfig
from auth_app.views import UserCreateAPIView

app_name = AuthAppConfig.name


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
]

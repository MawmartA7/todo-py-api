from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import CreateUserView
from django.urls import path

urlpatterns = [
    path('register/', CreateUserView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('token/verify/', TokenVerifyView.as_view(), name="verify_token"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh"),
]

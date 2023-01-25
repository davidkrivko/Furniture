from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.views import RegistrationView, UserView


urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("me/", UserView.as_view(), name="user"),
]

app_name = "user"

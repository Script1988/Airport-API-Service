from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.views import CreateUserView, ManageUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create_user"),
    path("token/", TokenObtainPairView.as_view(), name="obtain_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify_token"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"

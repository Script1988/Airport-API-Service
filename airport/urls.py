from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
# router.register()

urlpatterns = [path("", include(router.urls))]

app_name = "airport"

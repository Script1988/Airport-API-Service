from django.urls import path, include
from rest_framework import routers

from airport.views import OrderViewSet, CrewViewSet, AirportViewSet

router = routers.DefaultRouter()
router.register("orders", OrderViewSet)
router.register("crew", CrewViewSet)
router.register("airport", AirportViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"

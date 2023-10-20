from django.urls import path, include
from rest_framework import routers

from airport.views import (
    OrderViewSet,
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
)

router = routers.DefaultRouter()
router.register("orders", OrderViewSet)
router.register("crew", CrewViewSet)
router.register("airport", AirportViewSet)
router.register("route", RouteViewSet)
router.register("airplane_type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"

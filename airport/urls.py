from django.urls import path, include
from rest_framework import routers

from airport.views import (
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    FlightViewSet,
)

router = routers.DefaultRouter()
router.register("crew", CrewViewSet, basename="crew")
router.register("airport", AirportViewSet, basename="airport")
router.register("route", RouteViewSet, basename="route")
router.register("airplane_type", AirplaneTypeViewSet, basename="airplane_type")
router.register("airplane", AirplaneViewSet, basename="airplane")
router.register("flight", FlightViewSet, basename="flight")

urlpatterns = [path("", include(router.urls))]

app_name = "airport"

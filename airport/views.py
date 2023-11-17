from datetime import datetime
from typing import Type

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from rest_framework.serializers import Serializer

from django.db.models import F, Count

from airport.models import Crew, Airport, Route, AirplaneType, Airplane, Flight
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (
    CrewSerializer,
    CrewDetailSerializer,
    AirportSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    RouteSerializer,
    FlightSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return CrewDetailSerializer

        return self.serializer_class


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer

        return self.serializer_class


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneListSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related("route", "airplane").prefetch_related("crew").annotate(
        tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
        )
    )
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer

        return self.serializer_class

    def get_queryset(self) -> str:
        """Filtering the flights"""
        source_airport = self.request.query_params.get("source_airport")
        source_city = self.request.query_params.get("source_city")
        destination_airport = self.request.query_params.get("destination_airport")
        destination_city = self.request.query_params.get("destination_city")
        departure_time = self.request.query_params.get("departure_time")

        queryset = self.queryset

        if source_airport:
            queryset = queryset.filter(route__source__name__icontains=source_airport)

        if source_city:
            queryset = queryset.filter(
                route__source__closest_big_city__icontains=source_city
            )

        if destination_airport:
            queryset = queryset.filter(
                route__destination__name__icontains=destination_airport
            )

        if destination_city:
            queryset = queryset.filter(
                route__destination__closest_big_city__icontains=destination_city
            )

        if departure_time:
            date = datetime.strptime(departure_time, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__icontains=date)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source_airport",
                type=OpenApiTypes.STR,
                description="Filter by flight source airport (ex. ?source_airport=Heathrow)",
            ),
            OpenApiParameter(
                "source_city",
                type=OpenApiTypes.STR,
                description="Filter by flight source city (ex. ?source_city=London)",
            ),
            OpenApiParameter(
                "destination_airport",
                type=OpenApiTypes.STR,
                description="Filter by flight destination airport (ex. ?destination_airport=Heathrow)",
            ),
            OpenApiParameter(
                "destination_city",
                type=OpenApiTypes.STR,
                description="Filter by flight destination city (ex. ?destination_city=London)",
            ),
            OpenApiParameter(
                "departure_time",
                type=OpenApiTypes.DATE,
                description=(
                        "Filter by flight departure time"
                        "(ex. ?date=2023-10-23)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs) -> tuple:
        return super().list(request, *args, **kwargs)



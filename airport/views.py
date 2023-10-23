from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from django.db.models import F, Count

from airport.models import Order, Crew, Airport, Route, AirplaneType, Airplane, Flight
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (
    OrderSerializer,
    OrderListSerializer,
    CrewSerializer,
    AirportSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
)


class CrewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteListSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
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
    serializer_class = FlightListSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightDetailSerializer

        return self.serializer_class

    def get_queryset(self):
        """Filtering the flights"""
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        queryset = self.queryset

        if source:
            queryset = queryset.filter(route__source__name__icontains=source)

        if destination:
            queryset = queryset.filter(route__destination__name__icontains=destination)

        return queryset.distinct()


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route", "tickets__flight__airplane"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    # def get_serializer_class(self):
    #     if self.action == "list":
    #         return OrderListSerializer
    #
    #     return OrderSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

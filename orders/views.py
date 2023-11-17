from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from typing import Type
from rest_framework.serializers import Serializer

from orders.models import Order
from orders.serializers import OrderSerializer, OrderListSerializer


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

    def get_queryset(self) -> Order:
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return OrderListSerializer

        return self.serializer_class

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

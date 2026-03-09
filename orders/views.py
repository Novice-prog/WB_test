from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Order
from .serializer import OrderSerializer
from .services.order_service import OrderService


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related("items__product")
        )

    def create(self, request, *args, **kwargs):

        try:
            order = OrderService.create_order(request.user)
        except ValueError as e:
            raise ValidationError(str(e))

        serializer = self.get_serializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
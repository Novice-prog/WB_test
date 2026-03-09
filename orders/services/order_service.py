from django.db import transaction
from cart.models import CartItem
from orders.models import Order, OrderItem
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(user):

        cart_items = (
            CartItem.objects
            .select_related("product")
            .select_for_update()
            .filter(user=user)
        )

        if not cart_items.exists():
            raise ValueError("Cart is empty")

        cart_items = list(cart_items)

        total_price = Decimal("0.00")

        for item in cart_items:
            if item.product.stock < item.quantity:
                raise ValueError(f"Not enough stock for {item.product.name}")

            total_price += item.product.price * item.quantity

        if user.balance < total_price:
            raise ValueError("Not enough balance")

        user.balance -= total_price
        user.save(update_fields=["balance"])

        order = Order.objects.create(
            user=user,
            total_price=total_price
        )

        order_items = []
        products_to_update = []

        for item in cart_items:
            order_items.append(
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            )

            item.product.stock -= item.quantity
            products_to_update.append(item.product)

        OrderItem.objects.bulk_create(order_items)

        from products.models import Product
        Product.objects.bulk_update(products_to_update, ["stock"])

        CartItem.objects.filter(user=user).delete()

        logger.info(f"Order {order.id} created for user {user.id}")

        return order
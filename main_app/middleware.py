from django.utils.timezone import now
from .models import AbandonedCart, AbandonedCartItem, product

class AbandonedCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and "cart" in request.session:
            cart_data = request.session.get("cart", {})

            if cart_data:
                abandoned_cart, created = AbandonedCart.objects.get_or_create(user=request.user)

                for product_id, item in cart_data.items():
                    product_instance = product.objects.get(id=product_id)

                    AbandonedCartItem.objects.update_or_create(
                        cart=abandoned_cart,
                        product=product_instance,
                        defaults={"quantity": item["quantity"]},
                    )

                abandoned_cart.last_updated = now()
                abandoned_cart.save()

        return response

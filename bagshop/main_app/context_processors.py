# main_app/context_processors.py
from django.shortcuts import get_object_or_404
from main_app.models import product

def cart_context(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        prod = get_object_or_404(product, id=product_id)
        cart_items.append({
            'id': prod.id,
            'name': prod.name,
            'quantity': item['quantity'],
            'price': prod.price,
            'total_item_price': prod.price * item['quantity'],
        })
        total_price += prod.price * item['quantity']

    return {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': len(cart_items),
    }

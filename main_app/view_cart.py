from .models import product, Order
from django.shortcuts import render, get_object_or_404,redirect
from django.core.mail import send_mail


# Displaying the cart
def cart(request):
    cart = request.session.get('cart', {})
    cart_items =[]
    total_price =0 

    for product_id, item in cart.items():
        product_obj = get_object_or_404(product, id=product_id)
        item_total = product_obj.price * item['quantity']
        total_price += item_total
        
        cart_items.append({'id':product_obj.id, 'name':product_obj.name, 'price':product_obj.price,
                           'quantity':item['quantity'], 'total':item_total, 'image':product_obj.image})
        
    return render(redirect, 'index.html', {'cart_items':cart_items,'total_price':total_price })

# Add to cart functionality
def add_to_cart(request):
    

    return render(request,)
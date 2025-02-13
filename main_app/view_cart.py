from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from main_app.models import product

# View Cart
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, item in cart.items():
        product = get_object_or_404(product, id=product_id)
        cart_items.append({
            'id': product.id,
            'name': product.name,
            'quantity': item['quantity'],
            'price': product.price * item['quantity'],
        })
        total_price += product.price * item['quantity']
    
    return render(request, 'index.html', {'cart_items': cart_items, 'total_price': total_price})

# Add to Cart
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = {'quantity': cart.get(str(product_id), {}).get('quantity', 0) + 1}
    request.session['cart'] = cart
    return redirect('/')

# Remove Item from Cart
def delete_item(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('/')

# Update Cart Item
def update_item(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity
        request.session['cart'] = cart
    return redirect('/')

# Clear Cart
def clear(request):
    request.session['cart'] = {}
    return redirect('/')

# Checkout (Send Email & Clear Cart)
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('/')
    
    cart_items = []
    total_price = 0
    for product_id, item in cart.items():
        product = get_object_or_404(product, id=product_id)
        cart_items.append(f"{product.name} x {item['quantity']} - ${product.price * item['quantity']}")
        total_price += product.price * item['quantity']
    
    cart_summary = "\n".join(cart_items)
    
    # Send email
    subject = "Order Confirmation"
    message = f"Thank you for your order!\n\nYour Items:\n{cart_summary}\n\nTotal: ${total_price}"
    user_email = request.user.email if request.user.is_authenticated else 'customer@example.com'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email, settings.DEFAULT_FROM_EMAIL])
    
    request.session['cart'] = {}
    return redirect('/')

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
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] ['quantity'] +=1
    else:
        cart[str(product_id)] = {'quantity':1}

    request.session['cart'] = cart

    return redirect('index.html')

# update cart Functionality

def update_item(request, product_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity
            request.session['cart'] = cart

        return redirect('index.html')
    
# Remove cart item functionality

def remove_item(request, product_id):

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect('index.html')

# Clearing cart

def clear(request):
    request.session['cart'] = {}
    return redirect('index.html')

# checkout and email

def checkout(request):
    if request.method == 'POST':
        customer_email = request.POST.get("email")
        cart = request.session.get('cart', {})

        if not cart:
            return redirect('index.html')

        items_list = []
        total_price = 0

        # Calculate the total price and prepare order details
        for product_id, item in cart.items():
            product_obj = product.objects.get(id=product_id)
            item_total = product_obj.price * item['quantity']
            total_price += item_total
            items_list.append(f"{product_obj.name} (x{item['quantity']}) - ${item_total}")

        # Create an order in the database
        order = Order.objects.create(
            customer_email=customer_email,
            items="\n".join(items_list),
            total_price=total_price,
        )

        # Send email to the customer
        customer_subject = "Order Confirmation"
        customer_message = f"Thank you for your purchase!\n\nOrder Details:\n{order.items}\nTotal: ${order.total_price}"
        send_mail(customer_subject, customer_message, "your-email@gmail.com", [customer_email])

        # Send email to the store owner
        owner_subject = f"New Order from {customer_email}"
        owner_message = f"A new order has been placed.\n\nOrder Details:\n{order.items}\nTotal: ${order.total_price}"
        send_mail(owner_subject, owner_message, "your-email@gmail.com", ["store-owner-email@gmail.com"])

        # Clear the cart after the purchase
        request.session['cart'] = {}

        return redirect('order_success')

    return render(request, 'index.html')



    return render(request,)
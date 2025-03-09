from .models import product, Invoice, InvoiceItem, AbandonedCart
from django.shortcuts import render, get_object_or_404,redirect
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from .utils import generate_invoice_pdf
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import timedelta



# Displaying the cart
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, item in cart.items():
        Product = get_object_or_404(product, id=product_id)
        cart_items.append({
            'id': Product.id,
            'name': Product.name,
            'quantity': item['quantity'],
            'price': Product.price * item['quantity'],
        })
        total_price += Product.price * item['quantity']
    
    return render(request, 'index.html', {'cart_items': cart_items, 'total_price': total_price})

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

    return redirect('/')

# update cart Functionality

def update_item(request, product_id):
    cart = request.session.get('cart', {})

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
    elif request.method == "GET":
        quantity = int(request.GET.get('quantity', 1))
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] = max(1, quantity) 
        request.session['cart'] = cart
        return redirect('/')  

    return JsonResponse({"error": "Product not in cart"}, status=400)
    
# Remove cart item functionality

def remove_item(request, product_id):

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect('/')

# Clearing cart

def clear(request):
    request.session['cart'] = {}
    return redirect('/')

# checkout and email

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('/')
    

    
    cart_items = []
    total_price = 0
    for product_id, item in cart.items():
        Product = get_object_or_404(product, id=product_id)
        cart_items.append(f"{Product.name} x {item['quantity']} - ${Product.price * item['quantity']}")
        total_price += Product.price * item['quantity']


      # Create Invoice
    if request.user.is_authenticated:
        user = request.user
        user_email = user.email
    else:
        user = None
        user_email = request.session.get('guest_email', 'customer@example.com')

    # Create Invoice
    invoice = Invoice.objects.create(
        user=user,
        customer_email=user_email,
        total_amount=total_price,
        created_at=timezone.now()
    )

    for product_id, item in cart.items():
        Product = get_object_or_404(product, id=product_id)
        InvoiceItem.objects.create(
            invoice=invoice,
            product_name=Product.name,
            quantity=item['quantity'],
            price=Product.price
        )

    # Generate PDF Invoice
    pdf_buffer = generate_invoice_pdf(invoice)
    pdf_buffer.seek(0)
    

    # Email to Customer
    customer_email = EmailMessage(
        subject="Your Invoice from Bagshop",
        body=f"Dear Customer,\n\nThank you for your purchase!\n\nPlease find your invoice attached.\n\nTotal: ${total_price}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
    )
    customer_email.attach(f"Invoice_{invoice.invoice_number}.pdf", pdf_buffer.read(), "application/pdf")
    customer_email.send()

    # Email to Admin
    admin_email = EmailMessage(
        subject="New Order Notification",
        body=f"A new order has been placed.\n\nCustomer Email: {user_email}\nTotal Amount: ${total_price}\n\nInvoice is attached.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL],
    )
    admin_email.attach(f"Invoice_{invoice.invoice_number}.pdf", pdf_buffer.read(), "application/pdf")
    admin_email.send()

    pdf_buffer.close()

    request.session['cart'] = {}  # Clear cart
    messages.success(request, "Order placed successfully! Check your email for the invoice.")
    return redirect('/')


def chekout_template(request):
    if request.method == 'POST':
        guest_email = request.POST.get('email')
        if guest_email:
            request.session['guest_email'] = guest_email
            return redirect('checkout')  # Now proceed to checkout
        else:
            messages.error(request, "Email is required to continue.")
            return redirect('chekout_template')
    return render(request, 'checkout.html')



def send_abandoned_cart_reminder():
    carts = AbandonedCart.objects.filter(is_recovered=False, last_updated__lt=now() - timedelta(hours=24))

    for cart in carts:
        if cart.items.exists():  # Only send emails if there are items in the cart
            item_list = "\n".join([f"{item.product.name} (x{item.quantity})" for item in cart.items.all()])
            
            send_mail(
                subject="You left items in your cart!",
                message=f"Hi {cart.user.email},\n\nYou left these items in your cart:\n{item_list}\n\nComplete your purchase now!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[cart.user.email],
            )

            

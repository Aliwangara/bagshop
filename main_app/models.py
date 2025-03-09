from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

# Create your models here.

class Category(models.Model):
 name = models.CharField(max_length=50)

 def __str__(self):
  return self.name
 class Meta:
  verbose_name_plural = 'categories'
  


class product(models.Model):
 name = models.CharField(max_length=30)
 price =models.DecimalField(default=0,decimal_places=3, max_digits=6)
 image = models.ImageField(upload_to='static/upload')
 category = models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
 description = models.CharField(default='', max_length=200, null=True, blank=True)


 def __str__ (self):
  return self.name


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer_email}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price
    


class AbandonedCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="abandoned_carts")
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    is_recovered = models.BooleanField(default=False)  # Mark if the cart was later recovered

    def __str__(self):
        return f"Abandoned Cart - {self.user.email} ({self.created_at})"


class AbandonedCartItem(models.Model):
    cart = models.ForeignKey(AbandonedCart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) in {self.cart.user.email}'s cart"

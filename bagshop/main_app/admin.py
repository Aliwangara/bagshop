from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(product)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)




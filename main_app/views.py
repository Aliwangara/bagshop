from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404


# Create your views here.
def home(request):
    Products = product.objects.all()
    categories =Category.objects.all()
    
    return render(request , 'index.html', {'Products': Products, 'categories':categories})

def category(request , cat):
    category_obj = get_object_or_404(Category, name=cat)
    Products =product.objects.filter(category=category_obj)
    Categories = Category.objects.all()

    print("Category selected:", category_obj)
    print("All categories:", Categories)
    print("Products in category:", Products)

    return render(request, 'category.html', {'Products': Products, 'categories':category_obj, 'Categories':Categories} )




def prod(request, pk):
   
   Product= get_object_or_404(product, id=pk)
   

   return render(request, "product.html", {'Product':Product} )




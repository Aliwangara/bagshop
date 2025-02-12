from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404


# Create your views here.
def home(request):
    Products = product.objects.all()
    categories =Category.objects.all()
    
    return render(request , 'index.html', {'Products': Products, 'categories':categories})

def category(request , cat):
    category_obj = get_object_or_404(Category, name = cat)
    prodcts = product.objects.filter(category = category_obj)
    
    return render(request, "category.html",{'category_obj':category_obj,'prodcts':prodcts })




def prod(request, pk):
   
   Product= get_object_or_404(product, id=pk)
   

   return render(request, "product.html", {'Product':Product} )




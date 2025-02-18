from django.urls import path
from . import views, view_cart

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:cat>/', views.category, name = "categories"),
    path('prod/<int:pk>/,', views.prod, name='product'),

    # Cart urls
    path('cart/', view_cart.cart, name='cart'),
    path('cart/add/<int:product_id>/', view_cart.add_to_cart, name='add_to_cart' ),
    # path('cart/remove/<int:product_id>/', view_cart.delete_item, name='remove_from_cart'),
    # path('cart/update/<int:product_id>/', view_cart.update_item, name='update_cart'),
    # path('cart/clear/', view_cart.clear, name='clear_cart'),
    # path('checkout/', view_cart.checkout, name='checkout'),


    # Login and signup

    # path('')





]
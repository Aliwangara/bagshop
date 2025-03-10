from django.urls import path
from . import views, view_cart
from allauth.account import views as allauth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:cat>/', views.category, name = "categories"),
    path('prod/<int:pk>/,', views.prod, name='product'),

    # Cart urls
    path('cart/', view_cart.cart, name='cart'),
    path('cart/add/<int:product_id>/', view_cart.add_to_cart, name='add_to_cart' ),
    path('cart/remove/<int:product_id>/', view_cart.remove_item, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', view_cart.update_item, name='update_cart'),
    path('cart/clear/', view_cart.clear, name='clear_cart'),
    path('checkout/', view_cart.checkout, name='checkout'),
    path('chekout_template/',view_cart.chekout_template, name='chekout_template' ),


    # Login and signup

    path('accounts/login/', allauth_views.LoginView.as_view(template_name='authentication/login.html'), name='account_login'),
    path('accounts/signup/', allauth_views.SignupView.as_view(template_name='authentication/signup.html'), name='account_signup'),
    path('accounts/logout/', allauth_views.LogoutView.as_view(), name='account_logout'),

    # path('')





]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:cat>/', views.category, name = "categories"),
    path('prod/<int:pk>/,', views.prod, name='product'),
]
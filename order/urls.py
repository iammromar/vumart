from django.urls import path
from order import views


urlpatterns = [
   path('search/', views.search, name="search"),
   path('addtocart/', views.add_to_cart, name="add_to_cart"),
   path('remove/', views.remove, name="remove"),
   path('cart/', views.cart, name="cart"),
   path('checkout/', views.checkout, name="checkout"),
   path('checkout/success/', views.success, name="success"),
]


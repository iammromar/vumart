from django.urls import path
from order import views


urlpatterns = [
   path('search/', views.search, name="search_results"),
   path('addtocart/', views.add_to_cart, name="add_to_cart"),
   path('remove/', views.remove, name="remove"),
   path('cart/', views.cart, name="cart"),
   path('checkout/', views.checkout, name="checkout"),
   path('checkout/success/', views.success, name="success"),
   path('update_cart_count/', views.update_cart_count, name='update_cart_count'),
   path('update_cart_count_after_remove/', views.update_cart_count_after_remove, name='update_cart_count_after_remove'),
   path('wishlist/', views.wishlist, name='wishlist'),
   path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),





]


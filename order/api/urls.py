from django.urls import path
from order.api import views as api_views

app_name = 'order'

urlpatterns = [
    path('add_to_cart/', api_views.AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart/', api_views.CartAPIView.as_view(), name='cart'),
]

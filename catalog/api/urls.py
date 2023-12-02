from django.urls import path
from product.api import views as api_views

app_name = 'product'

urlpatterns = [
    path('product/list/', api_views.ProductListAPIView.as_view(), name='product-list'),
    path('category/list/', api_views.CategoryListAPIView.as_view(), name='category-list'),
    path('category/<int:pk>/', api_views.CategoryRetrieveAPIView.as_view(), name='category-retrieve'),
    path('category/products/', api_views.ProductListAPIView.as_view(), name='category-products'),
]

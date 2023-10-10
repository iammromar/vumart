from django.urls import path
from product import views


urlpatterns = [
   path('<int:id>/', views.category, name="category"),
   path('<int:id>/sort/', views.category2, name="category2"),
   path('<int:id>/price/<int:min>/<int:max>/', views.price_filter, name="price_filter"),
   path('product/<int:id>/', views.product, name="product"),
   path('brand/<int:id>/', views.product, name="brand"),
]


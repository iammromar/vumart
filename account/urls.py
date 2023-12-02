from django.urls import path
from account import views



urlpatterns = [
   ############################################
   path('signup/', views.signup, name="signup"),
   path('signin/', views.signin, name="signin"),
   path('logout/', views.logout_request, name="logout"),


   path('profile/', views.profile, name="profile"),
   path('profile/order/<int:id>/', views.order, name="order"),
   ############################################

   

   ############################################
   path('login/', views.login, name='login'),
   path('createaccount/', views.createaccount, name='createaccount'),
   ############################################



   path('forget/', views.signin, name="forget"),

   path('password/', views.password, name="password"),

   path('orders/', views.orders, name="orders"),
   path('order/<int:id>/', views.order, name="order"),

   path('wishlist/', views.wishlist, name="wishlist"),

   path('infos/', views.infos, name="infos"),

   path('addresses/', views.addresses, name="addresses"),
   path('addresses/<int:id>/edit/', views.addresses_edit, name="address-edit"),
   path('addresses/add/', views.addresses_add, name="address-add"),

   path('foryou/', views.foryou, name="foryou"),
   path('neokart/', views.neocard, name="neocard"),
   path('addwishlist/', views.add_to_wishlist, name="add_to_wishlist"),
   path('changeitem/', views.change_item, name="changeitem"),
   path('selectaddress/', views.select_address, name="select_address"),


]


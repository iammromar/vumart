from django.urls import path
from account import views
from django.contrib.auth import views as auth_views


urlpatterns = [
   ############################################
   path('signup/', views.signup, name="signup"),
   path('signin/', views.signin, name="signin"),
   path('logout/', views.logout_request, name="logout"),


   path('profile/', views.profile, name="profile"),
   path('edit_profile/', views.edit_profile, name='edit_profile'),
   path('profile/order/<int:id>/', views.order, name="order"),
   path('profile-setting/', views.profile_setting, name='profile_setting'),
   path('manage_address/', views.manage_address, name="manage_address"),
   path('new_address/', views.new_address, name='new_address'),
     path('change-password/', views.change_password, name='change_password'),

   
   ############################################

   


   ############################################
   path('login/', views.login, name='login'),
   path('createaccount/', views.createaccount, name='createaccount'),
   ############################################

   ############################################
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   ############################################



   path('forget/', views.signin, name="forget"),

   path('password/', views.password, name="password"),

   path('orders/', views.orders, name="orders"), 
   path('order/', views.order, name="order"),
   path('order/<int:id>/', views.order, name="order"),




   path('infos/', views.infos, name="infos"),

   path('addresses/', views.addresses, name="addresses"),
   path('addresses/<int:id>/edit/', views.addresses_edit, name="address-edit"),
   path('addresses/add/', views.addresses_add, name="address-add"),

   path('foryou/', views.foryou, name="foryou"),
   path('neokart/', views.neocard, name="neocard"),
   path('changeitem/', views.change_item, name="changeitem"),
   path('selectaddress/', views.select_address, name="select_address"),


]


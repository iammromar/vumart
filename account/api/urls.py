from django.urls import path
from account.api import views as api_views

app_name = 'account'

urlpatterns = [
    path('login/', api_views.CustomAuthToken.as_view()), 
    path('logout/',api_views.LogoutView.as_view()),
    path('signup/',api_views.SignUpAPIView.as_view()),
]

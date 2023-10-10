from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from core import views as core_views
from contact import views as contact_views
from account import views as account_views
from blog import views as blog_views
from catalog import views as catalog_views
from order import views as order_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name="index"),

    path('contact/', core_views.index, name="contact"),
    path('search/', core_views.index, name="search"),

    path('signup/', core_views.index, name="signup"),
    path('user/dashboard/', core_views.index, name="user-dashboard"),
    path('user/wishlist/', core_views.index, name="wishlist"),
    path('user/history/', core_views.index, name="user-history"),
    path('user/logout/', core_views.index, name="logout"),

    path('category/<int:id>/', catalog_views.category, name="category"),
    path('product/<int:id>/', catalog_views.product, name="product"),
    path('blog/<int:id>/', core_views.index, name="blog"),
    path('profile/address-add/', core_views.index, name="address-add"),
    path('profile/address-edit/<int:id>/', core_views.index, name="address-edit"),

    path('order/', include('order.urls')),
    path('account/', include('account.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

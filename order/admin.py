from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'payment', 'address', 'ordered_date_time')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)

admin.site.register(Wishlist)
from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','email','first_name','is_active','date_joined')

admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(City)
admin.site.register(Address)
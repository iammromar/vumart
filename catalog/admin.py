from django.contrib import admin
from .models import *

admin.site.register(Brand)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    readonly_fields = ('date',)
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProductImageInline, ProductPriceInline]


admin.site.register(Product, ProductAdmin)


class NewProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'updated_at', 'created_at')


admin.site.register(NewProduct, NewProductAdmin)


class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'updated_at', 'created_at')


admin.site.register(FeaturedProduct, FeaturedProductAdmin)



class BestSellerProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'updated_at', 'created_at')


admin.site.register(BestSellerProduct, BestSellerProductAdmin)

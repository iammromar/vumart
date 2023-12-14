from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.db import transaction
import csv
import json
from django.http import HttpResponse
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django import forms




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

class DecimalEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)
    
class ProductImportForm(forms.Form):
    file = forms.FileField()
    
class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_categories', 'get_brand', 'get_main_image', 'get_price', 'get_upload_date')
    inlines = [ProductImageInline, ProductPriceInline]
    actions = ['export_to_csv', 'export_to_json']
    actions = ['move_to_category']
    

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    display_categories.short_description = 'Categories'

    

    def get_brand(self, obj):
        return obj.brand.name if obj.brand else None
    get_brand.short_description = 'Brand'

    def get_main_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.main_image.url)
    get_main_image.short_description = 'Main Image'

    def get_price(self, obj):
        latest_price = obj.prices.order_by('-date').first()
        return latest_price.price if latest_price else None
    get_price.short_description = 'Price'

    def get_upload_date(self, obj):
        return obj.prices.order_by('-date').first().date if obj.prices.exists() else None
    get_upload_date.short_description = 'Upload Date'


    def move_to_category(self, request, queryset):
        selected_category_id = request.POST.get('category_to_move_to')
        if selected_category_id:
            try:
                with transaction.atomic():
                    target_category = Category.objects.get(pk=selected_category_id)
                    for product in queryset:
                        product.category.clear()
                        product.category.add(target_category)
                        product.save()
                    self.message_user(request, f'Successfully moved selected products to {target_category.name} category.')
            except Category.DoesNotExist:
                self.message_user(request, 'Target category does not exist.', level='error')
        else:
            self.message_user(request, 'Please select a category to move the products to.', level='error')

    move_to_category.short_description = 'Move selected products to category'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['categories'] = Category.objects.all()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Categories', 'Price', 'Brand', 'Image'])

        for product in queryset:
            categories = ', '.join([category.name for category in product.category.all()])
            writer.writerow([product.id, product.name, categories, product.prices.first().price if product.prices.exists() else None, product.brand.name if product.brand else None, product.main_image.url if product.main_image else None])

        return response

    export_to_csv.short_description = 'Export selected products to CSV'

    def export_to_json(self, request, queryset):
        data = []
        for product in queryset:
            categories = [category.name for category in product.category.all()]
            product_data = {
                'id': product.id,
                'name': product.name,
                'categories': categories,
                'price': float(product.prices.first().price) if product.prices.exists() else None,
                'brand': product.brand.name if product.brand else None,
                'img': product.main_image.url if product.main_image else None,
            }
            data.append(product_data)

        response = HttpResponse(
            json.dumps(data, indent=2, cls=DecimalEncoder),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="products.json"'
        return response

    export_to_json.short_description = 'Export selected products to JSON'
    
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

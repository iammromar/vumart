from django.shortcuts import render

from catalog.models import Category, Product, NewProduct
from core.models import General, Social
from order.models import Order


def category(request, id):
    if request.user_agent.is_mobile == True:
        context = {

        }
        return render(request, "mobile/page/index.html", context)
    else:
        cart = None
        if request.user.is_authenticated:
            cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
        cart_sum = 0
        if request.user.is_authenticated:
            order = Order.objects.filter(is_ordered=False, customer=request.user).last()
            if order:
                for o in order.items.all():
                    cart_sum = cart_sum + o.quantity * o.product.prices.last().price
        cats = Category.objects.filter(is_active=True)
        category = Category.objects.get(pk=id)
        general = General.objects.last()
        socials = Social.objects.all()
        context = {
            "socials": socials,
            "general": general,
            "cats": cats,
            "category": category,
            'cart': cart,
            'cart_sum': cart_sum,
        }
        return render(request, "desktop/catalog/category.html", context)

def product(request, id):
    if request.user_agent.is_mobile == True:
        context = {

        }
        return render(request, "mobile/page/index.html", context)
    else:
        cats = Category.objects.filter(is_active=True)
        product = Product.objects.get(pk=id)
        related_products = Product.objects.all()
        best_products = NewProduct.objects.all()
        context = {
            "cats": cats,
            "product": product,
            "best_products": best_products,
            "related_products": related_products,
        }
        return render(request, "desktop/catalog/product.html", context)
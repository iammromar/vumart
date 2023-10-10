from django.shortcuts import render

from catalog.models import Category, Product, NewProduct


def category(request, id):
    if request.user_agent.is_mobile == True:
        context = {

        }
        return render(request, "mobile/page/index.html", context)
    else:
        cats = Category.objects.filter(is_active=True)
        category = Category.objects.get(pk=id)
        context = {
            "cats": cats,
            "category": category,
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
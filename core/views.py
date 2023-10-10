from django.shortcuts import render

from account.models import Address
from blog.models import Post
from catalog.models import Category, Product, FeaturedProduct, NewProduct, BestSellerProduct
from core.models import General, Subscription, Social
from order.models import Order


def index(request):

    if request.user_agent.is_mobile == True:
        if request.method == 'POST' and request.POST.get("type") == 'unvan':
            for a in request.user.addresses.all():
                a.is_selected = False
                a.save()
            adr = Address.objects.get(pk=int(request.POST.get("id")))
            adr.is_selected=True
            adr.save()

        cats = Category.objects.filter(is_active=True)
        featured_cats = Category.objects.filter(is_active=True)
        featured_products = FeaturedProduct.objects.all()
        new_products = NewProduct.objects.all()
        posts = Post.objects.all()
        general = General.objects.last()
        context = {
            "general": general,
            "cats": cats,
            "featured_cats": featured_cats,
            "featured_products": featured_products,
            "new_products": new_products,
            "posts": posts,
        }
        return render(request, "mobile/page/index.html", context)
    else:
        if request.method == 'POST' and request.POST.get("type") == 'unvan':
            for a in request.user.addresses.all():
                a.is_selected = False
                a.save()
            adr = Address.objects.get(pk=int(request.POST.get("id")))
            adr.is_selected=True
            adr.save()
        cats = Category.objects.filter(is_active=True)
        featured_products = FeaturedProduct.objects.all()
        new_products = NewProduct.objects.all()
        best_products = BestSellerProduct.objects.all()





        cart = None
        if request.user.is_authenticated:
            cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
        cart_sum = 0
        if request.user.is_authenticated:
            order = Order.objects.filter(is_ordered=False, customer=request.user).last()
            if order:
                for o in order.items.all():
                    cart_sum = cart_sum + o.quantity * o.product.prices.last().price

        general = General.objects.last()
        socials = Social.objects.all()
        context = {
            "socials": socials,
            "general": general,
            "kampaniya_quantity": 5,
            "new_quantity": 6,
            "cats": cats,
            "featured_products": featured_products,
            "new_products": new_products,
            "best_products": best_products,
            'cart': cart,
            'cart_sum': cart_sum,
        }
        return render(request, "desktop/page/index.html", context)



def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        s = Subscription.objects.filter(email=email)
        if s:
            pass
        else:
            Subscription.objects.create(email=email)

        cats = Category.objects.filter(is_active=True)
        featured_products = FeaturedProduct.objects.all()
        new_products = NewProduct.objects.all()
        best_products = BestSellerProduct.objects.all()

        cart = None
        if request.user.is_authenticated:
            cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
        cart_sum = 0
        if request.user.is_authenticated:
            order = Order.objects.filter(is_ordered=False, customer=request.user).last()
            if order:
                for o in order.items.all():
                    cart_sum = cart_sum + o.quantity * o.product.prices.last().price

        general = General.objects.last()
        socials = Social.objects.all()
        context = {
            "socials": socials,
            "general": general,
            "kampaniya_quantity": 5,
            "new_quantity": 6,
            "cats": cats,
            "featured_products": featured_products,
            "new_products": new_products,
            "best_products": best_products,
            'cart': cart,
            'cart_sum': cart_sum,
        }
        return render(request, "desktop/page/subscribe.html", context)


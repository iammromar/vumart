from django.shortcuts import render

from account.models import Address
from blog.models import Post
from catalog.models import Category, Product, FeaturedProduct, NewProduct, BestSellerProduct
from core.models import General, Subscription, Social
from order.models import Order
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages


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



def determine_template(request):
    return 'mobile/account/login.html' if request.user_agent.is_mobile else 'desktop/account/signin.html'

def signin(request):
    main_categories = Category.objects.filter(parent=None)

    if request.user.is_authenticated:
        return redirect("profile")

    template_name = determine_template(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            username = username.replace('+994', '')
            username = username.replace('-', '')
            username = username.replace('(', '')
            username = username.replace(')', '')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                if not user.is_active:
                    messages.warning(request, "Your account is pending admin approval. Please wait.")
                    return redirect("waiting")

                messages.info(request, f"You are now logged in as {username}.")
                return redirect("profile")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
            form = AuthenticationForm()
            context = {
                "login_form": form,
                "failed": True,
                'main_categories': main_categories,
            }
            return render(request, template_name, context)

    form = AuthenticationForm()
    context = {
        "login_form": form,
        'main_categories': main_categories,
    }
    return render(request, template_name, context)



def my_custom_login_view(request):
    # your custom logic
    return LoginView.as_view()(request)

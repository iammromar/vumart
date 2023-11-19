from django.http import JsonResponse
from django.shortcuts import render, redirect

from core.models import General, Social
from order.models import Order, OrderItem
from catalog.models import Product, Category
from .forms import NewUserForm, SetPasswordForm, AddressForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth.decorators import login_required
import json
from .models import Wishlist, Address, City


def signin(request):
    main_categories = Category.objects.filter(parent=None)
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            username = username.replace('+994','')
            username = username.replace('-','')
            username = username.replace('(','')
            username = username.replace(')','')
            password = form.cleaned_data.get('password')
            print(username)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
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
            return render(request, 'desktop/account/signin.html', context)
    form = AuthenticationForm()
    context = {
        "login_form": form,
        'main_categories': main_categories,
    }
    return render(request, 'desktop/account/signin.html', context)


def signup(request):
    main_categories = Category.objects.filter(parent=None)
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("profile")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context = {
        "register_form": form,
        'main_categories': main_categories,
    }
    return render(request, 'desktop/account/signup.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


@login_required(login_url='/account/signin/')
def profile(request):
    general = General.objects.last()
    socials = Social.objects.all()
    cats = Category.objects.filter(is_active=True)
    total_orders = Order.objects.filter(customer=request.user, is_ordered=True).count()
    pending_orders = Order.objects.filter(status='PE', customer=request.user, is_ordered=True).count()
    wishlist_count = Wishlist.objects.filter(customer=request.user).count()
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    main_address = Address.objects.filter(customer=request.user, is_selected=True).last()
    orders = Order.objects.filter(customer=request.user, is_ordered=True)

    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)
        if not main_address and addresses:
            main_address = addresses.last()
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('type') == "addaddress":
        print('yeah1')
        city = ""
        name =""
        street = ""
        building = ""
        zip = ""
        note = ""
        try:
            city = request.POST.get('city')
        except:
            city = ""
        try:
            name = request.POST.get('name')
        except:
            name = ""
        try:
            street = request.POST.get('street')
        except:
            street = ""
        try:
            building = request.POST.get('building')
        except:
            building = ""
        try:
            zip = request.POST.get('zip')
        except:
            zip = ""
        try:
            note = request.POST.get('note')
        except:
            note = ""
        Address.objects.create(
            city=city,
        name = name,
        street = street,
        building = building,
        zip = zip,
        note = note,
            customer=request.user
        )


    context = {
        "socials": socials,
        "general": general,
        "cats": cats,
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'main_address': main_address,
        'orders': orders,
        'total_orders':total_orders,
        'pending_orders' : pending_orders,
        'wishlist_count' : wishlist_count

    }
    return render(request, 'desktop/account/dashboard.html', context)


@login_required(login_url='/account/signin/')
def orders(request):
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    orders = Order.objects.filter(customer=request.user, is_ordered=True)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)

        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price






    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'orders': orders,

    }
    return render(request, 'desktop/account/orders.html', context)


@login_required(login_url='/account/signin/')
def order(request, id):
    general = General.objects.last()
    socials = Social.objects.all()

    order_detail = Order.objects.get(pk=id)
    if request.user.id != order_detail.customer.id:
        order_detail = None
    cats = Category.objects.filter(is_active=True)
    ord = Order.objects.filter(pk=id,customer=request.user).last()
    orders = Order.objects.filter(customer=request.user, is_ordered=True)[:3]
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)

        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price




    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'order': ord,
        'general': general,
        'socials': socials,
        "cats": cats,
        "order_detail": order_detail,

    }
    return render(request, 'desktop/account/order.html', context)


@login_required(login_url='/account/signin/')
def wishlist(request):
    wishlist = None

    addresses = None
    main_categories = Category.objects.filter(parent=None)

    cart = None
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(customer=request.user)
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)

        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        print("seaaaaaaaaaarch")
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
            'addresses': addresses,


        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('remove') == "1":
        w_id = request.POST.get('item')
        wish = Wishlist.objects.get(pk=w_id)
        wish.delete()

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'addresses': addresses,
            'wishlist': wishlist,
        }

    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'wishlist': wishlist,

    }
    return render(request, 'account/wishlist.html', context)


@login_required(login_url='/account/signin/')
def infos(request):
    addresses = None
    main_categories = Category.objects.filter(parent=None)



    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)

        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        print("seaaaaaaaaaarch")
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
            'addresses': addresses,

        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('edit') == "1":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()


    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,

    }
    return render(request, 'account/infos.html', context)


@login_required(login_url='/account/signin/')
def foryou(request):
    main_categories = Category.objects.filter(parent=None)
    context = {
        "main_categories": main_categories,
    }
    return render(request, 'account/foryou.html', context)


@login_required(login_url='/account/signin/')
def neocard(request):
    main_categories = Category.objects.filter(parent=None)
    context = {
        "main_categories": main_categories,
    }
    return render(request, 'account/neocard.html', context)


@login_required(login_url='/account/signin/')
def addresses(request):
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        print("seaaaaaaaaaarch")
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
            'addresses': addresses,
        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('remove') == "1":
        address_id = request.POST.get('address_id')
        addr = Address.objects.get(pk=address_id)
        addr.delete()

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'addresses': addresses,
        }

        return render(request, 'account/addresses.html', context)
    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
    }
    return render(request, 'account/addresses.html', context)


@login_required(login_url='/account/signin/')
def addresses_edit(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).last()
    addresses = None
    cities = City.objects.all()
    main_categories = Category.objects.filter(parent=None)
    cart = None
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'address': address,
            'addresses': addresses,
            'cities': cities,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('edit') == "1":
        name = request.POST.get('name')
        cty = request.POST.get('city')
        street = request.POST.get('street')
        building = request.POST.get('building')
        apartment = request.POST.get('apartment')
        blok = request.POST.get('blok')
        blok_code = request.POST.get('blok_code')
        phone = request.POST.get('phone')
        default = request.POST.get('default')
        city = City.objects.get(pk=int(cty))

        address.name = name
        address.street = street
        address.city = city
        address.building = building
        address.apartment = apartment
        address.blok = blok
        address.blok_code = blok_code
        address.phone = phone
        address.save()
        if default == "on":
            addresses_all = Address.objects.filter(customer=request.user)
            for a in addresses_all:
                a.is_selected = False
                a.save()
            address.is_selected = True
            address.save()

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'addresses': addresses,
        }

        return render(request, 'account/addresses.html', context)
    context = {
        "main_categories": main_categories,
        'addresses': addresses,
        'cart': cart,
        'cart_sum': cart_sum,
        'address': address,
        'cities': cities,
    }
    return render(request, 'account/addresses_edit.html', context)


@login_required(login_url='/account/signin/')
def addresses_add(request):
    addresses = None
    cities = City.objects.all()
    main_categories = Category.objects.filter(parent=None)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        print("seaaaaaaaaaarch")
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'cities': cities,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
            'addresses': addresses,
        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('add') == "1":
        name = request.POST.get('name')
        cty = request.POST.get('city')
        street = request.POST.get('street')
        building = request.POST.get('building')
        apartment = request.POST.get('apartment')
        blok = request.POST.get('blok')
        blok_code = request.POST.get('blok_code')
        phone = request.POST.get('phone')
        default = request.POST.get('default')
        city = City.objects.get(pk=int(cty))

        print("---------d-d-d-d-d---------")
        print(default)
        address_new = Address.objects.create(
            customer=request.user,
            name=name,
            city=city,
            street=street,
            building=building,
            apartment=apartment,
            blok=blok,
            blok_code=blok_code,
            phone=phone
        )
        if default == "on":
            addresses_all = Address.objects.filter(customer=request.user)
            for a in addresses_all:
                a.is_selected = False
                a.save()
            address_new.is_selected = True
            address_new.save()

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'addresses': addresses,
        }

        return render(request, 'account/addresses.html', context)
    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'cities': cities,
    }
    return render(request, 'account/addresses_add.html', context)


@login_required(login_url='/account/signin/')
def password(request):
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    cart_sum = 0
    if request.user.is_authenticated:
        addresses = Address.objects.filter(customer=request.user)
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum = cart_sum + o.quantity * o.product.prices.last().price

    if request.method == "POST" and request.POST.get('isitsearch') == "1":
        print("seaaaaaaaaaarch")
        search = request.POST.get('search')
        search_products = Product.objects.filter(name__icontains=search)

        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'search_products': search_products,
            'addresses': addresses,
        }

        return render(request, 'desktop/page/search.html', context)


    if request.method == "POST" and request.POST.get('edit') == "1":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=request.user.username, password=request.POST.get('new_password1'))
            if user is not None:
                login(request, user)
                return redirect("profile")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)


    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
    }
    return render(request, 'account/password.html', context)


@login_required(login_url='/account/signin/')
def add_to_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            resp = {}
            wishlist = Wishlist.objects.filter(product=product, customer=request.user).last()
            if wishlist:
                wishlist.delete()
                resp["liked"] = 0
            else:
                Wishlist.objects.create(product=product, customer=request.user)
                resp["liked"] = 1

        return JsonResponse(resp, status=201)

@login_required(login_url='/account/signin/')
def change_item(request):
    if request.method == 'POST':

        if request.user.is_authenticated:
            item_id = int(request.POST.get('item_id'))
            qty = int(request.POST.get('qty'))
            item = OrderItem.objects.get(pk=item_id)
            item.quantity = qty
            item.save()
            resp = {"total":item.total_price,"grand": item.order.get_cart_total,"id":item.id}


        return JsonResponse(resp, status=201)
@login_required(login_url='/account/signin/')
def select_address(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            address_id = request.POST.get('id')
            address = Address.objects.get(id=address_id)
            addresses = Address.objects.filter(customer=request.user)
            for a in addresses:
                a.is_selected = False
                a.save()
            address.is_selected = True
            address.save()
            resp = {}

        return JsonResponse(resp, status=201)

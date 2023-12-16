from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from catalog.models import Category
from core.models import General, Social
from .models import *
from order.models import *
from django.utils.text import slugify
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib import messages


def search(request):
    general = General.objects.last()
    main_categories = Category.objects.filter(parent=None)

    if request.user_agent.is_mobile:
        template = 'mobile/page/search.html'
    else:
        template = 'desktop/page/search.html'

    query = request.GET.get('query')

    if query:
        # Use Q objects to perform a case-insensitive search on the Product model
        products = Product.objects.filter(name__icontains=query)
        context = {
            "general": general,
            'products': products,
            'query': query,
        }
    else:
        print("mehul gelmedi")
        context = {'general': general}

    return render(request, template, context)
        

def cart(request):
    general = General.objects.last()
    socials = Social.objects.all()
    cats = Category.objects.filter(is_active=True)
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    main_address = Address.objects.filter(customer=request.user, is_selected=True).last()
    orders = Order.objects.filter(customer=request.user, is_ordered=True)[:3]
    order_in_cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
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



    if request.method == "POST" and request.POST.get('remove') == "1":
        item_id = int(request.POST.get('product'))
        item = OrderItem.objects.get(pk=item_id)
        item.delete()
    if request.method == "POST" and request.POST.get('update') == "1":
        item_id = int(request.POST.get('product'))
        qty = int(request.POST.get('qty'))
        item = OrderItem.objects.get(pk=item_id)
        item.quantity = int(qty)
        item.save()
    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'orders': orders,
        "socials": socials,
        "general": general,
        "cats": cats,
        "order_in_cart": order_in_cart,

    }
    if request.user_agent.is_mobile:
        return render(request, "mobile/order/cart.html", context)
    else:
        return render(request, "desktop/order/cart.html", context)

def checkout(request):
    # Retrieve necessary data for the context
    general = General.objects.last()
    socials = Social.objects.all()
    cats = Category.objects.filter(is_active=True)
    order_in_cart = Order.objects.filter(customer=request.user, is_ordered=False).last()

    cart = None
    addresses = None

    # Check if the user is authenticated
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
        addresses = Address.objects.filter(customer=request.user)

    main_address = addresses.last() if addresses else None
    main_categories = Category.objects.filter(parent=None)

    cart_sum = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(is_ordered=False, customer=request.user).last()
        if order:
            for o in order.items.all():
                cart_sum += o.quantity * o.product.prices.last().price

    # Check if the form is submitted
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address_id = form.cleaned_data['address']
            add = Address.objects.get(pk=address_id)
            payment_cod = form.cleaned_data['checkout_payment_method']
            payment = None

            # Determine the payment method
            if payment_cod == "1":
                payment = Payment.objects.get(pk=1)
            elif payment_cod == "2":
                payment = Payment.objects.get(pk=2)

            # Update the order details
            order = Order.objects.filter(customer=request.user, is_ordered=False).last()
            if order:
                order.ordered_date_time = now()
                order.is_ordered = True
                order.payment = payment
                order.address = add
                order.save()
                print(f"Order ID after save: {order.id}")

                # Additional logic for handling the order success
                # (You may want to create order items, deduct stock, etc.)

                context = {
                    'main_categories': main_categories,
                    'cart': cart,
                    'cart_sum': cart_sum,
                    'addresses': addresses,
                    'main_address': main_address,
                    'order_in_cart': order_in_cart, 
                    'order': order,
                    "socials": socials,
                    "general": general,
                    "cats": cats,
                }

                return render(request, 'desktop/order/success.html', context)

    else:
        form = CheckoutForm()

    # Prepare the context for rendering the checkout page
    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'orders': order_in_cart,
        "socials": socials,
        "general": general,
        "cats": cats,
        "order_in_cart": order_in_cart,
        'form': form,
    }

    # Render the checkout page
    return render(request, "desktop/order/checkout.html", context)

def success(request):
    general = General.objects.last()
    socials = Social.objects.all()
    cats = Category.objects.filter(is_active=True)
    order_in_cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
    addresses = None
    main_categories = Category.objects.filter(parent=None)
    main_address = Address.objects.filter(customer=request.user, is_selected=True).last()
    orders = Order.objects.filter(customer=request.user, is_ordered=True)[:3]

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

    if order_in_cart:
        order_number = f'#0000{order_in_cart.id}'
    else:
        order_number = None

    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'orders': orders,
        "socials": socials,
        "general": general,
        "cats": cats,
        "order_in_cart": order_in_cart,
        "order_number": order_number,

    }

    return render(request, "desktop/order/success.html", context)

def remove(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            item_id = request.POST.get('item_id')
            exist_order_item = OrderItem.objects.get(pk=item_id)
            exist_order_item.delete()



        cart = {}
        prods = []
        ord = Order.objects.filter(is_ordered=False, customer=request.user).last()
        ord_items = OrderItem.objects.filter(order=ord).order_by('id')
        for i in ord_items:
            prd = {}
            prd['name'] = i.product.name
            prd['item_id'] = i.id
            prd['cat'] = i.product.category.all().last().name
            prd['id'] = i.product.id
            prd['image'] = i.product.main_image.url
            prd['qty'] = i.quantity

            prd['price'] = i.product.prices.last().price * i.quantity
            prods.append(prd)
        cart['products'] = prods
        cart['qty'] = 0

        cart_sum = 0
        if request.user.is_authenticated:
            order = Order.objects.filter(is_ordered=False, customer=request.user).last()
            if order:
                cart['qty'] = order.items.all().count()
                for o in order.items.all():
                    cart_sum = cart_sum + o.quantity * o.product.prices.last().price
        cart['summary'] = cart_sum

        print(cart)
        print(order.items.all().count())
        return JsonResponse(cart, status=201)

def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id')
            product_quantity = int(request.POST.get('product_quantity'))
            product = Product.objects.get(id=product_id)

            exist_order = Order.objects.filter(customer=request.user, is_ordered=False).last()
            if exist_order:
                exist_order_item = OrderItem.objects.filter(order=exist_order, product=product).last()
                if exist_order_item:
                    exist_order_item.quantity = exist_order_item.quantity + product_quantity
                    exist_order_item.save()
                else:
                    order_item = OrderItem.objects.create(
                        product=product,
                        order=exist_order,
                        quantity=product_quantity
                    )
            else:
                order = Order.objects.create(customer=request.user)
                order_item = OrderItem.objects.create(
                    product=product,
                    order=order,
                    quantity=product_quantity
                )

        cart = {}
        prods = []
        ord = Order.objects.filter(is_ordered=False, customer=request.user).last()
        ord_items = OrderItem.objects.filter(order=ord).order_by('id')
        for i in ord_items:
            prd = {}
            prd['name'] = i.product.name
            prd['item_id'] = i.id
            prd['cat'] = i.product.category.all().last().name
            prd['id'] = i.product.id
            prd['image'] = i.product.main_image.url
            prd['qty'] = i.quantity
            prd['price'] = i.product.prices.last().price * i.quantity
            prods.append(prd)
        cart['products'] = prods
        cart['qty'] = 0

        cart_sum = 0
        if request.user.is_authenticated:
            order = Order.objects.filter(is_ordered=False, customer=request.user).last()
            if order:
                cart['qty'] = order.items.all().count()
                for o in order.items.all():
                    cart_sum = cart_sum + o.quantity * o.product.prices.last().price
        cart['summary'] = cart_sum

    if request.user_agent.is_mobile:
        return JsonResponse(cart, status=201)
    else:
        return JsonResponse(cart, status=201)

def update_cart_count(request):
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
        cart_count = 1
        if cart:
            cart_count = cart.items.count()

        return JsonResponse({'cart_count': cart_count})
    else:
        return JsonResponse({'cart_count': 1})
    
    
from django.views.decorators.http import require_POST

@require_POST
def update_cart_count_after_remove(request):
    if request.user.is_authenticated:
        
        item_id = request.POST.get('item_id', None)
        
        cart_count = calculate_cart_count(request.user)

        return JsonResponse({'cart_count': cart_count})
    else:
        return JsonResponse({'cart_count': 0})
    



@login_required(login_url='/account/signin/')
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_item.delete()
        added = False
    else:
        added = True

    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return JsonResponse({'added': added, 'wishlist_count': wishlist_count})

@login_required(login_url='/account/signin/')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    general = General.objects.last()
    context = {
        'wishlist_items': wishlist_items,
        'general': general,
    }
    return render(request, 'desktop/order/wishlist.html', context)
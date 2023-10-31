from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from catalog.models import Category
from .models import *
from order.models import *
from django.utils.text import slugify

def search(request):
    context = {}
    return render(request, 'desktop/page/search.html', context)
def cart(request):
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
            'main_address': main_address,
        }

        return render(request, 'desktop/page/search.html', context)

    if request.method == "POST" and request.POST.get('remove') == "1":
        item_id = int(request.POST.get('item'))
        item = OrderItem.objects.get(pk=item_id)
        item.delete()
    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'orders': orders,

    }
    return render(request, "desktop/order/cart.html", context)


def checkout(request):
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
            'main_address': main_address,
        }

        return render(request, 'desktop/page/search.html', context)

    if request.method == "POST" and request.POST.get('order') == "1":

        address_id = request.POST.get('address')
        add = Address.objects.get(pk=int(address_id))
        payment_cod = request.POST.get('checkout_payment_method')
        payment = None
        if payment_cod == "1":
            payment = Payment.objects.get(pk=1)
        elif payment_cod == "2":
            payment = Payment.objects.get(pk=2)
        print("seaaaaaaaaaarch")
        print(address_id)
        print(payment_cod)
        order = Order.objects.filter(customer=request.user, is_ordered=False).last()
        order.ordered_date_time = now()
        order.is_ordered = True
        order.payment = payment
        order.address = add
        order.save()
        cart = Order.objects.filter(customer=request.user, is_ordered=False).last()
        cart_sum = 0
        context = {
            'main_categories': main_categories,
            'cart': cart,
            'cart_sum': cart_sum,
            'addresses': addresses,
            'main_address': main_address,
            'order': order,
        }

        return render(request, 'desktop/order/success.html', context)
    context = {
        "main_categories": main_categories,
        'cart': cart,
        'cart_sum': cart_sum,
        'addresses': addresses,
        'orders': orders,

    }
    return render(request, "desktop/order/checkout.html", context)

def success(request):
    context = {

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

        print(order.items.all().count())

        return JsonResponse(cart, status=201)










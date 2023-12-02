from django.contrib.auth import get_user_model
from rest_framework import permissions, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from order.models import Order, OrderItem
from product.models import Product

User = get_user_model()


from rest_framework.response import Response
from rest_framework.views import APIView


class AddToCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def post(self, request):
        qty = int(request.data.get('qty'))
        product_id = int(request.data.get('product'))
        product = Product.objects.get(pk=product_id)

        exist_order = Order.objects.filter(customer=request.user, is_ordered=False).last()
        if exist_order:
            exist_order_item = OrderItem.objects.filter(order=exist_order, product=product).last()
            if exist_order_item:
                exist_order_item.quantity = exist_order_item.quantity + qty
                exist_order_item.save()
            else:
                order_item = OrderItem.objects.create(
                    product=product,
                    order=exist_order,
                    quantity=qty
                )
        else:
            order = Order.objects.create(customer=request.user)
            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=qty
            )

        cart = {}
        prods = []
        ord = Order.objects.filter(is_ordered=False, customer=request.user).last()
        ord_items = OrderItem.objects.filter(order=ord)
        for i in ord_items:
            prd = {}
            prd['name'] = i.product.name
            prd['item_id'] = i.id
            prd['cat'] = i.product.category.all().last().name
            prd['id'] = i.product.id
            prd['image'] = i.product.images.first().image.url
            prd['qty'] = i.quantity
            prd['price'] = i.product.price * i.quantity
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


        return Response(cart)


    def patch(self, request):
        qty = int(request.data.get('qty'))
        product_id = int(request.data.get('product'))
        product = Product.objects.get(pk=product_id)

        exist_order = Order.objects.filter(customer=request.user, is_ordered=False).last()
        if qty < 0:
            pass
        else:
            if exist_order:
                exist_order_item = OrderItem.objects.filter(order=exist_order, product=product).last()
                if exist_order_item:
                    if qty == 0 or qty < 0:
                        exist_order_item.delete()
                    else:
                        exist_order_item.quantity = qty
                        exist_order_item.save()
                else:
                    order_item = OrderItem.objects.create(
                        product=product,
                        order=exist_order,
                        quantity=qty
                    )
            else:
                order = Order.objects.create(customer=request.user)
                order_item = OrderItem.objects.create(
                    product=product,
                    order=order,
                    quantity=qty
                )



        cart = {}
        prods = []
        ord = Order.objects.filter(is_ordered=False, customer=request.user).last()
        ord_items = OrderItem.objects.filter(order=ord)
        for i in ord_items:
            prd = {}
            prd['name'] = i.product.name
            prd['item_id'] = i.id
            prd['cat'] = i.product.category.all().last().name
            prd['id'] = i.product.id
            prd['image'] = i.product.images.first().image.url
            prd['qty'] = i.quantity
            prd['price'] = i.product.price * i.quantity
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


        return Response(cart)


    def delete(self, request):
        qty = int(request.data.get('qty'))
        product_id = int(request.data.get('product'))
        product = Product.objects.get(pk=product_id)

        exist_order = Order.objects.filter(customer=request.user, is_ordered=False).last()
        if exist_order:
            exist_order_item = OrderItem.objects.filter(order=exist_order, product=product).last()
            if exist_order_item:
                exist_order_item.quantity = qty
                exist_order_item.delete()



        cart = {}
        prods = []
        ord = Order.objects.filter(is_ordered=False, customer=request.user).last()
        ord_items = OrderItem.objects.filter(order=ord)
        for i in ord_items:
            prd = {}
            prd['name'] = i.product.name
            prd['item_id'] = i.id
            prd['cat'] = i.product.category.all().last().name
            prd['id'] = i.product.id
            prd['image'] = i.product.images.first().image.url
            prd['qty'] = i.quantity
            prd['price'] = i.product.price * i.quantity
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


        return Response(cart)




class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def get(self, request):

        exist_order = Order.objects.filter(customer=request.user, is_ordered=False).last()
        if exist_order:
            cart = {}
            prods = []
            ord = Order.objects.filter(is_ordered=False, customer=request.user).last()
            ord_items = OrderItem.objects.filter(order=ord)
            for i in ord_items:
                prd = {}
                prd['name'] = i.product.name
                prd['item_id'] = i.id
                prd['cat'] = i.product.category.all().last().name
                prd['id'] = i.product.id
                prd['image'] = i.product.images.first().image.url
                prd['qty'] = i.quantity
                prd['price'] = i.product.price * i.quantity
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

        else:
            cart = {}
            cart['products'] = 0
            cart['qty'] = 0

            cart['summary'] = 0

        return Response(cart)



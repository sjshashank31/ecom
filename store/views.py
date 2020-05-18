from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookie_cart, cart_data, guest_checkout


def store(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cart_items': cart_items}
    return render(request, 'store.html', context)


def cart(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']

    context = {'items': items, 'order': order,  'cart_items': cart_items}
    return render(request, 'cart.html', context)


def checkout(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('ProductId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("item was added", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guest_checkout(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zip_code=data['shipping']['zipcode'],
        )

    return JsonResponse('Order Processed and Payment Complete', safe=False)






from django.http.response import JsonResponse #when working with ajax 
from django.shortcuts import render

from basket.basket import Basket

from .models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key') #getting dat from ajax its form intent
        cust_name = request.POST.get('cust_name')
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # Check if order exists(if user press pay and nothing happens and then they press again that might create 2 orders)
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name=cust_name, address1='add1', #static values, replace them with form values
                                address2='add2', total_paid=baskettotal, order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
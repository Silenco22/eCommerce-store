import json

from account.models import Address
from basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from orders.models import Order, OrderItem

from .models import DeliveryOptions

# get all delivery options and display them on the page/ in hmtl file
@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})

#sending ajax request to this view
@login_required
def basket_update_delivery(request):
    basket = Basket(request) # we need info from basket class so we instantiate him here
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption")) # extracting form ajax request delivery option id and saving into the variable
        delivery_type = DeliveryOptions.objects.get(id=delivery_option) # geting particular option from database based upon the id
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price) # updating delivery price with func in basket called update_delivery and passing into the fucn the price of delivery option

        session = request.session # getting session informatino here from django
        if "delivery" not in request.session: # checking session if there is an area called purchase and if not create one. we are puting this infor in the session so that we can later have prechoosen delivery option, basically it doesnt forget the delivery option if we refresh the checkoutr page or we leave it
            session["delivery"] = {
                "delivery_id": delivery_type.id,
            }
        else: # if there is purchase in the session then just update it with new devlivery type id
            session["delivery"]["delivery_id"] = delivery_type.id
            session.modified = True # this is required to make changes in the session

        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price})
        return response # returning json response to template with total and delivery price

@login_required
def delivery_address(request):

    session = request.session
    if "delivery" not in request.session: # doesnt allow us to go to proceed with this template/view if didnt select any delivery option
        messages.success(request, "Please select delivery option") # message framework allows us to send them a message
        return HttpResponseRedirect(request.META["HTTP_REFERER"]) # returning them to the previous page

    addresses = Address.objects.filter(customer=request.user).order_by("-default") # getting addresses for specific user that we got form the request cause he needs to be loged in and orderign them by -default

    if "address" not in request.session: # checking if there is address field in the session stored
        session["address"] = {"address_id": str(addresses[0].id)} # add address field with the id of the default address addresses[0] its like that cause we order addresses by '-default' 
    else:
        session["address"]["address_id"] = str(addresses[0].id) # if there is already address id in the session than we just update it with new/old id
        session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})

@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session: # normaly ther will always be address selected but this secures if somebody wants to come to this page in a different way
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "checkout/payment_selection.html", {})

####
# PayPay
####
from paypalcheckoutsdk.orders import OrdersGetRequest #allows us to send request to paypal

from .paypal import PayPalClient # class with methods to read data 


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id # fetch allow us to get the user id from the request

    requestorder = OrdersGetRequest(data) # sending request to paypal with order id
    response = PPClient.client.execute(requestorder) # saving response from paypal

    total_paid = response.result.purchase_units[0].amount.value # example of reading data from the response

    basket = Basket(request)
    # saving order data into our database
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    # saving all the items form the basket for certain order into database
    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})
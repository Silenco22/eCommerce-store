from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse

from orders.views import user_orders

from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import Customer, Address
from .token import account_activation_token


@login_required
def dashboard(request):
    return render(request,'account/dashboard/dashboard.html')

@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation') 

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,'account/dashboard/edit_details.html', {'user_form': user_form})

def account_register(request):

    # if request.user.is_authenticated:
    #     return redirect('/')
    
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save() 

            #Email setup:
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html', {'form': registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')

def orders(request):
    orders = user_orders(request)
    return render(request,'account/dashboard/orders.html', {'orders': orders})

#Adress views

@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST) #fills data from the request in the form
        if address_form.is_valid(): # checks if data is vaild type acording to database model
            address_form = address_form.save(commit=False) #prepare for saving but dont commit in database
            address_form.customer = request.user #set customer with request.user cause there is no data about the customer in the form but we need it for the model
            address_form.save() #save model in the database model
            return HttpResponseRedirect(reverse("account:addresses")) #redirect us to account addresses HttpResponseRedirect esentially is redirect(redirect has more options to input in like model,view or url) 
    else:
        address_form = UserAddressForm() #if no data submited show form
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user) #get address where pk=id(we get that id from the url where <slug:id>) and customer form the request.user that part is for safety do that nobody can guess someelses id and then typing it in in the borwser and trying to edit their address
        address_form = UserAddressForm(instance=address, data=request.POST) # changing instance data with request.POST data 
        if address_form.is_valid(): # checking if all data is in valid types of data according to the model
            address_form.save() # saving form into database
            return HttpResponseRedirect(reverse("account:addresses")) #redirecting to the account addresses
    else:
        address = Address.objects.get(pk=id, customer=request.user) 
        address_form = UserAddressForm(instance=address) #its jsut gonna display form with instance data in it if there is no POS request / that shows first when we render template 
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form}) #passing form to the template

@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")

@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False) #set all customers addresses to default = False
    Address.objects.filter(pk=id, customer=request.user).update(default=True) # set praticular customer address with id to default = true
    return redirect("account:addresses")   
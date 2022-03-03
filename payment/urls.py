from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.BasketView, name='basket'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', views.stripe_webhook), #stripe sends data to webhook/ and then we forward taht to our view
 ]
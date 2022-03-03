//'use strict';


var stripe = Stripe(STRIPE_PUB_KEY);

var elem = document.getElementById('submit');
// collects clientsecret from the 'Pay' button
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
// react stylign 
var style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};

//card element on the page
var card = elements.create("card", { style: style });
card.mount("#card-element");

//displays erros where the <div id=card-errors>
card.on('change', function(event) {
var displayError = document.getElementById('card-errors')
if (event.error) {
  displayError.textContent = event.error.message;
  //boostrap styling added if erros
  $('#card-errors').addClass('alert alert-info');
  //boostrap styling removed if no erros
} else { 
  displayError.textContent = '';
  $('#card-errors').removeClass('alert alert-info');
}
});
//form element on the page
var form = document.getElementById('payment-form');
//even listenr, when someone press submit its gonna collect all the information in the form, ie perform an action
form.addEventListener('submit', function(ev) {
ev.preventDefault();

// collectin all the billign data by id in html code
var custName = document.getElementById("custName").value;
var custAdd = document.getElementById("custAdd").value;
var custAdd2 = document.getElementById("custAdd2").value;
var postCode = document.getElementById("postCode").value;

//with ajax request sending order to the server, creating new order in databse first, then stripe confirms payment and the we update billing status = True
$.ajax({
    type: "POST",
    url: 'http://127.0.0.1:8000/orders/add/',
    data: {
      order_key: clientsecret, // storing order key in datbase so that we can later on identify the order  after collecting data from stripe and update the billing status where the kyes match to True, all other data we get from session
      csrfmiddlewaretoken: CSRF_TOKEN,
      cust_name: custName,
      action: "post",
    },
    success: function (json) {
      console.log(json.success)
  
// sending payment 
      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address:{
                line1:custAdd,
                line2:custAdd2
            },
            name: custName
          },
        }
//checking if there was any errors and act acordingly
      }).then(function(result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
//if all ok redirect us to orderplacement
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
          }
        }
      });
    },
    error: function (xhr, errmsg, err) {},
  });

   


});
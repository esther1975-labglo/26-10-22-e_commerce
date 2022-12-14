from django.shortcuts import render,redirect
from .models import Cartitems, Customer, Product, Cart, Wishlist, Order
from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import csv
from django.views import View
from django.db.models import Q
from django.views.generic.list import ListView
from django.shortcuts import get_list_or_404, get_object_or_404
from math import ceil
from django.core import serializers 
import stripe
from django.views.generic import TemplateView
from django.conf import settings
stripe.api_key = settings.SECRET_KEY
from django.views.decorators.csrf import csrf_exempt

#SESSION_ID_MAPPING = "session_id":[session_id]

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = Product.objects.get(id = 1)
        product = Product.objects.get(name=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount':int(product.price)
                        ,
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url = YOUR_DOMAIN + '/success/',
            cancel_url = YOUR_DOMAIN + '/cancel/',
        )
        
        print("checkout_session", checkout_session)
        #event = json.loads(checkout_session)
        #print("HELLO", event)
        #if event['type'] == 'checkout.session.completed':
            #session = event['data']['object']
            #sessionID = session['id']
            #ID = session['metadata']['product_id']
            #Payment.objects.filter(id = ID).update(paid = True, description = sessionID)
        return redirect(checkout_session.url, status=200)



@csrf_exempt
def WebhookView(request):
    payload = request.body.decode('utf-8')
    print("payload", payload)
    event = json.loads(payload)
    print("HELLO", event)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        sessionID = session['id']
        ID = session['metadata']['product_id']
        Payment.objects.filter(id = ID).update(paid = True, description = sessionID)

    elif event['type'] == 'payment_intent.payment_failed':
        session = event['data']['object']
        sessionID = session['id']
        ID = session['metadata']['product_id']
        Payment.objects.filter(id = ID).update(paid = True, description = sessionID)   




    return HttpResponse(True, status = 200)

class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


def store(request):
    if request.user.is_authenticated:
        global cart
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer, is_active = False)
        cartitems = cart.cartitems_set.all()
        #wishlist, created = Wishlist.objects.get_or_create(customer = customer, is_active = False)
        #wishlistitems = wishlist.wishlistitems_set.all()
    products = Product.objects.all()
    context = {
    		'products':products,
    		'cart':cart,
           # 'wishlist_add':wishlist_add,
    		 }
    return render(request, 'store.html', context)

#def search(request):
	#q = request.GET.get('name')
	#data = Product.objects.filter(title__icontains = q).order_by('-id')
	#return render(request,'search.html',{'data':data})

"""def searchMatch(query, item):
    return True

def search(request):
    query = request.GET.get('search')
    allproducts = []
    products = Product.objects.values('title','name')
    things = {item['name'] for item in products}
    for i in things:
        a = Product.objects.filter(name = i)
        b = [item for item in a if searchMatch(query, item)]
        n = len(b)
        nSlides = n // 4 + ceil((n / 2) - (n // 4))
        allproducts.append([b, range(1, nSlides), nSlides])
        parems = {'allproducts':allproducts}
    return (request, 'store.html', parems)"""


class search(ListView):
    model = Product
    template_name = 'store.html'
    
    def get_queryset(self):
        
        queryset = Product.objects.all()
        if self.request.GET.keys():
           if self.request.GET.get('src') != '':
                keyword = self.request.GET.get('src')
                queryset = Product.objects.filter(Q(name__icontains = keyword.capitalize()) | Q(name__icontains = keyword.capitalize()))
              
        return queryset

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer, is_active = False)
        cartitems = cart.cartitems_set.all()
    else:
        cartitems = []
        cart = {"get_cart_total": 0, "get_itemtotal": 0}


    return render(request, 'cart.html', {'cartitems' : cartitems, 'cart':cart})


def checkout(request):
    return render(request, 'checkout.html', {})

def updateCart(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    product = Product.objects.get(id=productId)
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer = customer, is_active = False)
    cartitem, created = Cartitems.objects.get_or_create(cart = cart, product = product)

    if action == "add":
        cartitem.quantity += 1
        cartitem.save()
    

    return JsonResponse("Cart Updated", safe = False)

def updateQuantity(request):
    data = json.loads(request.body)
    quantityFieldValue = data['qfv']
    quantityFieldProduct = data['qfp']
    product = Cartitems.objects.filter(product__name = quantityFieldProduct).last()
    product.quantity = quantityFieldValue
    product.save()
    return JsonResponse("Quantity updated", safe = False)

"""def remove_cart(self, id):
        product_id = str(Product.id)
        if product_id in self.Cartitems.objects.all():
            del self.Cartitems[product_id]
            self.save()"""

def remove_cart(request, id):
    #cart = Cart.objects.get(id = id)
    product = get_object_or_404(Product, id = id)
    cart_item = Cartitems.objects.get(product = Product.product_id, cart = cart)
    cart_item.delete()
    return HttpResponseRedirect(reverse('cart'))



@login_required
def wishlist(request):
	wishlist = Wishlist.objects.filter(user = request.user)
	context = {'wishlist':wishlist}
	return render(request, 'wishlist.html', context)

@login_required
def order(request):
	order = Order.objects.filter(user = request.user)
	context = {'order':order}
	return render(request, 'order.html', context)


@login_required
def liked(request):
    wishlist = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user_id_id=request.user.pk)
        else:
            print("Please login")
            return HttpResponse("store")

    return render(request, template_name='wishlist.html', context={"wishlist": wishlist})

@login_required
def add_to_wishlist(request):
    if request.is_ajax() and request.POST and 'attr_id' in request.POST:
        if request.user.is_authenticated:
            data = Wishlist.objects.filter(user_id_id = request.user.pk, product_id_id = int(request.POST['attr_id']))
            if data.exists():
                data.delete()
            else:
                Wishlist.objects.create(user_id_id = request.user.pk, product_id_id = int(request.POST['attr_id']))
    else:
        print("No Product is Found")

    return redirect("main:home")
 

def brand_product_list(request, id):#brand_id):
	brand = Brand.objects.get(id=id)#brand_id)
	data = Product.objects.filter(brand=brand).order_by('-id')
	return render(request,'category_product_list.html', {'data':data})  

   

class product_list(ListView):
    model = Product
    def render_to_response(self, request):
        form = Product.objects.all()
        data = serializers.serialize("json", form, indent = 4)
        print("Get", data)
        obj = json.loads(data)
       
        return JsonResponse(obj, content_type = "application/json", status = 200, safe = False)

class cart_list(ListView):
    model = Cart
    def render_to_response(self, request):
        form = Cart.objects.all()
        data = serializers.serialize("json", form, indent = 4)
        print("Get", data)
        obj = json.loads(data)
        return JsonResponse(obj, content_type = "application/json", status = 200, safe = False)

class cart_items_list(ListView):
    model = Cartitems
    def render_to_response(self, request):
        form = Cartitems.objects.all()
        data = serializers.serialize("json", form, indent = 4)
        print("Get", data)
        obj = json.loads(data)
        return JsonResponse(obj, content_type = "application/json", status = 200, safe = False)

class wishlist_list(ListView):
    model = Wishlist
    def render_to_response(self, request):
        form = Wishlist.objects.all()
        data = serializers.serialize("json", form, indent = 4)
        print("Get", data)
        obj = json.loads(data)
        return JsonResponse(obj, content_type = "application/json", status = 200, safe = False)


#def order_create(request):
   # cart = 
from django.shortcuts import render
from .models import Cartitems, Customer, Product, Cart, Wishlist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
#import {FavoriteBorderIcon} from '@mui/icons-material';

def store(request):
    if request.user.is_authenticated:
    	global cart
    	customer = request.user.customer
    	cart, created = Cart.objects.get_or_create(customer = customer, is_active = False)
    	cartitems = cart.cartitems_set.all()
    products = Product.objects.all()
    context = {
    		'products':products,
    		'cart':cart,
    		 }
    return render(request, 'store.html', context)

def search(request):
	q = request.GET.get('name')
	data = Product.objects.filter(title__icontains = q).order_by('-id')
	return render(request,'search.html',{'data':data})


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
    
@login_required
def wishlist(request):
	wishlist = Wishlist.objects.filter(user = request.user)
	context = {'wishlist':wishlist}
	return render(request, 'wishlist.html', context)


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
            data = Wishlist.objects.filter(user_id_id = request.user.pk,music_id_id = int(request.POST['attr_id']))
            if data.exists():
                data.delete()
            else:
                Wishlist.objects.create(user_id_id = request.user.pk,music_id_id = int(request.POST['attr_id']))
    else:
        print("No Product is Found")

    return redirect("main:home")

def add_wishlist(request, id):
	pid = request.GET.get('product')
	product = Product.objects.get(id = id)
	data={'pid':pid}
	checkw = Wishlist.objects.filter(product = product,user = request.user).count()
	if checkw > 0:
		data = { 
			'bool':False
		}
	else:
		wishlist = Wishlist.objects.create(
			product = product,
			user = request.user
		)
		data = {
			'bool':True
		}
	return JsonResponse(data)

# My Wishlist
def my_wishlist(request):
	wlist = Wishlist.objects.filter(user = request.user).order_by('-id')
	return render(request, 'wishlist.html',{'wlist':wlist})
    
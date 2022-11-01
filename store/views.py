from django.shortcuts import render
from .models import Cartitems, Customer, Product, Cart, Wishlist
from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.shortcuts import get_list_or_404, get_object_or_404

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

"""def remove_cart(self, id):
        product_id = str(Product.id)
        if product_id in self.Cartitems.objects.all():
            del self.Cartitems[product_id]
            self.save()"""

def remove_cart(request, id):
    #cart = Cart.objects.get(id = id)
    product = get_object_or_404(Product, id = id)
    cart_item = Cartitems.objects.get(product = Product.product_id)#, cart = cart)
    cart_item.delete()
    return HttpResponseRedirect(reverse('cart'))



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
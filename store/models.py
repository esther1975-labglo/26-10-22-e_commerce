from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.lookups import IntegerFieldFloatRounding

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Product(models.Model):
	title = models.CharField(max_length = 50)
	name = models.CharField(max_length = 50)
	price = models.FloatField(default = 10.55)
	image = models.ImageField(upload_to="static/image/")
	stock_aval = models.BooleanField(null = True)
	def __str__(self):
		return self.name

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=False)
	

    @property
    def get_cart_total(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.get_total for item in cartitems])
        return total
    
    @property
    def get_itemtotal(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.quantity for item in cartitems])
        return total

    def __str__(self):
        return str(self.id)

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    tax = models.FloatField(default=2.25)
    
    def grand_total(self):
    	return self.get_total() * (1 + self.tax)
 
  
    @property
    def get_total(self):
        total = self.quantity * self.product.price + 2.55
        if total == 0.00:
            self.delete()
        return total

    

    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)

    def __str__(self):
        return self.address

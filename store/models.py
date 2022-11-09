from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.lookups import IntegerFieldFloatRounding

FAILED = 0
PENDING = 1
SUCCESS = 2

Order_choices = [
    ('PENDING', 'pending'),
    ('FAILED', 'failed'),
    ('SUCCESS', 'success'),
]

class TimeStampBaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Product(TimeStampBaseModel):
        title = models.CharField(max_length = 50)
        name = models.CharField(max_length = 50)
        price = models.FloatField(default = 10.55)
        brand = models.ImageField(upload_to = "static/image/")
        image = models.ImageField(upload_to = "static/image/")
        stock_aval = models.BooleanField(null = True)
        @staticmethod
        def autocomplete_search_fields():
            return ("title__icontains", "name__icontains", "price__icontains", "image__icontains")
        def __str__(self):
            return self.name

class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="static/image/")

    def __str__(self):
        return self.title

class Cart(TimeStampBaseModel):
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

class Cartitems(TimeStampBaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    tax = models.FloatField(default=22.50)
    
    def grand_total(self):
    	return self.get_total() * (1 + self.tax)
 
  
    @property
    def get_total(self):
        total = self.quantity * self.product.price + 22.50
        if total == 0.00:
            self.delete()
        return total

    

    def __str__(self):
        return self.product.name
        
class Order(TimeStampBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_items = models.ForeignKey(Cartitems, on_delete=models.CASCADE)
    status = models.BooleanField(default = False)

    def placeorder(self):
        self.save

    def get_order_by_customer(self, id):
        return Order.objects.filter(customer = customer_id)

class ProductOrder(TimeStampBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart_product = models.ManyToManyField(Cart)
    tax = models.FloatField()
    status = models.IntegerField(
        choices=Order_choices,
        default=PENDING
    )

    def __str__(self):
        return self.user.username

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)

    def __str__(self):
        return self.address


class Wishlist(TimeStampBaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	wished_item = models.ForeignKey(Product, on_delete=models.CASCADE)
	added_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.wished_item.title

class Payment(models.Model):
    transaction_id = models.TextField()
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    #status = models.SmallIntegerField(choices=Order_choices, default = 1)
    status = models.BooleanField(default = 1)
    



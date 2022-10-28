from django.contrib import admin
from . models import *


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(Wishlist)
#admin.site.register(wishlist_items)
admin.site.register(ShippingAddress)

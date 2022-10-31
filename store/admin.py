from django.contrib import admin
from . models import *


admin.site.register(Customer)
admin.site.register(Product)
class cartadmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
admin.site.register(Cart, cartadmin)
admin.site.register(Cartitems)
admin.site.register(Wishlist)
#admin.site.register(wishlist_items)
admin.site.register(ShippingAddress)

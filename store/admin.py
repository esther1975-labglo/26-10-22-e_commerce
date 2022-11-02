from django.contrib import admin
from . models import *


admin.site.register(Customer)


admin.site.register(Product)

admin.site.register(Brand)

class cartadmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
admin.site.register(Cart, cartadmin)

admin.site.register(Cartitems)

admin.site.register(Wishlist)

#admin.site.register(wishlist_items)
admin.site.register(ShippingAddress)


class ProductAdmin(admin.ModelAdmin):
   raw_id_fields = ('title', 'name', 'price', 'image',)
   autocomplete_lookup_fields = {
   'fk': ['featured_user','featured_story'],
   }
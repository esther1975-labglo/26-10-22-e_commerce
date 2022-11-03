from django.contrib import admin
from . models import *


admin.site.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "name", "brand", "price", "image")
    search_fields = ('name', 'title')
    list_display_links = ( "image", )
    list_editable = ('title',)
    list_filter = ('title', 'name')
    
    fieldsets = (
        (None, {
            'fields': (
                'id'
                'title',
                'name',
                'brand',
                'price',
                'image'
            )
        }),
    )
admin.site.register(Product, ProductAdmin)

admin.site.register(Brand)

class cartadmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
  

admin.site.register(Cartitems)

admin.site.register(Wishlist)

#admin.site.register(wishlist_items)
admin.site.register(ShippingAddress)


class ProductAdmin(admin.ModelAdmin):
   raw_id_fields = ('title', 'name', 'price', 'image',)
   autocomplete_lookup_fields = {
   'fk': ['featured_user','featured_story'],
   }
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import product_list, cart_list, cart_items_list, wishlist_list, search


from . import views

urlpatterns = [
    path('store/', views.store, name = 'store'),
    path('search/', search.as_view(), name = 'search'),
    #path('search', views.search, name = 'search'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('updatecart', views.updateCart, name = 'updatecart'),
    path('updatequantity', views.updateQuantity, name = 'updatequantity'),
    path('remove_cart/<int:id>', views.remove_cart, name = 'remove_cart'),   
    path('wishlist', views.wishlist, name = 'wishlist'),
    path('order', views.order, name = 'order'),
   
    path('wishlist/123', views.liked, name='liked'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'), # For add to wishlist

    #json

    path('product_json/', product_list.as_view()),
   
    path('cart_json/', cart_list.as_view()),
    path('cartitems_json/', cart_items_list.as_view()),
    path('wishlist_json/', wishlist_list.as_view()),
   
   # path('add-wishlist', views.add_wishlist, name='add_wishlist'),
   # path('my-wishlist', views.my_wishlist, name='my_wishlist'),
    #path('update_wishlist', views.update_wishlist, name = 'update_wishlist'),
    #path('updatequantity_wishlist', views.updateQuantity_wishlist, name = 'updatequantity_wishlist'),
    #path("add_wishlist/<int:Product_id>/",views.add_wishlist,name = 'add_wishlist'),
    #path("wishall", login_required(views.Wishproducts.as_view()), name='wishlist'),
   # path("remove_wishlist/<int:Product_id>/", views.remove_wishlist, name='remove_wish'),
]

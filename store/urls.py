from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store, name = 'store'),
    path('search', views.search, name = 'search'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('updatecart', views.updateCart, name = 'updatecart'),
    path('updatequantity', views.updateQuantity, name = 'updatequantity'),
    path('wishlist', views.wishlist, name = 'wishlist'),
    path('wishlist/123', views.liked, name='liked'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'), # For add to wishlist
    path('add-wishlist', views.add_wishlist, name='add_wishlist'),
    path('my-wishlist', views.my_wishlist, name='my_wishlist'),
    #path('update_wishlist', views.update_wishlist, name = 'update_wishlist'),
    #path('updatequantity_wishlist', views.updateQuantity_wishlist, name = 'updatequantity_wishlist'),

]

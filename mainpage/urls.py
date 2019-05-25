from django.urls import path
from . import views

app_name = 'mainpage'
urlpatterns = [
    path('', views.home, name='home'),
    path('restaurant_menu/<int:restaurant_id>/', views.MenuView.as_view(), name='menu'),
    path('add_item_to_cart/', views.addToCart, name='addCart'),
    path('flush_shopping_cart/', views.flushCart, name='flushCart'),
    path('cart_detail/', views.cart_detail, name="showCart"),
    path('address_management/', views.manage_address, name="manageAddress"),
    path('set_default_address/', views.set_default_address, name="setDefaultAddress"),
    path('add_address/', views.add_address, name="addAddress"),
    path('delete_address/', views.delete_address, name="delAddress"),
    path('edit_address/<int:address_id>/', views.edit_address, name="editAddress")
]
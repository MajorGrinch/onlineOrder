from django.urls import path
from . import views

app_name = 'mainpage'
urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='home'),
    path('menu/<int:restaurant_id>/', views.MenuView.as_view(), name='menu'),
    path('add_item_to_cart/', views.addToCart, name='addCart'),
    path('flush_shopping_cart/', views.flushCart, name='flushCart'),
    path('cart_detail/', views.cart_detail, name="showCart"),
]
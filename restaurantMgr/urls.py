from django.urls import path
from . import views

app_name = 'restaurantMgr'

urlpatterns = [
    path('', views.index, name="index"),
    path('check_order/<int:pk>/', views.OrderDetailView.as_view(), name="orderDetail"),
    path('menu_management/<int:restaurant_id>/', views.MenuItemView.as_view(), name="manageMenu"),
    path('add_menuitem/', views.add_menuitem, name="addMenuItem"),
    path('edit_menuitem/<int:menuitem_id>/', views.edit_menuitem, name="editMenuItem"),
    path('delete_menuitem/<int:menuitem_id>/', views.delete_menuitem, name="deleteMenuItem"),
    path('restore_menuitem/<int:menuitem_id>/', views.restore_menuitem, name="restoreMenuItem"),
    path('edit_restaurant/<int:restaurant_id>/', views.edit_restaurant, name="editRestaurant"),
    path('create_restaurant/', views.create_restaurant, name="createRestaurant"),
]
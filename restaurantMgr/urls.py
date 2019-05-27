from django.urls import path
from . import views

app_name = 'restaurantMgr'

urlpatterns = [
    path('', views.index, name="index"),
    path('check_order/<int:pk>/', views.OrderDetailView.as_view(), name="orderDetail"),
    path('menu_management/<int:restaurant_id>/', views.MenuItemView.as_view(), name="manageMenu"),
    path('add_menuitem/', views.add_menuitem, name="addMenuItem"),
]
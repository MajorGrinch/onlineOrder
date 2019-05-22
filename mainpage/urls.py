from django.urls import path
from . import views

app_name = 'mainpage'
urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='home'),
    path('menu/<int:restaurant_id>/', views.MenuView.as_view(), name='menu'),
]
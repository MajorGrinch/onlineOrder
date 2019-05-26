from django.urls import path
from . import views

app_name = 'restaurantMgr'

urlpatterns = [
    path('', views.index, name="index")
]
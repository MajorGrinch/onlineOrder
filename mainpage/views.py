from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.utils import timezone
from .models import Restaurant, MenuItem

# Create your views here.

def home(request):
    context = {'curr_time' : timezone.now()}
    return render(request, 'mainpage/home.html', context)

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'mainpage/home.html'
    context_object_name = 'restaurant_list'

class MenuView(ListView):
    model = MenuItem
    template_name = 'mainpage/restaurant_menu.html'
    context_object_name = 'menuitem_list'


    def get_queryset(self):
        # self.restaurant = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        return MenuItem.objects.filter(restaurant=self.kwargs['restaurant_id'])
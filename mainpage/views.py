from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.utils import timezone
from .models import Restaurant, MenuItem
from django.http import HttpResponse
import json

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_id'] = self.kwargs['restaurant_id']
        context['restaurant_name'] = Restaurant.objects.get(pk=int(self.kwargs['restaurant_id'])).name
        # print(context)
        return context

def addToCart(request):
    if request.method == 'POST':
        try:
            # menu_item_id = int(request.POST['item_id'])
            # restaurant_id_str = request.POST['restaurant_id']

            # shopping_cart = request.session.setdefault("cart", {})

            # shopping_cart.setdefault(restaurant_id_str, []).append(menu_item_id)
            # request.session.save()
            # print(request.session.get('cart'))
            # return HttpResponse(menu_item_id)
            menu_item_id = int(request.POST['item_id'])
            menu_item = MenuItem.objects.get(pk=menu_item_id)
            item_price = menu_item.price
            item_title = menu_item.title
            item_image = menu_item.image.name
            ret_obj = {'price': item_price, 'title': item_title, 'image': item_image}
        except:
            return HttpResponse(0)
        else:
            return HttpResponse(json.dumps(ret_obj))

def flushCart(request):
    try:
        if 'cart' in request.session.keys():
            request.session.pop('cart')
    except:
        return HttpResponse(0)
    else:
        return HttpResponse(1)

def cart_detail(request):
    if request.method == 'GET':
        return render(request, 'mainpage/cart_detail.html', {})
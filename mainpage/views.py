from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.utils import timezone
from .models import Restaurant, MenuItem, Order, OrderItem, Address
from django.http import HttpResponse
import json
from django.db import transaction

# Create your views here.

def home(request):
    if request.method == 'GET':
        restaurant_list = Restaurant.objects.all()
        top2_restaurants = Restaurant.objects.order_by('-rating')[:2]
        context = {'restaurant_list': restaurant_list, 'top2_restaurants': top2_restaurants}
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


def place_order(request):
    curr_user = request.user.id
    subtotal = int(request.POST['subtotal'])
    restaurant_id = request.POST['restaurant_id']
    address_id = request.POST['address_id']
    o = Order(order_num='{:%Y%m%d%H%M%S}-{:d}'.format(timezone.now(), 22),
            subtotal=subtotal, user=curr_user, restaurant_id=restaurant_id,
            address_id=address_id)
    return HttpResponse(1)


def manage_address(request):
    if request.method == 'GET':
        user_addresses = Address.objects.filter(user=request.user)
        context = {'addresses': user_addresses}
        return render(request, 'mainpage/address_management.html', context)

def cancal_default_address(request):
    if request.method == 'POST':
        try:
            address_id = request.POST['address_id']
            address = Address.objects.get(pk=address_id)
            address.is_default = False
            return HttpResponse(1)
        except:
            return HttpResponse(0)

@transaction.atomic
def set_default_address(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        address_id = data['address_id']
        new_default_address = Address.objects.get(pk=address_id)
        old_default_address = Address.objects.get(user=request.user, is_default=True)
        old_default_address.is_default = False
        old_default_address.save()
        new_default_address.is_default = True
        new_default_address.save()
        return HttpResponse(1)


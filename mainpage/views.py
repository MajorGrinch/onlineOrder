from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic import ListView
from django.utils import timezone
from .models import Restaurant, MenuItem, Order, OrderItem, Address
from django.http import HttpResponse
import json
from django.contrib import messages
from django.db import transaction
from .forms import AddressCreationForm, AddressChangeForm
from django.core.serializers import serialize, deserialize
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

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
        return MenuItem.objects.filter(restaurant=self.kwargs['restaurant_id'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_id'] = self.kwargs['restaurant_id']
        context['restaurant_name'] = Restaurant.objects.get(pk=int(self.kwargs['restaurant_id'])).name
        # print(context)
        return context


def get_restaurant_info(request, restaurant_id):
    if request.method == 'GET':
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        context = {'name': restaurant.name, 'delivering_fee': restaurant.delivering_fee}
        return JsonResponse(context)

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
            return JsonResponse(ret_obj)

def flushCart(request):
    try:
        if 'cart' in request.session.keys():
            request.session.pop('cart')
    except:
        return HttpResponse(0)
    else:
        return HttpResponse(1)

def cart_detail(request):
    """get will redirect to cart detail page
       in that page, post is used to get address list
       when use click the address button
    """
    if request.method == 'GET':
        return render(request, 'mainpage/cart_detail.html')

@login_required
def get_address_list(request):
    address_list = Address.objects.filter(user=request.user)
    return HttpResponse(serialize('json', address_list))


def manage_address(request):
    if request.method == 'GET':
        user_addresses = Address.objects.filter(user=request.user, is_active=True)
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
    """set the default address of the current user"""
    if request.method == 'POST':
        data = json.loads(request.body)
        address_id = data['address_id']
        new_default_address = Address.objects.get(pk=address_id)
        try:
            with transaction.atomic():
                old_default_address = Address.objects.get(user=request.user, is_default=True)
                old_default_address.is_default = False
                old_default_address.save()
        except Address.DoesNotExist:
            print('No default address. SKIP.')

        new_default_address.is_default = True
        new_default_address.save()
        messages.success(request, 'Set successfully')
        return HttpResponse(1)


def add_address(request):
    """add a address for the current user"""
    if request.method == 'POST':
        try:
            form = AddressCreationForm(request.POST)
            if form.is_valid():
                new_address = form.save(commit=False)
                new_address.user = request.user
                new_address.save()
                return redirect('mainpage:manageAddress')
        except:
            return render(request, 'mainpage/address_creation_page.html', {'form': form})
    else:
        form = AddressCreationForm()
        context = {'form': form}
        return render(request, 'mainpage/address_creation_page.html', context)


def delete_address(request):
    """delete address for the current user"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            address_id = data['address_id']
            address = Address.objects.get(pk=address_id)
            if address.is_default:
                raise ValueError('Default_Address')
            # address.delete()
            address.is_active = False
            address.save()
            return HttpResponse(1)
        except ValueError as e:
            return HttpResponse(e)
        except:
            return HttpResponse(0)



def edit_address(request, address_id):
    if request.method == 'POST':
        address = Address.objects.get(pk=address_id)
        form = AddressChangeForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('mainpage:manageAddress')
        else:
            return render(request, 'mainpage/address_change_page.html', {'form': form})
    else:
        address = Address.objects.get(pk=address_id)
        form = AddressChangeForm(instance=address)
        return render(request, 'mainpage/address_change_page.html', {'form': form})

@transaction.atomic
def place_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        address_id = data['address_id']
        if address_id == None:
            try:
                address_id = Address.objects.get(user=request.user, is_default=True).id
            except ObjectDoesNotExist:
                messages.success(request,'No address selected or default address. Order cannot be processed')
                return HttpResponse('No address choosed')

        restaurant_cart = data['restaurant_cart']
        restaurant_id = int(restaurant_cart['id'][11:])
        user_id = request.user.id
        order = Order.objects.create(order_num='{:%Y%m%d%H%M%S}-{:d}'.format(timezone.now(), user_id),
                subtotal=restaurant_cart['subtotal'], user_id=user_id, restaurant_id=restaurant_id,
                address_id=address_id)
        order.save()
        iteminfo_list = restaurant_cart['iteminfo_list']
        print(iteminfo_list)
        for menuitem in iteminfo_list:
            menuitem_id = int(menuitem[5:])
            iteminfo = iteminfo_list[menuitem]
            orderitem = OrderItem(quantity=iteminfo['quantity'], unit_price=iteminfo['price'],
                    menuitem_id=menuitem_id, order=order)
            orderitem.save()
        return HttpResponse(restaurant_cart['id'])


def order_list(request):
    if request.method == 'GET':
        all_orders = Order.objects.filter(user=request.user).order_by('-order_time')
        order_length = all_orders.count()
        all_orders_paged = Paginator(all_orders, 5)
        page_id = int(request.GET['page'])
        curr_order_list = all_orders_paged.get_page(page_id)
        context = {'order_length': order_length, 'order_list': curr_order_list}
        return render(request, 'mainpage/order_management.html', context)



@login_required
def get_order_detail(request, order_id):
    orderitems = OrderItem.objects.filter(order_id=order_id)
    orderitem_list = []
    for orderitem in orderitems:
        menuitem = orderitem.menuitem
        orderitem_list.append({'image': menuitem.image.name,
                                'title': menuitem.title,
                                'unit_price': orderitem.unit_price,
                                'quantity': orderitem.quantity, 'restaurant_id': menuitem.restaurant.id} )
    return HttpResponse(json.dumps(orderitem_list))

@login_required
def confirm_delivery(request):
    if request.method == 'POST':
        try:
            order_id = request.POST['order_id']
            order = Order.objects.get(pk=order_id)
            order.status = 2
            order.save()
            return HttpResponse(1)
        except:
            return HttpResponse(0)
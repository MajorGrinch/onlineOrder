from django.shortcuts import render, redirect
from mainpage.models import Restaurant, Order, OrderItem, MenuItem
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.http import HttpResponse
from .forms import MenuItemCreationForm, MenuItemChangeForm, RestaurantChangeForm, RestaurantCreationForm
from pymongo import MongoClient
from bson.objectid import ObjectId

# Create your views here.


@login_required
def index(request):
    restaurant = Restaurant.objects.get(user=request.user)
    orders_all = Order.objects.filter(restaurant=restaurant)
    orders_pending = orders_all.filter(status=0)
    orders_delivered = orders_all.filter(status=2)
    orders_confirmed = orders_all.filter(status=1)
    request.session['restaurant_id'] = restaurant.id
    context = {
        'orders_pending': orders_pending,
        'orders_delivered': orders_delivered,
        'orders_confirmed': orders_confirmed
    }
    return render(request, 'restaurantMgr/index.html', context)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'restaurantMgr/order_detail.html'
    context_object_name = 'order'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderitem_list'] = OrderItem.objects.filter(
            order=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        order = self.get_object()
        if action == 'confirm':
            order.status = 1
            order.save()
            return HttpResponse("confirm order")
        if action == 'decline':
            order.status = 3
            order_dict = {
                "order_num": order.order_num,
                "order_id": order.id,
                "order_time": order.order_time,
                "subtotal": order.subtotal,
                "restaurant": str(order.restaurant),
                "restaurant_id": order.restaurant.id,
                "address": str(order.address),
                "status": order.status,
                "item_list": []
            }
            orderitems = OrderItem.objects.filter(order=order)
            orderitem_list = []
            for orderitem in orderitems:
                menuitem = orderitem.menuitem
                orderitem_list.append({
                    'image': menuitem.image.name,
                    'title': menuitem.title,
                    'unit_price': orderitem.unit_price,
                    'quantity': orderitem.quantity,
                    'restaurant_id': menuitem.restaurant.id
                })
            order_dict["item_list"] = orderitem_list
            # order.save()
            db = MongoClient().takeout
            order_user = order.user
            orderlist_id = order_user.orderlist_id
            if orderlist_id == '':
                orderlist_id = db.order.insert_one({
                    'order_list': []
                }).inserted_id
                order_user.orderlist_id = orderlist_id
                order_user.save()
            result = db.order.update_one({'_id': ObjectId(orderlist_id)},
                                         {'$push': {
                                             'order_list': order_dict
                                         }})
            if result.modified_count == 1:
                order.delete()
                return HttpResponse("decline order")
        return HttpResponse(1)


class MenuItemView(ListView):
    model = MenuItem
    template_name = 'restaurantMgr/menu_management.html'
    context_object_name = 'menuitem_list'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        restaurant_id = self.request.session['restaurant_id']
        return MenuItem.objects.filter(restaurant=restaurant_id)


@login_required
def add_menuitem(request):
    if request.method == 'POST':
        form = MenuItemCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_menuitem = form.save(commit=False)
            new_menuitem.restaurant = request.session['restaurant_id']
            new_menuitem.save()
            return redirect('restaurantMgr:manageMenu')
        else:
            context = {'form': form}
            return render(request, 'restaurantMgr/menuitem_creation_page.html',
                          context)

    else:
        form = MenuItemCreationForm()
        context = {'form': form}
        return render(request, 'restaurantMgr/menuitem_creation_page.html',
                      context)


@login_required
def edit_menuitem(request, menuitem_id):
    menuitem = MenuItem.objects.get(pk=menuitem_id)
    if request.method == 'POST':
        form = MenuItemChangeForm(request.POST,
                                  request.FILES,
                                  instance=menuitem)
        if form.is_valid():
            form.save()
            return redirect('restaurantMgr:manageMenu')
        else:
            context = {'form': form}
            return render(request, 'restaurantMgr/menuitem_change_page.html',
                          context)
    else:
        form = MenuItemChangeForm(instance=menuitem)
        context = {'form': form}
        return render(request, 'restaurantMgr/menuitem_change_page.html',
                      context)


@login_required
def delete_menuitem(request, menuitem_id):
    if request.method == 'GET':
        menuitem = MenuItem.objects.get(pk=menuitem_id)
        menuitem.is_active = False
        menuitem.save()
        return redirect('restaurantMgr:manageMenu')


@login_required
def restore_menuitem(request, menuitem_id):
    if request.method == 'GET':
        menuitem = MenuItem.objects.get(pk=menuitem_id)
        menuitem.is_active = True
        menuitem.save()
        return redirect('restaurantMgr:manageMenu')


@login_required
def edit_restaurant(request):
    restaurant = Restaurant.objects.get(pk=request.session['restaurant_id'])
    if request.method == 'POST':
        form = RestaurantChangeForm(request.POST,
                                    request.FILES,
                                    instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurantMgr:editRestaurant')
        else:
            form = RestaurantChangeForm(instance=restaurant)
            context = {'form': form}
            return render(request, 'restaurantMgr/restaurant_change_page.html',
                          context)

    else:
        form = RestaurantChangeForm(instance=restaurant)
        context = {'form': form}
        return render(request, 'restaurantMgr/restaurant_change_page.html',
                      context)


@login_required
def create_restaurant(request):
    if request.method == 'POST':
        form = RestaurantCreationForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            user = request.user
            user.is_restaurant = True
            restaurant.user = user
            user.save()
            restaurant.save()
            return redirect('restaurantMgr:index')
        else:
            form = RestaurantCreationForm(instance=restaurant)
            context = {'form': form}
            return render(request,
                          'restaurantMgr/restaurant_creation_page.html',
                          context)
    else:
        form = RestaurantCreationForm()
        context = {'form': form}
        return render(request, 'restaurantMgr/restaurant_creation_page.html',
                      context)

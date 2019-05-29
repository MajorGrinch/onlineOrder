from django.shortcuts import render, redirect
from mainpage.models import Restaurant, Order, OrderItem, MenuItem
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.http import HttpResponse
from .forms import MenuItemCreationForm, MenuItemChangeForm, RestaurantChangeForm, RestaurantCreationForm

# Create your views here.

@login_required
def index(request):
    restaurant = Restaurant.objects.get(user=request.user)
    orders_all = Order.objects.filter(user=request.user)
    orders_pending = orders_all.filter(status=0)
    orders_delivered = orders_all.filter(status=2)
    orders_confirmed = orders_all.filter(status=1)
    context = {'restaurant': restaurant, 'orders_pending': orders_pending,
                'orders_delivered': orders_delivered, 'orders_confirmed': orders_confirmed}
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
        context['orderitem_list'] = OrderItem.objects.filter(order=self.kwargs['pk'])
        context['restaurant'] = Restaurant.objects.get(user=self.request.user)
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
            order.save()
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
        # print('restaurant_id: ', self.kwargs['restaurant_id'])
        return MenuItem.objects.filter(restaurant=self.kwargs['restaurant_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        return context


@login_required
def add_menuitem(request):
    restaurant = Restaurant.objects.get(user=request.user)
    if request.method == 'POST':
        form = MenuItemCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_menuitem = form.save(commit=False)
            new_menuitem.restaurant = restaurant
            new_menuitem.save()
            return redirect('restaurantMgr:manageMenu', restaurant.id)
        else:
            context = {'form': form, 'restaurant': restaurant}
            return render(request, 'restaurantMgr/menuitem_creation_page.html', context)

    else:
        form = MenuItemCreationForm()
        context = {'form': form, 'restaurant': restaurant}
        return render(request, 'restaurantMgr/menuitem_creation_page.html', context)

@login_required
def edit_menuitem(request, menuitem_id):
    restaurant = Restaurant.objects.get(user=request.user)
    menuitem = MenuItem.objects.get(pk=menuitem_id)
    if request.method == 'POST':
        form = MenuItemChangeForm(request.POST, request.FILES, instance=menuitem)
        if form.is_valid():
            form.save()
            return redirect('restaurantMgr:manageMenu', restaurant.id)
        else:
            context = {'form': form, 'restaurant': restaurant}
            return render(request, 'restaurantMgr/menuitem_change_page.html', context)
    else:
        form = MenuItemChangeForm(instance=menuitem)
        context = {
            'restaurant': restaurant,
            'form': form}
        return render(request, 'restaurantMgr/menuitem_change_page.html', context)

@login_required
def delete_menuitem(request, menuitem_id):
    if request.method == 'GET':
        menuitem = MenuItem.objects.get(pk=menuitem_id)
        restaurant = Restaurant.objects.get(user=request.user)
        # menuitem.delete()
        menuitem.is_active = False
        menuitem.save()
        return redirect('restaurantMgr:manageMenu', restaurant.id)

@login_required
def edit_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(user=request.user)
    if request.method == 'POST':
        form = RestaurantChangeForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurantMgr:editRestaurant', restaurant.id)
        else:
            form = RestaurantChangeForm(instance=restaurant)
            context = {'restaurant': restaurant,
                    'form': form}
            return render(request, 'restaurantMgr/restaurant_change_page.html', context)

    else:
        form = RestaurantChangeForm(instance=restaurant)
        context = {'restaurant': restaurant,
                'form': form}
        return render(request, 'restaurantMgr/restaurant_change_page.html', context)

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
            return render(request, 'restaurantMgr/restaurant_creation_page.html', context)
    else:
        form = RestaurantCreationForm()
        context = {'form': form}
        return render(request, 'restaurantMgr/restaurant_creation_page.html', context)
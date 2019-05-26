from django.shortcuts import render
from mainpage.models import Restaurant, Order
from django.contrib.auth.decorators import login_required

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

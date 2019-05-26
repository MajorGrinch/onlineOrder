from django.shortcuts import render
from mainpage.models import Restaurant, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.http import HttpResponse

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
        context['orderitem_list'] = OrderItem.objects.filter(order_id=self.kwargs['pk'])
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
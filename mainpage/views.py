from django.shortcuts import render
from django.views.generic import ListView
from django.utils import timezone
from .models import Restaurant

# Create your views here.

def home(request):
    context = {'curr_time' : timezone.now()}
    return render(request, 'mainpage/home.html', context)

class IndexView(ListView):
    model = Restaurant
    template_name = 'mainpage/home.html'
    context_object_name = 'restaurant_list'
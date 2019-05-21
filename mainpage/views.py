from django.shortcuts import render
from django.utils import timezone

# Create your views here.

def home(request):
    context = {'curr_time' : timezone.now()}
    return render(request, 'mainpage/home.html', context)
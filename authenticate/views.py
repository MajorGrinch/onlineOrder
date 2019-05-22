from django.shortcuts import render, redirect
from .forms import UserCreationForm, EditProfileForm, MyAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.utils import timezone


class MyLoginView(LoginView):
    template_name = 'authenticate/login.html'
    authentication_form=MyAuthenticationForm

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.last_login = timezone.now()
            messages.success(request, ('You have been logged in!'))
            return redirect('mainpage:home')
        else:
            messages.success(request, 'Error logging in, please try again!')
            return redirect('authenticate:login')


def register_user(request):
    # TODO: if password1 != password2, make it fail
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have registered!'))
            return redirect('mainpage:home')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'authenticate/register.html', context)

def edit_user_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('Update successfully!'))
            return redirect('mainpage:home')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'authenticate/edit_profile.html', context)
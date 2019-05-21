from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView
from .forms import MyAuthenticationForm, MyPasswordChangeForm

app_name = 'authenticate'
urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', views.register_user, name="register"),
    path(
        'edit_user_profile/',
        views.edit_user_profile,
        name='edit_user_profile'),
    path(
        'change_password/',
        PasswordChangeView.as_view(
            template_name='authenticate/change_password.html',
            form_class=MyPasswordChangeForm,
            success_url='/'),
        name='change_password')
]
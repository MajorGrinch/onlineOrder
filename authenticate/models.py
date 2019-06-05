from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('Must provide email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save()
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    USERNAME_FIELD = 'username'
    objects = UserManager()

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_restaurant = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    cart_text = models.TextField(blank=True)
    REQUIRED_FIELDS = ['email',]

    class Meta:
        db_table = 'user'

    def __str__(self):
        return '{name}--{id}'.format(name=self.username, id=self.id)


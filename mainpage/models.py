from django.db import models
from authenticate.models import User


class Address(models.Model):
    full_name = models.CharField(max_length=100)
    street_address1 = models.CharField(max_length=50)
    street_address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'address'

    def __str__(self):
        return '{0}, {1}, {2}'.format(
            self.full_name, self.street_address1, self.user)


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    starting_price = models.IntegerField(default=0)
    delivering_fee = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    image = models.ImageField(upload_to='restaurant_images/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accumulated_score = models.FloatField(default=0)
    rated_times = models.IntegerField(default=0)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'restaurant'

    def __str__(self):
        return self.name


class SalesInfo(models.Model):
    date = models.DateField(auto_now=True)
    sales_num = models.IntegerField(default=0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        db_table = 'salesinfo'

    def __str__(self):
        return '{}, {}, {}'.format(self.date.isoformat(), self.restaurant,
                                   self.sales_num)

class MenuItem(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_item/', blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'menuitem'

    def __str__(self):
        return self.title + self.restaurant.name

class Order(models.Model):
    order_num = models.CharField(max_length=30)
    order_time = models.DateTimeField(auto_now=True)
    subtotal = models.IntegerField()
    status = models.SmallIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, null=True, on_delete=models.SET_NULL)
    address = models.ForeignKey(Address, null=True ,on_delete=models.SET_NULL)

    class Meta:
        db_table = 'order'

    def __str__(self):
        return self.order_num



class OrderItem(models.Model):
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    menuitem = models.ForeignKey(MenuItem, null=True ,on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orderitem'

    def __str__(self):
        return str(self.order) + ' | ' + str(self.menuitem) + ' | ' + str(self.quantity)
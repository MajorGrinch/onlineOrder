from django.forms import ModelForm
from mainpage.models import MenuItem, Restaurant

class MenuItemCreationForm(ModelForm):
    class Meta:
        model = MenuItem
        exclude = ['restaurant', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'


class MenuItemChangeForm(ModelForm):
    class Meta:
        model = MenuItem
        exclude = ['restaurant', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'


class RestaurantCreationForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'starting_price', 'delivering_fee', 'image', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['starting_price'].widget.attrs['class'] = 'form-control'
        self.fields['delivering_fee'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'


class RestaurantChangeForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'starting_price', 'delivering_fee', 'image', 'description']
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['starting_price'].widget.attrs['class'] = 'form-control'
        self.fields['delivering_fee'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
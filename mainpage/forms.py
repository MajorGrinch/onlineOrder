from django.forms import ModelForm
from .models import Address


class AddressCreationForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'is_default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['class'] = 'form-control'
        self.fields['street_address1'].widget.attrs['class'] = 'form-control'
        self.fields['street_address2'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'


class AddressChangeForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'is_default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['class'] = 'form-control'
        self.fields['street_address1'].widget.attrs['class'] = 'form-control'
        self.fields['street_address2'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
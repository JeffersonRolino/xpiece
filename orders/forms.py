from django import forms

from .models import Order


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'email']
        widgets = {'user': forms.HiddenInput()}

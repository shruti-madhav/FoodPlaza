from django import forms
from .models import Food,Customer

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

class CustForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

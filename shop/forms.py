# -*- coding: utf-8 -*-
from django import forms
from .models import Order


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, 
    	coerce=int, label="Кількість")
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)





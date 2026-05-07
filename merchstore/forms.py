from django import forms

from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'type',
            'image',
            'description',
            'price',
            'stock',
            'status',
        ]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount',]

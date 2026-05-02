from django import forms

from .models import *


class ItemForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'type',
            'description',
            'image',
            'price',
            'stock',
            'status',
        ]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount',]

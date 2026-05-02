from django import forms

from .models import *


class ItemForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'type',
            'image',
            'description',
            'price',
            'stock',
        ]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
        ]

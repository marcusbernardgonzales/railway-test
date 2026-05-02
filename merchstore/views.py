from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import *
from .forms import *


class ItemListView(ListView):
    model = Product
    template_name = 'merchstore/item_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Product.objects.all()
        return context


class ItemDetailView(DetailView, CreateView):
    model = Product
    form_class = TransactionForm
    template_name = 'merchstore/item_detail.html'
    context_object_name = 'product'


class ItemCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ItemForm
    template_name = 'merchstore/item_add.html'


class ItemUpdateView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ItemForm
    template_name = 'merchstore/item_update.html'


class CartView(ListView, LoginRequiredMixin):
    model = Transaction
    template_name = 'merchstore/cart.html'
    context_object_name = 'transaction'


class TransactionListView(ListView, LoginRequiredMixin):
    model = Transaction
    template_name = 'merchstore/transaction_list.html'
    context_object_name = 'transaction'
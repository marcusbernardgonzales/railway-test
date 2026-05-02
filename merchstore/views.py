from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Product


class ItemListView(ListView):
    model = Product
    template_name = 'merchstore/item_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Product.objects.all()
        return context


class ItemDetailView(DetailView):
    model = Product
    template_name = 'merchstore/item_detail.html'
    context_object_name = 'product'


class ItemCreateView(CreateView):
    model = Product
    template_name = 'merchstore/item_add.html'
    context_object_name = 'product'


class ItemUpdateView(UpdateView):
    model = Product
    template_name = 'merchstore/item_update.html'
    context_object_name = 'product'

class CartView(ListView):
    model = Transactions
    template_name = 'merchstore/cart.html'
    context_object_name = 'transaction'


class TransactionListView(ListView):
    model = TransactionListView
    template_name = 'merchstore/transaction_list.html'
    conext_object_name = 'transaction'

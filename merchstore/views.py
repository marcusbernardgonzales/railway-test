from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import *
from .models import *


class ProductListView(ListView):
    model = Product
    template_name = 'merchstore/item_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            created = Product.objects.filter(owner=profile)
            other = Product.exclude(owner=profile)

            context['created_products'] = created
            context['all_products'] = other

        else:
            context['all_products'] = Product.objects.all()

        return context


class ProductDetailView(DetailView, CreateView):
    model = Product
    form_class = TransactionForm
    template_name = 'merchstore/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        has_stock = product.amount >= 1

        is_owner = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            is_owner = product.owner.filter(id=profile.id).exists()
        
        context['is_owner'] = is_owner
        context['has_stock'] = has_stock

        return context


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ItemForm
    template_name = 'merchstore/item_add.html'


class ProductUpdateView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ItemForm
    template_name = 'merchstore/item_update.html'


class CartView(ListView, LoginRequiredMixin):
    model = Transaction
    template_name = 'merchstore/cart.html'
    context_object_name = 'transactions'


class TransactionListView(ListView, LoginRequiredMixin):
    model = Transaction
    template_name = 'merchstore/transaction_list.html'
    context_object_name = 'transactions'

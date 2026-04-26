from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

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

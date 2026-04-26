from django.urls import path

from .views import *

urlpatterns = [
    path('merchstore/items', ItemListView.as_view(),
         name='item_list'),
    path('merchstore/item/<int:pk>', ItemDetailView.as_view(),
         name='item_detail'),
    path('merchstore/item/<int:pk>/edit', ItemUpdateView.as_view(),
         name='item_update'),
    path('merchstore/item/add', ItemCreateView.as_view(),
         name='item_create'),
    path('merchstore/cart', CartView.as_view(),
         name='cart'),
    path('merchstore/transactions', TransactionDetailView.as_view(),
         name='transaction_detail'),
]

app_name = "merchstore"

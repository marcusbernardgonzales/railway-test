from django.urls import path

from .views import *

urlpatterns = [
    path('merchstore/items', ProductListView.as_view(), name='item_list'),
    path('merchstore/item/<int:pk>', ProductDetailView.as_view(),
         name='item_detail'),
    path('merchstore/item/<int:pk>/edit', ProductUpdateView.as_view(),
         name='item_update'),
    path('merchstore/item/add', ProductCreateView.as_view(),
         name='item_create'),
    path('merchstore/cart', CartView.as_view(), name='cart'),
    path('merchstore/transactions', TransactionListView.as_view(),
         name='transaction_list'),
]

app_name = "merchstore"

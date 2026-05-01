from django.urls import path

from .views import *

urlpatterns = [
    path('bookclub/books', BookListView.as_view(),
         name='book_list'),
    path('bookclub/book/<int:pk>', BookDetailView.as_view(),
         name='book_detail'),
    path('bookclub/book/add', BookCreateView.as_view(),
         name='book_add'),
    path('bookclub/book/<int:pk>/edit', BookUpdateView.as_view(),
         name='book_edit'),
    path('bookclub/book/<int:pk>/borrow', borrow_book, name='book_borrow'),
]

app_name = 'bookclub'

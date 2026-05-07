from django.contrib import admin

from .models import Genre, Book, BookReview, Bookmark, Borrow


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    list_display = ('name',)
    search_fields = ('name',)

    fieldsets = [
        ('Details', {
            'fields': [
                'name',
                'description',
            ]
        })
    ]


class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ('title', 'author', 'genre', 'publication_year',
                    'created_on', 'updated_on', 'available_to_borrow')
    list_filter = ('genre', 'publication_year')
    search_fields = ('title', 'author')

    fieldsets = [
        ('Details', {
            'fields': [
                'title',
                'author',
                'genre',
                'publication_year',
                'synopsis',
                'available_to_borrow',
                'contributer',
            ]
        }),
    ]


class BookReviewAdmin(admin.ModelAdmin):
    model = BookReview
    list_display = ('title', 'book')

    fieldsets = [
        ('Details', {
            'fields': [
                'book',
                'title',
                'comment',
                'user_reviewer',
                'anon_reviewer',
            ]
        })
    ]


class BookmarkAdmin(admin.ModelAdmin):
    model = Bookmark
    list_display = ('profile', 'book', 'date_bookmarked')

    fieldsets = [
        ('Details', {
            'fields': [
                'profile',
                'book',
                'date_bookmarked'
            ]
        })
    ]


class BorrowAdmin(admin.ModelAdmin):
    model = Borrow
    list_display = ('book', 'borrower', 'name',
                    'date_borrowed', 'date_to_return')

    fieldsets = [
        ('Details', {
            'fields': [
                'book',
                'borrower',
                'name',
                'date_borrowed',
                'date_to_return'
            ]
        })
    ]


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Borrow, BorrowAdmin)

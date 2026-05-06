from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [
        ProfileInLine,
    ]


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
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


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'type', 'price',)
    list_filter = ('type',)
    search_fields = ('name',)

    fieldsets = [
        ('Details', {
            'fields': [
                'name',
                'type',
                'image',
                'description',
                'price',
                'stock',
                'status',
            ]
        })
    ]


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('buyer', 'product', 'amount')
    list_filter = ('buyer', 'product')
    search_fields = ('buyer', 'product')

    fieldsets = [
        ('Details', {
            'fields': [
                'buyer',
                'product',
                'amount',
                'status',
            ]
        })
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)

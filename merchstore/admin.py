from django.contrib import admin

from .models import *


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
                'price',
                'description',
            ]
        })
    ]


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)

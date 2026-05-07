from django.contrib import admin

from .models import *


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
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


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('title', 'category', 'location', 'start_time', 'end_time',)
    list_filter = ('category',)
    search_fields = ('title', 'location',)

    fieldsets = [
        ('Details', {
            'fields': [
                'title',
                'category',
                'description',
                'location',
                'start_time',
                'end_time',
            ]
        })
    ]


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)

from django.contrib import admin

from .models import CommissionType, Commission, Job, JobApplication


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType
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


class JobInline(admin.TabularInline):
    model = Job
    extra = 1


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    list_display = ('title', 'type', 'maker', 'status', 'people_required', 'created_on', 'updated_on',)
    search_fields = ('title',)
    list_filter = ('created_on', 'status', 'type')

    inlines = [JobInline]

    fieldsets = [
        ('Details', {
            'fields': [
                'title',
                'description',
                'type',
                'maker',
                'people_required',
                'status',
            ]
        }),
    ]


class JobInline(admin.TabularInline):
    model = Job
    extra = 1


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job)
admin.site.register(JobApplication)

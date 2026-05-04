from django.contrib import admin

from .models import ProjectCategory, Project, Profile, ProjectRating, ProjectReview, Favorite


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
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


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('title', 'category', 'created_on',)
    list_filter = ('category',)
    search_fields = ('title',)
    fieldsets = [
        ('Details', {
            'fields': [
                'title',
                'category',
                'description',
                'materials',
                'steps',
            ]
        })
    ]

admin.site.register(Profile)
admin.site.register(ProjectRating)
admin.site.register(ProjectReview)
admin.site.register(Favorite)

admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)

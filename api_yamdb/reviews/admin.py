from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('slug',)
    list_display_links = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('slug',)
    list_display_links = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'year',
        'rating'
    )
    search_fields = ('name',)
    list_filter = ('category',)
    list_display_links = ('name',)
    filter_horizontal = ('genre',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)

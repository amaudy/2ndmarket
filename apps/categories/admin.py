from django.contrib import admin
from .models import MainCategory, SubCategory

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('display_order', 'name')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_category', 'slug', 'is_active', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('main_category', 'is_active')
    search_fields = ('name', 'main_category__name')
    ordering = ('main_category', 'display_order', 'name') 
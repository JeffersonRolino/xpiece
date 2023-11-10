from django.contrib import admin

from .models import Category, Format, Product, Screenshot


class FormatInline(admin.StackedInline):
    model = Format
    extra = 1


class ScreenshotInline(admin.StackedInline):
    model = Screenshot
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'created', 'updated', 'published']
    list_filter = ['created', 'updated']
    list_editable = ['price', 'published']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        FormatInline,
        ScreenshotInline,
    ]

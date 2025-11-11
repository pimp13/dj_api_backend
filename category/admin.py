from django.contrib import admin

from category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "created_at")
    prepopulated_fields = {"slug": ("title",)}

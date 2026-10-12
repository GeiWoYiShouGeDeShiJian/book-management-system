from django.contrib import admin
from .models import Book, Category, Author


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'isbn', 'available_copies', 'total_copies', 'status', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['title', 'isbn', 'author__name']
    date_hierarchy = 'created_at'
    list_editable = ['status']

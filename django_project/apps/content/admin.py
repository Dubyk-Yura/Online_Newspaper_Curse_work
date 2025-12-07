from django.contrib import admin
from .models import Publication, Category

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_breaking', 'created_at')
    list_filter = ('category', 'is_breaking')
    search_fields = ('title', 'content')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user  # Automatically sets the current logged-in user as author
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
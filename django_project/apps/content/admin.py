from django.contrib import admin
from .models import Publication, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def article_count(self, obj):
        return obj.publication_set.count()

    article_count.short_description = "Articles Count"


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'type_badge', 'created_at', 'is_breaking')

    list_filter = ('is_breaking', 'is_exclusive', 'category', 'created_at')

    search_fields = ('title', 'content')

    date_hierarchy = 'created_at'

    readonly_fields = ('created_at',)

    fieldsets = (
        ("Main Content", {
            "fields": ('title', 'content', 'category')
        }),
        ("Settings & Strategy", {
            "fields": ('type', 'is_exclusive', 'is_breaking', 'urgency_level'),
            "classes": ('collapse',),
        }),
        ("Meta Info", {
            "fields": ('author', 'created_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def type_badge(self, obj):
        from django.utils.html import format_html
        color = "red" if obj.is_breaking else "blue"
        return format_html('<span style="color: {};">{}</span>', color,
                           obj.get_type_display() if hasattr(obj, 'get_type_display') else obj.type)

    type_badge.short_description = "Type"
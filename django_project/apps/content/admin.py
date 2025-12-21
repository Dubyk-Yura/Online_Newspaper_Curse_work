from django.contrib import admin
from .models import Publication, Category, Comment, Rating


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')

    def article_count(self, obj):
        return obj.publication_set.count()

    article_count.short_description = "Articles Count"


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_category_slug', 'type_badge', 'created_at', 'is_breaking')
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

    def get_category_slug(self, obj):
        return obj.category.slug if obj.category else "-"

    get_category_slug.short_description = 'Category'
    get_category_slug.admin_order_field = 'category__slug'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def type_badge(self, obj):
        from django.utils.html import format_html
        color = "red" if obj.is_breaking else "blue"
        display_text = obj.get_type_display() if hasattr(obj, 'get_type_display') else obj.type
        return format_html('<span style="color: {};">{}</span>', color, display_text)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            field = super().formfield_for_foreignkey(db_field, request, **kwargs)
            field.label_from_instance = lambda obj: f"{obj.slug}"
            return field
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    type_badge.short_description = "Type"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'publication', 'short_text', 'created_at')
    search_fields = ('text', 'author__username', 'publication__title')
    list_filter = ('created_at',)

    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    short_text.short_description = "Comment"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('publication', 'user', 'value')
    list_filter = ('value',)

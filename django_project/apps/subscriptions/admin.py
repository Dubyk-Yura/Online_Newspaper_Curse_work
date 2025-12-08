from django.contrib import admin
from .models import UserSubscription, SubscriptionPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'duration_days')
    list_editable = ('base_price',)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'status_colored', 'expire_date', 'calculated_price')
    list_filter = ('type', 'is_active')
    search_fields = ('user__username', 'user__email')

    def status_colored(self, obj):
        from django.utils.html import format_html
        if obj.is_active:
            return format_html('<b style="color:green;">Active</b>')
        return format_html('<span style="color:gray;">Inactive</span>')

    status_colored.short_description = "Status"

    def calculated_price(self, obj):
        return f"{obj.calculate_final_price()} UAH"
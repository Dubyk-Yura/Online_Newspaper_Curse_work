from django.contrib import admin
from .models import UserSubscription, SubscriptionPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin configuration for setting up different tariff plans"""
    list_display = ('name', 'base_price', 'duration_days')


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    """Admin configuration for viewing active user subscriptions"""
    list_display = ('user', 'type', 'is_active', 'expire_date', 'calculated_price')
    list_filter = ('type', 'is_active')

    @admin.display(description='Final Price')
    def calculated_price(self, obj):
        return obj.calculate_final_price()

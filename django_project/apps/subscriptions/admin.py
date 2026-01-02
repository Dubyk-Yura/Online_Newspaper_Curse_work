from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import UserSubscription, SubscriptionPlan
from core.singleton import SystemConfig
from django.contrib import messages

@admin.action(description=_("Cancel selected subscriptions"))
def cancel_subscription(modeladmin, request, queryset):
    updated_count = queryset.update(is_active=False)

    modeladmin.message_user(
        request,
        f"{updated_count} subscriptions were successfully cancelled.",
        messages.SUCCESS
    )

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    # 'current_price_display' will show the calculated price in the list
    list_display = ('name', 'price_mode', 'value_formatted', 'current_price_display', 'duration_days', 'strategy_type')

    # Add 'preview_price' to the form as a read-only field
    readonly_fields = ('preview_price',)

    # Define the order of fields in the edit form
    fields = ('name', 'price_mode', 'value', 'preview_price', 'duration_days', 'strategy_type')

    @admin.display(description=_("Settings (Value)"))
    def value_formatted(self, obj):
        """Displays what is stored in DB (percentage or fixed value)."""
        if obj.price_mode == 'percentage':
            return f"{obj.value:.0f}%"
        return f"{obj.value:.2f} UAH"

    @admin.display(description=_("Current Real Price"))
    def current_price_display(self, obj):
        """Calculates and displays the final price based on the current Base Price."""
        price = obj.calculate_actual_price()
        return f"{price:.2f} UAH"

    @admin.display(description=_("Price Calculation Preview"))
    def preview_price(self, obj):
        """Shows the calculation formula in the edit form."""
        price = obj.calculate_actual_price()

        if obj.price_mode == 'fixed':
            return _("Fixed price: %(price)s UAH") % {'price': price}

        # If percentage, show the formula: Base * % = Total
        config = SystemConfig.get_instance()
        return _("Base Price (%(base)s UAH) * %(percent)s%% = %(total).2f UAH") % {
            'base': config.base_subscription_price,
            'percent': obj.value,
            'total': price
        }



@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'is_active', 'expire_date', 'calculated_price')
    list_filter = ('plan', 'is_active')

    actions = [cancel_subscription]

    @admin.display(description=_("Final Price"))
    def calculated_price(self, obj):
        return f"{obj.calculate_final_price():.2f} UAH"
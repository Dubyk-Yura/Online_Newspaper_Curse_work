from django.contrib import admin
from .models import GlobalSettings
from core.singleton import SystemConfig


@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the GlobalSettings model.
    Overrides methods to ensure only the Singleton instance is edited (pk=1).
    """
    list_display = ('base_subscription_price', 'maintenance_mode')

    def has_add_permission(self, request):
        """Disables 'Add' button if the Singleton record already exists."""
        return not GlobalSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Disables deleting the Singleton record."""
        return False
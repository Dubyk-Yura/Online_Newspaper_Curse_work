from django.core.exceptions import ImproperlyConfigured
from django.apps import apps
from decimal import Decimal
from typing import Any


def get_global_settings_model():
    """Load the GlobalSettings model from the 'config' app"""
    try:
        return apps.get_model('config', 'GlobalSettings')
    except LookupError:
        raise ImproperlyConfigured("GlobalSettings model must be defined in the 'config' app.")


class SystemConfig:
    """
    Guarantees a single in-memory configuration object synchronized with the DB
    """
    _instance = None

    base_price = Decimal(0.00)
    maintenance_mode = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SystemConfig, cls).__new__(cls)
            cls._instance.load_from_db()
        return cls._instance

    @classmethod
    def get_instance(cls):
        from config.models import GlobalSettings

        if cls._instance is None:
            obj, created = GlobalSettings.objects.get_or_create(pk=1)
            cls._instance = obj

        return cls._instance

    @classmethod
    def clear_cache(cls):
        cls._instance = None

    def load_from_db(self):
        SettingsModel = get_global_settings_model()
        try:
            settings = SettingsModel.objects.get(pk=1)
            self.base_price = settings.base_subscription_price
            self.maintenance_mode = settings.maintenance_mode
            print("[CONFIG] Singleton successfully loaded settings from database.")
        except SettingsModel.DoesNotExist:
            SettingsModel.objects.create(pk=1, base_subscription_price=100.00, maintenance_mode=False)
            self.base_price = Decimal(100.00)
            print("[CONFIG] Singleton initialized default settings (DB row was missing).")

    def update_settings(self, key: str, value: Any):
        if hasattr(self, key):
            setattr(self, key, value)

            SettingsModel = get_global_settings_model()
            settings = SettingsModel.objects.get(pk=1)

            if key == 'base_price':
                settings.base_subscription_price = value
            elif key == 'maintenance_mode':
                settings.maintenance_mode = value

            settings.save()
            print(f"[CONFIG] '{key}' updated and saved to DB.")
        else:
            print(f"[ERROR] Setting '{key}' not found.")
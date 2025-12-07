from django.db import models


class GlobalSettings(models.Model):
    """
    DB table to store global configuration settings.

    """
    base_subscription_price = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    maintenance_mode = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Overrides save to ensure only one record exists."""
        if not self.pk and GlobalSettings.objects.exists():
            raise Exception("There can be only one GlobalSettings instance.")
        return super(GlobalSettings, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Global System Setting (Singleton)"
        verbose_name_plural = "Global System Settings (Singleton)"
        # App label is 'config' by default due to its location
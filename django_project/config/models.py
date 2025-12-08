from django.db import models
from django.utils.translation import gettext_lazy as _

class GlobalSettings(models.Model):
    """
    DB table to store global configuration settings.

    """
    base_subscription_price = models.DecimalField(max_digits=6, decimal_places=2, default=100.00,
                                                  verbose_name=_('Base Subscription Price'))
    maintenance_mode = models.BooleanField(default=False, verbose_name=_('Maintenance Mode'))

    def save(self, *args, **kwargs):
        """Overrides save to ensure only one record exists."""
        if not self.pk and GlobalSettings.objects.exists():
            raise Exception("There can be only one GlobalSettings instance.")
        return super(GlobalSettings, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Global System Setting')
        verbose_name_plural = _('Global System Settings')

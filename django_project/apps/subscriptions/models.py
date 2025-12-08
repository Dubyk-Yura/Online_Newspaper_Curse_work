from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .strategies import StudentStrategy, CorporateStrategy, PremiumStrategy
from core.singleton import SystemConfig

class SubscriptionPlan(models.Model):
    """Model to store subscription tariff settings"""
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    base_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('Base Price'))
    duration_days = models.IntegerField(default=30, verbose_name=_('Duration (days)'))

    def __str__(self):
        return f"{self.name} ({self.base_price} UAH)"

    class Meta:
        verbose_name = _('Subscription Plan')
        verbose_name_plural = _('Subscription Plans')


class UserSubscription(models.Model):
    """
    Links a user to their current tariff type and handles price delegation.
    """
    STRATEGY_CHOICES = [
        ('student', _('Student')),
        ('corporate', _('Corporate')),
        ('premium', _('Premium')),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription', verbose_name=_('User'))
    type = models.CharField(max_length=20, choices=STRATEGY_CHOICES, default='premium', verbose_name=_('Type'))
    is_active = models.BooleanField(default=False, verbose_name=_('Is Active'))
    expire_date = models.DateField(null=True, blank=True, verbose_name=_('Expiration Date'))

    def get_strategy_object(self):
        if self.type == 'student':
            return StudentStrategy()
        elif self.type == 'corporate':
            return CorporateStrategy()
        return PremiumStrategy()

    def calculate_final_price(self):
        config = SystemConfig.get_instance()
        base_price = config.base_price

        strategy = self.get_strategy_object()
        return strategy.calculate_price(float(base_price))

    def check_access(self):
        return self.is_active and self.type in ['premium', 'corporate']

    def __str__(self):
        return f"Subscription of {self.user.username}: {self.type}"

    class Meta:
        verbose_name = _('User Subscription')
        verbose_name_plural = _('User Subscriptions')
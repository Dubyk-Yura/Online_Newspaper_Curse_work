from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .strategies import StudentStrategy, CorporateStrategy, PremiumStrategy
from core.singleton import SystemConfig
from decimal import Decimal


class SubscriptionPlan(models.Model):
    STRATEGY_CHOICES = [
        ('student', _('Student Logic')),
        ('corporate', _('Corporate Logic')),
        ('premium', _('Premium Logic')),
    ]

    PRICE_MODE_CHOICES = [
        ('fixed', _('Fixed Price (UAH)')),
        ('percentage', _('Percentage of Base')),
    ]

    name = models.CharField(max_length=50, verbose_name=_('Name'))

    price_mode = models.CharField(max_length=20, choices=PRICE_MODE_CHOICES, default='fixed',
                                  verbose_name=_('Pricing Mode'))
    value = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name=_('Value (Price or %)'))
    duration_days = models.IntegerField(default=30, verbose_name=_('Duration (days)'))
    strategy_type = models.CharField(max_length=20, choices=STRATEGY_CHOICES, default='premium',
                                     verbose_name=_('Strategy Type'))

    def calculate_actual_price(self):
        if self.price_mode == 'fixed':
            return self.value

        config = SystemConfig.get_instance()
        base_price = config.base_subscription_price
        return base_price * (self.value / Decimal(100))

    def __str__(self):
        return f"{self.name} (~{self.calculate_actual_price():.2f} UAH)"

    class Meta:
        verbose_name = _('Subscription Plan')
        verbose_name_plural = _('Subscription Plans')


class UserSubscription(models.Model):
    """
    Links a user to their current tariff type and handles price delegation.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription',
                                verbose_name=_('User'))

    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='subscriptions',
                             verbose_name=_('Selected Plan'))

    is_active = models.BooleanField(default=False, verbose_name=_('Is Active'))
    expire_date = models.DateField(null=True, blank=True, verbose_name=_('Expiration Date'))

    def get_strategy_object(self):
        if not self.plan:
            return PremiumStrategy()

        if self.plan.strategy_type == 'student':
            return StudentStrategy()
        elif self.plan.strategy_type == 'corporate':
            return CorporateStrategy()
        return PremiumStrategy()

    def calculate_final_price(self):
        if not self.plan:
            return 0.00

        base_price_from_plan = self.plan.calculate_actual_price()
        strategy = self.get_strategy_object()
        return strategy.calculate_price(float(base_price_from_plan))

    def check_access(self):
        if not self.is_active or not self.plan:
            return False
        return True

    def __str__(self):
        plan_name = self.plan.name if self.plan else "No Plan"
        return f"{self.user.username} - {plan_name}"

    class Meta:
        verbose_name = _('User Subscription')
        verbose_name_plural = _('User Subscriptions')
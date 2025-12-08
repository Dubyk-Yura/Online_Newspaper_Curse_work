from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'config'
    label = 'config'
    verbose_name = _('System Settings')
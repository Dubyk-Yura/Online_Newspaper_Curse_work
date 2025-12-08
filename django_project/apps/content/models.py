from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.interfaces import IPublication


class Category(models.Model):
    """Model for Rubrics/Categories (e.g., Politics, Sport)."""
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'content'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Publication(models.Model, IPublication):
    """
    Base model for all types of content.
    Implements IPublication interface, guaranteeing publish/archive methods.
    """
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Content'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='publications',
                               verbose_name=_('Author'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Category'))

    is_exclusive = models.BooleanField(default=False, verbose_name=_('Exclusive'))
    is_breaking = models.BooleanField(default=False, verbose_name=_('Breaking News'))
    urgency_level = models.IntegerField(default=0, verbose_name=_('Urgency Level'))
    type = models.CharField(max_length=20, default='article', verbose_name=_('Type'))

    def publish(self):
        """Implementation of the publish method."""
        print(f"Publicizing: {self.title}")
        self.save()

    def archive(self):
        """Implementation of the archive method."""
        pass

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'content'
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')

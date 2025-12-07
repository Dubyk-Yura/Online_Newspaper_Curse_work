from django.db import models
from django.conf import settings
from core.interfaces import IPublication


class Category(models.Model):
    """Model for Rubrics/Categories (e.g., Politics, Sport)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'content'
        verbose_name = 'Rubric'
        verbose_name_plural = 'Rubrics'


class Publication(models.Model, IPublication):
    """
    Base model for all types of content.
    Implements IPublication interface, guaranteeing publish/archive methods.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='publications')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    is_exclusive = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)
    urgency_level = models.IntegerField(default=0)
    type = models.CharField(max_length=20, default='article')

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
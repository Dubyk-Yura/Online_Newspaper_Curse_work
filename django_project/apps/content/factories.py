from abc import ABC, abstractmethod
from .models import Publication
from django.db import models

class Content(ABC):
    """Abstract Factory Interface"""
    @abstractmethod
    def create_publication(self, author: models.Model, **kwargs) -> Publication:
        pass


class ArticleFactory(Content):
    """Concrete Factory: Creates standard articles"""

    def create_publication(self, author: models.Model, **kwargs) -> Publication:
        kwargs.pop('is_breaking', None)

        return Publication.objects.create(
            author=author,
            type='article',
            is_breaking=False,
            **kwargs
        )


class BreakingNewsFactory(Content):
    """Concrete Factory: Creates Breaking News"""

    def create_publication(self, author: models.Model, **kwargs) -> Publication:
        kwargs.pop('is_breaking', None)

        return Publication.objects.create(
            author=author,
            type='breaking_news',
            is_breaking=True,
            urgency_level=kwargs.get('urgency_level', 5),
            **kwargs
        )
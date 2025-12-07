from abc import ABC, abstractmethod
from .models import Publication
from django.db import models

class Content(ABC):
    """Abstract Factory. Defines the contract for content creation"""
    @abstractmethod
    def create_publication(self, author: models.Model, title: str, content: str, **kwargs) -> Publication:
        pass

class ArticleFactory(Content):
    """Concrete Factory: Creates standard long-form articles"""
    def create_publication(self, author: models.Model, title: str, content: str, **kwargs) -> Publication:
        return Publication.objects.create(
            author=author,
            title=title,
            content=content,
            type='article',
            is_exclusive=kwargs.get('is_exclusive', False)
        )

class BreakingNewsFactory(Content):
    """Concrete Factory: Creates urgent, short-form breaking news items."""
    def create_publication(self, author: models.Model, title: str, content: str, **kwargs) -> Publication:
        # Note: Saving with is_breaking=True will trigger the Observer Signal
        return Publication.objects.create(
            author=author,
            title=title,
            content=content,
            type='breaking_news',
            is_breaking=True,
            urgency_level=kwargs.get('urgency_level', 5)
        )
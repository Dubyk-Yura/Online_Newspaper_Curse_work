from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from apps.users.models import User
from .services import NewsPublisher

@receiver(post_save, sender=apps.get_model('content', 'Publication'))
def notify_subscribers_on_breaking_news(sender, instance, created, **kwargs):
    """
    Django Signal that acts as the trigger for the Observer pattern.
    Activates when a new Publication object is created and is marked as 'Breaking News'
    """
    if created and instance.is_breaking:
        publisher = NewsPublisher.get_instance()

        subscribers = User.objects.filter(is_active=True)

        for user in subscribers:
            publisher.subscribe(user)

        publisher.notify_all(instance.title)
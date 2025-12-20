from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Publication
from apps.users.models import User

#Realization of OBSERVER
@receiver(post_save, sender=Publication)
def notify_subscribers(sender, instance, created, **kwargs):
    if instance.is_breaking:

        print(f"\n--- [OBSERVER TRIGGERED] ---")
        action_type = "Створено" if created else "Оновлено"
        print(f"Подія: {action_type} термінову новину: {instance.title}")

        if instance.is_exclusive:
            print("Тип новини: Premium. Розсилка тільки для підписників.")
            subscribers = User.objects.filter(subscription__is_active=True, email__isnull=False)
        else:
            print("Тип новини: Public. Розсилка для всіх користувачів.")
            subscribers = User.objects.filter(email__isnull=False)

        recipient_list = [user.email for user in subscribers if user.email]

        if recipient_list:
            print(f"Отримувачі ({len(recipient_list)}): {recipient_list}")

            prefix = "PREMIUM" if instance.is_exclusive else " BREAKING"
            subject = f"{prefix}: {instance.title}"

            message = (
                f"Вітаємо!\n\n"
                f"Важливе повідомлення:\n"
                f"{instance.title}\n\n"
                f"{instance.content[:200]}...\n\n"
                f"Читайте повну версію на сайті."
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
        else:
            print("Не знайдено користувачів з email для розсилки.")


@receiver(post_save, sender=Publication)
def notify_subscribers(sender, instance, created, **kwargs):
    if not created:
        return

    print(f"\n--- [OBSERVER] Нова публікація: {instance.title} ---")

    recipients = set()

    author_fans = instance.author.followers.filter(email__isnull=False)
    for fan in author_fans:
        print(f" -> Додано фаната автора: {fan.email}")
        recipients.add(fan.email)

    if instance.is_breaking:
        print(" -> Це Breaking News")
        if instance.is_exclusive:
            users = User.objects.filter(subscription__is_active=True, email__isnull=False)
        else:
            users = User.objects.filter(email__isnull=False)

        for u in users:
            recipients.add(u.email)

    if recipients:
        print(f"Відправка листів на: {recipients}")
        send_mail(
            subject=f"Нова стаття від {instance.author.username}: {instance.title}",
            message=f"Привіт!\nАвтор, на якого ви підписані або термінова новина:\n\n{instance.title}\n\n",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(recipients),
            fail_silently=False,
        )
    else:
        print("Немає кому відправляти.")
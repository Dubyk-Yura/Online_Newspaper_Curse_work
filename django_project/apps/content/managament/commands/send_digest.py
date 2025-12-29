from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta

from apps.content.models import Publication
from apps.users.models import User


class Command(BaseCommand):
    help = 'Відправляє щоденний дайджест новин користувачам'

    def handle(self, *args, **options):
        self.stdout.write("Починаємо формування дайджесту...")

        yesterday = timezone.now() - timedelta(days=1)

        daily_news = Publication.objects.filter(created_at__gte=yesterday).order_by('-is_breaking', '-created_at')

        if not daily_news.exists():
            self.stdout.write(self.style.WARNING("За останні 24 години новин не було. Дайджест не відправлено."))
            return

        count_news = daily_news.count()
        self.stdout.write(f"Знайдено {count_news} свіжих новин.")

        users = User.objects.filter(is_active=True).exclude(email='')

        if not users.exists():
            self.stdout.write(self.style.WARNING("Немає користувачів з email для відправки."))
            return

        sent_count = 0

        html_message = render_to_string('emails/digest.html', {
            'news_list': daily_news,
            'site_url': 'http://127.0.0.1:8000'
        })

        plain_message = f"Привіт! Ось {count_news} новин за сьогодні. Зайдіть на сайт, щоб прочитати."

        for user in users:
            try:
                subject = f"Щоденний дайджест новин | Online Newspaper"

                send_mail(
                    subject=subject,
                    message=plain_message,
                    html_message=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                sent_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Помилка відправки для {user.email}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Дайджест успішно відправлено {sent_count} користувачам!"))
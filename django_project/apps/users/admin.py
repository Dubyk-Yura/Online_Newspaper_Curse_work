from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.management import call_command
from django.contrib import messages
from .models import User
import io
import sys


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_editor', 'is_admin', 'is_active')
    list_filter = ('is_editor', 'is_admin', 'is_active')
    actions = ['send_digest_to_selected']

    fieldsets = UserAdmin.fieldsets + (
        ('Role Permissions', {'fields': ('is_editor', 'is_admin')}),
    )

    @admin.action(description="Надіслати дайджест обраним користувачам")
    def send_digest_to_selected(self, request, queryset):
        global output
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        try:
            call_command('send_digest')

            output = buffer.getvalue()

            self.message_user(request, f"Дайджест успішно відправлено! Перевірте консоль для деталей.",
                              messages.SUCCESS)

        except Exception as e:
            self.message_user(request, f"Помилка: {e}", messages.ERROR)

        finally:
            sys.stdout = old_stdout
            print(output)

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from core.interfaces import IObserver


class User(AbstractUser, IObserver):
    """
    Base User model, extended from Django's AbstractUser.
    Implements the IObserver interface.

    NOTE: M2M fields (groups, user_permissions) are explicitly defined 
    to resolve conflicts in modular architectures (using 'through')
    """
    is_editor = models.BooleanField(default=False, verbose_name="Editor")
    is_admin = models.BooleanField(default=False, verbose_name="Administrator")

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to.'),
        related_name="user_groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="user_permissions",
    )

    def update(self, message: str):
        """Implementation of the IObserver update method."""
        print(f"[Notification to {self.username}]: {message}")

    class Meta:
        app_label = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

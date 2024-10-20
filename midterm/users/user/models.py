import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), is_active=True, username=username)
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(
            email=email,
            password=password,
            username=username
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def active(self):
        return self.filter(is_active=True)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['email']),
        ]

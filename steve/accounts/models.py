from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

from core.base import BaseModel


class UserManager(BaseUserManager):
    @transaction.atomic
    def create(self, **fields):
        password = fields.pop("password", None)
        user = super().create(**fields)

        if password is not None:
            user.set_password(password)
            user.save()

        return user

    def create_superuser(self, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)

        return self.create_user(**fields)


class User(BaseModel, AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(unique=True, verbose_name="email address")
    password = models.CharField(max_length=128, verbose_name="password")

    objects = UserManager()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(*args, **kwargs)

    def restore(self, *args, **kwargs):
        self.is_active = True
        self.save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, first_name, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    is_verify = models.BooleanField(default=False)
    objects = CustomUserManager()
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )

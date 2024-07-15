from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model.
    """
    def create_user(self, username, email, password, first_name, **extra_fields):
        """
        Create and save a regular user with the given username, email, password, and first name.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        if not first_name:
            raise ValueError('The given first name must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password, first_name, last_name):
        """
        Create and save a superuser with the given username, email, password, first name, and last name.
        """
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
    """
    Custom user model extending Django's AbstractUser with an additional is_verify field.
    """
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

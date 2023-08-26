"""
Django custom user model
"""
import os
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, mobile, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        if not mobile:
            raise ValueError("User must have a valid mobile number.")
        user = self.model(
            email=self.normalize_email(email), mobile=mobile, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, mobile, password, **extra_fields):
        """Create and return a new superuser."""
        user = self.create_user(email, mobile, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model for register the user on the site for different purposes
    """

    name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'(0|91)?[6-9][0-9]{9}', message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "mobile"

    REQUIRED_FIELDS = ["email","name"]

    def __str__(self):
        return self.mobile

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



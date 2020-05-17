import uuid
from django.utils import timezone
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email,  password=None, first_name=None, last_name=None, username=None,  **extra_fields):
        """ Creating and saving new user """
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            """ Generating random unique username if not given """
            username = uuid.uuid4().hex[:12].upper()

        if not first_name:
            first_name = 'No'

        if not last_name:
            last_name = 'Name'

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None,  **extra_fields):
        """ Create and saves a new superuser """

        user = self.create_user(
            email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that support email instent of username """
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    joined_date = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_username(self):
        """ it will return unique string """
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def send_email(self, subject, message, from_email=None, silentError=None, **kwargs):
        """Send an email to this user."""

        if not silentError:
            silentError = True

        send_mail(subject, message, from_email, [
                  self.email], fail_silently=silentError, **kwargs)

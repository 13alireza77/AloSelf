from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^(\+98|0)?9\d{9}$', message="Phone number must enter in this format")
    ida_regex = RegexValidator(regex=r'[0-9]{8}', message="ida must enter in this format")
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=False)
    ida = models.CharField(validators=[ida_regex], max_length=8, unique=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    full_name = models.CharField(_('full name'), max_length=130, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', ]  # Email & Password are required by default.

    def __str__(self):
        return self.phone


class Profile(models.Model):
    profile = models.ImageField()
    student_card = models.ImageField()
    points = models.PositiveIntegerField(default=0)
    gender = models.BinaryField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    verified = models.BooleanField(default=False)
    slug = models.SlugField(blank=False)

    def __str__(self):
        return self.user.full_name

import re

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField

from apps.models.BaseModel import UUIDBaseModel


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("The phone number must be set")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)

class User(AbstractUser, UUIDBaseModel):
    class RoleType(TextChoices):
        SPECIALIST = 'specialist', 'Specialist'
        ADMIN = 'admin', 'Admin'
        CLIENT = 'client', 'Client'

    phone_number = CharField(max_length=15, unique=True)
    role = CharField(max_length=50, choices=RoleType.choices)
    avatar = ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    username = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def check_phone(self):
            pattern = re.compile(r'^(?:\+?998[\s-]*)?(\d{2})[\s-]*(\d{3})[\s-]*(\d{2,4})(?:[\s-]*(\d{2}))?$')
            m = pattern.match(self.phone)
            if not m:
                raise ValueError(f"Invalid UZ number: {self.phone}")
            return "".join(g for g in m.groups() if g)

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        if self.phone:
            self.phone = self.check_phone()
        super().full_clean(exclude, validate_unique, validate_constraints)

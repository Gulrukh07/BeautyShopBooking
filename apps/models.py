import re

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, CASCADE, ForeignKey, JSONField
from django.db.models import Model
from django.db.models.enums import TextChoices
from django.db.models.fields import (CharField, BigIntegerField, BooleanField,
                                     TimeField, DateField, DecimalField)
from django.db.models.fields import DateTimeField
from django_ckeditor_5.fields import CKEditor5Field


class CreatedBaseModel(Model):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


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


class User(AbstractUser, CreatedBaseModel):
    class RoleType(TextChoices):
        SPECIALIST = 'specialist', 'Specialist'
        ADMIN = 'admin', 'Admin'
        CLIENT = 'client', 'Client'

    phone_number = CharField(
        max_length=15,
        unique=True,
        error_messages={
            'unique': 'User with this phone number already exists.',
        }
    )
    role = CharField(max_length=50, choices=RoleType.choices)
    avatar = ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    unhashed_password = CharField(null=True, blank=True)

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

class Business(CreatedBaseModel):
    class Type(TextChoices):
        CLINIC = 'clinic', 'Clinic'
        BARBERSHOP = 'barbershop', 'Barber Shop'
        BEAUTYSHOP = 'beautyshop', 'Beauty Shop'
        SPORT = 'sport', 'Sport'

    name = CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True)
    type = CharField(max_length=50, choices=Type)
    address = CharField(max_length=255)
    latitude = DecimalField(max_digits=50, decimal_places=15, blank=True, null=True)
    longitude = DecimalField(max_digits=50, decimal_places=15, blank=True, null=True)
    contact = CharField(max_length=255, blank=True, null=True)
    opening_hours = JSONField(blank=True, null=True)
    is_active = BooleanField(default=False)

    def __str__(self):
        return self.name

class Service(CreatedBaseModel):
    name = CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True)
    business_id = ForeignKey(Business, related_name='services', on_delete=CASCADE)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.name

class SubService(CreatedBaseModel):
    name = CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True)
    service_id = ForeignKey(Service, related_name='sub_services', on_delete=CASCADE)
    specialist_id = ForeignKey(User, related_name='sub_services', on_delete=CASCADE)

    def __str__(self):
        return self.name


class ServiceBySpecialist(CreatedBaseModel):
    specialist_id = ForeignKey(User, related_name='specialist_services', on_delete=CASCADE)
    sub_service_id = ForeignKey(SubService, related_name='specialist_services', on_delete=CASCADE)
    price = BigIntegerField()
    duration = BigIntegerField()

    def __str__(self):
        return f"{self.specialist_id} - {self.sub_service_id}"


class BusinessWorker(CreatedBaseModel):
    specialist_id = ForeignKey(User, related_name='business_workers', on_delete=CASCADE)
    service_id = ForeignKey(Service, related_name='business_workers', on_delete=CASCADE)
    position = CharField(max_length=255)
    bio = CKEditor5Field(blank=True, null=True)
    years_of_experience = BigIntegerField(default=0)
    is_active = BooleanField(default=True)

    def __str__(self):
        return f"{self.specialist_id} - {self.position}"


class Appointment(CreatedBaseModel):
    class Status(TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELED = 'canceled', 'Canceled'
        MOVED = 'moved', 'Moved'

    specialist_id = ForeignKey(User, related_name='appointments_as_specialist', on_delete=CASCADE)
    client_id = ForeignKey(User, related_name='appointments_as_client', on_delete=CASCADE)
    service_id = ForeignKey(Service, related_name='appointments', on_delete=CASCADE)
    status = CharField(max_length=20, choices=Status, default=Status.PENDING)

    def __str__(self):
        return f"Appointment {self.id} - {self.status}"


class Review(CreatedBaseModel):
    class Rating(TextChoices):
        ONE = "1", "1"
        TWO = "2", "2"
        THREE = "3", "3"
        FOUR = "4", "4"
        FIVE = "5", "5"
    appointment_id = ForeignKey(Appointment, related_name='reviews', on_delete=CASCADE)
    client_id = ForeignKey(User, related_name='reviews', on_delete=CASCADE)
    rating = CharField(max_length=20, choices=Rating.choices, default=Rating.FIVE)
    comment = CKEditor5Field(blank=True, null=True)

    def __str__(self):
        return f"Review by {self.client_id}"


class Notification(CreatedBaseModel):
    class Status(TextChoices):
        BOOKING = 'booking', 'Booking'
        REMINDER = 'reminder', 'Reminder'
        CANCELLED = 'cancelled', 'Cancelled'

    user_id = ForeignKey(User, related_name='notifications', on_delete=CASCADE)
    message = CKEditor5Field()
    type = CharField(max_length=50, choices=Status)
    is_read = BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user_id}"


class WorkSchedule(CreatedBaseModel):
    specialist_id = ForeignKey(User, related_name='work_schedules', on_delete=CASCADE)
    start_time = TimeField()
    end_time = TimeField()
    is_active = BooleanField(default=True)

    def __str__(self):
        return f"{self.specialist_id} - {self.start_time} to {self.end_time}"


class TimeOff(CreatedBaseModel):
    specialist_id = ForeignKey(User, related_name='time_offs', on_delete=CASCADE)
    work_schedule_id = ForeignKey(WorkSchedule, related_name='time_offs', on_delete=CASCADE)
    date = DateField()
    reason = CKEditor5Field(blank=True, null=True)

    def __str__(self):
        return f"Time off {self.specialist_id} - {self.date}"

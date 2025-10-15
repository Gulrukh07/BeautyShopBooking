from django.db.models import IntegerField, ForeignKey, CASCADE
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, DecimalField, DateField, TimeField, BooleanField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.BaseModel import CreatedBaseModel


class Service(CreatedBaseModel):
    name = CharField(max_length=255)
    description = CKEditor5Field(null=True, blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    duration = IntegerField()


class Appointment(CreatedBaseModel):
    class StatusType(TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
    service = ForeignKey('Service', related_name="appointments", on_delete=CASCADE)
    specialist_id = ForeignKey('apps.User', related_name="appointments", on_delete=CASCADE)
    client_id = ForeignKey('apps.User', related_name="appointments", on_delete=CASCADE)
    date = DateField()
    time = TimeField()
    status = CharField(max_length=50, choices=StatusType.choices, default=StatusType.PENDING)


class WorkSchedule(CreatedBaseModel):
    class Weekdays(TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'
    specialist_id = ForeignKey('apps.User', related_name="work_schedules", on_delete=CASCADE)
    week_day = CharField(max_length=50, choices=Weekdays.choices)
    start_time = TimeField()
    end_time = TimeField()

class Notification(CreatedBaseModel):
    message = CKEditor5Field(null=True, blank=True)
    is_read = BooleanField(default=False)
    user_id = ForeignKey('apps.User', on_delete=CASCADE)


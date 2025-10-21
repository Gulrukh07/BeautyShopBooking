from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.models import User, Business, Appointment, Service, SubService, Review, Notification
from apps.permissions import IsAdminUser
from apps.serializers import UserModelSerializer, BusinessModelSerializer, AppointmentModelSerializer, \
    ServiceModelSerializer, SubServiceModelSerializer, NotificationModelSerializer, ReviewModelSerializer


# Create your views here.

@extend_schema(tags=['Users'])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Business'])
class BusinessViewSet(ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessModelSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Appointments'])
class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentModelSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Services'])
class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceModelSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['SubServices'])
class SubServiceViewSet(ModelViewSet):
    queryset = SubService.objects.all()
    serializer_class = SubServiceModelSerializer
    # permission_classes = [IsAdminUser]


@extend_schema(tags=['Reviews'])
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Notifications'])
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationModelSerializer
    # permission_classes = [IsAdminUser]
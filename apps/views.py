from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.models import User, Business, Appointment, Service, SubService
from apps.serializers import UserModelSerializer, BusinessModelSerializer, AppointmentModelSerializer, \
    ServiceModelSerializer, SubServiceModelSerializer


# Create your views here.

@extend_schema(tags=['Users'])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # permission_classes = [IsAuthenticated, AdminPermission]

@extend_schema(tags=['Business'])
class BusinessViewSet(ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessModelSerializer
    # permission_classes = [IsAuthenticated, AdminPermission]

@extend_schema(tags=['Appointments'])
class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentModelSerializer
    # permission_classes = [IsAuthenticated, AdminPermission]

@extend_schema(tags=['Services'])
class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceModelSerializer
    # permission_classes = [IsAuthenticated, AdminPermission]

@extend_schema(tags=['SubServices'])
class SubServiceViewSet(ModelViewSet):
    queryset = SubService.objects.all()
    serializer_class = SubServiceModelSerializer
    # permission_classes = [IsAuthenticated, AdminPermission]

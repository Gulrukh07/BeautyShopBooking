from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from apps.models import User, Business, Appointment, Service, SubService, Review, Notification
from apps.serializers import UserModelSerializer, BusinessModelSerializer, AppointmentModelSerializer, \
    ServiceModelSerializer, SubServiceModelSerializer, NotificationModelSerializer, ReviewModelSerializer


# Create your views here.

@extend_schema(tags=['Users'])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ('role',)
    # permission_classes = [IsAdminUser]
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering_fields = ('id', 'created_at')
    ordering = ['-created_at']

@extend_schema(tags=['Business'])
class BusinessViewSet(ModelViewSet):
    queryset = Business.objects.all()
    filter_backends = (DjangoFilterBackend,SearchFilter, OrderingFilter)
    serializer_class = BusinessModelSerializer
    filterset_fields = ('type',)
    search_fields = ['name', 'description', 'type']
    ordering_fields = ('id', 'created_at')
    ordering = ['-created_at']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Appointments'])
class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('status',)
    ordering_fields = ('id', 'created_at')
    ordering = ['-created_at']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Services'])
class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['name', 'description']
    ordering_fields = ('id', 'created_at')
    ordering = ['-created_at']
    # permission_classes = [IsAdminUser]


@extend_schema(tags=['SubServices'])
class SubServiceViewSet(ModelViewSet):
    queryset = SubService.objects.all()
    serializer_class = SubServiceModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ('id', 'created_at')
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Reviews'])
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    # permission_classes = [IsAdminUser]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ('id', 'created_at')
    ordering = ['-created_at']
    search_fields = ['comment', 'client_first_name', 'client_last_name']

@extend_schema(tags=['Notifications'])
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    ordering_fields = ('id', 'created_at')
    ordering = ['-created_at']
    filterset_fields = ('type',)
    # permission_classes = [IsAdminUser]
    search_fields = ['message', 'user_first_name', 'user_last_name', 'type']
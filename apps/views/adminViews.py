from django.db.models.aggregates import Count
from django.db.models.functions import TruncDate
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import User, Business, Appointment, Service, SubService, Review, Notification
from apps.serializers import UserModelSerializer, BusinessModelSerializer, AppointmentModelSerializer, \
    ServiceModelSerializer, SubServiceModelSerializer, NotificationModelSerializer, ReviewModelSerializer, \
    AppointmentStatsSerializer, TopServicesSerializer


# Create your views here.

@extend_schema(tags=['Users'])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ('role',)
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering_fields = ('created_at',)
    ordering = ['created_at']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Business'])
class BusinessViewSet(ModelViewSet):
    queryset = Business.objects.all()
    filter_backends = (DjangoFilterBackend,SearchFilter, OrderingFilter)
    serializer_class = BusinessModelSerializer
    filterset_fields = ('type',)
    search_fields = ['name', 'description', 'type']
    ordering_fields = ('created_at',)
    ordering = ['created_at']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Appointments'])
class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('status',)
    ordering_fields = ('created_at',)
    ordering = ['created_at']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Services'])
class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('is_active',)
    search_fields = ['name', 'description']
    ordering_fields = ('created_at',)
    ordering = ['created_at']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['SubServices'])
class SubServiceViewSet(ModelViewSet):
    queryset = SubService.objects.all()
    serializer_class = SubServiceModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ('created_at',)
    search_fields = ['name', 'description']
    ordering = ['created_at']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Reviews'])
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ('created_at',)
    ordering = ['created_at']
    search_fields = ['comment', 'client_first_name', 'client_last_name']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Notifications'])
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    ordering_fields = ('created_at',)
    ordering = ['created_at']
    filterset_fields = ('type',)
    search_fields = ['message', 'user_first_name', 'user_last_name', 'type']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['Statistics'], request=AppointmentStatsSerializer)
class AppointmentStatisticView(APIView):
    def post(self, request):
        serializer = AppointmentStatsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        start = data['start']
        end = data['end'] if 'end' in data else None
        if start and not end:
            appointments = Appointment.objects.filter(created_at__date=start)

            statistics = (
                appointments
                .annotate(day=TruncDate('created_at'))
                .values('day')
                .annotate(total=Count('id'))
                .order_by('day')
            )

            return Response({
                'start': start,
                'statistics': statistics
            })

        if start and end:
            total_appointments = Appointment.objects.filter(
                created_at__date__gte=start,
                created_at__date__lte=end
            ).count()

            return Response({
                'start': start,
                'end': end,
                'total': total_appointments
            })

        return Response(
            {'error': 'Invalid input'},
            status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Statistics'],
               responses={200: TopServicesSerializer(many=True)})
class TopServicesView(APIView):

    def get(self, request):
        top_services = (
            Appointment.objects
            .values('service_id', 'service_id__name')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        return Response(top_services)
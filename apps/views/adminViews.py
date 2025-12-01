from datetime import datetime, timedelta

from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import User, Business, Appointment, Service, BusinessWorker
from apps.serializers import UserModelSerializer, BusinessModelSerializer, AppointmentModelSerializer, \
    ServiceModelSerializer, TopServicesSerializer, AppointmentStatsSerializer, CustomTokenObtainPairSerializer, \
    BusinessWorkerModelSerializer, TopClientSerializer


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
    queryset = Business.objects.all().prefetch_related('services')
    filter_backends = (DjangoFilterBackend,SearchFilter, OrderingFilter )
    serializer_class = BusinessModelSerializer
    filterset_fields = ('type', 'is_active')
    search_fields = ['name', 'description', 'type']
    ordering_fields = ('created_at',)
    ordering = ['created_at']
    # permission_classes = [IsAdminUser]

@extend_schema(tags=['BusinessWorkers'])
class BusinessWorkerViewSet(ModelViewSet):
    queryset = BusinessWorker.objects.all()
    serializer_class = BusinessWorkerModelSerializer

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

@extend_schema(tags=['Statistics'], responses=AppointmentStatsSerializer)
class AppointmentStatisticView(APIView):
    def get(self, request):
        start_str = request.query_params.get('start')
        end_str = request.query_params.get('end')

        if not start_str:
            return Response({'error': 'Start date is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start = datetime.strptime(start_str, "%Y-%m-%d")
            if end_str:
                end = datetime.strptime(end_str, "%Y-%m-%d") + timedelta(days=1) - timedelta(microseconds=1)
            else:
                end = start + timedelta(days=1) - timedelta(microseconds=1)
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        appointments = Appointment.objects.filter(created_at__gte=start, created_at__lte=end)

        statistics = (
            appointments
            .values('service_id', 'service_id__name')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        results = [
            {
                'service_id': stat['service_id'],
                'service_name': stat['service_id__name'],
                'total_appointments': stat['total']
            }
            for stat in statistics
        ]

        return (Response(
            {
                'start': start_str,
                'end': end_str,
                'statistics': results
            },
            status=status.HTTP_200_OK
        ))
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

@extend_schema(tags=["Users",], responses={200: UserModelSerializer})
class GetMe(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        serializer = UserModelSerializer(user)
        return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# class CustomTokenRefreshView(TokenRefreshView):
#     serializer_class = CustomTokenRefreshSerializer

@extend_schema(
    tags=["Statistics"],
    responses={200: TopClientSerializer(many=True)}
)
class TopClientsView(APIView):

    def get(self, request):
        top_clients = (
            Appointment.objects
            .values('client_id', 'client_id__first_name' , 'client_id__last_name')
            .annotate(total_appointments=Count('id'))
            .order_by('-total_appointments')[:10]
        )

        results = [
            {
                'client_id': client['client_id'],
                "client_name": f"{client['client_id__first_name']} {client['client_id__last_name']}".strip(),
                'total_appointments': client['total_appointments']
            }
            for client in top_clients
        ]

        return Response(results)
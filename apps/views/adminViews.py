from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import User, Business, Appointment, Service, BusinessWorker
from apps.serializers import UserModelSerializer, BusinessModelSerializer, AppointmentModelSerializer, \
    ServiceModelSerializer, CustomTokenObtainPairSerializer, \
    BusinessWorkerModelSerializer, UserUpdateSerializer


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

@extend_schema(tags=["Users",], responses={200: UserModelSerializer})
class GetMe(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        serializer = UserModelSerializer(user)
        return Response(serializer.data)

# @extend_schema(tags=['Users'])
class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# class CustomTokenRefreshView(TokenRefreshView):
#     serializer_class = CustomTokenRefreshSerializer

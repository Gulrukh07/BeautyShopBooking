from datetime import datetime, timedelta

from django.db.models.aggregates import Count
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Appointment
from apps.serializers import TopServicesSerializer, AppointmentStatsSerializer, TopClientSerializer, \
    TopSpecialistSerializer


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
@extend_schema(
    tags=["Statistics"],
    responses={200: TopSpecialistSerializer(many=True)}
)
class TopSpecialistView(APIView):

    def get(self, request):
        top_specialists = (
            Appointment.objects
            .values('specialist_id', 'specialist_id__first_name' , 'specialist_id__last_name')
            .annotate(total_appointments=Count('id'))
            .order_by('-total_appointments')[:10]
        )

        results = [
            {
                'specialist_id': specialist['specialist_id'],
                "specialist_name": f"{specialist['specialist_id__first_name']} {specialist['specialist_id__last_name']}".strip(),
                'total_appointments': specialist['total_appointments']
            }
            for specialist in top_specialists
        ]

        return Response(results)

@extend_schema(tags=["Statistics"],)
class TopBusinessesView(APIView):

    def get(self, request):
        top_businesses = (
            Appointment.objects
            .values('service_id__business_id', 'service_id__business_id__name')
            .annotate(total_appointments=Count('id'))
            .order_by('-total_appointments')[:10]
        )

        results = [
            {
                'business_id': business['service_id__business_id'],
                "business_name": business['service_id__business_id__name'].strip(),
                'total_appointments': business['total_appointments']
            }
            for business in top_businesses
        ]

        return Response(results)

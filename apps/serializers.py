import re

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (ModelSerializer, CharField, Serializer,
                                        DateField, IntegerField, SerializerMethodField)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import User, Business, Appointment, Service, SubService, BusinessWorker


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields  = ('id', 'first_name', 'last_name', 'phone_number', 'role', 'avatar',
                   'created_at', 'password', 'unhashed_password')
        read_only_fields = 'created_at', 'updated_at', 'date_joined', 'unhashed_password'

    def validate_phone_number(self, value):
        phone = re.sub('\D', '', value)
        pattern = r'^998(90|91|93|94|95|97|98|99|33|88|50|77)\d{7}$'

        if not re.match(pattern, phone ):
            raise ValidationError ('Phone number must be in this format: +998XXXXXXXXX')

        queryset = User.objects.filter(phone_number=phone )
        if queryset.exists():
            raise ValidationError('User with this phone number already exists.')
        return f"+{phone}"

    def validate_password(self, value):
        if len(value) < 4:
            raise ValidationError('Password must be at least 4 characters long.')
        if len(value) > 20:
            raise ValidationError('Password must be at most 20 characters long.')
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError('Password must contain at least one letter.')

        return value

    def validate_avatar(self, value):
        if value and not value.name.lower().endswith(('.jpg', 'jpeg', 'png')):
            raise ValidationError('Avatar must be an image.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.unhashed_password = password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class BusinessModelSerializer(ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'
        read_only_fields = 'created_at', 'updated_at'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['services'] = ServiceModelSerializer(instance.services.all(),many=True).data
        return data

class SpecialistModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "phone_number", "avatar"]

class BusinessWorkerSerializer(ModelSerializer):
    specialist = SpecialistModelSerializer(source='specialist_id', read_only=True)

    class Meta:
        model = BusinessWorker
        fields = ["id", "specialist", "position", "bio", "years_of_experience"]
        read_only_fields = ['created_at', 'updated_at']

class AppointmentModelSerializer(ModelSerializer):
    specialist_name = SerializerMethodField()
    client_name = SerializerMethodField()
    service_name = SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'created_at', 'updated_at', 'status',
            'specialist_id', 'client_id', 'service_id',
            'specialist_name', 'client_name', 'service_name'
        ]
        read_only_fields = ('created_at', 'updated_at')

    def get_specialist_name(self, obj):
        if obj.specialist_id:
            return f"{obj.specialist_id.first_name} {obj.specialist_id.last_name}"
        return None

    def get_client_name(self, obj):
        if obj.client_id:
            return f"{obj.client_id.first_name} {obj.client_id.last_name}"
        return None

    def get_service_name(self, obj):
        if obj.service_id:
            return obj.service_id.name
        return None

class ServiceModelSerializer(ModelSerializer):
    business_title = CharField(source='business_id.name', read_only=True)
    specialists = SerializerMethodField()
    appointments = SerializerMethodField()

    class Meta:
            model = Service
            fields = '__all__'

    def get_specialists(self, obj):
        specialists = BusinessWorker.objects.filter(service_id_id = obj, is_active = True,
                                                    specialist_id__role = User.RoleType.SPECIALIST)
        return BusinessWorkerSerializer(specialists, many=True).data
    def get_appointments(self, obj):
        appointments = Appointment.objects.filter(service_id_id = obj)
        return AppointmentModelSerializer(appointments, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sub services'] = SubServiceModelSerializer(instance.sub_services, many=True).data
        return data

class SubServiceModelSerializer(ModelSerializer):
    class Meta:
        model = SubService
        fields = '__all__'

class AppointmentStatsSerializer(Serializer):
    start = DateField(required=True)
    end = DateField(required=False)

    def validate(self, data):
        start = data.get('start')
        end = data.get('end')

        if end and end < start:
            raise ValidationError('End date must be greater than or equal to start date.')

        return data

class TopServicesSerializer(Serializer):
    service_id = IntegerField()
    service_name = CharField()
    total = IntegerField()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        return {"status_code": status.HTTP_200_OK, "data": data,
                "message": "Successfully authenticated",
                }
class BusinessWorkerModelSerializer(ModelSerializer):
    class Meta:
        model = BusinessWorker
        fields = '__all__'
        read_only_fields = 'created_at', 'updated_at'

    def validate_specialist_id(self, specialist_id):
        if specialist_id is None:
            raise ValidationError('Specialist_id is required')
        if specialist_id.role != User.RoleType.SPECIALIST:
            raise ValidationError('Specialist with given id is not found')
        return specialist_id

# class CustomTokenRefreshSerializer(TokenRefreshSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#
#         return {
#             "status_code": status.HTTP_200_OK,
#             "message": "Token refreshed successfully",
#             # "access": data.get("access"),
#             # "refresh": attrs.get("refresh")
#         }

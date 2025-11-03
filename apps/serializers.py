import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField

from apps.models import User, Business, Appointment, Service, SubService, Notification


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields  = '__all__'
        read_only_fields = 'created_at', 'updated_at', 'date_joined'

    def validate_phone_number(self, value):
        phone = re.sub('\D', '', value)
        pattern = r'^998(90|91|93|94|95|97|98|99|33|88|50|77)\d{7}$'

        if not re.match(pattern, phone):
            raise ValidationError ('Phone number must be in this format: +998XXXXXXXXX')

        queryset = User.objects.filter(phone_number=phone)
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
        user.set_password(password)
        user.save()
        return user

class BusinessModelSerializer(ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'
        read_only_fields = 'created_at', 'updated_at'


class AppointmentModelSerializer(ModelSerializer):
    specialist_name = CharField(source='specialist.first_name', read_only=True)
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = 'created_at', 'updated_at'

class ServiceModelSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sub services'] = SubServiceModelSerializer(instance.sub_services, many=True).data
        return data

class SubServiceModelSerializer(ModelSerializer):
    class Meta:
        model = SubService
        fields = '__all__'

class ReviewModelSerializer(ModelSerializer):
    class Meta:
        model = SubService
        fields = '__all__'

class NotificationModelSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
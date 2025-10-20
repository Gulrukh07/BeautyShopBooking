from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView

from apps.models import User
from apps.serializers import UserModelSerializer


# Create your views here.
@extend_schema(request=UserModelSerializer, responses={201: UserModelSerializer})
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
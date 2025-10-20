from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from apps.models import User
from apps.serializers import UserModelSerializer


# Create your views here.
@extend_schema(request=UserModelSerializer, responses={201: UserModelSerializer})
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


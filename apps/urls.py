from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import AppointmentViewSet, ServiceViewSet, SubServiceViewSet, UserViewSet, BusinessViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('business', BusinessViewSet)
router.register('appointments', AppointmentViewSet),
router.register('services', ServiceViewSet),
router.register('subservices', SubServiceViewSet)

urlpatterns = [
    path('admin/', include(router.urls)),
]

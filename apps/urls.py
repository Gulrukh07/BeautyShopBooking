from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views.adminViews import AppointmentViewSet, ServiceViewSet, SubServiceViewSet, UserViewSet, BusinessViewSet, \
    NotificationViewSet, ReviewViewSet, AppointmentStatisticView, TopServicesView

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('business', BusinessViewSet)
router.register('appointments', AppointmentViewSet),
router.register('services', ServiceViewSet),
router.register('subservices', SubServiceViewSet)
router.register('notifications', NotificationViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('admin/', include(router.urls)),
    path('statistics/', AppointmentStatisticView.as_view()),
    path('top-services/', TopServicesView.as_view()),
]

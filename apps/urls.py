from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views.adminViews import (AppointmentViewSet, ServiceViewSet, UserViewSet,
                                   BusinessViewSet,
                                   GetMe, CustomTokenObtainPairView, BusinessWorkerViewSet, UserUpdateView)
from apps.views.otp_views import RequestPhoneChangeView, VerifyPhoneOTPView
from apps.views.statisticviews import AppointmentStatisticView, TopServicesView, TopClientsView, TopBusinessesView, \
    TopSpecialistView

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('business', BusinessViewSet)
router.register('appointments', AppointmentViewSet),
router.register('services', ServiceViewSet),
router.register('business-workers', BusinessWorkerViewSet),

urlpatterns = [
    path('admin/', include(router.urls)),
    path('statistics/', AppointmentStatisticView.as_view()),
    path('top-services/', TopServicesView.as_view()),
    path('top-clients/', TopClientsView.as_view()),
    path('top-businesses/', TopBusinessesView.as_view()),
    path('top-specialists/', TopSpecialistView.as_view()),
    path('get-me/', GetMe.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('user-update/', UserUpdateView.as_view()),
    path('change-phone/', RequestPhoneChangeView.as_view()),
    path('verify-phone/', VerifyPhoneOTPView.as_view()),
    # path('token/refresh/', CustomTokenRefreshView.as_view()),

]

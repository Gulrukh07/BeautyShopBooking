from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views.adminViews import (AppointmentViewSet, ServiceViewSet, UserViewSet,
                                   BusinessViewSet, AppointmentStatisticView,
                                   TopServicesView, GetMe, CustomTokenObtainPairView, BusinessWorkerViewSet,
                                   TopClientsView, )

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
    path('top-users/', TopClientsView.as_view()),
    path('get-me/', GetMe.as_view()),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', CustomTokenRefreshView.as_view()),

]

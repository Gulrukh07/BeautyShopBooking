from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.models import BusinessWorker
from apps.views.adminViews import (AppointmentViewSet, ServiceViewSet, UserViewSet,
                                   BusinessViewSet, AppointmentStatisticView,
                                   TopServicesView, GetMe, CustomTokenObtainPairView, BusinessWorkerlistView, )

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('business', BusinessViewSet)
router.register('appointments', AppointmentViewSet),
router.register('services', ServiceViewSet),

urlpatterns = [
    path('admin/', include(router.urls)),
    path('statistics/', AppointmentStatisticView.as_view()),
    path('top-services/', TopServicesView.as_view()),
    path('get-me/', GetMe.as_view()),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('business-workers/', BusinessWorkerlistView.as_view()),
    # path('token/refresh/', CustomTokenRefreshView.as_view()),

]

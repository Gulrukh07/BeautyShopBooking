from django.urls import path

from apps.views import UserCreateView

urlpatterns = [
    path('user-create', UserCreateView.as_view())
]
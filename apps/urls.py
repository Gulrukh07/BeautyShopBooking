from django.urls import path

from apps.views import UserCreateView, UserListView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('admin/users', UserCreateView.as_view()),
    path('admin/users-list', UserListView.as_view()),
    path('admin/users-edit/<int:pk>', UserUpdateView.as_view()),
    path('admin/users-delete/<int:pk>', UserDeleteView.as_view()),
]

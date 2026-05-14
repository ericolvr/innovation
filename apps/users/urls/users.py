from django.urls import path
from apps.users.views import UserListCreateView, UserDetailView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]

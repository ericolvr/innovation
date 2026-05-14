from django.urls import path
from .views import TechnicianListCreateView, TechnicianDetailView

urlpatterns = [
    path('', TechnicianListCreateView.as_view(), name='technician-list'),
    path('<int:pk>/', TechnicianDetailView.as_view(), name='technician-detail'),
]

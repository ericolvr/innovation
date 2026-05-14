from django.urls import path
from apps.condominiums.views import MaintenanceListView, MaintenanceDetailView, maintenance_dashboard

urlpatterns = [
    path('', MaintenanceListView.as_view(), name='maintenance-list'),
    path('dashboard/', maintenance_dashboard, name='maintenance-dashboard'),
    path('<int:pk>/', MaintenanceDetailView.as_view(), name='maintenance-detail'),
]

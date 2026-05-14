from django.urls import path
from apps.condominiums.views import (
    MyCondominiumsView, CondominiumDetailView, CondominiumEquipmentListView,
    FloorListCreateView, FloorDetailView,
    DeviceListCreateView, DeviceDetailView,
    EquipmentListCreateView, EquipmentDetailView,
)

urlpatterns = [
    # Condominiums
    path('', MyCondominiumsView.as_view(), name='condominium-list'),
    path('equipment-list/', CondominiumEquipmentListView.as_view(), name='condominium-equipment-list'),
    path('<int:pk>/', CondominiumDetailView.as_view(), name='condominium-detail'),

    # Floors (nested under condominium)
    path('<int:pk>/floors/', FloorListCreateView.as_view(), name='floor-list'),
    path('floors/<int:pk>/', FloorDetailView.as_view(), name='floor-detail'),

    # Devices (nested under floor)
    path('floors/<int:pk>/devices/', DeviceListCreateView.as_view(), name='device-list'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),

    # Equipments (nested under device)
    path('devices/<int:pk>/equipments/', EquipmentListCreateView.as_view(), name='equipment-list'),
    path('equipments/<int:pk>/', EquipmentDetailView.as_view(), name='equipment-detail'),
]

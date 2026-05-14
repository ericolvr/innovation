from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Condominium, Floor, Device, Equipment, Maintenance, MaintenanceItem, Schedule
from .serializers import (
    CondominiumSerializer, CondominiumDetailSerializer,
    FloorSerializer, DeviceSerializer, EquipmentSerializer,
    MaintenanceSerializer, ScheduleSerializer,
)


def _sync_floors(condo):
    existing_count = condo.floor_levels.count()
    new_count = condo.floors
    if new_count > existing_count:
        for i in range(existing_count + 1, new_count + 1):
            Floor.objects.create(condominium=condo, name=f'{i}º Andar')


class MyCondominiumsView(generics.ListCreateAPIView):
    serializer_class = CondominiumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Condominium.objects.select_related('client').all()
        client_id = self.request.query_params.get('client')
        if client_id:
            qs = qs.filter(client_id=client_id)
        active = self.request.query_params.get('active')
        if active is not None:
            qs = qs.filter(active=active.lower() == 'true')
        return qs

    def perform_create(self, serializer):
        condo = serializer.save()
        _sync_floors(condo)


class CondominiumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Condominium.objects.select_related('client').prefetch_related(
        'floor_levels__devices__equipments'
    )
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CondominiumDetailSerializer
        return CondominiumSerializer

    def perform_update(self, serializer):
        condo = serializer.save()
        _sync_floors(condo)


# --- Floors ---

class FloorListCreateView(generics.ListCreateAPIView):
    serializer_class = FloorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Floor.objects.filter(condominium_id=self.kwargs['pk']).prefetch_related(
            'devices__equipments'
        )

    def perform_create(self, serializer):
        serializer.save(condominium_id=self.kwargs['pk'])


class FloorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Floor.objects.prefetch_related('devices__equipments')
    serializer_class = FloorSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- Devices ---

class DeviceListCreateView(generics.ListCreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(floor_id=self.kwargs['pk']).prefetch_related('equipments')

    def perform_create(self, serializer):
        serializer.save(floor_id=self.kwargs['pk'])


class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.prefetch_related('equipments')
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- Equipments ---

class EquipmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Equipment.objects.filter(device_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(device_id=self.kwargs['pk'])


class EquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- Maintenances ---

class MaintenanceListView(generics.ListCreateAPIView):
    serializer_class = MaintenanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Maintenance.objects.prefetch_related('items__device', 'items__equipment')
        condo_id = self.request.query_params.get('condominium')
        if condo_id:
            qs = qs.filter(condominium_id=condo_id)
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


class MaintenanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maintenance.objects.prefetch_related('items__device', 'items__equipment')
    serializer_class = MaintenanceSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def maintenance_dashboard(request):
    today = timezone.localdate()

    qs = Maintenance.objects.all()

    by_status = {
        status: qs.filter(status=status).count()
        for status, _ in Maintenance.STATUS_CHOICES
    }

    by_type = {
        t: qs.filter(type=t).count()
        for t, _ in Maintenance.TYPE_CHOICES
    }

    today_qs = (
        Maintenance.objects
        .filter(scheduled_at__date=today)
        .select_related('condominium', 'technician')
        .prefetch_related('items__device', 'items__equipment')
        .order_by('scheduled_at')
    )
    today_list = [
        {
            'id': m.id,
            'condominium_name': m.condominium.name,
            'technician_name': m.technician.name if m.technician else None,
            'type': m.type,
            'status': m.status,
            'scheduled_at': m.scheduled_at,
            'items_count': m.items.count(),
        }
        for m in today_qs
    ]

    recent_qs = (
        Maintenance.objects
        .select_related('condominium', 'technician')
        .order_by('-created_at')[:10]
    )
    recent_list = [
        {
            'id': m.id,
            'condominium_name': m.condominium.name,
            'technician_name': m.technician.name if m.technician else None,
            'type': m.type,
            'status': m.status,
            'scheduled_at': m.scheduled_at,
            'finished_at': m.finished_at,
        }
        for m in recent_qs
    ]

    return Response({
        'by_status': by_status,
        'by_type': by_type,
        'today': today_list,
        'recent': recent_list,
    })


class CondominiumEquipmentListView(generics.ListAPIView):
    serializer_class = CondominiumDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Condominium.objects.prefetch_related('floor_levels__devices__equipments').select_related('client')
        if user.type == 2 and user.client_id:
            qs = qs.filter(client_id=user.client_id)
        return qs.filter(active=True)


class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Schedule.objects.select_related('maintenance', 'condominium', 'technician')
        if user.type == 2 and user.client_id:
            qs = qs.filter(condominium__client_id=user.client_id)
        return qs

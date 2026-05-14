from rest_framework import serializers
from .models import Condominium, Floor, Device, Equipment, Maintenance, MaintenanceItem, Schedule



class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'type', 'name', 'ip', 'device', 'created_at']
        read_only_fields = ['id', 'device', 'created_at']


class DeviceSerializer(serializers.ModelSerializer):
    equipments = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'type', 'name', 'ip', 'floor', 'equipments', 'created_at']
        read_only_fields = ['id', 'floor', 'equipments', 'created_at']


class FloorSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = ['id', 'name', 'condominium', 'devices', 'created_at']
        read_only_fields = ['id', 'condominium', 'devices', 'created_at']


class CondominiumSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True, default=None)

    class Meta:
        model = Condominium
        fields = ['id', 'client', 'client_name', 'name', 'zipcode', 'state', 'city', 'neighborhood', 'address', 'complement', 'floors', 'active']


class CondominiumDetailSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True, default=None)
    floor_levels = FloorSerializer(many=True, read_only=True)

    class Meta:
        model = Condominium
        fields = ['id', 'client', 'client_name', 'name', 'zipcode', 'state', 'city', 'neighborhood', 'address', 'complement', 'floors', 'active', 'floor_levels']


class MaintenanceItemSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True, default=None)
    equipment_name = serializers.CharField(source='equipment.name', read_only=True, default=None)
    equipment_type = serializers.CharField(source='equipment.type', read_only=True, default=None)

    class Meta:
        model = MaintenanceItem
        fields = ['id', 'device', 'device_name', 'equipment', 'equipment_name', 'equipment_type']
        read_only_fields = ['id', 'device_name', 'equipment_name', 'equipment_type']


class MaintenanceSerializer(serializers.ModelSerializer):
    condominium_name = serializers.CharField(source='condominium.name', read_only=True)
    technician_name = serializers.CharField(source='technician.name', read_only=True, default=None)
    items = MaintenanceItemSerializer(many=True, required=False)

    class Meta:
        model = Maintenance
        fields = [
            'id', 'condominium', 'condominium_name',
            'technician', 'technician_name',
            'items',
            'type', 'status',
            'scheduled_at', 'finished_at',
            'notes', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'condominium_name', 'technician_name']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        maintenance = Maintenance.objects.create(**validated_data)
        for item in items_data:
            MaintenanceItem.objects.create(maintenance=maintenance, **item)
        return maintenance

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                MaintenanceItem.objects.create(maintenance=instance, **item)
        return instance


class ScheduleSerializer(serializers.ModelSerializer):
    condominium_name = serializers.CharField(source='condominium.name', read_only=True)
    maintenance_type = serializers.CharField(source='maintenance.get_type_display', read_only=True)
    technician_name = serializers.CharField(source='technician.name', read_only=True)
    technician_document = serializers.CharField(source='technician.document', read_only=True)
    technician_mobile = serializers.CharField(source='technician.mobile', read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'maintenance', 'maintenance_type',
            'condominium', 'condominium_name',
            'technician_name', 'technician_document', 'technician_mobile',
            'scheduled_date',
        ]
        read_only_fields = fields

from django.db import models
from apps.clients.models import Client


class Condominium(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='condominiums', null=True, blank=True)
    name = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=9)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    complement = models.CharField(max_length=100, blank=True, default='')
    floors = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'condominiums'
        ordering = ['name']

    def __str__(self):
        return self.name


class Floor(models.Model):
    condominium = models.ForeignKey(Condominium, on_delete=models.CASCADE, related_name='floor_levels')
    name = models.CharField(max_length=100)  # "Térreo", "1º Andar"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'floors'
        ordering = ['id']

    def __str__(self):
        return f'{self.condominium.name} — {self.name}'


class Device(models.Model):
    NVR = 'nvr'
    DVR = 'dvr'
    RACK = 'rack'
    TYPE_CHOICES = [
        (NVR, 'NVR'),
        (DVR, 'DVR'),
        (RACK, 'Rack'),
    ]

    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='devices')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=NVR)
    name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'devices'

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'


class Equipment(models.Model):
    CAMERA = 'camera'
    BIOMETRIA = 'biometria'
    CENTRAL_ALARME = 'central_alarme'
    TYPE_CHOICES = [
        (CAMERA, 'Câmera'),
        (BIOMETRIA, 'Biometria'),
        (CENTRAL_ALARME, 'Central de Alarme'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='equipments')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=CAMERA)
    name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'equipments'

    def __str__(self):
        return self.name


class Maintenance(models.Model):
    PREVENTIVE = 'preventive'
    CORRECTIVE = 'corrective'
    TYPE_CHOICES = [(PREVENTIVE, 'Preventiva'), (CORRECTIVE, 'Corretiva')]

    SCHEDULED = 'scheduled'
    EXECUTING = 'executing'
    FINISHED = 'finished'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (SCHEDULED, 'Agendada'),
        (EXECUTING, 'Executando'),
        (FINISHED, 'Finalizada'),
        (CANCELLED, 'Cancelada'),
    ]

    condominium = models.ForeignKey(Condominium, on_delete=models.CASCADE, related_name='maintenances')
    technician = models.ForeignKey('technicians.Technician', null=True, blank=True, on_delete=models.SET_NULL, related_name='maintenances')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=PREVENTIVE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SCHEDULED)
    scheduled_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'maintenances'
        ordering = ['scheduled_at']

    def __str__(self):
        return f'{self.condominium.name} — {self.get_type_display()} — {self.scheduled_at:%d/%m/%Y}'


class MaintenanceItem(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, related_name='items')
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.SET_NULL, related_name='maintenance_items')
    equipment = models.ForeignKey(Equipment, null=True, blank=True, on_delete=models.SET_NULL, related_name='maintenance_items')

    class Meta:
        db_table = 'maintenance_items'


class Schedule(models.Model):
    maintenance = models.OneToOneField(Maintenance, on_delete=models.CASCADE, related_name='schedule')
    condominium = models.ForeignKey(Condominium, on_delete=models.CASCADE, related_name='schedules')
    technician = models.ForeignKey('technicians.Technician', on_delete=models.CASCADE, related_name='schedules')
    scheduled_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schedules'
        ordering = ['scheduled_date']

    def __str__(self):
        return f'{self.condominium.name} — {self.technician.name} — {self.scheduled_date:%d/%m/%Y}'

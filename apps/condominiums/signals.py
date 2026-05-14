from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Maintenance, Schedule

ACTIVE_STATUSES = {Maintenance.SCHEDULED, Maintenance.EXECUTING}


@receiver(post_save, sender=Maintenance)
def sync_schedule(sender, instance, **kwargs):
    if instance.status in ACTIVE_STATUSES and instance.technician_id:
        Schedule.objects.update_or_create(
            maintenance=instance,
            defaults={
                'condominium_id': instance.condominium_id,
                'technician_id': instance.technician_id,
                'scheduled_date': instance.scheduled_at.date(),
            },
        )
    else:
        Schedule.objects.filter(maintenance=instance).delete()

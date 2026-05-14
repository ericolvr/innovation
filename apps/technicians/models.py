from django.db import models


class Technician(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    document = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'technicians'
        ordering = ['name']

    def __str__(self):
        return self.name

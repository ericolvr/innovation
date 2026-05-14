from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    document = models.CharField(max_length=20, blank=True, default='')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'
        ordering = ['name']

    def __str__(self):
        return self.name

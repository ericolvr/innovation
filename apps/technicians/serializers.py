from rest_framework import serializers
from .models import Technician


class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = ['id', 'name', 'mobile', 'document', 'active', 'created_at']
        read_only_fields = ['id', 'created_at']

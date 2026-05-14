from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'mobile', 'email', 'document', 'active', 'created_at', 'password']
        read_only_fields = ['id', 'created_at']

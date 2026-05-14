from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'mobile', 'type', 'active', 'created_at']
        read_only_fields = ['id', 'created_at']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'mobile', 'type', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

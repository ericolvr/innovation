import random
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .models import Client
from .serializers import ClientSerializer
from apps.users.models import User


def _random_password():
    return str(random.randint(100000, 999999))


class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.filter(active=True)
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        client = serializer.save()
        password = _random_password()
        try:
            User.objects.create_user(
                mobile=client.mobile,
                password=password,
                name=client.name,
                type=User.MANAGER,
                client=client,
            )
            self._generated_password = password
        except IntegrityError:
            self._generated_password = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        if getattr(self, '_generated_password', None):
            data = {**data, 'generated_password': self._generated_password}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        password = serializer.validated_data.pop('password', None)
        client = serializer.save()

        user = client.users.first()
        if user:
            updated_fields = []

            if user.name != client.name:
                user.name = client.name
                updated_fields.append('name')

            if user.mobile != client.mobile:
                user.mobile = client.mobile
                updated_fields.append('mobile')

            if password:
                user.set_password(password)
                updated_fields.append('password')

            if updated_fields:
                updated_fields.append('updated_at')
                user.save(update_fields=updated_fields)

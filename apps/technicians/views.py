from rest_framework import generics, permissions
from .models import Technician
from .serializers import TechnicianSerializer


class TechnicianListCreateView(generics.ListCreateAPIView):
    serializer_class = TechnicianSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Technician.objects.all()
        active = self.request.query_params.get('active')
        if active is not None:
            qs = qs.filter(active=active.lower() == 'true')
        return qs


class TechnicianDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [permissions.IsAuthenticated]

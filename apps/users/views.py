from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, CreateUserSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        mobile = request.data.get('mobile', '').strip()
        password = request.data.get('password', '').strip()

        if not mobile or not password:
            return Response({'error': 'Celular e senha são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=mobile, password=password)
        if not user:
            return Response({'error': 'Celular ou senha incorretos'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.active:
            return Response({'error': 'Usuário inativo'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login realizado com sucesso',
            'token': str(refresh.access_token),
            'user': {
                'id': user.id,
                'name': user.name,
                'mobile': user.mobile,
                'type': user.type,
                'client_id': user.client_id,
            }
        })


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(active=True).order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

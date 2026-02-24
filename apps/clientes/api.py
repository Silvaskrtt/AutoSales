from rest_framework import viewsets, permissions
from .models import Cliente
from .serializers import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """API para listar, criar, editar e desativar clientes."""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # associa o usuário autenticado ao criar o cliente
        serializer.save(user=self.request.user)

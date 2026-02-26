from rest_framework import viewsets, permissions
from .models import Venda
from .serializers import VendaSerializer

class VendaViewSet(viewsets.ModelViewSet):
    """API para listar, criar, editar e desativar vendas."""
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # associa o usuário autenticado ao criar a venda
        serializer.save(user=self.request.user)
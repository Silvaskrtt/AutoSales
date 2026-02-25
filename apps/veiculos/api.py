from rest_framework import viewsets, permissions
from .models import Veiculo
from .serializers import VeiculoSerializer

class VeiculoViewSet(viewsets.ModelViewSet):
    """API para listar, criar, editar e desativar veículos."""
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # associa o usuário autenticado ao criar o veículo
        serializer.save(user=self.request.user)
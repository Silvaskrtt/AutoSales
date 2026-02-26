from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """API para listar, criar, editar e desativar clientes."""
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Desativa a paginação para retornar todos os clientes do usuário logado em uma única resposta
    pagination_class = None

    def get_queryset(self):
        # Retorna apenas os clientes do usuário logado, ordenados
        print(f"Usuário logado: {self.request.user}")  # Debug
        queryset = Cliente.objects.filter(user=self.request.user).order_by('-data_cadastro')
        print(f"Clientes encontrados: {queryset.count()}")  # Debug
        return queryset

    def perform_create(self, serializer):
        print(f"Criando cliente para usuário: {self.request.user}")  # Debug
        serializer.save(user=self.request.user)
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Parcela
from .serializers import ParcelaSerializer

class ParcelaViewSet(viewsets.ModelViewSet):
    """API para listar, criar, editar e desativar parcelas."""
    serializer_class = ParcelaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Desativa a paginação para retornar todas as parcelas do usuário logado em uma única resposta
    pagination_class = None

    def get_queryset(self):
        # Retorna apenas as parcelas do usuário logado, ordenados
        print(f"Usuário logado: {self.request.user}")  # Debug
        queryset = Parcela.objects.filter(user=self.request.user).order_by('-data_vencimento')
        print(f"Parcelas encontradas: {queryset.count()}")  # Debug
        return queryset

    def perform_create(self, serializer):
        print(f"Criando parcela para usuário: {self.request.user}")  # Debug
        serializer.save(user=self.request.user)
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Financiamento
from .serializers import FinanciamentoSerializer

class FinanciamentoViewSet(viewsets.ModelViewSet):
    """API para listar, criar, editar e desativar financiamentos."""
    serializer_class = FinanciamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Desativa a paginação para retornar todos os financiamentos do usuário logado em uma única resposta
    pagination_class = None

    def get_queryset(self):
        # Retorna apenas os financiamentos do usuário logado, ordenados
        print(f"Usuário logado: {self.request.user}")  # Debug
        queryset = Financiamento.objects.filter(user=self.request.user).order_by('-data_cadastro')
        print(f"Financiamentos encontrados: {queryset.count()}")  # Debug
        return queryset

    def perform_create(self, serializer):
        print(f"Criando financiamento para usuário: {self.request.user}")  # Debug
        serializer.save(user=self.request.user)
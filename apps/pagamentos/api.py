from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Pagamento
from .serializers import PagamentoSerializer

class PagamentoViewSet(viewsets.ModelViewSet):
    """API para listar, criar, editar e desativar pagamentos."""
    serializer_class = PagamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Desativa a paginação para retornar todos os pagamentos do usuário logado em uma única resposta
    pagination_class = None

    def get_queryset(self):
        # Retorna apenas os pagamentos do usuário logado, ordenados
        print(f"Usuário logado: {self.request.user}")  # Debug
        queryset = Pagamento.objects.filter(user=self.request.user).order_by('-data_cadastro')
        print(f"Pagamentos encontrados: {queryset.count()}")  # Debug
        return queryset

    def perform_create(self, serializer):
        print(f"Criando pagamento para usuário: {self.request.user}")  # Debug
        serializer.save(user=self.request.user)
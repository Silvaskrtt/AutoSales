# veiculos/api.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Veiculo
from .serializers import VeiculoSerializer 

class VeiculoViewSet(viewsets.ModelViewSet):
    """API para gerenciar veículos."""
    serializer_class = VeiculoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna veículos ativos e inativos, mas filtra por usuário se não for staff"""
        user = self.request.user
        
        if user.is_staff:
            return Veiculo.objects.all()
        
        # Usuários normais veem apenas seus próprios veículos
        return Veiculo.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Associa o usuário autenticado ao criar o veículo"""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Atualiza o veículo mantendo o usuário original"""
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Ativa/desativa um veículo"""
        veiculo = self.get_object()
        veiculo.is_active = not veiculo.is_active
        veiculo.save()
        return Response({'status': 'success', 'is_active': veiculo.is_active})
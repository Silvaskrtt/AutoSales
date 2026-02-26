# veiculos/serializers.py
from rest_framework import serializers
from .models import Veiculo
from modelos.models import Modelo

class VeiculoSerializer(serializers.ModelSerializer):
    modelo_nome = serializers.CharField(source='modelo.nome', read_only=True)
    marca_nome = serializers.CharField(source='modelo.marca.nome', read_only=True)
    imagem_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Veiculo
        fields = [
            'id', 'placa', 'ano', 'cor', 'preco', 'status',
            'imagem_veiculo', 'imagem_url', 'is_active', 'user',
            'modelo', 'modelo_nome', 'marca_nome', 'created_at'
        ]
        
        read_only_fields = ['id', 'user', 'created_at']
    
    def get_imagem_url(self, obj):
        if obj.imagem_veiculo:
            return obj.imagem_veiculo.url
        return None
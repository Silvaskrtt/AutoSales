from rest_framework import serializers
from .models import Veiculo
from datetime import date
from modelos.models import Modelo
import re

class VeiculoSerializer(serializers.ModelSerializer):
    modelo_nome = serializers.CharField(source='modelo.nome', read_only=True)
    marca_nome = serializers.CharField(source='modelo.marca.nome', read_only=True)
    imagem_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Veiculo
        fields = [
            'id', 'placa', 'ano', 'cor', 'preco', 'status',
            'imagem_veiculo', 'is_active', 'user',
            'modelo', 'modelo_nome', 'marca_nome', 'imagem_url'
        ]
        read_only_fields = ['id', 'user']
    
    def validate_placa(self, value):
        """Validação personalizada para placa"""
        # Remove hífen se existir para validação
        placa_clean = value.replace('-', '')
        
        # Valida formato Mercosul (AAA1A23)
        if re.match(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$', placa_clean):
            return value
            
        # Valida formato antigo com hífen (AAA-1234)
        if re.match(r'^[A-Z]{3}-[0-9]{4}$', value):
            return value
            
        raise serializers.ValidationError(
            'Placa inválida. Use o formato AAA1A23 (Mercosul) ou AAA-1234 (Antigo).'
        )
    
    def validate_ano(self, value):
        """Validação do ano"""
        current_year = date.today().year
        if value < 1886 or value > current_year + 1:
            raise serializers.ValidationError(
                f'Ano deve estar entre 1886 e {current_year + 1}'
            )
        return value
    
    def get_imagem_url(self, obj):
        if obj.imagem_veiculo:
            return obj.imagem_veiculo.url
        return None
from rest_framework import serializers
from .models import Veiculo

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = [
            'id', 'marca', 'modelo', 'ano', 'cor', 'preco',
            'is_active', 'user'
        ]
        
        read_only_fields = ['id', 'user']

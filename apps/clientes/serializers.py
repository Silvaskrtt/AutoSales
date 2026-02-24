from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id', 'nome', 'sobrenome', 'cpf', 'telefone', 'email',
            'rua', 'numero', 'bairro', 'cidade', 'estado', 'is_active', 'user'
        ]
        read_only_fields = ['id', 'user']

from rest_framework import serializers
from .models import Pagamento


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = [
            'id', 'metodo', 'valor', 'data_pagamento', 'referencia', 'venda', 'parcela'
        ]
        read_only_fields = ['id', 'venda']

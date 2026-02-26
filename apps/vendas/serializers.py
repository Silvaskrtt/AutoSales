from rest_framework import serializers
from .models import Venda

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = [
            'id', 'valor_total', 'entrada', 'saldo_devedor', 'tipo_pagamento', 'cliente', 'user', 'veiculo'
        ]

        read_only_fields = ['id', 'user']
from rest_framework import serializers
from .models import Financiamento


class FinanciamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financiamento
        fields = [
            'id', 'instituicao_financeira', 'valor_financiado', 'taxa_juros',
            'parcelas', 'data_inicio', 'contrato', 'venda'
        ]
        read_only_fields = ['id', 'venda']

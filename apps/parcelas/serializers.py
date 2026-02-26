from rest_framework import serializers
from .models import Parcela


class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = [
            'id', 'numero', 'valor', 'data_vencimento', 'status', 'venda'
        ]
        read_only_fields = ['id', 'venda']
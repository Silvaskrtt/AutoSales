from django.db import models

from vendas.models import Venda
from parcelas.models import Parcela

class Pagamento(models.Model):
    TYPE_CHOICES = [
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('boleto', 'Boleto Bancário'),
        ('pix', 'Pix'),
        ('dinheiro', 'Dinheiro'),
    ]
    
    metodo = models.CharField(max_length=50, choices=TYPE_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='pagamentos')
    parcela = models.ForeignKey(Parcela, on_delete=models.CASCADE, related_name='pagamentos', blank=True, null=True)
    
    def __str__(self):
        return f'Pagamento de {self.valor} via {self.get_metodo_display()} em {self.data_pagamento.strftime("%Y-%m-%d %H:%M:%S")}'
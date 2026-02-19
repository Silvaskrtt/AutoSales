from django.db import models

from vendas.models import Venda

class Financiamento(models.Model):
    
    instituicao_financeira = models.CharField(max_length=100)
    valor_financiado = models.DecimalField(max_digits=10, decimal_places=2)
    taxa_juros = models.DecimalField(max_digits=5, decimal_places=2)
    parcelas = models.IntegerField()
    data_inicio = models.DateField()
    contrato = models.FileField(upload_to='contratos_financiamento/')
    venda = models.OneToOneField(Venda, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Financiamento - {self.instituicao_financeira} - {self.venda}"
from django.db import models

from vendas.models import Venda

class Parcela(models.Model):
    TYPE_CHOICES = (
        ('PEDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADA', 'Atrasada'),
    )
    
    numero = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    
    status = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES, 
        default='PENDENTE'
    )
    
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='parcelas')
    
    def __str__(self):
        return f'Parcela {self.numero} - {self.status}'
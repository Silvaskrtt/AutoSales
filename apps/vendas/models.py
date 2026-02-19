from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from clientes.models import Cliente
from accounts.models import User
from veiculos.models import Veiculo

class Venda(models.Model):
    
    data_venda = models.DateTimeField(_("Data da Venda"), auto_now_add=True)
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Valor Total",
    )
    
    entrada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Entrada",
    )
    
    saldo_devedor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Saldo Devedor",
    )
    
    tipo_pagamento = models.CharField(
        max_length=20,
        choices=[
            ('avista', 'À Vista'),
            ('parcelado', 'Parcelado'),
        ],
        verbose_name="Tipo de Pagamento",
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Vendedor responsável pela venda
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.cliente} - {self.veiculo}"
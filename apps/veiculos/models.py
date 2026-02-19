from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date

from modelos.models import Modelo

def current_year():
    return date.today().year

class Veiculo(models.Model):
    # TYPE_CHOICES feito para 'status'
    TYPE_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('VENDIDO', 'Vendido'),
        ('RESERVADO', 'Reservado'),
        ('MANUTENCAO', 'Manutenção'),
    ]
    
    # Validador para aceitar:
    # 1. Padrao antigo: AAA-1234
    # 2. Padrao Mercosul: AAA1A23 (três letras, um número, uma letra, dois números)
    placa_validator = RegexValidator(
        regex='^[A-Z]{3}\d[A-J0-9]\d{2}$',
        message='Placa inválida. Use o formato AAA1A23 (Mercosul) ou AAA-1234 (Antigo).',
        code='placa_invalida' 
    )
    
    placa = models.CharField(
        max_length=8, # 'AAA-1234' tem 8 caracteres, 'AAA1A23' tem 7
        validators=[placa_validator],
        unique=True,
        help_text="Formato: AAA1A23 ou AAA-1234"
    )
    
    ano = models.PositiveSmallIntegerField(
        default=current_year(),
        validators=[
            MinValueValidator(1800),
            MaxValueValidator(3000)
        ]
    )
    
    cor = models.CharField(max_length=50)
    
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Preço",
        help_text="Preço do veículo em reais (ex.: 50000.00)"
    )
    
    status = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='DISPONIVEL'
    )
    
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.modelo} - {self.placa} - {self.status}"
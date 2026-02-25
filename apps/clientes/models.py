from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from allauth.account import app_settings
from django.utils.translation import gettext_lazy as _

class Cliente(models.Model):
    """
    Modelo de Cliente
    """
    ESTADO_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
       verbose_name=_("user"),
       on_delete=models.CASCADE,
       related_name='clientes'
    )
    
    nome = models.CharField(max_length=150)
    sobrenome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True) # 11 números + 3 de pontuação
    telefone = models.CharField(max_length=20)
    
    email = models.EmailField(
        db_index=True,
        max_length=app_settings.EMAIL_MAX_LENGTH,
        verbose_name=_("Endereço de Email"),
    )
    
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    
    data_cadastro = models.DateTimeField(_("data de cadastro"), auto_now_add=True)
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.cpf} - {self.sobrenome}"
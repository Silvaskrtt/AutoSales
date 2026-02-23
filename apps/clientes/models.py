from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from allauth.account import app_settings
from django.utils.translation import gettext_lazy as _

class Cliente(models.Model):
    """
    Modelo de Cliente
    """
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
    estado = models.CharField(max_length=100)
    
    data_cadastro = models.DateTimeField(_("data de cadastro"), auto_now_add=True)
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.cpf} - {self.sobrenome}"
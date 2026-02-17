from django.db import models
from allauth.account import app_settings
from django.utils.translation import gettext_lazy as _

class Cliente(models.Model):
    
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True) # 11 números + 3 de pontuação
    telefone = models.CharField(max_length=20)
    email = models.EmailField(
        db_index=True,
        max_length=app_settings.EMAIL_MAX_LENGTH,
        verbose_name=_("Endereço de Email"),
    )
    endereco_completo = models.TextField(
        help_text="Insira o endereço completo",
        verbose_name=_("Endereço Completo"),
    )
    data_cadastro = models.DateTimeField(_("data de cadastro"), auto_now_add=True)

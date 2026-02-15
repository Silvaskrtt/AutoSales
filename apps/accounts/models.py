from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Modelo de usuário personalizado
    """
    status = models.BooleanField(_("status"), default=True)
    data_criacao = models.DateTimeField(_("data de criação"), auto_now_add=True)
    
    def __str__(self):
        return self.username

class Perfil(models.Model):
    
    nome_perfil = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=False)
    
class userPerfil(models.Model,):
    
    # Definindo as Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    class Meta:
        # Define PK composta (usuario, perfil)
        unique_together = (('user', 'perfil'),)
    
        
    def __str__(self):
        return f"{self.user.username} - {self.perfil.nome_perfil}"
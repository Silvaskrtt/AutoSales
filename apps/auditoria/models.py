from django.db import models

from accounts.models import User

class LogAcesso(models.Model):
    
    data_hora = models.DateTimeField(auto_now_add=True)
    acao = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.data_hora} - {self.acao} - {self.user.username}"

class LogSistema(models.Model):
    
    descricao = models.TextField()
    tipo = models.CharField(max_length=50)
    data_hora = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
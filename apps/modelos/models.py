from django.db import models

from marcas.models import Marca

class Modelo(models.Model):
    
    nome = models.CharField(max_length=150)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nome} - {self.marca}"
    
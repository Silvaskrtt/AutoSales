from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Cliente
    """
    list_display = ('nome', 'sobrenome', 'cpf', 'telefone', 'email', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'data_cadastro')
    list_filter = ('nome', 'email', 'cpf')
    
    search_fields = ('nome', 'cpf', 'email')
    ordering = ('nome',)
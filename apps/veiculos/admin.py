from django.contrib import admin
from .models import Veiculo


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Veiculo
    """
    list_display = ('placa', 'modelo', 'ano', 'cor', 'preco', 'status')
    list_filter = ('status', 'ano', 'modelo')
    search_fields = ('placa', 'modelo__nome')
    
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('placa', 'modelo', 'ano')
        }),
        ('Características', {
            'fields': ('cor', 'preco')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

from django.contrib import admin
from .models import Venda

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Venda
    """
    list_display = ('veiculo', 'cliente', 'data_venda', 'valor_total', 'user')
    list_filter = ('data_venda', 'cliente', 'user', 'veiculo')
    search_fields = ('veiculo__placa', 'cliente__nome', 'user__username')
    
    fieldsets = (
        ('Informações da Venda', {
            'fields': ('veiculo', 'cliente', 'valor_total', 'user')
        }),
    )

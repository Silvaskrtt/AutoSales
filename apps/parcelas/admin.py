from django.contrib import admin

from .models import Parcela

@admin.register(Parcela)
class ParcelaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Parcela.
    """
    list_display = ('numero', 'valor', 'data_vencimento', 'status', 'venda')
    list_filter = ('status',)
    search_fields = ('venda__cliente__nome',)
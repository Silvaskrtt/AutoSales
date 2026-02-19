from django.contrib import admin

from .models import Financiamento

@admin.register(Financiamento)
class FinanciamentoAdmin(admin.ModelAdmin):
    """"Admin para o modelo Financiamento.
    """
    list_display = ('instituicao_financeira', 'valor_financiado', 'parcelas', 'taxa_juros', 'contrato', 'data_inicio', 'venda')
    list_filter = ('data_inicio', 'instituicao_financeira',)
    search_fields = ('instituicao_financeira', 'venda__id')
from django.contrib import admin

from .models import Pagamento

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    """
    Admin interface for Pagamento model.
    """
    list_display = ('metodo', 'valor', 'data_pagamento', 'referencia', 'venda')
    list_filter = ('metodo',)
    search_fields = ('metodo', 'venda__id')

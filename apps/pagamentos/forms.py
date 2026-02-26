from django import forms
from .models import Pagamento

class PagamentoForm(forms.ModelForm):
    """
    Formulário para gerenciamento de Pagamentos
    """

    class Meta:
        model = Pagamento
        fields = ['metodo', 'valor', 'data_pagamento', 'referencia', 'venda', 'parcela']
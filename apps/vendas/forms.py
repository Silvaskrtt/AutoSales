from django.forms import forms
from .models import Venda

class VendaForm(forms.ModelForm):
    """
    Formulário para gerenciamento de Vendas
    """

    class Meta:
        model = Venda
        fields = ['valor_total', 'entrada', 'saldo_devedor', 'tipo_pagamento', 'status', 'cliente', 'user', 'veiculo']
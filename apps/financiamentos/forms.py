from django import forms
from .models import Financiamento

class FinanciamentoForm(forms.ModelForm):
    """
    Formulário para gerenciamento de Financiamentos
    """

    class Meta:
        model = Financiamento
        fields = ['instituicao_financeira', 'valor_financiado', 'taxa_juros', 'parcelas', 'data_inicio', 'contrato', 'venda']
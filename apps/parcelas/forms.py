from django import forms
from .models import Parcela

class ParcelaForm(forms.ModelForm):
    """
    Formulário para gerenciamento de Parcelas
    """

    class Meta:
        model = Parcela
        fields = ['numero', 'valor', 'data_vencimento', 'status', 'venda']
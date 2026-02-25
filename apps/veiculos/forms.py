from django.forms import forms
from .models import Veiculo

class VeiculoForm(forms.ModelForm):
    """
    Formulário para gerenciamento de Veículos
    """

    class Meta:
        model = Veiculo
        fields = ['placa', 'ano', 'cor', 'preco', 'status', 'modelo']
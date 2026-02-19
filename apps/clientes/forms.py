from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    """
    Formulário para gerenciamento de Clientes
    """

    class Meta:
        model = Cliente
        fields = ['nome', 'sobrenome', 'cpf', 'telefone', 'email', 'rua', 'numero', 'cidade', 'estado', 'data_cadastro']
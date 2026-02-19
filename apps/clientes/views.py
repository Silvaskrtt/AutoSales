from django.shortcuts import render

from clientes.models import Cliente
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

def listarCliente(request, Cliente):
    """
    Obtém todos os clientes cadastrados.
    """
    # Buscar todos os clientes
    clientes = Cliente.objects.filter(
        user = request.user,
        is_active=True
    ).order_by('nome')

    return render(request, 'clientes/lista.html')
from django.urls import path
from .views import listarCliente

urlpatterns = [
    path('clientes/', listarCliente, name='listaClientes'),
]

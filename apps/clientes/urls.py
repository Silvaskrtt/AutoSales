from django.urls import path
from .views import GerenciarCliente

urlpatterns = [
    path('clientes/', GerenciarCliente.as_view(), name='lista_clientes'),
]
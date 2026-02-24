from django.urls import path
from .views import EditarCliente, GerenciarCliente, CriarCliente, DesativarCliente

urlpatterns = [
    path('clientes/', GerenciarCliente.as_view(), name='lista_clientes'),
    path('clientes/criar/', CriarCliente.as_view(), name='criar_cliente'),
    path('clientes/editar/<int:pk>/', EditarCliente.as_view(), name='editar_cliente'),
    path('clientes/desativar/<int:pk>/', DesativarCliente.as_view(), name='desativar_cliente'),
]

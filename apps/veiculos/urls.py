from django.urls import path
from .views import GerenciarVeiculo

urlpatterns = [
    # View para renderizar o template
    path('veiculos/', GerenciarVeiculo.as_view(), name='lista_veiculos'),
]
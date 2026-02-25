from django.urls import path, include
from .views import GerenciarVeiculo, CriarVeiculo, EditarVeiculo, DesativarVeiculo, DetalheVeiculo
from rest_framework import routers
from .api import VeiculoViewSet

router = routers.DefaultRouter()
router.register(r'api/veiculos', VeiculoViewSet, basename='api-veiculos')

urlpatterns = [
    path('veiculos/', GerenciarVeiculo.as_view(), name='lista_veiculos'),
    path('', include(router.urls)),
]

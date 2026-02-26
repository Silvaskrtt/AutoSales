from django.urls import path, include
from .views import GerenciarVenda, CriarVenda, EditarVenda, DesativarVenda, DetalheVenda
from rest_framework import routers
from .api import VendaViewSet

router = routers.DefaultRouter()
router.register(r'api/vendas', VendaViewSet, basename='api-vendas')

urlpatterns = [
    path('vendas/', GerenciarVenda.as_view(), name='lista_vendas'),
    # Rotas da API (DRF)
    path('', include(router.urls)),
]

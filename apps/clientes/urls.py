from django.urls import path, include
from .views import EditarCliente, GerenciarCliente, CriarCliente, DesativarCliente
from rest_framework import routers
from .api import ClienteViewSet

router = routers.DefaultRouter()
router.register(r'api/clientes', ClienteViewSet, basename='api-clientes')

urlpatterns = [
    path('clientes/', GerenciarCliente.as_view(), name='lista_clientes'),
    # Rotas da API (DRF)
    path('', include(router.urls)),
]

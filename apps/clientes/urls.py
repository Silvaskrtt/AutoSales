from django.urls import path, include
from .views import EditarCliente, GerenciarCliente, CriarCliente, DesativarCliente
from rest_framework import routers
from .api import ClienteViewSet

router = routers.DefaultRouter()
router.register(r'api/clientes', ClienteViewSet, basename='api-clientes')

urlpatterns = [
    path('clientes/', GerenciarCliente.as_view(), name='lista_clientes'),
    path('clientes/criar/', CriarCliente.as_view(), name='criar_cliente'),
    path('clientes/editar/<int:pk>/', EditarCliente.as_view(), name='editar_cliente'),
    path('clientes/desativar/<int:pk>/', DesativarCliente.as_view(), name='desativar_cliente'),
    # Rotas da API (DRF)
    path('', include(router.urls)),
]

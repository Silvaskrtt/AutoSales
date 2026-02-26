from django.urls import path, include
from .views import GerenciarParcela, CriarParcela, EditarParcela, DesativarParcela
from rest_framework import routers
from .api import ParcelaViewSet

router = routers.DefaultRouter()
router.register(r'api/parcelas', ParcelaViewSet, basename='api-parcelas')

urlpatterns = [
    path('parcelas/', GerenciarParcela.as_view(), name='lista_parcelas'),
    # Rotas da API (DRF)
    path('', include(router.urls)),
]
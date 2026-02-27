from django.urls import path, include
from rest_framework import routers
from .api import VeiculoViewSet

router = routers.DefaultRouter()
router.register(r'veiculos', VeiculoViewSet, basename='api-veiculos')

urlpatterns = [
    path('', include(router.urls)),
]
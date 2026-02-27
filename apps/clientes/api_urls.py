from django.urls import path, include
from rest_framework import routers
from .api import ClienteViewSet

router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='api-clientes')

urlpatterns = [
    path('', include(router.urls)),
]
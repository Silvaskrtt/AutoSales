from django.urls import path, include
from .views import GerenciarFinanciamento
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
	path('financiamentos/', GerenciarFinanciamento.as_view(), name='lista_financiamentos'),
	path('', include(router.urls)),
]

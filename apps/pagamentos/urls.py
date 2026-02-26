from django.urls import path, include
from .views import GerenciarPagamentos
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
	path('pagamentos/', GerenciarPagamentos.as_view(), name='lista_pagamentos'),
	path('', include(router.urls)),
]

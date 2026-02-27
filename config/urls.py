from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Autenticação (django-allauth)
    path('accounts/', include('allauth.urls')),
    
    # APIs
    path('api/', include('clientes.api_urls')),
    path('api/', include('veiculos.api_urls')), 
    
    # Dashboards na raiz
    path('', include('dashboards.urls')),

    # Views
    path('', include('clientes.urls')),
    path('', include('veiculos.urls')),
    path('', include('relatorios.urls')),
]
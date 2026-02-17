from django.contrib import admin
from .models import Modelo
from marcas.models import Marca

@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    """
    Admin personalizado para Modelo
    """
    list_display = ('nome', 'marca')
    list_filter = ('nome', 'marca')
    
    search_fields = ('nome', 'marca')
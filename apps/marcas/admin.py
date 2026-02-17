from django.contrib import admin
from .models import Marca

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    """
    Admin para modele Marca
    """
    list_display = ('nome',)
    list_filter = ('nome',)
    
    search_fields = ('nome',)
    ordering = ('nome',)
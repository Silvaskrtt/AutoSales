from django.contrib import admin

from .models import LogAcesso, LogSistema

@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    list_display = ('data_hora', 'acao', 'ip', 'user')
    search_fields = ('acao', 'ip', 'user__username')
    list_filter = ('data_hora',)
    
@admin.register(LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo', 'data_hora', 'user')
    search_fields = ('descricao', 'tipo', 'user__username')
    list_filter = ('tipo', 'data_hora')
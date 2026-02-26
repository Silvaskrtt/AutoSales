from django.contrib import admin

from .models import LogAcesso, LogSistema, AuditLog


@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    list_display = ('id_log', 'data_hora', 'acao', 'ip', 'user')
    search_fields = ('acao', 'ip', 'user__username')
    list_filter = ('data_hora',)
    readonly_fields = ('data_hora', 'acao', 'ip', 'user')
    

@admin.register(LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = ('id_log', 'descricao', 'tipo', 'data_hora', 'user')
    search_fields = ('descricao', 'tipo', 'user__username')
    list_filter = ('tipo', 'data_hora')
    readonly_fields = ('descricao', 'tipo', 'data_hora', 'user')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'content_type', 'object_id', 'user', 'created_at')
    readonly_fields = ('action', 'content_type', 'object_id', 'object_repr', 'changes', 'user', 'ip_address', 'created_at')
    search_fields = ('object_repr', 'object_id', 'user__username')
from django.contrib import admin
from .models import Relatorio


@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner', 'created_at')
	search_fields = ('title', 'description')
	prepopulated_fields = {'slug': ('title',)}

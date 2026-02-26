from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Relatorio


class RelatorioListView(PermissionRequiredMixin, ListView):
	permission_required = 'relatorios.view_relatorio'
	model = Relatorio
	template_name = 'relatorios/relatorio_list.html'
	context_object_name = 'relatorios'
	paginate_by = 20


class RelatorioDetailView(PermissionRequiredMixin, DetailView):
	permission_required = 'relatorios.view_relatorio'
	model = Relatorio
	template_name = 'relatorios/relatorio_detail.html'
	context_object_name = 'relatorio'

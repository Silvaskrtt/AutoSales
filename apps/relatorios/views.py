from django.views.generic import ListView, DetailView
from .models import Relatorio


class RelatorioListView(ListView):
	model = Relatorio
	template_name = 'relatorios/relatorio_list.html'
	context_object_name = 'relatorios'
	paginate_by = 20


class RelatorioDetailView(DetailView):
	model = Relatorio
	template_name = 'relatorios/relatorio_detail.html'
	context_object_name = 'relatorio'

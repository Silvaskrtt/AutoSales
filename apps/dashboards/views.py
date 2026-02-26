from django.views.generic import ListView, DetailView
from .models import Dashboard


class DashboardListView(ListView):
	model = Dashboard
	template_name = "dashboards/dashboard_list.html"
	context_object_name = "dashboards"
	paginate_by = 20


class DashboardDetailView(DetailView):
	model = Dashboard
	template_name = "dashboards/dashboard_detail.html"
	context_object_name = "dashboard"

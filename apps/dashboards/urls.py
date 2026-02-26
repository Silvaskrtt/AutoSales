from django.urls import path
from . import views

app_name = "dashboards"

# A listagem fica na raiz ('/'), mas detalhes ficam sob '/dashboards/<slug>/'
# Isso evita que rotas como '/clientes/' sejam interpretadas como slug.
urlpatterns = [
    path("", views.DashboardListView.as_view(), name="list"),
    path("dashboards/<slug:slug>/", views.DashboardDetailView.as_view(), name="detail"),
]

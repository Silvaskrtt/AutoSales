from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('relatorios/', views.RelatorioListView.as_view(), name='list'),
    path('relatorios/<slug:slug>/', views.RelatorioDetailView.as_view(), name='detail'),
]

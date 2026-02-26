from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from modelos.models import Modelo
from .models import Veiculo
import json

class GerenciarVeiculo(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'veiculos.view_veiculo'
    """
    View baseada em classe para listar todos os veículos cadastrados.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Lista os veículos ordenados alfabeticamente por modelo.
    """
    model = Veiculo
    template_name = 'veiculos/list.html'
    context_object_name = 'veiculos'
    ordering = ['modelo']
    
    def get_queryset(self):
        """Retorna apenas veículos ativos"""
        return Veiculo.objects.filter(is_active=True).order_by('modelo')
    
    def get_context_data(self, **kwargs):
        """Adiciona modelos ao contexto para o select do formulário"""
        context = super().get_context_data(**kwargs)
        
        # Buscar modelos ativos para o select
        modelos = Modelo.objects.all().select_related('marca')
        context['modelos'] = modelos
        
        # Serializar modelos para JavaScript (para uso no frontend)
        modelos_data = [
            {
                'id': m.id,
                'nome': m.nome,
                'marca_nome': m.marca.nome
            } for m in modelos
        ]
        context['modelos_json'] = json.dumps(modelos_data)
        
        return context
    
class CriarVeiculo(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'veiculos.add_veiculo'
    """
    View baseada em classe para criação de novos veículos.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Associa automaticamente o veículo criado ao usuário logado.
    
    Attributes:
        model: Modelo Veiculo que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário
        template_name: Template responsável pela renderização do formulário
        success_url: URL de redirecionamento após o cadastro bem-sucedido
    
    Methods:
        form_valid: Sobrescrito para associar o usuário logado ao veículo antes de salvar
    """
    model = Veiculo
    fields = ['placa', 'modelo', 'ano', 'cor', 'preco', 'status', 'imagem_veiculo']
    template_name = 'veiculos/modal_form.html'
    success_url = reverse_lazy('lista_veiculos')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EditarVeiculo(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'veiculos.change_veiculo'
    """
    View baseada em classe para edição de veículos existentes.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite editar os detalhes de um veículo específico.
    
    Attributes:
        model: Modelo Veiculo que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário
        template_name: Template responsável pela renderização do formulário
        success_url: URL de redirecionamento após a edição bem-sucedida
    """
    model = Veiculo
    fields = ['marca', 'modelo', 'ano', 'preco', 'descricao']
    template_name = 'veiculos/modal_edit.html'
    success_url = reverse_lazy('lista_veiculos')
    
class DetalheVeiculo(LoginRequiredMixin, View):
    """
    View baseada em classe para exibir os detalhes de um veículo específico.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Exibe as informações detalhadas de um veículo selecionado.
    
    Methods:
        get: Processa a requisição GET para exibir os detalhes do veículo
    """
    def get(self, request, pk):
        """
        Processa a requisição GET para exibir os detalhes do veículo.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do veículo a ser exibido
            
        Returns:
            HttpResponse: Resposta HTTP com a renderização dos detalhes do veículo"""
        veiculo = get_object_or_404(Veiculo, pk=pk)
        return render(request, 'veiculos/modal_detail.html', {'veiculo': veiculo})
    
class DesativarVeiculo(LoginRequiredMixin, View):
    """
    View baseada em classe para desativar veículos.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Em vez de excluir o veículo do banco de dados, marca-o como inativo.
    
    Methods:
        post: Processa a requisição POST para desativar o veículo
    """
    def post(self, request, pk):
        """
        Desativa um veículo específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do veículo a ser desativado
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após a desativação
        """
        veiculo = get_object_or_404(Veiculo, pk=pk)
        veiculo.is_active = False
        veiculo.save()
        return redirect('lista_veiculos')
    
class ReativarVeiculo(LoginRequiredMixin, View):
    """
    View baseada em classe para reativar veículos desativados.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite reativar um veículo previamente desativado.
    
    Methods:
        post: Processa a requisição POST para reativar o veículo
    """
    def post(self, request, pk):
        """
        Reativa um veículo específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do veículo a ser reativado
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após a reativação
        """
        veiculo = get_object_or_404(Veiculo, pk=pk)
        veiculo.is_active = True
        veiculo.save()
        return redirect('lista_veiculos')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from .models import Financiamento
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class GerenciarFinanciamento(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'financiamentos.view_financiamento'
    """
    View baseada em classe para listar todos os financiamentos cadastrados.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Lista os financiamentos ordenados alfabeticamente por instituição financeira.
    
    Attributes:
        model: Modelo Financiamento que será consultado
        template_name: Template responsável pela renderização da lista
        context_object_name: Nome da variável de contexto disponível no template
        ordering: Critério de ordenação dos registros (por instituição financeira)
    """
    model = Financiamento
    template_name = 'financiamentos/list.html'
    context_object_name = 'financiamentos'
    ordering = ['instituicao_financeira']
    
    def get_queryset(self):
        return Financiamento.objects.filter(user=self.request.user).order_by('instituicao_financeira')
        
class CriarFinanciamento(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'financiamentos.add_financiamento'
    """
    View baseada em classe para criação de novos financiamentos.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Associa automaticamente o financiamento criado ao usuário logado.
    
    Attributes:
        model: Modelo Financiamento que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário
        template_name: Template responsável pela renderização do formulário
        success_url: URL de redirecionamento após o cadastro bem-sucedido
    
    Methods:
        form_valid: Sobrescrito para associar o usuário logado ao financiamento antes de salvar
    """
    model = Financiamento
    fields = ['instituicao_financeira', 'valor_financiado', 'taxa_juros', 'parcelas', 'data_inicio', 'contrato', 'venda']
    template_name = 'financiamentos/modal_form.html'
    success_url = reverse_lazy('lista_financiamentos')
    
    def form_valid(self, form):
        """
        Valida e processa o formulário de criação de financiamento.
        
        Antes de salvar, associa o financiamento ao usuário atualmente logado.
        
        Args:
            form: Formulário válido com os dados do financiamento
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após o salvamento
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EditarFinanciamento(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'financiamentos.change_financiamento'
    """
    View baseada em classe para edição de financiamentos existentes.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite editar os campos do financiamento selecionado.
    
    Attributes:
        model: Modelo Financiamento que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário de edição
        template_name: Template responsável pela renderização do formulário de edição
        success_url: URL de redirecionamento após a edição bem-sucedida
    """
    model = Financiamento
    fields = ['instituicao_financeira', 'valor_financiado', 'taxa_juros', 'parcelas', 'data_inicio', 'contrato', 'venda']
    template_name = 'financiamentos/modal_edit.html'
    success_url = reverse_lazy('lista_financiamentos')
    
class DesativarFinanciamento(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'financiamentos.change_financiamento'
    """
    View baseada em classe para desativar financiamentos.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Em vez de excluir o financiamento do banco de dados, marca-o como inativo.
    
    Methods:
        post: Processa a requisição POST para desativar o financiamento
    """
    def post(self, request, pk):
        """
        Desativa um financiamento específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do financiamento a ser desativado
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após a desativação
        """
        financiamento = get_object_or_404(Financiamento, pk=pk)
        financiamento.is_active = False
        financiamento.save()
        
        return redirect('lista_financiamentos')
    
class ReativarFinanciamento(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'financiamentos.change_financiamento'
    """
    View baseada em classe para reativar financiamentos desativados.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite reativar um financiamento previamente desativado.
    
    Methods:
        post: Processa a requisição POST para reativar o financiamento
    """
    def post(self, request, pk):
        """
        Reativa um financiamento específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do financiamento a ser reativado
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após a reativação
        """
        financiamento = get_object_or_404(Financiamento, pk=pk)
        financiamento.is_active = True
        financiamento.save()
        
        return redirect('lista_financiamentos')
    
class DetalheFinanciamento(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'financiamentos.view_financiamento'
    """
    View baseada em classe para exibir detalhes de um financiamento específico.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Exibe informações detalhadas do financiamento selecionado.
    
    Methods:
        get: Processa a requisição GET para exibir os detalhes do financiamento
    """
    def get(self, request, pk):
        """
        Exibe os detalhes de um financiamento específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do financiamento cujos detalhes serão exibidos
            
        Returns:
            HttpResponse: Resposta HTTP com a renderização dos detalhes do financiamento
        """
        financiamento = get_object_or_404(Financiamento, pk=pk)
        return render(request, 'financiamentos/modal_detail.html', {'financiamento': financiamento})
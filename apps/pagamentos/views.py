from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from .models import Pagamento
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class GerenciarPagamentos(LoginRequiredMixin, ListView):
    """
    View baseada em classe para listar todos os pagamentos cadastrados.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Lista os pagamentos ordenados alfabeticamente por instituição financeira.
    
    Attributes:
        model: Modelo Pagamento que será consultado
        template_name: Template responsável pela renderização da lista
        context_object_name: Nome da variável de contexto disponível no template
        ordering: Critério de ordenação dos registros (por instituição financeira)
    """
    model = Pagamento
    template_name = 'pagamentos/list.html'
    context_object_name = 'pagamentos'
    ordering = ['instituicao_financeira']
    
    def get_queryset(self):
        return Pagamento.objects.filter(user=self.request.user).order_by('instituicao_financeira')
        
class CriarPagamento(LoginRequiredMixin, CreateView):
    """
    View baseada em classe para criação de novos pagamentos.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Associa automaticamente o pagamento criado ao usuário logado.
    
    Attributes:
        model: Modelo Pagamento que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário
        template_name: Template responsável pela renderização do formulário
        success_url: URL de redirecionamento após o cadastro bem-sucedido
    
    Methods:
        form_valid: Sobrescrito para associar o usuário logado ao pagamento antes de salvar
    """
    model = Pagamento
    fields = ['instituicao_financeira', 'valor', 'data_pagamento', 'referencia', 'venda']
    template_name = 'pagamentos/modal_form.html'
    success_url = reverse_lazy('lista_pagamentos')
    
    def form_valid(self, form):
        """
        Valida e processa o formulário de criação de pagamento.
        
        Antes de salvar, associa o pagamento ao usuário atualmente logado.
        
        Args:
            form: Formulário válido com os dados do pagamento
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após o salvamento
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EditarPagamento(LoginRequiredMixin, UpdateView):
    """
    View baseada em classe para edição de pagamentos existentes.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite editar os campos do pagamento selecionado.
    
    Attributes:
        model: Modelo Pagamento que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário de edição
        template_name: Template responsável pela renderização do formulário de edição
        success_url: URL de redirecionamento após a edição bem-sucedida
    """
    model = Pagamento
    fields = ['instituicao_financeira', 'valor', 'data_pagamento', 'referencia']
    template_name = 'pagamentos/modal_edit.html'
    success_url = reverse_lazy('lista_pagamentos')
    
class DesativarPagamento(LoginRequiredMixin, View):
    """
    View baseada em classe para desativar pagamentos.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Em vez de excluir o pagamento do banco de dados, marca-o como inativo.
    
    Methods:
        post: Processa a requisição POST para desativar o pagamento
    """
    def post(self, request, pk):
        """
        Desativa um pagamento específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do pagamento a ser desativado
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após a desativação
        """
        pagamento = get_object_or_404(Pagamento, pk=pk)
        pagamento.is_active = False
        pagamento.save()
        
        return redirect('lista_pagamentos')
    
class ReativarPagamento(LoginRequiredMixin, View):
    """
    View baseada em classe para reativar pagamentos desativados.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite reativar um pagamento previamente desativado.
    
    Methods:
        post: Processa a requisição POST para reativar o pagamento
    """
    def post(self, request, pk):
        """
        Reativa um pagamento específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do pagamento a ser reativado
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após a reativação
        """
        pagamento = get_object_or_404(Pagamento, pk=pk)
        pagamento.is_active = True
        pagamento.save()
        
        return redirect('lista_pagamentos')
    
class DetalhePagamento(LoginRequiredMixin, View):
    """
    View baseada em classe para exibir detalhes de um pagamento específico.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Exibe informações detalhadas do pagamento selecionado.
    
    Methods:
        get: Processa a requisição GET para exibir os detalhes do pagamento
    """
    def get(self, request, pk):
        """
        Exibe os detalhes de um pagamento específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do pagamento cujos detalhes serão exibidos
            
        Returns:
            HttpResponse: Resposta HTTP com a renderização dos detalhes do pagamento
        """
        pagamento = get_object_or_404(Pagamento, pk=pk)
        return render(request, 'pagamentos/modal_detail.html', {'pagamento': pagamento})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from clientes.models import Cliente
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class GerenciarCliente(LoginRequiredMixin, ListView):
    """
    View baseada em classe para listar todos os clientes cadastrados.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Lista os clientes ordenados alfabeticamente por nome.
    
    Attributes:
        model: Modelo Cliente que será consultado
        template_name: Template responsável pela renderização da lista
        context_object_name: Nome da variável de contexto disponível no template
        ordering: Critério de ordenação dos registros (por nome)
    """
    model = Cliente
    template_name = 'clientes/list.html'
    context_object_name = 'clientes'
    ordering = ['nome']
    
    def get_queryset(self):
        # Retorna apenas clientes do usuário logado
        return Cliente.objects.filter(
            user=self.request.user, 
            is_active=True
        ).order_by('nome')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_clientes'] = self.get_queryset().count()
        return context
        
class CriarCliente(LoginRequiredMixin, CreateView):
    """
    View baseada em classe para criação de novos clientes.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Associa automaticamente o cliente criado ao usuário logado.
    
    Attributes:
        model: Modelo Cliente que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário
        template_name: Template responsável pela renderização do formulário
        success_url: URL de redirecionamento após o cadastro bem-sucedido
    
    Methods:
        form_valid: Sobrescrito para associar o usuário logado ao cliente antes de salvar
    """
    model = Cliente
    fields = ['nome', 'sobrenome', 'cpf', 'telefone', 'email', 'rua', 'numero', 'bairro', 'cidade', 'estado']
    template_name = 'clientes/modal_form.html'
    success_url = reverse_lazy('lista_clientes')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        """
        Valida e processa o formulário de criação de cliente.
        
        Antes de salvar, associa o cliente ao usuário atualmente logado.
        
        Args:
            form: Formulário válido com os dados do cliente
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após o salvamento
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EditarCliente(LoginRequiredMixin, UpdateView):
    """
    View baseada em classe para edição de clientes existentes.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite editar os campos do cliente selecionado.
    
    Attributes:
        model: Modelo Cliente que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário de edição
        template_name: Template responsável pela renderização do formulário de edição
        success_url: URL de redirecionamento após a edição bem-sucedida
    """
    model = Cliente
    fields = ['nome', 'sobrenome', 'cpf', 'telefone', 'email', 'rua', 'numero', 'bairro', 'cidade', 'estado']
    template_name = 'clientes/modal_edit.html'
    success_url = reverse_lazy('lista_clientes')
    
class DesativarCliente(LoginRequiredMixin, View):
    """
    View baseada em classe para desativar clientes.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Em vez de excluir o cliente do banco de dados, marca-o como inativo.
    
    Methods:
        post: Processa a requisição POST para desativar o cliente
    """
    def post(self, request, pk):
        """
        Desativa um cliente específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do cliente a ser desativado
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após a desativação
        """
        cliente = get_object_or_404(Cliente, pk=pk)
        cliente.is_active = False
        cliente.save()
        
        return redirect('lista_clientes')
    
class ReativarCliente(LoginRequiredMixin, View):
    """
    View baseada em classe para reativar clientes desativados.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite reativar um cliente previamente desativado.
    
    Methods:
        post: Processa a requisição POST para reativar o cliente
    """
    def post(self, request, pk):
        """
        Reativa um cliente específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do cliente a ser reativado
            
        Returns:
            HttpResponse: Resposta HTTP de redirecionamento após a reativação
        """
        cliente = get_object_or_404(Cliente, pk=pk)
        cliente.is_active = True
        cliente.save()
        
        return redirect('lista_clientes')
    
class DetalheCliente(LoginRequiredMixin, View):
    """
    View baseada em classe para exibir detalhes de um cliente específico.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Exibe informações detalhadas do cliente selecionado.
    
    Methods:
        get: Processa a requisição GET para exibir os detalhes do cliente
    """
    def get(self, request, pk):
        """
        Exibe os detalhes de um cliente específico.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária do cliente cujos detalhes serão exibidos
            
        Returns:
            HttpResponse: Resposta HTTP com a renderização dos detalhes do cliente
        """
        cliente = get_object_or_404(Cliente, pk=pk)
        return render(request, 'clientes/modal_detail.html', {'cliente': cliente})
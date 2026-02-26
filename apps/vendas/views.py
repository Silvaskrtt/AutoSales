from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from .models import Venda

class GerenciarVenda(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'vendas.view_venda'
    """
    View baseada em classe para listar todas as vendas cadastradas.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Lista as vendas ordenadas pela data de venda, da mais recente para a mais antiga.
    
    Attributes:
        model: Modelo Venda que será consultado
        template_name: Template responsável pela renderização da lista
        context_object_name: Nome da variável de contexto disponível no template
        ordering: Critério de ordenação dos registros (data_venda)
    """
    model = Venda
    template_name = 'vendas/list.html'
    context_object_name = 'vendas'
    ordering = ['-data_venda']
    
    def get_queryset(self):
        return Venda.objects.filter(is_active=True).order_by('-data_venda')
    
class CriarVenda(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'vendas.add_venda'
    """
    View baseada em classe para criação de novas vendas.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Associa automaticamente a venda criada ao usuário logado.
    
    Attributes:
        model: Modelo Venda que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário
        template_name: Template responsável pela renderização do formulário
        success_url: URL de redirecionamento após o cadastro bem-sucedido
    
    Methods:
        form_valid: Sobrescrito para associar o usuário logado à venda antes de salvar
    """
    model = Venda
    fields = ['cliente', 'veiculo', 'data_venda', 'valor_total', 'entrada', 'saldo_devedor', 'tipo_pagamento']
    template_name = 'vendas/modal_form.html'
    success_url = reverse_lazy('lista_vendas')
    
    def form_valid(self, form):
        """
        Valida e processa o formulário de criação de venda.
        
        Antes de salvar, associa a venda ao usuário atualmente logado.
        
        Args:
            form: Formulário válido com os dados da venda
            
        Returns:
            Redirecionamento para a URL de sucesso após salvar a venda
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class DetalhesVenda(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'vendas.view_venda'
    """
    View baseada em classe para exibir os detalhes de uma venda específica.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Exibe os detalhes da venda selecionada, garantindo que a venda pertença ao usuário logado.
    
    Methods:
        get: Processa a requisição GET para exibir os detalhes da venda
    """
    def get(self, request, pk):
        venda = get_object_or_404(Venda, pk=pk, user=request.user)
        return render(request, 'vendas/detalhes.html', {'venda': venda})

class EditarVenda(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'vendas.change_venda'
    """
    View baseada em classe para edição de vendas existentes.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite editar os detalhes de uma venda específica, garantindo que a venda pertença ao usuário logado.
    
    Attributes:
        model: Modelo Venda que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário de edição
        template_name: Template responsável pela renderização do formulário de edição
        success_url: URL de redirecionamento após a edição bem-sucedida
    """
    model = Venda
    fields = ['cliente', 'veiculo', 'data_venda', 'valor_total', 'entrada', 'saldo_devedor', 'tipo_pagamento']
    template_name = 'vendas/modal_edit.html'
    success_url = reverse_lazy('lista_vendas')
    
class CancelarVenda(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'vendas.change_venda'
    """
    View baseada em classe para cancelar (desativar) vendas.
    
    Requer que the usuário esteja autenticado (LoginRequiredMixin).
    Em vez de excluir a venda do banco de dados, marca-a como inativa.
    
    Methods:
        post: Processa a requisição POST para cancelar a venda
    """
    def post(self, request, pk):
        venda = get_object_or_404(Venda, pk=pk, user=request.user)
        venda.is_active = False
        venda.save()
        return redirect('lista_vendas')
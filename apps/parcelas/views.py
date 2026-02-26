from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from .models import Parcela
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class GerenciarParcela(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'parcelas.view_parcela'
    """
    View baseada em classe para listar todos os parcelas cadastrados.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Lista as parcelas ordenados alfabeticamente por cliente.
    
    Attributes:
        model: Modelo Parcela que será consultado
        template_name: Template responsável pela renderização da lista
        context_object_name: Nome da variável de contexto disponível no template
        ordering: Critério de ordenação dos registros (por cliente)
    """
    model = Parcela
    template_name = 'parcelas/list.html'
    context_object_name = 'parcelas'
    ordering = ['cliente']
    
    def get_queryset(self):
        return Parcela.objects.filter(is_active=True).order_by('cliente')
    
class CriarParcela(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'parcelas.add_parcela'
    """
    View baseada em classe para criação de novos parcelas.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Associa automaticamente o parcela criado ao usuário logado.
    
    Attributes:
        model: Modelo Parcela que será utilizado no formulário
        fields: Campos do modelo que serão exibidos no formulário
        template_name: Template responsável pela renderização do formulário
        success_url: URL de redirecionamento após o cadastro bem-sucedido
    
    Methods:
        form_valid: Sobrescrito para associar o usuário logado ao parcela antes de salvar
    """
    model = Parcela
    fields = ['cliente', 'valor', 'data_vencimento', 'status']
    template_name = 'parcelas/modal_form.html'
    success_url = reverse_lazy('lista_parcelas')
    
    def form_valid(self, form):
        """
        Valida e processa o formulário de criação de parcela.
        
        Antes de salvar, associa a parcela ao usuário atualmente logado.
        
        Args:
            form: Formulário válido com os dados da parcela
            
        Returns:
            Redirecionamento para a URL de sucesso após salvar a parcela
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EditarParcela(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'parcelas.change_parcela'
    """
    View baseada em classe para edição de parcelas existentes.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite editar os detalhes de uma parcela específica.
    
    Attributes:
        model: Modelo Parcela que será editado
        fields: Campos do modelo que serão exibidos no formulário de edição
        template_name: Template responsável pela renderização do formulário de edição
        success_url: URL de redirecionamento após a edição bem-sucedida
    
    Methods:
        form_valid: Sobrescrito para garantir que a parcela editada permaneça associada ao usuário logado
    """
    model = Parcela
    fields = ['cliente', 'valor', 'data_vencimento', 'status']
    template_name = 'parcelas/modal_form.html'
    success_url = reverse_lazy('lista_parcelas')
    
    def form_valid(self, form):
        """
        Valida e processa o formulário de edição de parcela.
        
        Garante que a parcela editada permaneça associada ao usuário atualmente logado.
        
        Args:
            form: Formulário válido com os dados atualizados da parcela
            
        Returns:
            Redirecionamento para a URL de sucesso após salvar as alterações na parcela
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

class CancelarParcela(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'parcelas.change_parcela'
    """
    View baseada em classe para cancelar (desativar) parcelas.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite marcar uma parcela como inativa, indicando que foi cancelada.
    
    Methods:
        post: Processa a requisição POST para cancelar a parcela selecionada
    """
    def post(self, request, pk):
        """
        Processa a requisição POST para cancelar uma parcela específica.
        
        Marca a parcela como inativa (is_active=False) em vez de deletá-la do banco de dados.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária da parcela a ser cancelada
            
        Returns:
            Redirecionamento para a lista de parcelas após o cancelamento
        """
        parcela = get_object_or_404(Parcela, pk=pk)
        parcela.is_active = False
        parcela.save()
        return redirect('lista_parcelas')
    
class ReativarParcela(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'parcelas.change_parcela'
    """
    View baseada em classe para reativar parcelas canceladas.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Permite marcar uma parcela como ativa novamente, indicando que foi reativada.
    
    Methods:
        post: Processa a requisição POST para reativar a parcela selecionada
    """
    def post(self, request, pk):
        """
        Processa a requisição POST para reativar uma parcela específica.
        
        Marca a parcela como ativa (is_active=True) em vez de deletá-la do banco de dados.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária da parcela a ser reativada
            
        Returns:
            Redirecionamento para a lista de parcelas após a reativação
        """
        parcela = get_object_or_404(Parcela, pk=pk)
        parcela.is_active = True
        parcela.save()
        return redirect('lista_parcelas')
    
class DetalheParcela(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'parcelas.view_parcela'
    """
    View baseada em classe para exibir detalhes de uma parcela específica.
    
    Requer que o usuário esteja autenticado (LoginRequiredMixin).
    Exibe informações detalhadas sobre a parcela selecionada.
    
    Methods:
        get: Processa a requisição GET para exibir os detalhes da parcela
    """
    def get(self, request, pk):
        """
        Processa a requisição GET para exibir os detalhes de uma parcela específica.
        
        Recupera a parcela com base na chave primária (pk) e renderiza um template com seus detalhes.
        
        Args:
            request: Objeto HttpRequest contendo os dados da requisição
            pk: Chave primária da parcela cujos detalhes serão exibidos
            
        Returns:
            Renderização do template de detalhes da parcela com o contexto contendo a parcela
        """
        parcela = get_object_or_404(Parcela, pk=pk)
        return render(request, 'parcelas/detail.html', {'parcela': parcela})
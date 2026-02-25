// Helpers
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';').map(c => c.trim());
    for (const c of cookies) {
        if (c.startsWith(name + '=')) return decodeURIComponent(c.split('=')[1]);
    }
    return '';
}

const API_BASE = '/api/clientes/';

// Renderização
function renderClientes(clientes) {
    const tbody = document.getElementById('tabela-corpo');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    if (!clientes.length) {
        const estadoVazio = document.getElementById('estado-vazio');
        const paginacao = document.getElementById('paginacao');
        if (estadoVazio) estadoVazio.style.display = 'block';
        if (paginacao) paginacao.style.display = 'none';
        return;
    }
    
    const estadoVazio = document.getElementById('estado-vazio');
    const paginacao = document.getElementById('paginacao');
    if (estadoVazio) estadoVazio.style.display = 'none';
    if (paginacao) paginacao.style.display = 'flex';
    
    clientes.forEach(c => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${c.nome} ${c.sobrenome || ''}</td>
            <td>${c.cpf || ''}</td>
            <td>${c.telefone || ''}</td>
            <td>${c.email || ''}</td>
            <td>${c.cidade || ''}</td>
            <td class="actions-cell">
                <button class="btn btn-info" data-id="${c.id}" onclick="verDetalhesCliente(${c.id})" title="Ver detalhes">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="3"/>
                        <path d="M22 12c-2.667 4.667-6 7-10 7s-7.333-2.333-10-7c2.667-4.667 6-7 10-7s7.333 2.333 10 7z"/>
                    </svg>
                </button>
                <button class="btn btn-primary" data-id="${c.id}" onclick="editarCliente(${c.id})" title="Editar">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
                    </svg>
                </button>
                <button class="btn btn-danger" data-id="${c.id}" onclick="excluirCliente(${c.id})" title="Excluir">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                        <path d="M10 11v5M14 11v5"/>
                    </svg>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    
    const totalClientes = document.getElementById('total-clientes');
    if (totalClientes) totalClientes.textContent = clientes.length;
}

// Requisições à API
async function fetchClientes() {
    try {
        const res = await fetch(API_BASE, {credentials: 'same-origin'});
        if (!res.ok) return renderClientes([]);
        const data = await res.json();
        const clientes = Array.isArray(data) ? data : (data.results || []);
        renderClientes(clientes);
    } catch (error) {
        console.error('Erro ao buscar clientes:', error);
        renderClientes([]);
    }
}

async function criarCliente(payload) {
    const res = await fetch(API_BASE, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        credentials: 'same-origin',
        body: JSON.stringify(payload)
    });
    return res;
}

async function atualizarCliente(id, payload) {
    const res = await fetch(`${API_BASE}${id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        credentials: 'same-origin',
        body: JSON.stringify(payload)
    });
    return res;
}

// Variável global para armazenar o ID do cliente a ser excluído
let clienteIdParaExcluir = null;

// Função de exclusão modificada para usar o modal personalizado
async function excluirCliente(id) {
    // Armazenar o ID para uso posterior
    clienteIdParaExcluir = id;
    
    // Mostrar modal de confirmação
    const modalExclusao = document.getElementById('modal-exclusao');
    if (modalExclusao) {
        modalExclusao.style.display = 'block';
    } else {
        // Fallback para confirm() caso o modal não exista
        if (confirm('Confirma exclusão deste cliente?')) {
            await confirmarExclusao(id);
        }
    }
}

// Função para confirmar a exclusão (chamada pelo botão do modal)
async function confirmarExclusao(id) {
    // Mostrar loading no botão
    const btnConfirmar = document.getElementById('confirmar-exclusao');
    const btnTexto = btnConfirmar.querySelector('.btn-texto');
    const btnLoading = btnConfirmar.querySelector('.btn-loading');
    
    if (btnTexto && btnLoading) {
        btnTexto.style.display = 'none';
        btnLoading.style.display = 'inline-block';
    }
    
    try {
        const res = await fetch(`${API_BASE}${id}/`, {
            method: 'DELETE',
            headers: {'X-CSRFToken': getCSRFToken()},
            credentials: 'same-origin'
        });
        
        if (res.ok) {
            // Fechar modal
            document.getElementById('modal-exclusao').style.display = 'none';
            
            // Recarregar lista
            await fetchClientes();
            
            // Mostrar toast de sucesso
            mostrarToast('Cliente excluído com sucesso!', 'success');
        } else {
            const errorData = await res.json().catch(() => null);
            alert('Erro ao excluir: ' + (errorData?.message || res.statusText));
        }
    } catch (error) {
        alert('Erro ao excluir: ' + error.message);
    } finally {
        // Restaurar botão
        if (btnTexto && btnLoading) {
            btnTexto.style.display = 'inline-block';
            btnLoading.style.display = 'none';
        }
        
        // Limpar ID armazenado
        clienteIdParaExcluir = null;
    }
}

// Função para cancelar a exclusão
function cancelarExclusao() {
    document.getElementById('modal-exclusao').style.display = 'none';
    clienteIdParaExcluir = null;
}

// Função para exibir detalhes do cliente
async function verDetalhesCliente(id) {
    try {
        // Busca dados do cliente
        const res = await fetch(`${API_BASE}${id}/`, {
            credentials: 'same-origin'
        });
        
        if (!res.ok) throw new Error('Erro ao buscar detalhes do cliente');

        const cliente = await res.json();
        
        // Pegar referência ao modal de detalhes
        const modalDetalhes = document.getElementById('modal-detalhes');
        
        if (!modalDetalhes) {
            throw new Error('Modal de detalhes não encontrado');
        }

        // Preencher informações pessoais
        document.getElementById('detalhe-nome').textContent = 
            `${cliente.nome || ''} ${cliente.sobrenome || ''}`.trim() || 'Não informado';
        document.getElementById('detalhe-cpf').textContent = 
            cliente.cpf || 'Não informado';
        document.getElementById('detalhe-telefone').textContent = 
            cliente.telefone || 'Não informado';
        document.getElementById('detalhe-email').textContent = 
            cliente.email || 'Não informado';

        // Preencher endereço
        document.getElementById('detalhe-rua').textContent = 
            cliente.rua || 'Não informado';
        document.getElementById('detalhe-numero').textContent = 
            cliente.numero || 'Não informado';
        document.getElementById('detalhe-bairro').textContent = 
            cliente.bairro || 'Não informado';
        document.getElementById('detalhe-cidade').textContent = 
            cliente.cidade || 'Não informado';
        document.getElementById('detalhe-estado').textContent = 
            cliente.estado || 'Não informado';

        // Preencher estatísticas (dados mockados ou da API se disponível)
        document.getElementById('detalhe-total-compras').textContent = 
            cliente.total_compras || '0';
        document.getElementById('detalhe-ultima-compra').textContent = 
            cliente.ultima_compra || 'N/A';
        
        // Formatar data de cadastro se disponível
        if (cliente.data_cadastro) {
            const data = new Date(cliente.data_cadastro);
            document.getElementById('detalhe-data-cadastro').textContent = 
                data.toLocaleDateString('pt-BR');
        } else {
            document.getElementById('detalhe-data-cadastro').textContent = 'N/A';
        }

        // Guardar ID para edição posterior
        const btnEditarDetalhes = document.getElementById('editar-de-detalhes');
        if (btnEditarDetalhes) {
            btnEditarDetalhes.dataset.clienteId = id;
        }

        // Mostrar modal
        modalDetalhes.style.display = 'block';
    } catch (error) {
        console.error('Erro ao exibir detalhes:', error);
        alert('Erro ao carregar detalhes do cliente: ' + error.message);
    }
}

// Função de edição corrigida
async function editarCliente(id) {
    try {
        // Busca dados do cliente
        const res = await fetch(`${API_BASE}${id}/`, {
            credentials: 'same-origin'
        });
        
        if (!res.ok) throw new Error('Erro ao buscar cliente');

        const cliente = await res.json();
        
        // Pegar referências aos elementos do DOM
        const modalEdit = document.getElementById('modal-editar');
        const formEdit = document.getElementById('form-editar-cliente');
        
        if (!modalEdit || !formEdit) {
            throw new Error('Modal de edição não encontrado');
        }

        // Preencher campos do formulário (corrigido o seletor)
        Object.keys(cliente).forEach(key => {
            const input = formEdit.querySelector(`[name="${key}"]`);
            if (input) input.value = cliente[key] || '';
        });

        // Guardar ID para atualização
        formEdit.dataset.clienteId = id;

        // Mostrar modal
        modalEdit.style.display = 'block';
    } catch (error) {
        console.error('Erro ao editar:', error);
        alert('Erro ao carregar dados do cliente: ' + error.message);
    }
}

// Função para mostrar toast
function mostrarToast(mensagem, tipo = 'success') {
    const toastContainer = document.getElementById('toast-container');
    const toastMensagem = document.querySelector('.toast-mensagem');
    
    if (toastContainer && toastMensagem) {
        toastMensagem.textContent = mensagem;
        toastContainer.style.display = 'block';
        
        // Esconder após 3 segundos
        setTimeout(() => {
            toastContainer.style.display = 'none';
        }, 3000);
    }
}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do modal de criação
    const btnNovoCliente = document.getElementById('btn-novo-cliente');
    const btnPrimeiroCliente = document.getElementById('btn-primeiro-cliente');
    const modalCliente = document.getElementById('modal-cliente');
    const fecharModal = document.getElementById('fechar-modal');
    const cancelarForm = document.getElementById('cancelar-form');
    const formCliente = document.getElementById('form-cliente');
    
    // Elementos do modal de edição
    const modalEdit = document.getElementById('modal-editar');
    const fecharModalEdit = document.getElementById('fechar-modal-editar');
    const cancelarEditForm = document.getElementById('cancelar-edicao');
    const formEditCliente = document.getElementById('form-editar-cliente');

    // Elementos do modal de detalhes
    const modalDetalhes = document.getElementById('modal-detalhes');
    const fecharModalDetalhes = document.getElementById('fechar-modal-detalhes');
    const fecharDetalhes = document.getElementById('fechar-detalhes');
    const editarDeDetalhes = document.getElementById('editar-de-detalhes');

    // Elementos do modal de exclusão
    const modalExclusao = document.getElementById('modal-exclusao');
    const cancelarExclusaoBtn = document.getElementById('cancelar-exclusao');
    const confirmarExclusaoBtn = document.getElementById('confirmar-exclusao');
    const fecharModalExclusao = document.querySelector('#modal-exclusao .modal-close');

    // Event listeners para modal de criação
    if (btnNovoCliente && modalCliente) {
        btnNovoCliente.addEventListener('click', () => {
            modalCliente.style.display = 'block';
        });
    }
    
    if (btnPrimeiroCliente && modalCliente) {
        btnPrimeiroCliente.addEventListener('click', () => {
            modalCliente.style.display = 'block';
        });
    }
    
    if (fecharModal && modalCliente) {
        fecharModal.addEventListener('click', () => {
            modalCliente.style.display = 'none';
        });
    }
    
    if (cancelarForm && modalCliente) {
        cancelarForm.addEventListener('click', () => {
            modalCliente.style.display = 'none';
        });
    }

    // Event listeners para modal de edição
    if (fecharModalEdit && modalEdit) {
        fecharModalEdit.addEventListener('click', () => {
            modalEdit.style.display = 'none';
        });
    }
    
    if (cancelarEditForm && modalEdit) {
        cancelarEditForm.addEventListener('click', () => {
            modalEdit.style.display = 'none';
        });
    }

    // Formulário de criação
    if (formCliente) {
        formCliente.addEventListener('submit', async function(e) {
            e.preventDefault();
            const payload = Object.fromEntries(new FormData(this).entries());
            
            try {
                const res = await criarCliente(payload);
                if (res.ok) {
                    this.reset();
                    if (modalCliente) modalCliente.style.display = 'none';
                    await fetchClientes();
                    mostrarToast('Cliente criado com sucesso!');
                } else {
                    const err = await res.json().catch(() => null);
                    alert('Erro ao salvar: ' + (err && JSON.stringify(err) || res.statusText));
                }
            } catch (error) {
                alert('Erro ao salvar: ' + error.message);
            }
        });
    }

    // Formulário de edição
    if (formEditCliente) {
        formEditCliente.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const clienteId = this.dataset.clienteId;
            if (!clienteId) {
                alert('ID do cliente não encontrado');
                return;
            }
            
            const payload = Object.fromEntries(new FormData(this).entries());
            
            try {
                const res = await atualizarCliente(clienteId, payload);
                
                if (res.ok) {
                    this.reset();
                    if (modalEdit) modalEdit.style.display = 'none';
                    await fetchClientes();
                    mostrarToast('Cliente atualizado com sucesso!');
                } else {
                    const err = await res.json().catch(() => null);
                    alert('Erro ao atualizar: ' + (err && JSON.stringify(err) || res.statusText));
                }
            } catch (error) {
                alert('Erro ao atualizar: ' + error.message);
            }
        });
    }

    // Event listeners para modal de detalhes
    if (fecharModalDetalhes && modalDetalhes) {
        fecharModalDetalhes.addEventListener('click', () => {
            modalDetalhes.style.display = 'none';
        });
    }
    
    if (fecharDetalhes && modalDetalhes) {
        fecharDetalhes.addEventListener('click', () => {
            modalDetalhes.style.display = 'none';
        });
    }

    // Botão "Editar" dentro do modal de detalhes
    if (editarDeDetalhes && modalDetalhes) {
        editarDeDetalhes.addEventListener('click', function() {
            const clienteId = this.dataset.clienteId;
            if (clienteId) {
                modalDetalhes.style.display = 'none';
                editarCliente(clienteId);
            }
        });
    }

    // Event listeners para modal de exclusão
    if (cancelarExclusaoBtn && modalExclusao) {
        cancelarExclusaoBtn.addEventListener('click', cancelarExclusao);
    }
    
    if (confirmarExclusaoBtn && modalExclusao) {
        confirmarExclusaoBtn.addEventListener('click', async function() {
            if (clienteIdParaExcluir) {
                await confirmarExclusao(clienteIdParaExcluir);
            }
        });
    }
    
    // Botão de fechar (X) no modal de exclusão
    if (fecharModalExclusao && modalExclusao) {
        fecharModalExclusao.addEventListener('click', cancelarExclusao);
    }

    // Fechar modais clicando fora
    window.addEventListener('click', (event) => {
        if (modalCliente && event.target === modalCliente) {
            modalCliente.style.display = 'none';
        }
        if (modalEdit && event.target === modalEdit) {
            modalEdit.style.display = 'none';
        }
        if (modalDetalhes && event.target === modalDetalhes) {
            modalDetalhes.style.display = 'none';
        }
        if (modalExclusao && event.target === modalExclusao) {
            cancelarExclusao();
        }
    });

    // Inicializar busca de clientes
    fetchClientes();
});
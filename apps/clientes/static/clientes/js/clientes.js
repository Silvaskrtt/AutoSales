// Estado da aplicação
let clients = [];
let editingClient = null;
let pendingDeleteId = null;

// Configuração da API
const API_BASE_URL = '/api/clientes/';

// Utilitários de Formatação
function formatCPF(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    input.value = value;
}

function formatPhone(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    if (value.length > 6) {
        value = value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
    } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    }
    input.value = value;
}

// Funções de API
async function fetchClients() {
    try {
        console.log('Buscando clientes de:', API_BASE_URL);
        
        const response = await fetch(API_BASE_URL, {
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        });
        
        console.log('Status da resposta:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Dados recebidos:', data);
        
        clients = Array.isArray(data) ? data : [];
        console.log('Clientes processados:', clients.length);
        
        renderTable();
        updateClientCount();
        checkLimit();
    } catch (error) {
        console.error('Erro ao carregar clientes:', error);
        showToast('Erro ao carregar clientes', 'error');
        clients = [];
        renderTable();
    }
}

async function createClient(clientData) {
    try {
        console.log('Enviando dados:', clientData);
        
        const dataToSend = {
            nome: clientData.nome,
            sobrenome: clientData.sobrenome,
            cpf: clientData.cpf,
            telefone: clientData.telefone,
            email: clientData.email,
            rua: clientData.rua || '',
            numero: clientData.numero || '',
            bairro: clientData.bairro || '',
            cidade: clientData.cidade || '',
            estado: clientData.estado || '',
            is_active: true
        };

        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(dataToSend)
        });
        
        console.log('Status da resposta:', response.status);
        
        if (response.ok) {
            const newClient = await response.json();
            console.log('Cliente criado:', newClient);
            
            if (!Array.isArray(clients)) {
                clients = [];
            }
            
            clients.push(newClient);
            
            renderTable();
            updateClientCount();
            showToast('Cliente cadastrado com sucesso!', 'success');
            return { isOk: true, data: newClient };
        } else {
            const errorData = await response.json();
            console.error('Erro detalhado:', errorData);
            showToast('Erro ao salvar cliente', 'error');
            return { isOk: false, error: errorData };
        }
    } catch (error) {
        console.error('Erro completo:', error);
        showToast('Erro ao salvar cliente', 'error');
        return { isOk: false, error };
    }
}

async function updateClient(clientData) {
    try {
        const response = await fetch(`${API_BASE_URL}${clientData.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(clientData)
        });
        
        if (response.ok) {
            const updatedClient = await response.json();
            
            if (!Array.isArray(clients)) {
                clients = [];
            }
            
            const index = clients.findIndex(c => c.id === updatedClient.id);
            if (index !== -1) {
                clients[index] = updatedClient;
            } else {
                clients.push(updatedClient);
            }
            
            renderTable();
            showToast('Cliente atualizado com sucesso!', 'success');
            return { isOk: true };
        }
        throw new Error('Erro ao atualizar cliente');
    } catch (error) {
        console.error('Erro ao atualizar:', error);
        showToast('Erro ao atualizar cliente', 'error');
        return { isOk: false };
    }
}

async function deleteClient(clientId) {
    try {
        const response = await fetch(`${API_BASE_URL}${clientId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            if (Array.isArray(clients)) {
                clients = clients.filter(c => c.id !== clientId);
            } else {
                clients = [];
            }
            
            renderTable();
            updateClientCount();
            showToast('Cliente excluído com sucesso!', 'success');
            return { isOk: true };
        }
        throw new Error('Erro ao excluir cliente');
    } catch (error) {
        console.error('Erro ao excluir:', error);
        showToast('Erro ao excluir cliente', 'error');
        return { isOk: false };
    }
}

async function toggleClientStatus(clientId, currentStatus) {
    const newStatus = currentStatus === 'ativo' ? 'inativo' : 'ativo';
    const client = clients.find(c => c.id === clientId);
    
    if (client) {
        client.is_active = newStatus === 'ativo';
        return await updateClient(client);
    }
}

// Funções de UI
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-emerald-500/20 border-emerald-500/50' : 
                    type === 'error' ? 'bg-red-500/20 border-red-500/50' : 
                    'bg-cyan-500/20 border-cyan-500/50';
    const textColor = type === 'success' ? 'text-emerald-400' : 
                      type === 'error' ? 'text-red-400' : 
                      'text-cyan-400';
    
    toast.className = `toast glass-card ${bgColor} ${textColor} px-6 py-4 rounded-xl border flex items-center gap-3`;
    
    const icon = type === 'success' ? 
        '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>' :
        type === 'error' ?
        '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>' :
        '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>';
    
    toast.innerHTML = `${icon}<span>${message}</span>`;
    container.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

function updateClientCount() {
    const countEl = document.getElementById('client-count');
    if (!countEl) return;
    
    const count = clients.length;
    countEl.textContent = `${count} cliente${count !== 1 ? 's' : ''}`;
}

function checkLimit() {
    const warning = document.getElementById('limit-warning');
    if (!warning) return;
    
    if (clients.length >= 999) {
        warning.classList.remove('hidden');
    } else {
        warning.classList.add('hidden');
    }
}

function renderTable() {
    const tbody = document.getElementById('clients-table');
    if (!tbody) return;
    
    console.log('Renderizando tabela com', clients.length, 'clientes');
    
    if (clients.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="px-4 py-12 text-center text-slate-500">
                    <div class="flex flex-col items-center gap-2">
                        <svg class="w-12 h-12 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                        </svg>
                        <span>Nenhum cliente cadastrado</span>
                    </div>
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = clients.map(client => {
        const isActive = client.is_active;
        const isPendingDelete = pendingDeleteId === client.id;
        
        return `
            <tr class="glass-table-row" data-id="${client.id}">
                <td class="px-4 py-4">
                    <div class="font-medium text-white">${client.nome} ${client.sobrenome}</div>
                </td>
                <td class="px-4 py-4 text-slate-300 text-sm">${client.cpf}</td>
                <td class="px-4 py-4 text-slate-300 text-sm hidden md:table-cell">${client.telefone}</td>
                <td class="px-4 py-4 text-slate-300 text-sm hidden lg:table-cell">${client.email}</td>
                <td class="px-4 py-4 text-slate-300 text-sm hidden xl:table-cell">
                    ${client.cidade ? `${client.cidade}${client.estado ? '/' + client.estado : ''}` : '-'}
                </td>
                <td class="px-4 py-4">
                    <button onclick="window.toggleStatus(${client.id})" 
                        class="px-3 py-1.5 rounded-lg text-xs font-medium ${isActive ? 'status-active' : 'status-inactive'} cursor-pointer transition-all hover:scale-105">
                        ${isActive ? 'Ativo' : 'Inativo'}
                    </button>
                </td>
                <td class="px-4 py-4">
                    <div class="flex items-center justify-center gap-2">
                        ${isPendingDelete ? `
                            <button onclick="window.confirmDelete(${client.id})" 
                                class="action-btn p-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 delete-confirm"
                                title="Confirmar exclusão">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                                </svg>
                            </button>
                            <button onclick="window.cancelDelete()" 
                                class="action-btn p-2 rounded-lg bg-slate-500/20 text-slate-400 hover:bg-slate-500/30"
                                title="Cancelar">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                            </button>
                        ` : `
                            <button onclick="window.editClient(${client.id})" 
                                class="action-btn p-2 rounded-lg bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30"
                                title="Editar">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                </svg>
                            </button>
                            <button onclick="window.initiateDelete(${client.id})" 
                                class="action-btn p-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30"
                                title="Excluir">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                </svg>
                            </button>
                        `}
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// Handlers de Ações
async function handleSubmit(e) {
    e.preventDefault();
    
    if (clients.length >= 999 && !editingClient) {
        showToast('Limite de 999 clientes atingido!', 'error');
        return;
    }

    const form = e.target;
    const submitBtn = document.getElementById('submit-btn');
    const submitText = document.getElementById('submit-text');
    const submitIcon = document.getElementById('submit-icon');
    
    submitBtn.disabled = true;
    submitText.textContent = editingClient ? 'Atualizando...' : 'Salvando...';
    submitIcon.innerHTML = '<div class="loading-spinner w-5 h-5 rounded-full"></div>';

    const formData = {
        nome: form.nome.value,
        sobrenome: form.sobrenome.value,
        cpf: form.cpf.value,
        telefone: form.telefone.value,
        email: form.email.value,
        rua: form.rua.value || '',
        numero: form.numero.value || '',
        bairro: form.bairro.value || '',
        cidade: form.cidade.value || '',
        estado: form.estado.value || '',
        is_active: editingClient ? editingClient.is_active : true
    };

    let result;
    if (editingClient) {
        formData.id = editingClient.id;
        result = await updateClient(formData);
    } else {
        result = await createClient(formData);
    }

    submitBtn.disabled = false;
    submitText.textContent = 'Salvar Cliente';
    submitIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>';

    if (result.isOk) {
        form.reset();
        cancelEdit();
    }
}

function editClient(id) {
    const client = clients.find(c => c.id === id);
    if (!client) return;

    editingClient = client;
    
    document.getElementById('nome').value = client.nome || '';
    document.getElementById('sobrenome').value = client.sobrenome || '';
    document.getElementById('cpf').value = client.cpf || '';
    document.getElementById('telefone').value = client.telefone || '';
    document.getElementById('email').value = client.email || '';
    document.getElementById('rua').value = client.rua || '';
    document.getElementById('numero').value = client.numero || '';
    document.getElementById('bairro').value = client.bairro || '';
    document.getElementById('cidade').value = client.cidade || '';
    document.getElementById('estado').value = client.estado || '';

    document.getElementById('form-title-text').textContent = 'Editar Cliente';
    document.getElementById('submit-text').textContent = 'Atualizar';
    document.getElementById('cancel-btn').classList.remove('hidden');
    
    document.getElementById('client-form').scrollIntoView({ behavior: 'smooth' });
}

function cancelEdit() {
    editingClient = null;
    document.getElementById('client-form').reset();
    document.getElementById('form-title-text').textContent = 'Cadastrar Novo Cliente';
    document.getElementById('submit-text').textContent = 'Salvar Cliente';
    document.getElementById('cancel-btn').classList.add('hidden');
}

function initiateDelete(id) {
    pendingDeleteId = id;
    renderTable();
}

function cancelDelete() {
    pendingDeleteId = null;
    renderTable();
}

async function confirmDelete(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row) {
        row.style.opacity = '0.5';
        row.style.pointerEvents = 'none';
    }

    const result = await deleteClient(id);
    
    pendingDeleteId = null;
    
    if (result.isOk && editingClient && editingClient.id === id) {
        cancelEdit();
    }
}

async function toggleStatus(id) {
    const client = clients.find(c => c.id === id);
    if (!client) return;

    const result = await toggleClientStatus(id, client.is_active ? 'ativo' : 'inativo');
    
    if (result && result.isOk) {
        showToast(`Cliente ${client.is_active ? 'ativado' : 'desativado'}!`, 'info');
        fetchClients();
    }
}

// Utilitários
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    
    if (!cookieValue) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            cookieValue = csrfToken.value;
        }
    }
    
    return cookieValue;
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM carregado, inicializando...');
    
    clients = [];
    fetchClients();
    
    window.formatCPF = formatCPF;
    window.formatPhone = formatPhone;
    window.handleSubmit = handleSubmit;
    window.editClient = editClient;
    window.cancelEdit = cancelEdit;
    window.initiateDelete = initiateDelete;
    window.cancelDelete = cancelDelete;
    window.confirmDelete = confirmDelete;
    window.toggleStatus = toggleStatus;
    
    console.log('Inicialização completa');
});
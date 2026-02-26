// veiculos/static/veiculos/js/veiculos.js

// Estado da aplicação - com prefixo veiculo para evitar conflitos
let veiculosList = [];
let veiculoEditing = null;
let veiculoPendingDeleteId = null;

// Configuração da API
const VEICULOS_API_URL = '/api/veiculos/';

// Utilitários de Formatação
function formatPlaca(input) {
    let value = input.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
    
    // Formato Mercosul: AAA1A23
    if (value.length === 7 && /^[A-Z]{3}\d[A-Z]\d{2}$/.test(value)) {
        // Já está no formato correto
    }
    // Formato Antigo: AAA-1234
    else if (value.length === 7 && /^[A-Z]{3}\d{4}$/.test(value)) {
        value = value.substring(0, 3) + '-' + value.substring(3);
    }
    
    input.value = value;
}

function formatPreco(input) {
    let value = input.value.replace(/\D/g, '');
    if (value) {
        value = (parseInt(value) / 100).toFixed(2);
        input.value = value;
    }
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Funções de API
async function fetchVeiculos() {
    try {
        console.log('Buscando veículos de:', VEICULOS_API_URL);
        
        const response = await fetch(VEICULOS_API_URL, {
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        });
        
        console.log('Status da resposta:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Resposta de erro:', errorText);
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Dados recebidos:', data);
        
        veiculosList = Array.isArray(data) ? data : [];
        console.log('Veículos processados:', veiculosList);
        
        renderTable();
        updateVeiculoCount();
        checkLimit();
    } catch (error) {
        console.error('Erro detalhado ao carregar veículos:', error);
        showToast('Erro ao carregar veículos: ' + error.message, 'error');
        veiculosList = [];
        renderTable();
    }
}

async function createVeiculo(veiculoData) {
    try {
        console.log('Enviando dados:', veiculoData);
        
        // Criar FormData para enviar arquivo
        const formData = new FormData();
        
        // Adicionar campos ao FormData
        Object.keys(veiculoData).forEach(key => {
            if (veiculoData[key] !== null && veiculoData[key] !== undefined) {
                // Tratar números para evitar problemas de formatação
                if (key === 'ano' || key === 'preco') {
                    formData.append(key, veiculoData[key].toString());
                } else {
                    formData.append(key, veiculoData[key]);
                }
            }
        });

        // Log do FormData para debugging
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }

        const response = await fetch(VEICULOS_API_URL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        });
        
        console.log('Status da resposta:', response.status);
        
        if (response.ok) {
            const newVeiculo = await response.json();
            console.log('Veículo criado:', newVeiculo);
            
            if (!Array.isArray(veiculosList)) {
                veiculosList = [];
            }
            
            veiculosList.push(newVeiculo);
            
            renderTable();
            updateVeiculoCount();
            showToast('Veículo cadastrado com sucesso!', 'success');
            return { isOk: true, data: newVeiculo };
        } else {
            const errorData = await response.json();
            console.error('Erro detalhado:', errorData);
            
            // Extrair mensagens de erro detalhadas
            let errorMessage = 'Erro ao salvar veículo';
            if (errorData && typeof errorData === 'object') {
                if (errorData.placa) {
                    errorMessage = `Erro na placa: ${errorData.placa}`;
                } else if (errorData.ano) {
                    errorMessage = `Erro no ano: ${errorData.ano}`;
                } else if (errorData.preco) {
                    errorMessage = `Erro no preço: ${errorData.preco}`;
                } else if (errorData.modelo) {
                    errorMessage = `Erro no modelo: ${errorData.modelo}`;
                } else if (errorData.non_field_errors) {
                    errorMessage = errorData.non_field_errors[0];
                }
            }
            
            showToast(errorMessage, 'error');
            return { isOk: false, error: errorData };
        }
    } catch (error) {
        console.error('Erro completo:', error);
        showToast('Erro ao salvar veículo: ' + error.message, 'error');
        return { isOk: false, error };
    }
}

async function updateVeiculo(veiculoData) {
    try {
        console.log('Atualizando veículo:', veiculoData);
        
        // Criar FormData para enviar arquivo
        const formData = new FormData();
        
        // Adicionar campos ao FormData
        Object.keys(veiculoData).forEach(key => {
            if (veiculoData[key] !== null && veiculoData[key] !== undefined) {
                if (key === 'ano' || key === 'preco') {
                    formData.append(key, veiculoData[key].toString());
                } else {
                    formData.append(key, veiculoData[key]);
                }
            }
        });

        // Importante: Para PUT, o Django REST framework espera todos os campos
        const response = await fetch(`${VEICULOS_API_URL}${veiculoData.id}/`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        });
        
        if (response.ok) {
            const updatedVeiculo = await response.json();
            
            if (!Array.isArray(veiculosList)) {
                veiculosList = [];
            }
            
            const index = veiculosList.findIndex(v => v.id === updatedVeiculo.id);
            if (index !== -1) {
                veiculosList[index] = updatedVeiculo;
            } else {
                veiculosList.push(updatedVeiculo);
            }
            
            renderTable();
            showToast('Veículo atualizado com sucesso!', 'success');
            return { isOk: true, data: updatedVeiculo };
        } else {
            const errorData = await response.json();
            console.error('Erro detalhado:', errorData);
            
            let errorMessage = 'Erro ao atualizar veículo';
            if (errorData && typeof errorData === 'object') {
                if (errorData.placa) {
                    errorMessage = `Erro na placa: ${errorData.placa}`;
                } else if (errorData.ano) {
                    errorMessage = `Erro no ano: ${errorData.ano}`;
                }
            }
            
            showToast(errorMessage, 'error');
            return { isOk: false, error: errorData };
        }
    } catch (error) {
        console.error('Erro ao atualizar:', error);
        showToast('Erro ao atualizar veículo: ' + error.message, 'error');
        return { isOk: false };
    }
}

async function deleteVeiculo(veiculoId) {
    try {
        const response = await fetch(`${VEICULOS_API_URL}${veiculoId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            if (Array.isArray(veiculosList)) {
                veiculosList = veiculosList.filter(v => v.id !== veiculoId);
            } else {
                veiculosList = [];
            }
            
            renderTable();
            updateVeiculoCount();
            showToast('Veículo excluído com sucesso!', 'success');
            return { isOk: true };
        }
        throw new Error('Erro ao excluir veículo');
    } catch (error) {
        console.error('Erro ao excluir:', error);
        showToast('Erro ao excluir veículo', 'error');
        return { isOk: false };
    }
}

async function toggleVeiculoStatus(veiculoId) {
    const veiculo = veiculosList.find(v => v.id === veiculoId);
    
    if (veiculo) {
        veiculo.is_active = !veiculo.is_active;
        return await updateVeiculo(veiculo);
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

function updateVeiculoCount() {
    const countEl = document.getElementById('veiculo-count');
    if (!countEl) return;
    
    const count = veiculosList.length;
    countEl.textContent = `${count} veículo${count !== 1 ? 's' : ''}`;
}

function checkLimit() {
    const warning = document.getElementById('limit-warning');
    if (!warning) return;
    
    if (veiculosList.length >= 999) {
        warning.classList.remove('hidden');
    } else {
        warning.classList.add('hidden');
    }
}

function getStatusClass(status) {
    const statusMap = {
        'DISPONIVEL': 'status-disponivel',
        'VENDIDO': 'status-vendido',
        'RESERVADO': 'status-reservado',
        'MANUTENCAO': 'status-manutencao'
    };
    return statusMap[status] || 'status-disponivel';
}

function getStatusText(status) {
    const statusMap = {
        'DISPONIVEL': 'Disponível',
        'VENDIDO': 'Vendido',
        'RESERVADO': 'Reservado',
        'MANUTENCAO': 'Manutenção'
    };
    return statusMap[status] || status;
}

function renderTable() {
    const tbody = document.getElementById('veiculos-table');
    if (!tbody) return;
    
    if (veiculosList.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="px-4 py-12 text-center text-slate-500">
                    <div class="flex flex-col items-center gap-2">
                        <svg class="w-12 h-12 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        </svg>
                        <span>Nenhum veículo cadastrado</span>
                    </div>
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = veiculosList.map(veiculo => {
        const isActive = veiculo.is_active;
        const isPendingDelete = veiculoPendingDeleteId === veiculo.id;
        const imagemUrl = veiculo.imagem_veiculo ? veiculo.imagem_veiculo : '/static/veiculos/img/default-car.png';
        
        return `
            <tr class="glass-table-row" data-id="${veiculo.id}">
                <td class="px-4 py-4">
                    <img src="${imagemUrl}" alt="${veiculo.modelo}" class="table-image" onerror="this.src='/static/veiculos/img/default-car.png'">
                </td>
                <td class="px-4 py-4">
                    <div class="font-medium text-white">${veiculo.modelo_nome || veiculo.modelo}</div>
                    <div class="text-xs text-slate-400">${veiculo.marca_nome || ''}</div>
                </td>
                <td class="px-4 py-4 text-slate-300 text-sm font-mono">${veiculo.placa}</td>
                <td class="px-4 py-4 text-slate-300 text-sm hidden md:table-cell">
                    ${veiculo.ano} • ${veiculo.cor}
                </td>
                <td class="px-4 py-4 text-slate-300 text-sm hidden lg:table-cell font-medium text-cyan-300">
                    ${formatCurrency(veiculo.preco)}
                </td>
                <td class="px-4 py-4">
                    <span class="px-3 py-1.5 rounded-lg text-xs font-medium ${getStatusClass(veiculo.status)}">
                        ${getStatusText(veiculo.status)}
                    </span>
                </td>
                <td class="px-4 py-4">
                    <button onclick="window.veiculoToggleStatus(${veiculo.id})" 
                        class="px-3 py-1.5 rounded-lg text-xs font-medium ${isActive ? 'status-active' : 'status-inactive'} cursor-pointer transition-all hover:scale-105">
                        ${isActive ? 'Ativo' : 'Inativo'}
                    </button>
                </td>
                <td class="px-4 py-4">
                    <div class="flex items-center justify-center gap-2">
                        ${isPendingDelete ? `
                            <button onclick="window.veiculoConfirmDelete(${veiculo.id})" 
                                class="action-btn p-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 delete-confirm"
                                title="Confirmar exclusão">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                                </svg>
                            </button>
                            <button onclick="window.veiculoCancelDelete()" 
                                class="action-btn p-2 rounded-lg bg-slate-500/20 text-slate-400 hover:bg-slate-500/30"
                                title="Cancelar">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                            </button>
                        ` : `
                            <button onclick="window.veiculoEdit(${veiculo.id})" 
                                class="action-btn p-2 rounded-lg bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30"
                                title="Editar">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                </svg>
                            </button>
                            <button onclick="window.veiculoInitiateDelete(${veiculo.id})" 
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
async function veiculoHandleSubmit(e) {
    e.preventDefault();
    
    if (veiculosList.length >= 999 && !veiculoEditing) {
        showToast('Limite de 999 veículos atingido!', 'error');
        return;
    }

    const form = e.target;
    const submitBtn = document.getElementById('submit-btn');
    const submitText = document.getElementById('submit-text');
    const submitIcon = document.getElementById('submit-icon');
    
    // Show loading state
    submitBtn.disabled = true;
    submitText.textContent = veiculoEditing ? 'Atualizando...' : 'Salvando...';
    submitIcon.innerHTML = '<div class="loading-spinner w-5 h-5 rounded-full"></div>';

    // Criar objeto com os dados do formulário
    const formData = {
        modelo: form.modelo.value,
        placa: form.placa.value.toUpperCase(),
        ano: parseInt(form.ano.value),
        cor: form.cor.value,
        preco: parseFloat(form.preco.value),
        status: form.status.value,
        is_active: veiculoEditing ? veiculoEditing.is_active : true
    };

    // Adicionar imagem se selecionada
    const imagemInput = document.getElementById('imagem_veiculo');
    if (imagemInput.files.length > 0) {
        formData.imagem_veiculo = imagemInput.files[0];
    }

    let result;
    if (veiculoEditing) {
        formData.id = veiculoEditing.id;
        result = await updateVeiculo(formData);
    } else {
        result = await createVeiculo(formData);
    }

    // Reset button state
    submitBtn.disabled = false;
    submitText.textContent = 'Salvar Veículo';
    submitIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>';

    if (result.isOk) {
        form.reset();
        clearImagePreview();
        veiculoCancelEdit();
    }
}

function veiculoEdit(id) {
    const veiculo = veiculosList.find(v => v.id === id);
    if (!veiculo) return;

    veiculoEditing = veiculo;
    
    document.getElementById('modelo').value = veiculo.modelo || '';
    document.getElementById('placa').value = veiculo.placa || '';
    document.getElementById('ano').value = veiculo.ano || '';
    document.getElementById('cor').value = veiculo.cor || '';
    document.getElementById('preco').value = veiculo.preco || '';
    document.getElementById('status').value = veiculo.status || 'DISPONIVEL';

    // Mostrar preview da imagem se existir
    if (veiculo.imagem_veiculo) {
        const preview = document.getElementById('image-preview');
        const previewImg = preview.querySelector('img');
        previewImg.src = veiculo.imagem_veiculo;
        preview.classList.remove('hidden');
    }

    document.getElementById('form-title-text').textContent = 'Editar Veículo';
    document.getElementById('submit-text').textContent = 'Atualizar';
    document.getElementById('cancel-btn').classList.remove('hidden');
    
    document.getElementById('veiculo-form').scrollIntoView({ behavior: 'smooth' });
}

function veiculoCancelEdit() {
    veiculoEditing = null;
    document.getElementById('veiculo-form').reset();
    clearImagePreview();
    document.getElementById('form-title-text').textContent = 'Cadastrar Novo Veículo';
    document.getElementById('submit-text').textContent = 'Salvar Veículo';
    document.getElementById('cancel-btn').classList.add('hidden');
}

function veiculoInitiateDelete(id) {
    veiculoPendingDeleteId = id;
    renderTable();
}

function veiculoCancelDelete() {
    veiculoPendingDeleteId = null;
    renderTable();
}

async function veiculoConfirmDelete(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row) {
        row.style.opacity = '0.5';
        row.style.pointerEvents = 'none';
    }

    const result = await deleteVeiculo(id);
    
    veiculoPendingDeleteId = null;
    
    if (result.isOk && veiculoEditing && veiculoEditing.id === id) {
        veiculoCancelEdit();
    }
}

async function veiculoToggleStatus(id) {
    const veiculo = veiculosList.find(v => v.id === id);
    if (!veiculo) return;

    const result = await toggleVeiculoStatus(id);
    
    if (result && result.isOk) {
        showToast(`Veículo ${veiculo.is_active ? 'ativado' : 'desativado'}!`, 'info');
        fetchVeiculos();
    }
}

// Funções de imagem
function handleImagePreview(input) {
    const preview = document.getElementById('image-preview');
    const previewImg = preview.querySelector('img');
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            preview.classList.remove('hidden');
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}

function clearImagePreview() {
    const preview = document.getElementById('image-preview');
    const imagemInput = document.getElementById('imagem_veiculo');
    
    preview.classList.add('hidden');
    preview.querySelector('img').src = '';
    imagemInput.value = '';
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
    console.log('DOM carregado, inicializando app de veículos...');
    
    veiculosList = [];
    
    fetchVeiculos();
    
    // Adicionar evento de preview de imagem
    const imagemInput = document.getElementById('imagem_veiculo');
    if (imagemInput) {
        imagemInput.addEventListener('change', function() {
            handleImagePreview(this);
        });
    }
    
    // Registrar funções no window com prefixo para evitar conflitos
    window.formatPlaca = formatPlaca;
    window.formatPreco = formatPreco;
    window.veiculoHandleSubmit = veiculoHandleSubmit;
    window.veiculoEdit = veiculoEdit;
    window.veiculoCancelEdit = veiculoCancelEdit;
    window.veiculoInitiateDelete = veiculoInitiateDelete;
    window.veiculoCancelDelete = veiculoCancelDelete;
    window.veiculoConfirmDelete = veiculoConfirmDelete;
    window.veiculoToggleStatus = veiculoToggleStatus;
    window.clearImagePreview = clearImagePreview;
    
    console.log('Inicialização do app de veículos completa');
});
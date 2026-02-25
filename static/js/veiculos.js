// State
let vehicles = [];
let currentFilter = 'all';
let vehicleToDelete = null;
let isEditing = false;

// Default config
const defaultConfig = {
    page_title: 'Vehicle Inventory',
    add_button_text: 'Add Vehicle',
    background_color: '#faf5ff',
    surface_color: '#ffffff',
    text_color: '#1f2937',
    primary_action_color: '#7c3aed',
    secondary_action_color: '#8b5cf6'
};

// Car brands and their SVG colors
const brandColors = {
    'toyota': '#eb0a1e',
    'honda': '#cc0000',
    'ford': '#003478',
    'chevrolet': '#d4a636',
    'bmw': '#0066b1',
    'mercedes': '#00adef',
    'audi': '#bb0a30',
    'volkswagen': '#001e50',
    'nissan': '#c3002f',
    'hyundai': '#002c5f',
    'default': '#7c3aed'
};

// Status badge config
const statusConfig = {
    available: { 
        bg: 'bg-emerald-100 dark:bg-emerald-900/30', 
        text: 'text-emerald-700 dark:text-emerald-300', 
        label: 'Available' 
    },
    reserved: { 
        bg: 'bg-amber-100 dark:bg-amber-900/30', 
        text: 'text-amber-700 dark:text-amber-300', 
        label: 'Reserved' 
    },
    sold: { 
        bg: 'bg-red-100 dark:bg-red-900/30', 
        text: 'text-red-700 dark:text-red-300', 
        label: 'Sold' 
    }
};

// Helper Functions
function getBrandColor(brand) {
    return brandColors[brand.toLowerCase()] || brandColors.default;
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', { 
        style: 'currency', 
        currency: 'USD', 
        minimumFractionDigits: 0 
    }).format(price);
}

function formatMileage(mileage) {
    return new Intl.NumberFormat('en-US').format(mileage) + ' mi';
}

function generateCarSVG(color, vehicleColor) {
    const bodyColor = vehicleColor || '#6b7280';
    return `
        <svg viewBox="0 0 200 100" class="w-full h-full">
            <defs>
                <linearGradient id="bodyGrad${color.replace('#', '')}" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:${bodyColor};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:${bodyColor};stop-opacity:0.7" />
                </linearGradient>
                <linearGradient id="windowGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#1e293b;stop-opacity:0.9" />
                    <stop offset="100%" style="stop-color:#334155;stop-opacity:0.8" />
                </linearGradient>
            </defs>
            <!-- Car body -->
            <path d="M30 60 L45 35 L85 30 L130 30 L155 45 L175 50 L175 65 L25 65 L25 55 Z" fill="url(#bodyGrad${color.replace('#', '')})" />
            <!-- Windows -->
            <path d="M50 38 L80 33 L80 55 L48 55 Z" fill="url(#windowGrad)" />
            <path d="M85 33 L125 33 L145 48 L85 55 Z" fill="url(#windowGrad)" />
            <!-- Wheels -->
            <circle cx="55" cy="65" r="15" fill="#1f2937" />
            <circle cx="55" cy="65" r="10" fill="#374151" />
            <circle cx="55" cy="65" r="5" fill="#6b7280" />
            <circle cx="145" cy="65" r="15" fill="#1f2937" />
            <circle cx="145" cy="65" r="10" fill="#374151" />
            <circle cx="145" cy="65" r="5" fill="#6b7280" />
            <!-- Headlights -->
            <ellipse cx="170" cy="52" rx="4" ry="6" fill="#fef08a" opacity="0.9" />
            <ellipse cx="30" cy="55" rx="3" ry="5" fill="#fca5a5" opacity="0.8" />
            <!-- Details -->
            <line x1="25" y1="58" x2="175" y2="58" stroke="#ffffff" stroke-width="1" opacity="0.3" />
        </svg>
    `;
}

function showToast(message) {
    const toast = document.getElementById('toast');
    document.getElementById('toast-message').textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
}

// Vehicle Card Creation
function createVehicleCard(vehicle) {
    const status = statusConfig[vehicle.status] || statusConfig.available;
    const brandColor = getBrandColor(vehicle.brand);

    const card = document.createElement('div');
    card.className = 'card-hover bg-white dark:bg-gray-800 rounded-2xl shadow-lg shadow-purple-500/5 dark:shadow-purple-500/10 overflow-hidden border border-purple-100 dark:border-purple-900/50 animate-fade-in';
    card.dataset.vehicleId = vehicle.__backendId;
    
    card.innerHTML = `
        <div class="relative h-36 bg-gradient-to-br from-purple-100 to-violet-100 dark:from-purple-900/30 dark:to-violet-900/30 flex items-center justify-center p-4">
            ${generateCarSVG(brandColor, vehicle.color)}
            <span class="absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-semibold ${status.bg} ${status.text}">${status.label}</span>
        </div>
        <div class="p-4">
            <div class="flex items-start justify-between mb-2">
                <div>
                    <h3 class="font-bold text-gray-800 dark:text-white">${vehicle.brand} ${vehicle.model}</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400">${vehicle.year} • ${vehicle.color}</p>
                </div>
            </div>
            <div class="flex items-center gap-2 mb-3">
                <span class="text-xs px-2 py-1 rounded-lg bg-purple-50 dark:bg-purple-900/30 text-purple-600 dark:text-purple-300">${formatMileage(vehicle.mileage)}</span>
            </div>
            <div class="flex items-center justify-between pt-3 border-t border-gray-100 dark:border-gray-700">
                <span class="text-lg font-bold text-purple-600 dark:text-purple-400">${formatPrice(vehicle.price)}</span>
                <div class="flex gap-2">
                    <button class="edit-btn p-2 rounded-lg text-gray-400 hover:text-purple-600 hover:bg-purple-50 dark:hover:bg-purple-900/30 transition-all" aria-label="Edit vehicle">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                    </button>
                    <button class="delete-btn p-2 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 transition-all" aria-label="Delete vehicle">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `;

    card.querySelector('.edit-btn').addEventListener('click', () => openEditModal(vehicle));
    card.querySelector('.delete-btn').addEventListener('click', () => openDeleteModal(vehicle));

    return card;
}

// Render Vehicles
function renderVehicles() {
    const grid = document.getElementById('vehicle-grid');
    const emptyState = document.getElementById('empty-state');
    const limitWarning = document.getElementById('limit-warning');

    const filtered = currentFilter === 'all'
        ? vehicles
        : vehicles.filter(v => v.status === currentFilter);

    // Update count
    document.getElementById('vehicle-count').textContent = `${vehicles.length} vehicle${vehicles.length !== 1 ? 's' : ''}`;

    // Show/hide limit warning
    limitWarning.classList.toggle('hidden', vehicles.length < 999);

    if (filtered.length === 0) {
        grid.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
    }

    emptyState.classList.add('hidden');

    // Selective updates
    const existingCards = new Map([...grid.children].map(el => [el.dataset.vehicleId, el]));
    const filteredIds = new Set(filtered.map(v => v.__backendId));

    // Remove cards not in filtered list
    existingCards.forEach((el, id) => {
        if (!filteredIds.has(id)) el.remove();
    });

    // Add or update cards
    filtered.forEach((vehicle, index) => {
        if (!existingCards.has(vehicle.__backendId)) {
            const card = createVehicleCard(vehicle);
            card.style.animationDelay = `${index * 50}ms`;
            grid.appendChild(card);
        }
    });
}

// Modal Functions
function openModal(title, submitText) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('submit-text').textContent = submitText;
    document.getElementById('modal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
    document.getElementById('vehicle-form').reset();
    document.getElementById('vehicle-id').value = '';
    isEditing = false;
}

function openEditModal(vehicle) {
    isEditing = true;
    document.getElementById('vehicle-id').value = vehicle.__backendId;
    document.getElementById('brand').value = vehicle.brand;
    document.getElementById('model').value = vehicle.model;
    document.getElementById('year').value = vehicle.year;
    document.getElementById('price').value = vehicle.price;
    document.getElementById('color').value = vehicle.color;
    document.getElementById('mileage').value = vehicle.mileage;
    document.getElementById('status').value = vehicle.status;
    openModal('Edit Vehicle', 'Save Changes');
}

function openDeleteModal(vehicle) {
    vehicleToDelete = vehicle;
    document.getElementById('delete-modal').classList.remove('hidden');
}

function closeDeleteModal() {
    document.getElementById('delete-modal').classList.add('hidden');
    vehicleToDelete = null;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Filter handlers
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => {
                b.classList.remove('active-filter', 'bg-purple-600', 'text-white', 'shadow-md');
                b.classList.add('filter-btn');
                b.setAttribute('aria-selected', 'false');
            });
            btn.classList.add('active-filter');
            btn.classList.remove('filter-btn');
            btn.setAttribute('aria-selected', 'true');
            currentFilter = btn.dataset.filter;
            renderVehicles();
        });
    });

    // Theme toggle
    document.getElementById('theme-toggle').addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
    });

    // Add vehicle button
    document.getElementById('add-vehicle-btn').addEventListener('click', () => {
        if (vehicles.length >= 999) {
            showToast('Maximum limit reached');
            return;
        }
        openModal('Add New Vehicle', 'Add Vehicle');
    });

    // Modal close buttons
    document.getElementById('cancel-btn').addEventListener('click', closeModal);
    document.getElementById('modal-backdrop').addEventListener('click', closeModal);
    document.getElementById('cancel-delete-btn').addEventListener('click', closeDeleteModal);
    document.getElementById('delete-backdrop').addEventListener('click', closeDeleteModal);

    // Form submit
    document.getElementById('vehicle-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = document.getElementById('submit-btn');
        const submitText = document.getElementById('submit-text');
        const submitLoading = document.getElementById('submit-loading');

        submitBtn.disabled = true;
        submitText.classList.add('hidden');
        submitLoading.classList.remove('hidden');

        const vehicleData = {
            id: Date.now().toString(),
            brand: document.getElementById('brand').value,
            model: document.getElementById('model').value,
            year: parseInt(document.getElementById('year').value),
            price: parseFloat(document.getElementById('price').value),
            color: document.getElementById('color').value,
            mileage: parseInt(document.getElementById('mileage').value),
            status: document.getElementById('status').value,
            createdAt: new Date().toISOString()
        };

        let result;
        if (isEditing) {
            const existingVehicle = vehicles.find(v => v.__backendId === document.getElementById('vehicle-id').value);
            result = await window.dataSdk.update({ ...existingVehicle, ...vehicleData });
        } else {
            result = await window.dataSdk.create(vehicleData);
        }

        submitBtn.disabled = false;
        submitText.classList.remove('hidden');
        submitLoading.classList.add('hidden');

        if (result.isOk) {
            showToast(isEditing ? 'Vehicle updated' : 'Vehicle added');
            closeModal();
        } else {
            showToast('Error saving vehicle');
        }
    });

    // Delete confirmation
    document.getElementById('confirm-delete-btn').addEventListener('click', async () => {
        if (!vehicleToDelete) return;

        const deleteBtn = document.getElementById('confirm-delete-btn');
        const deleteText = document.getElementById('delete-text');
        const deleteLoading = document.getElementById('delete-loading');

        deleteBtn.disabled = true;
        deleteText.classList.add('hidden');
        deleteLoading.classList.remove('hidden');

        const result = await window.dataSdk.delete(vehicleToDelete);

        deleteBtn.disabled = false;
        deleteText.classList.remove('hidden');
        deleteLoading.classList.add('hidden');

        if (result.isOk) {
            showToast('Vehicle deleted');
            closeDeleteModal();
        } else {
            showToast('Error deleting vehicle');
        }
    });
});

// Data handler
const dataHandler = {
    onDataChanged(data) {
        vehicles = data;
        renderVehicles();
    }
};

// Element handler
const elementHandler = {
    defaultConfig,
    async onConfigChange(config) {
        const title = config.page_title || defaultConfig.page_title;
        const btnText = config.add_button_text || defaultConfig.add_button_text;

        document.getElementById('page-title').textContent = title;
        document.getElementById('add-btn-text').textContent = btnText;
    },
    mapToCapabilities(config) {
        return {
            recolorables: [
                {
                    get: () => config.background_color || defaultConfig.background_color,
                    set: (v) => { config.background_color = v; window.elementSdk.setConfig({ background_color: v }); }
                },
                {
                    get: () => config.surface_color || defaultConfig.surface_color,
                    set: (v) => { config.surface_color = v; window.elementSdk.setConfig({ surface_color: v }); }
                },
                {
                    get: () => config.text_color || defaultConfig.text_color,
                    set: (v) => { config.text_color = v; window.elementSdk.setConfig({ text_color: v }); }
                },
                {
                    get: () => config.primary_action_color || defaultConfig.primary_action_color,
                    set: (v) => { config.primary_action_color = v; window.elementSdk.setConfig({ primary_action_color: v }); }
                },
                {
                    get: () => config.secondary_action_color || defaultConfig.secondary_action_color,
                    set: (v) => { config.secondary_action_color = v; window.elementSdk.setConfig({ secondary_action_color: v }); }
                }
            ],
            borderables: [],
            fontEditable: undefined,
            fontSizeable: undefined
        };
    },
    mapToEditPanelValues(config) {
        return new Map([
            ['page_title', config.page_title || defaultConfig.page_title],
            ['add_button_text', config.add_button_text || defaultConfig.add_button_text]
        ]);
    }
};

// Initialize SDKs
(async () => {
    if (window.elementSdk) {
        window.elementSdk.init(elementHandler);
    }
    if (window.dataSdk) {
        const result = await window.dataSdk.init(dataHandler);
        if (!result.isOk) {
            console.error('Failed to initialize data SDK');
        }
    }
})();
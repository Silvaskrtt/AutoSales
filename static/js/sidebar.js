// Sidebar functionality
class SidebarManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.toggleBtn = document.getElementById('sidebarToggle');
        this.closeBtn = document.getElementById('sidebarClose');
        this.overlay = document.getElementById('sidebarOverlay');
        this.mainContent = document.querySelector('.main-content');
        
        this.init();
    }
    
    init() {
        // Check if we're on mobile
        this.checkScreenSize();
        
        // Add event listeners
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.openSidebar());
        }
        
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.closeSidebar());
        }
        
        if (this.overlay) {
            this.overlay.addEventListener('click', () => this.closeSidebar());
        }
        
        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.sidebar?.classList.contains('open')) {
                this.closeSidebar();
            }
        });
        
        // Handle window resize
        window.addEventListener('resize', () => this.checkScreenSize());
        
        // Highlight active link
        this.highlightActiveLink();
    }
    
    openSidebar() {
        if (!this.sidebar) return;
        this.sidebar.classList.add('open');
        this.sidebar.classList.remove('closed');
        if (this.overlay) this.overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    closeSidebar() {
        if (!this.sidebar) return;
        this.sidebar.classList.remove('open');
        this.sidebar.classList.add('closed');
        if (this.overlay) this.overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    checkScreenSize() {
        const isMobile = window.innerWidth <= 1024;
        
        if (!isMobile && this.sidebar) {
            // Desktop: always show sidebar
            this.sidebar.classList.remove('closed', 'open');
            if (this.overlay) this.overlay.classList.remove('active');
            document.body.style.overflow = '';
        } else if (isMobile && this.sidebar) {
            // Mobile: hide by default
            this.sidebar.classList.add('closed');
            this.sidebar.classList.remove('open');
        }
    }
    
    highlightActiveLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.sidebar-nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath === href) {
                link.closest('.sidebar-nav-item').classList.add('active');
            }
        });
    }
}

// Initialize sidebar when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SidebarManager();
});
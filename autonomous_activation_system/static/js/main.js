/* Main JavaScript - Autonomous Activation System */
document.addEventListener('DOMContentLoaded', () => {
    // Update time
    updateTime();
    setInterval(updateTime, 1000);

    // Sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
    }

    // Close sidebar on outside click (mobile)
    document.addEventListener('click', (e) => {
        if (window.innerWidth < 992 && sidebar && sidebar.classList.contains('show')) {
            if (!sidebar.contains(e.target) && (!sidebarToggle || !sidebarToggle.contains(e.target))) {
                sidebar.classList.remove('show');
            }
        }
    });
});

function updateTime() {
    const el = document.getElementById('currentTime');
    if (el) {
        const now = new Date();
        el.textContent = now.toLocaleTimeString('en-US', { hour12: false });
    }
}

function formatDate(date) {
    return new Date(date).toLocaleString();
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

function getSeverityColor(severity) {
    const colors = { info: 'info', warning: 'warning', critical: 'danger' };
    return colors[severity] || 'secondary';
}

function showNotification(title, message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${type} border-0 position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body"><strong>${title}</strong><br><small>${message}</small></div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 5000 });
    bsToast.show();
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

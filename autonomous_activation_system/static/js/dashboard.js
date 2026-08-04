/* Dashboard JavaScript */
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    initMap();
    initWebSocket();
});

function initCharts() {
    // Weekly Detection Chart
    const weeklyCtx = document.getElementById('weeklyChart');
    if (weeklyCtx && typeof weeklyData !== 'undefined') {
        new Chart(weeklyCtx, {
            type: 'bar',
            data: {
                labels: weeklyData.map(d => d.day),
                datasets: [{
                    label: 'AI Detections',
                    data: weeklyData.map(d => d.count),
                    backgroundColor: 'rgba(0, 212, 255, 0.6)',
                    borderColor: '#00d4ff',
                    borderWidth: 2,
                    borderRadius: 8,
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af' } },
                    x: { grid: { display: false }, ticks: { color: '#9ca3af' } }
                }
            }
        });
    }

    // Detection Type Pie Chart
    const pieCtx = document.getElementById('detectionPieChart');
    if (pieCtx && typeof detectionBreakdown !== 'undefined') {
        new Chart(pieCtx, {
            type: 'doughnut',
            data: {
                labels: detectionBreakdown.map(d => d.detection_type),
                datasets: [{
                    data: detectionBreakdown.map(d => d.count),
                    backgroundColor: ['#00d4ff', '#a855f7', '#10b981', '#f59e0b', '#ef4444', '#6366f1', '#ec4899', '#14b8a6'],
                    borderWidth: 0,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#9ca3af', padding: 15, font: { size: 11 } } }
                },
                cutout: '65%',
            }
        });
    }
}

function initMap() {
    const mapEl = document.getElementById('map');
    if (!mapEl) return;

    const map = L.map(mapEl).setView([40.7128, -74.0060], 10);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap © CARTO',
        maxZoom: 19,
    }).addTo(map);

    if (typeof gpsData !== 'undefined' && gpsData.length > 0) {
        const bounds = [];
        gpsData.forEach(v => {
            const marker = L.marker([v.latitude, v.longitude], {
                icon: L.divIcon({
                    className: 'vehicle-marker',
                    html: `<div style="background: #00d4ff; width: 14px; height: 14px; border-radius: 50%; box-shadow: 0 0 10px #00d4ff; border: 2px solid white;"></div>`,
                    iconSize: [14, 14],
                })
            }).addTo(map);
            marker.bindPopup(`<b>${v.vehicle}</b><br>Speed: ${v.speed} km/h`);
            bounds.push([v.latitude, v.longitude]);
        });
        if (bounds.length > 0) map.fitBounds(bounds, { padding: [30, 30] });
    }
}

function initWebSocket() {
    if (typeof ws !== 'undefined') {
        initDashboardWS();
        initDetectionWS();
    }
}

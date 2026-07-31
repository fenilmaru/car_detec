/* Analytics & Reports JavaScript */
document.addEventListener('DOMContentLoaded', () => {
    initAnalyticsCharts();
});

function initAnalyticsCharts() {
    // Trend Chart (30-day)
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx && typeof trendData !== 'undefined') {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: trendData.map(d => d.date),
                datasets: [{
                    label: 'Detections',
                    data: trendData.map(d => d.count),
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3,
                    pointBackgroundColor: '#00d4ff',
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af' } },
                    x: { grid: { display: false }, ticks: { color: '#9ca3af', maxRotation: 45 } }
                }
            }
        });
    }

    // Severity Chart
    const sevCtx = document.getElementById('sevChart');
    if (sevCtx && typeof sevData !== 'undefined') {
        new Chart(sevCtx, {
            type: 'bar',
            data: {
                labels: sevData.map(d => d.severity),
                datasets: [{
                    label: 'Accidents',
                    data: sevData.map(d => d.count),
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#7c3aed', '#991b1b'],
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

    // Detection Type Chart
    const detCtx = document.getElementById('detTypeChart');
    if (detCtx && typeof detTypeData !== 'undefined') {
        new Chart(detCtx, {
            type: 'bar',
            data: {
                labels: detTypeData.map(d => d.detection_type.replace('_', ' ')),
                datasets: [{
                    label: 'Count',
                    data: detTypeData.map(d => d.count),
                    backgroundColor: ['#00d4ff', '#a855f7', '#10b981', '#f59e0b', '#ef4444', '#6366f1', '#ec4899', '#14b8a6'],
                    borderRadius: 8,
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af' } },
                    y: { grid: { display: false }, ticks: { color: '#9ca3af' } }
                }
            }
        });
    }

    // Severity Chart (Reports)
    const sevChart2 = document.getElementById('severityChart');
    if (sevChart2 && typeof severityData !== 'undefined') {
        new Chart(sevChart2, {
            type: 'pie',
            data: {
                labels: severityData.map(d => d.severity),
                datasets: [{
                    data: severityData.map(d => d.count),
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#7c3aed', '#991b1b'],
                    borderWidth: 0,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#9ca3af' } }
                }
            }
        });
    }
}

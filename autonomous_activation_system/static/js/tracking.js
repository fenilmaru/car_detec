/* Vehicle Tracking JavaScript */
document.addEventListener('DOMContentLoaded', () => {
    initTrackingMap();
});

function initTrackingMap() {
    const mapEl = document.getElementById('trackingMap');
    if (!mapEl) return;

    const map = L.map(mapEl).setView([40.7128, -74.0060], 10);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap © CARTO',
        maxZoom: 19,
    }).addTo(map);

    const markers = {};

    // Add vehicle markers from data
    if (typeof gpsMarkers !== 'undefined' && gpsMarkers.length > 0) {
        const bounds = [];
        gpsMarkers.forEach(v => {
            const icon = L.divIcon({
                className: 'vehicle-marker',
                html: `<div style="
                    background: ${parseFloat(v.speed) > 100 ? '#ef4444' : parseFloat(v.speed) > 60 ? '#f59e0b' : '#00d4ff'};
                    width: 16px; height: 16px; border-radius: 50%;
                    box-shadow: 0 0 12px ${parseFloat(v.speed) > 100 ? '#ef4444' : '#00d4ff'};
                    border: 2px solid white;
                "></div>`,
                iconSize: [16, 16],
            });
            const marker = L.marker([parseFloat(v.latitude), parseFloat(v.longitude)], { icon }).addTo(map);
            marker.bindPopup(`
                <div style="font-family: sans-serif;">
                    <strong>${v.vehicle || 'Vehicle'}</strong><br>
                    Speed: ${v.speed || 0} km/h<br>
                    Heading: ${v.heading || 'N/A'}<br>
                    Last Update: ${v.timestamp ? new Date(v.timestamp).toLocaleString() : 'Just now'}
                </div>
            `);
            markers[v.vehicle] = marker;
            bounds.push([parseFloat(v.latitude), parseFloat(v.longitude)]);
        });
        if (bounds.length > 0) map.fitBounds(bounds, { padding: [30, 30] });
    }

    // Click on vehicle list to pan
    document.querySelectorAll('.vehicle-item').forEach(item => {
        item.addEventListener('click', () => {
            const lat = parseFloat(item.dataset.lat);
            const lng = parseFloat(item.dataset.lng);
            if (lat && lng) map.setView([lat, lng], 15);
        });
    });

    // Poll for updates
    setInterval(async () => {
        const data = await API.gps.list();
        if (data && data.results) {
            data.results.forEach(loc => {
                if (markers[loc.vehicle_plate]) {
                    markers[loc.vehicle_plate].setLatLng([parseFloat(loc.latitude), parseFloat(loc.longitude)]);
                }
            });
        }
    }, 10000);
}

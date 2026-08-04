/* WebSocket Client - Real-time Communication */
class WSClient {
    constructor() {
        this.connections = {};
        this.reconnectInterval = 3000;
        this.maxReconnectAttempts = 5;
    }

    connect(url, callbacks = {}) {
        if (this.connections[url]) return this.connections[url];

        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsUrl = `${protocol}${window.location.host}${url}`;

        let reconnectAttempts = 0;

        const connect = () => {
            const ws = new WebSocket(wsUrl);

            ws.onopen = () => {
                console.log(`[WS] Connected: ${url}`);
                reconnectAttempts = 0;
                if (callbacks.onOpen) callbacks.onOpen();
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (callbacks.onMessage) callbacks.onMessage(data);
                } catch (e) {
                    console.error('[WS] Parse error:', e);
                }
            };

            ws.onclose = () => {
                console.log(`[WS] Disconnected: ${url}`);
                delete this.connections[url];
                if (reconnectAttempts < this.maxReconnectAttempts) {
                    reconnectAttempts++;
                    setTimeout(connect, this.reconnectInterval * reconnectAttempts);
                }
            };

            ws.onerror = (error) => {
                console.error(`[WS] Error: ${url}`, error);
            };

            this.connections[url] = ws;
            return ws;
        };

        return connect();
    }

    send(url, data) {
        const ws = this.connections[url];
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(data));
        }
    }

    close(url) {
        const ws = this.connections[url];
        if (ws) {
            ws.close();
            delete this.connections[url];
        }
    }

    closeAll() {
        Object.keys(this.connections).forEach(url => this.close(url));
    }
}

// Initialize WebSocket connections
const ws = new WSClient();

// Connect to dashboard
function initDashboardWS() {
    ws.connect('/ws/dashboard/', {
        onOpen: () => ws.send('/ws/dashboard/', { action: 'get_stats' }),
        onMessage: (data) => {
            if (data.type === 'dashboard_stats') {
                updateDashboardStats(data);
            }
        }
    });
}

// Connect to GPS
function initGPSWS(vehicleId = 'all') {
    ws.connect(`/ws/gps/${vehicleId}/`, {
        onMessage: (data) => {
            if (data.type === 'gps_update' && window.updateVehicleMarker) {
                window.updateVehicleMarker(data);
            }
        }
    });
}

// Connect to detections
function initDetectionWS() {
    ws.connect('/ws/detections/', {
        onMessage: (data) => {
            if (data.type === 'detection_update') {
                addDetectionFeedItem(data.data);
            }
        }
    });
}

// Connect to emergency
function initEmergencyWS() {
    ws.connect('/ws/emergency/', {
        onMessage: (data) => {
            if (data.type === 'emergency_alert') {
                showNotification('EMERGENCY', data.message || 'New emergency alert!', 'danger');
            }
        }
    });
}

function updateDashboardStats(data) {
    // Update stat cards if they exist
    console.log('[Dashboard Stats]', data);
}

function addDetectionFeedItem(data) {
    const feed = document.querySelector('.detection-feed');
    if (!feed) return;
    const item = document.createElement('div');
    item.className = 'detection-item p-2 mb-2 rounded-3 bg-dark-subtle';
    item.style.animation = 'fadeIn 0.5s ease';
    item.innerHTML = `
        <div class="d-flex justify-content-between">
            <div>
                <span class="badge bg-${getSeverityColor(data.severity || 'info')}">${data.severity || 'info'}</span>
                <strong class="text-light ms-2">${data.detection_type || 'Detection'}</strong>
            </div>
            <small class="text-muted">Just now</small>
        </div>
        <p class="mb-0 small text-muted">${data.description || ''}</p>
    `;
    feed.insertBefore(item, feed.firstChild);
    if (feed.children.length > 20) feed.removeChild(feed.lastChild);
}

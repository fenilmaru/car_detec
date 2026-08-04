/* API Client - REST API Integration */
const API = {
    headers: {
        'Content-Type': 'application/json',
    },

    async get(url, params = {}) {
        const query = new URLSearchParams(params).toString();
        const fullUrl = query ? `${API_BASE}${url}?${query}` : `${API_BASE}${url}`;
        try {
            const res = await fetch(fullUrl, { headers: API.headers });
            return res.ok ? await res.json() : null;
        } catch (e) {
            console.error(`API GET Error: ${url}`, e);
            return null;
        }
    },

    async post(url, data = {}) {
        try {
            const res = await fetch(`${API_BASE}${url}`, {
                method: 'POST',
                headers: { ...API.headers, 'X-CSRFToken': CSRF_TOKEN },
                body: JSON.stringify(data),
            });
            return res.ok ? await res.json() : null;
        } catch (e) {
            console.error(`API POST Error: ${url}`, e);
            return null;
        }
    },

    async put(url, data = {}) {
        try {
            const res = await fetch(`${API_BASE}${url}`, {
                method: 'PUT',
                headers: { ...API.headers, 'X-CSRFToken': CSRF_TOKEN },
                body: JSON.stringify(data),
            });
            return res.ok ? await res.json() : null;
        } catch (e) {
            console.error(`API PUT Error: ${url}`, e);
            return null;
        }
    },

    async delete(url) {
        try {
            const res = await fetch(`${API_BASE}${url}`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': CSRF_TOKEN },
            });
            return res.ok;
        } catch (e) {
            console.error(`API DELETE Error: ${url}`, e);
            return false;
        }
    },

    // Vehicle APIs
    vehicles: {
        list: (params) => API.get('/vehicles/', params),
        get: (id) => API.get(`/vehicles/${id}/`),
        create: (data) => API.post('/vehicles/', data),
        update: (id, data) => API.put(`/vehicles/${id}/`, data),
        delete: (id) => API.delete(`/vehicles/${id}/`),
    },

    // Driver APIs
    drivers: {
        list: (params) => API.get('/drivers/', params),
        get: (id) => API.get(`/drivers/${id}/`),
    },

    // Accident APIs
    accidents: {
        list: (params) => API.get('/accidents/', params),
        get: (id) => API.get(`/accidents/${id}/`),
    },

    // GPS APIs
    gps: {
        list: (params) => API.get('/gps/', params),
    },

    // Analytics
    analytics: () => API.get('/analytics/'),

    // Reports
    reports: (period) => API.get('/reports/', { period }),

    // Notifications
    notifications: {
        list: () => API.get('/notifications/'),
        markRead: (id) => API.post(`/notifications/${id}/read/`),
    },

    // Auth
    auth: {
        login: (credentials) => API.post('/auth/token/', credentials),
        refresh: (refresh) => API.post('/auth/token/refresh/', { refresh }),
    }
};

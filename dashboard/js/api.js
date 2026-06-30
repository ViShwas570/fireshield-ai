// ============================================================
// FireShield AI - API Service Module
// Handles all communication with the backend API
// Falls back to SampleData when API is unavailable
// ============================================================

const API = (() => {
    const BASE_URL = 'https://fireshield-ai-p41f.onrender.com';
    let authToken = null;
    let wsConnection = null;
    let wsReconnectTimer = null;
    let apiAvailable = null; // null = unknown, true/false after check

    // ─── Helpers ────────────────────────────────────────────
    async function request(endpoint, options = {}) {
        const url = `${BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {}),
            ...options.headers
        };

        try {
            const response = await fetch(url, {
                ...options,
                headers,
                signal: AbortSignal.timeout(5000) // 5s timeout
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            apiAvailable = true;
            return await response.json();
        } catch (error) {
            console.warn(`API request failed for ${endpoint}:`, error.message);
            apiAvailable = false;
            return null;
        }
    }

    // ─── Health Check ───────────────────────────────────────
    async function checkHealth() {
        const result = await request('/health');
        return result !== null;
    }

    // ─── Auth ───────────────────────────────────────────────
    function setToken(token) {
        authToken = token;
        localStorage.setItem('fireshield_token', token);
    }

    function getToken() {
        if (!authToken) {
            authToken = localStorage.getItem('fireshield_token');
        }
        return authToken;
    }

    function clearToken() {
        authToken = null;
        localStorage.removeItem('fireshield_token');
    }

    // ─── Incidents ──────────────────────────────────────────
    async function fetchIncidents(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = `/api/incidents${queryString ? '?' + queryString : ''}`;
        const data = await request(endpoint);

        if (data) return data;
        // Fallback to sample data
        let filtered = [...SampleData.incidents];

        if (params.status) {
            filtered = filtered.filter(i => i.status === params.status);
        }
        if (params.severity) {
            filtered = filtered.filter(i => i.severity === parseInt(params.severity));
        }
        if (params.search) {
            const s = params.search.toLowerCase();
            filtered = filtered.filter(i =>
                i.title.toLowerCase().includes(s) ||
                i.location.toLowerCase().includes(s) ||
                i.city.toLowerCase().includes(s) ||
                i.id.toLowerCase().includes(s)
            );
        }

        return filtered;
    }

    async function fetchIncidentById(id) {
        const data = await request(`/api/incidents/${id}`);
        if (data) return data;
        return SampleData.incidents.find(i => i.id === id) || null;
    }

    async function updateIncidentStatus(id, status, notes = '') {
        const data = await request(`/api/incidents/${id}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status, notes })
        });

        if (data) return data;

        // Simulate locally
        const incident = SampleData.incidents.find(i => i.id === id);
        if (incident) {
            incident.status = status;
            if (notes) incident.notes = notes;
            const now = new Date().toISOString();
            if (status === 'acknowledged') incident.acknowledged_at = now;
            if (status === 'assigned') incident.assigned_at = now;
            if (status === 'arrived') incident.arrived_at = now;
            if (status === 'resolved') incident.resolved_at = now;
        }
        return incident;
    }

    async function assignTeam(incidentId, teamId) {
        const data = await request(`/api/incidents/${incidentId}/assign`, {
            method: 'PUT',
            body: JSON.stringify({ team_id: teamId })
        });

        if (data) return data;

        const incident = SampleData.incidents.find(i => i.id === incidentId);
        const team = SampleData.teams.find(t => t.id === teamId);
        if (incident && team) {
            incident.assigned_team = team.name.split(' ')[0];
            incident.status = 'assigned';
            incident.assigned_at = new Date().toISOString();
            team.current_assignment = incidentId;
            team.status = 'en_route';
        }
        return incident;
    }

    // ─── Analytics ──────────────────────────────────────────
    async function fetchAnalytics(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = `/api/analytics${queryString ? '?' + queryString : ''}`;
        const data = await request(endpoint);

        if (data) return data;
        return SampleData.analyticsData;
    }

    // ─── Heatmap ────────────────────────────────────────────
    async function fetchHeatmapData() {
        const data = await request('/api/heatmap');

        if (data) return data;
        return SampleData.incidents.map(i => ({
            lat: i.latitude,
            lng: i.longitude,
            intensity: i.severity / 5
        }));
    }

    // ─── Stations ───────────────────────────────────────────
    async function fetchNearbyStations(lat, lng, radius = 50) {
        const data = await request(`/api/stations/nearby?lat=${lat}&lng=${lng}&radius=${radius}`);

        if (data) return data;
        return SampleData.fireStations;
    }

    async function fetchStations() {
        const data = await request('/api/stations');
        if (data) return data;
        return SampleData.fireStations;
    }

    // ─── Teams ──────────────────────────────────────────────
    async function fetchTeams() {
        const data = await request('/api/teams');
        if (data) return data;
        return SampleData.teams;
    }

    async function fetchTeamById(id) {
        const data = await request(`/api/teams/${id}`);
        if (data) return data;
        return SampleData.teams.find(t => t.id === id) || null;
    }

    // ─── WebSocket ──────────────────────────────────────────
    function connectWebSocket(onMessage) {
        if (wsConnection && wsConnection.readyState === WebSocket.OPEN) {
            return wsConnection;
        }

        try {
            const wsUrl = BASE_URL.replace('http', 'ws') + '/ws';
            wsConnection = new WebSocket(wsUrl);

            wsConnection.onopen = () => {
                console.log('🔌 WebSocket connected');
                if (wsReconnectTimer) {
                    clearTimeout(wsReconnectTimer);
                    wsReconnectTimer = null;
                }
            };

            wsConnection.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (onMessage) onMessage(data);
                } catch (e) {
                    console.warn('WebSocket message parse error:', e);
                }
            };

            wsConnection.onclose = () => {
                console.log('🔌 WebSocket disconnected');
                scheduleReconnect(onMessage);
            };

            wsConnection.onerror = (error) => {
                console.warn('WebSocket error:', error);
            };

            return wsConnection;
        } catch (e) {
            console.warn('WebSocket connection failed:', e);
            scheduleReconnect(onMessage);
            return null;
        }
    }

    function scheduleReconnect(onMessage) {
        if (wsReconnectTimer) return;
        wsReconnectTimer = setTimeout(() => {
            wsReconnectTimer = null;
            connectWebSocket(onMessage);
        }, 5000);
    }

    function disconnectWebSocket() {
        if (wsReconnectTimer) {
            clearTimeout(wsReconnectTimer);
            wsReconnectTimer = null;
        }
        if (wsConnection) {
            wsConnection.close();
            wsConnection = null;
        }
    }

    // ─── Public API ─────────────────────────────────────────
    return {
        checkHealth,
        setToken,
        getToken,
        clearToken,
        fetchIncidents,
        fetchIncidentById,
        updateIncidentStatus,
        assignTeam,
        fetchAnalytics,
        fetchHeatmapData,
        fetchNearbyStations,
        fetchStations,
        fetchTeams,
        fetchTeamById,
        connectWebSocket,
        disconnectWebSocket,
        isApiAvailable: () => apiAvailable,
        BASE_URL
    };
})();
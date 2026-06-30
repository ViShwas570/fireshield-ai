/* ═══════════════════════════════════════════════════════════
   FireShield AI — Command Center Application
   Complete Dashboard Logic
   ═══════════════════════════════════════════════════════════ */

let incidents = [...SAMPLE_INCIDENTS];
let map = null;
let markersLayer = null;
let heatLayer = null;
let chartsInitialized = false;

// ─── Page Navigation ─────────────────────────────────────
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const page = document.getElementById('page-' + pageId);
    if (page) page.classList.add('active');
    const nav = document.querySelector(`.nav-item[data-page="${pageId}"]`);
    if (nav) nav.classList.add('active');
    if (pageId === 'map') initMap();
    if (pageId === 'analytics' && !chartsInitialized) initAnalyticsCharts();
    if (pageId === 'teams') renderTeams();
    if (pageId === 'incidents') renderIncidentsTable(incidents);
}

// ─── Initialize App ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    // Nav links
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            showPage(item.dataset.page);
        });
    });

    // Sidebar toggle
    document.getElementById('menuBtn')?.addEventListener('click', () => {
        document.getElementById('sidebar').classList.toggle('open');
    });

    // Theme toggle
    document.getElementById('themeBtn')?.addEventListener('click', toggleTheme);

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('globalSearch')?.focus();
        }
        if (e.key === 'Escape') closeModal();
    });

    // Global search
    document.getElementById('globalSearch')?.addEventListener('input', (e) => {
        const q = e.target.value.toLowerCase();
        if (q.length > 1) {
            const results = incidents.filter(i =>
                i.title.toLowerCase().includes(q) || i.address.toLowerCase().includes(q) || i.id.toLowerCase().includes(q)
            );
            showPage('incidents');
            renderIncidentsTable(results);
        }
    });

    // Init dashboard
    renderDashboard();
    renderRecentTable();
    renderActivityFeed();
    initDashboardCharts();

    // Simulate live notifications
    setTimeout(() => showToast('🚨 New SOS alert received from Gurgaon', 'danger'), 5000);
    setTimeout(() => showToast('✅ Alpha Team arrived at Manesar', 'success'), 12000);
    setTimeout(() => showToast('📊 Severity analysis complete for INC-1009', 'info'), 20000);

    // Update stats
    updateStats();
});

// ─── Dashboard Stats ─────────────────────────────────────
function updateStats() {
    const active = incidents.filter(i => i.status !== 'resolved').length;
    const resolved = incidents.filter(i => i.status === 'resolved').length;
    const rts = incidents.filter(i => i.response_time_mins).map(i => i.response_time_mins);
    const avg = rts.length ? (rts.reduce((a, b) => a + b, 0) / rts.length).toFixed(1) : '0';
    document.getElementById('statTotal').textContent = incidents.length;
    document.getElementById('statActive').textContent = active;
    document.getElementById('statResponse').innerHTML = avg + '<small>min</small>';
    document.getElementById('statResolved').textContent = resolved;
    document.getElementById('incidentCount').textContent = incidents.length;
}

function renderDashboard() {
    updateStats();
}

// ─── Recent Table ────────────────────────────────────────
function renderRecentTable() {
    const tbody = document.getElementById('recentTableBody');
    if (!tbody) return;
    const recent = [...incidents].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 8);
    tbody.innerHTML = recent.map(inc => `
        <tr onclick="showIncidentModal('${inc.id}')">
            <td><strong>${inc.id}</strong></td>
            <td>${inc.title.substring(0, 35)}...</td>
            <td>${inc.address.split(',')[0]}</td>
            <td><span class="severity-badge severity-${inc.severity}">${inc.severity}</span></td>
            <td><span class="status-badge status-${inc.status}">${inc.status.replace('_', ' ')}</span></td>
            <td>${timeAgo(inc.created_at)}</td>
        </tr>
    `).join('');
}

// ─── Activity Feed ───────────────────────────────────────
function renderActivityFeed() {
    const feed = document.getElementById('activityFeed');
    if (!feed) return;
    const activities = [
        { text: '<strong>SOS Alert</strong> received from Manesar Industrial Area', time: '2 min ago', color: '#ef4444' },
        { text: '<strong>Alpha Team</strong> dispatched to Factory Fire', time: '5 min ago', color: '#f97316' },
        { text: '<strong>AI Analysis</strong> completed — Severity: Critical (5)', time: '8 min ago', color: '#8b5cf6' },
        { text: '<strong>Bravo Team</strong> arrived at Lajpat Nagar', time: '15 min ago', color: '#22c55e' },
        { text: 'Incident INC-1003 marked as <strong>Resolved</strong>', time: '1 hr ago', color: '#22c55e' },
        { text: '<strong>Echo Team</strong> assigned to Hospital Generator Fire', time: '2 hr ago', color: '#3b82f6' },
        { text: 'New incident reported: <strong>Mall Fire in Kolkata</strong>', time: '3 hr ago', color: '#eab308' },
        { text: '<strong>Forest Response Unit</strong> en route to Bandipur', time: '4 hr ago', color: '#f97316' },
    ];
    feed.innerHTML = activities.map(a => `
        <div class="activity-item">
            <div class="activity-dot" style="background:${a.color}"></div>
            <div>
                <div class="activity-text">${a.text}</div>
                <div class="activity-time">${a.time}</div>
            </div>
        </div>
    `).join('');
}

// ─── Dashboard Charts ────────────────────────────────────
function initDashboardCharts() {
    // Severity distribution
    const sevCtx = document.getElementById('severityChart')?.getContext('2d');
    if (sevCtx) {
        const sevCounts = [0, 0, 0, 0, 0];
        incidents.forEach(i => { if (i.severity >= 1 && i.severity <= 5) sevCounts[i.severity - 1]++; });
        new Chart(sevCtx, {
            type: 'doughnut',
            data: {
                labels: ['Minor (1)', 'Low (2)', 'Medium (3)', 'High (4)', 'Critical (5)'],
                datasets: [{ data: sevCounts, backgroundColor: ['#22c55e', '#84cc16', '#eab308', '#f97316', '#ef4444'], borderWidth: 0, hoverOffset: 8 }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', font: { family: 'Inter' }, padding: 16 } } }, cutout: '65%' }
        });
    }

    // Monthly trend
    const trendCtx = document.getElementById('trendChart')?.getContext('2d');
    if (trendCtx) {
        const gradient = trendCtx.createLinearGradient(0, 0, 0, 260);
        gradient.addColorStop(0, 'rgba(255, 87, 34, 0.3)');
        gradient.addColorStop(1, 'rgba(255, 87, 34, 0.01)');
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{ label: 'Incidents', data: [22, 18, 32, 28, 35, 24], fill: true, backgroundColor: gradient, borderColor: '#ff5722', borderWidth: 2, tension: 0.4, pointBackgroundColor: '#ff5722', pointBorderColor: '#1a2332', pointBorderWidth: 2, pointRadius: 5, pointHoverRadius: 7 }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } }, y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } } } }
        });
    }
}

// ─── Analytics Charts ────────────────────────────────────
function initAnalyticsCharts() {
    chartsInitialized = true;
    const chartDefaults = { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#94a3b8', font: { family: 'Inter' } } } }, scales: { x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } }, y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } } } };

    // Incidents over time
    const timeCtx = document.getElementById('timeChart')?.getContext('2d');
    if (timeCtx) {
        const g = timeCtx.createLinearGradient(0, 0, 0, 260);
        g.addColorStop(0, 'rgba(255, 152, 0, 0.3)');
        g.addColorStop(1, 'rgba(255, 152, 0, 0.01)');
        new Chart(timeCtx, { type: 'line', data: { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], datasets: [{ label: 'Incidents', data: [22, 18, 32, 28, 35, 24], fill: true, backgroundColor: g, borderColor: '#ff9800', borderWidth: 2, tension: 0.4, pointRadius: 4 }] }, options: chartDefaults });
    }

    // By city
    const cityCtx = document.getElementById('cityChart')?.getContext('2d');
    if (cityCtx) {
        new Chart(cityCtx, { type: 'bar', data: { labels: ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Pune', 'Jaipur', 'Hyderabad'], datasets: [{ label: 'Incidents', data: [42, 35, 28, 24, 18, 15, 12, 10], backgroundColor: ['#ff5722', '#ff7043', '#ff8a65', '#ffab91', '#ffc107', '#ffca28', '#ffd54f', '#ffe082'], borderRadius: 6, borderWidth: 0 }] }, options: { ...chartDefaults, indexAxis: 'y', plugins: { legend: { display: false } } } });
    }

    // Fire types
    const typeCtx = document.getElementById('typeChart')?.getContext('2d');
    if (typeCtx) {
        new Chart(typeCtx, { type: 'polarArea', data: { labels: ['Building', 'Industrial', 'Kitchen', 'Electrical', 'Vehicle', 'Forest', 'Gas Leak'], datasets: [{ data: [35, 28, 20, 18, 12, 8, 6], backgroundColor: ['rgba(255,87,34,0.7)', 'rgba(239,68,68,0.7)', 'rgba(234,179,8,0.7)', 'rgba(59,130,246,0.7)', 'rgba(139,92,246,0.7)', 'rgba(34,197,94,0.7)', 'rgba(249,115,22,0.7)'], borderWidth: 0 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { color: '#94a3b8', font: { family: 'Inter' } } } } } });
    }

    // Response time
    const respCtx = document.getElementById('responseChart')?.getContext('2d');
    if (respCtx) {
        new Chart(respCtx, { type: 'line', data: { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], datasets: [{ label: 'Avg Response (min)', data: [9.2, 8.5, 7.8, 7.3, 6.9, 7.3], borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.1)', fill: true, tension: 0.4, borderWidth: 2 }, { label: 'Target', data: [8, 8, 8, 8, 8, 8], borderColor: '#ef4444', borderDash: [5, 5], borderWidth: 1, pointRadius: 0, fill: false }] }, options: chartDefaults });
    }
}

// ─── Incidents Table ─────────────────────────────────────
function renderIncidentsTable(data) {
    const tbody = document.getElementById('incidentsTableBody');
    if (!tbody) return;
    tbody.innerHTML = data.map(inc => `
        <tr onclick="showIncidentModal('${inc.id}')">
            <td><strong>${inc.id}</strong></td>
            <td>${inc.title.substring(0, 40)}${inc.title.length > 40 ? '...' : ''}</td>
            <td>${inc.address.split(',').slice(0, 2).join(',')}</td>
            <td>${inc.category}</td>
            <td><span class="severity-badge severity-${inc.severity}">${inc.severity}</span></td>
            <td><span class="status-badge status-${inc.status}">${inc.status.replace('_', ' ')}</span></td>
            <td>${inc.assigned_team || '—'}</td>
            <td>${inc.response_time_mins ? inc.response_time_mins + ' min' : '—'}</td>
            <td>
                <button class="btn-action" onclick="event.stopPropagation(); showIncidentModal('${inc.id}')"><i class="fas fa-eye"></i></button>
            </td>
        </tr>
    `).join('');
}

function filterIncidents() {
    let data = [...incidents];
    const status = document.getElementById('filterStatus')?.value;
    const severity = document.getElementById('filterSeverity')?.value;
    const search = document.getElementById('filterSearch')?.value?.toLowerCase();
    if (status) data = data.filter(i => i.status === status);
    if (severity) data = data.filter(i => i.severity === parseInt(severity));
    if (search) data = data.filter(i => i.title.toLowerCase().includes(search) || i.address.toLowerCase().includes(search) || i.id.toLowerCase().includes(search));
    renderIncidentsTable(data);
}

// ─── Map ─────────────────────────────────────────────────
function initMap() {
    if (map) return;
    map = L.map('liveMap').setView([22.5, 79.0], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors', maxZoom: 18
    }).addTo(map);

    // Marker cluster
    markersLayer = L.markerClusterGroup();
    const severityColors = { 1: '#22c55e', 2: '#84cc16', 3: '#eab308', 4: '#f97316', 5: '#ef4444' };

    incidents.forEach(inc => {
        const color = severityColors[inc.severity] || '#eab308';
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="width:28px;height:28px;border-radius:50%;background:${color};display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:12px;border:3px solid rgba(255,255,255,0.8);box-shadow:0 2px 8px rgba(0,0,0,0.3);${inc.severity >= 5 ? 'animation:pulse 1.5s infinite;' : ''}">${inc.severity}</div>`,
            iconSize: [28, 28], iconAnchor: [14, 14]
        });
        const marker = L.marker([inc.latitude, inc.longitude], { icon }).bindPopup(`
            <div style="min-width:200px;font-family:Inter,sans-serif">
                <strong>${inc.id}: ${inc.title}</strong><br>
                <span style="color:#666">📍 ${inc.address}</span><br>
                <span style="color:${color}">● Severity: ${inc.severity}/5</span> | 
                <span>Status: ${inc.status.replace('_', ' ')}</span><br>
                ${inc.assigned_team ? `<span>👥 ${inc.assigned_team}</span>` : ''}
            </div>
        `);
        markersLayer.addLayer(marker);
    });
    map.addLayer(markersLayer);

    // Fire stations
    FIRE_STATIONS.forEach(fs => {
        const icon = L.divIcon({
            className: 'station-marker',
            html: `<div style="width:24px;height:24px;border-radius:4px;background:#3b82f6;display:flex;align-items:center;justify-content:center;color:white;font-size:12px;border:2px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3)">🚒</div>`,
            iconSize: [24, 24], iconAnchor: [12, 12]
        });
        L.marker([fs.lat, fs.lng], { icon }).addTo(map).bindPopup(`<strong>🚒 ${fs.name}</strong>`);
    });

    // Heat layer data
    const heatData = incidents.map(i => [i.latitude, i.longitude, i.severity / 5]);
    heatLayer = L.heatLayer(heatData, { radius: 35, blur: 25, maxZoom: 10, gradient: { 0.2: '#22c55e', 0.4: '#eab308', 0.6: '#f97316', 0.8: '#ef4444', 1: '#dc2626' } });

    setTimeout(() => map.invalidateSize(), 200);
}

function toggleMapLayer(layer) {
    if (!map) return;
    if (layer === 'heat') {
        if (map.hasLayer(heatLayer)) {
            map.removeLayer(heatLayer);
            document.getElementById('toggleHeat')?.classList.remove('active');
        } else {
            map.addLayer(heatLayer);
            document.getElementById('toggleHeat')?.classList.add('active');
        }
    }
    if (layer === 'markers') {
        if (map.hasLayer(markersLayer)) {
            map.removeLayer(markersLayer);
            document.getElementById('toggleMarkers')?.classList.remove('active');
        } else {
            map.addLayer(markersLayer);
            document.getElementById('toggleMarkers')?.classList.add('active');
        }
    }
}

// ─── Teams ───────────────────────────────────────────────
function renderTeams() {
    const grid = document.getElementById('teamsGrid');
    if (!grid) return;
    const statusMap = { available: 'status-resolved', on_scene: 'status-arrived', en_route: 'status-en_route', off_duty: 'status-reported' };
    grid.innerHTML = SAMPLE_TEAMS.map(t => `
        <div class="team-card" style="--team-color:${t.color}">
            <div class="team-name">${t.name}</div>
            <span class="status-badge ${statusMap[t.status] || ''}">${t.status.replace('_', ' ')}</span>
            <div class="team-stats">
                <div class="team-stat"><span class="team-stat-val">${t.members}</span><span class="team-stat-label">Members</span></div>
                <div class="team-stat"><span class="team-stat-val">${t.stats.missions}</span><span class="team-stat-label">Missions</span></div>
                <div class="team-stat"><span class="team-stat-val">${t.stats.avgResponse}</span><span class="team-stat-label">Avg Resp.</span></div>
            </div>
            <div>🚛 ${t.vehicle}</div>
            ${t.assignment ? `<div class="team-assignment">📋 <strong>Current:</strong> ${t.assignment}</div>` : '<div class="team-assignment" style="color:#22c55e">✅ Available for dispatch</div>'}
        </div>
    `).join('');
}

// ─── Incident Modal ──────────────────────────────────────
function showIncidentModal(id) {
    const inc = incidents.find(i => i.id === id);
    if (!inc) return;
    document.getElementById('modalTitle').textContent = `${inc.id}: ${inc.title}`;
    const ai = inc.ai_analysis;
    document.getElementById('modalBody').innerHTML = `
        <div class="modal-section">
            <h4><i class="fas fa-info-circle"></i> Incident Details</h4>
            <div class="detail-grid">
                <div class="detail-item"><label>Category</label><span>${inc.category}</span></div>
                <div class="detail-item"><label>Severity</label><span class="severity-badge severity-${inc.severity}">${inc.severity}</span></div>
                <div class="detail-item"><label>Status</label><span class="status-badge status-${inc.status}">${inc.status.replace('_', ' ')}</span></div>
                <div class="detail-item"><label>Response Time</label><span>${inc.response_time_mins ? inc.response_time_mins + ' min' : 'Pending'}</span></div>
                <div class="detail-item"><label>Location</label><span>📍 ${inc.address}</span></div>
                <div class="detail-item"><label>Team</label><span>${inc.assigned_team || 'Unassigned'}</span></div>
            </div>
            <p style="margin-top:12px;color:var(--text-secondary);font-size:13px">${inc.description}</p>
        </div>
        ${ai ? `
        <div class="modal-section">
            <h4><i class="fas fa-robot"></i> AI Analysis (Gemini)</h4>
            <div class="ai-analysis-box">
                <strong>Fire Type:</strong> ${ai.fire_type}
                <strong>Risk Level:</strong> <span style="color:${ai.risk_level === 'CRITICAL' ? '#ef4444' : ai.risk_level === 'HIGH' ? '#f97316' : '#eab308'}">${ai.risk_level}</span>
                <strong>Severity Score:</strong> ${ai.severity_score}/5.0 (Confidence: ${(ai.confidence_score * 100).toFixed(0)}%)
                <strong>Affected Area:</strong> ${ai.estimated_affected_area}
                <strong>Recommended Units:</strong> ${ai.recommended_units}

${ai.analysis_text}
            </div>
        </div>` : ''}
        <div class="modal-section">
            <h4><i class="fas fa-tasks"></i> Dispatcher Controls</h4>
            <div class="dispatch-controls">
                <select onchange="updateStatus('${inc.id}', this.value)">
                    <option value="">Update Status...</option>
                    <option value="acknowledged">Acknowledged</option>
                    <option value="assigned">Assigned</option>
                    <option value="en_route">En Route</option>
                    <option value="arrived">Arrived</option>
                    <option value="resolved">Resolved</option>
                </select>
                <select onchange="assignTeam('${inc.id}', this.value)">
                    <option value="">Assign Team...</option>
                    ${SAMPLE_TEAMS.map(t => `<option value="${t.name}">${t.name} (${t.status.replace('_',' ')})</option>`).join('')}
                </select>
            </div>
        </div>
    `;
    document.getElementById('modalOverlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modalOverlay')?.classList.remove('active');
}

function updateStatus(id, status) {
    if (!status) return;
    const inc = incidents.find(i => i.id === id);
    if (inc) {
        inc.status = status;
        showToast(`✅ ${id} status updated to ${status.replace('_', ' ')}`, 'success');
        renderRecentTable();
        updateStats();
        closeModal();
    }
}

function assignTeam(id, team) {
    if (!team) return;
    const inc = incidents.find(i => i.id === id);
    if (inc) {
        inc.assigned_team = team;
        inc.status = 'assigned';
        showToast(`👥 ${team} assigned to ${id}`, 'info');
        renderRecentTable();
        updateStats();
        closeModal();
    }
}

// ─── Export CSV ──────────────────────────────────────────
function exportCSV() {
    const headers = ['ID', 'Title', 'Location', 'Category', 'Severity', 'Status', 'Team', 'Response Time', 'Created'];
    const rows = incidents.map(i => [i.id, `"${i.title}"`, `"${i.address}"`, i.category, i.severity, i.status, i.assigned_team || '', i.response_time_mins || '', i.created_at]);
    const csv = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'fireshield_incidents.csv'; a.click();
    showToast('📥 CSV exported successfully', 'success');
}

// ─── Toast Notifications ─────────────────────────────────
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const icons = { success: 'fa-check-circle', danger: 'fa-exclamation-circle', warning: 'fa-exclamation-triangle', info: 'fa-info-circle' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info} toast-icon"></i>
        <span class="toast-text">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
    `;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 6000);
}

// ─── Theme Toggle ────────────────────────────────────────
function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';
    html.setAttribute('data-theme', isDark ? 'light' : 'dark');
    const btn = document.getElementById('themeBtn');
    if (btn) btn.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    if (!isDark) {
        document.documentElement.style.setProperty('--bg-primary', '#0a0e1a');
        document.documentElement.style.setProperty('--bg-secondary', '#111827');
        document.documentElement.style.setProperty('--bg-card', '#1a2332');
        document.documentElement.style.setProperty('--text-primary', '#e2e8f0');
        document.documentElement.style.setProperty('--text-secondary', '#94a3b8');
    } else {
        document.documentElement.style.setProperty('--bg-primary', '#f1f5f9');
        document.documentElement.style.setProperty('--bg-secondary', '#ffffff');
        document.documentElement.style.setProperty('--bg-card', '#ffffff');
        document.documentElement.style.setProperty('--text-primary', '#1e293b');
        document.documentElement.style.setProperty('--text-secondary', '#475569');
    }
}

// ─── Helpers ─────────────────────────────────────────────
function timeAgo(dateStr) {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 60) return mins + ' min ago';
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return hrs + 'h ago';
    return Math.floor(hrs / 24) + 'd ago';
}

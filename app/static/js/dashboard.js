/**
 * PiDNS Dashboard JavaScript
 * Lightweight client-side functionality for the network monitoring dashboard
 */

class PiDNSDashboard {
    constructor() {
        this.refreshInterval = 30000; // 30 seconds
        this.intervalId = null;
        this.lastUpdate = null;

        this.init();
    }

    init() {
        // Bind event listeners
        document.getElementById('refresh-btn').addEventListener('click', () => this.refreshData());

        // Initial data load
        this.refreshData();

        // Start auto-refresh
        this.startAutoRefresh();
    }

    async refreshData() {
        try {
            // Show loading state
            this.setLoadingState(true);

            // Fetch devices and stats with authentication
            const headers = this.getAuthHeaders();
            const [devicesResponse, statsResponse] = await Promise.all([
                fetch('/api/devices', { headers }),
                fetch('/api/stats', { headers })
            ]);
    
            if (!devicesResponse.ok || !statsResponse.ok) {
                if (devicesResponse.status === 401 || statsResponse.status === 401) {
                    this.handleAuthRequired();
                    return;
                }
                throw new Error('Failed to fetch data');
            }

            const devicesData = await devicesResponse.json();
            const statsData = await statsResponse.json();

            if (devicesData.success && statsData.success) {
                this.updateStats(statsData.stats);
                this.updateDevices(devicesData.devices);
                this.updateLastUpdate();
            } else {
                throw new Error(devicesData.error || statsData.error || 'Unknown error');
            }

        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showError('Failed to load network data. Please try again.');
        } finally {
            this.setLoadingState(false);
        }
    }

    updateStats(stats) {
        document.getElementById('total-devices').textContent = stats.total_devices || 0;
        document.getElementById('active-devices').textContent = stats.active_devices || 0;

        // Update network status based on device count
        const networkStatus = document.getElementById('network-status');
        if (stats.total_devices > 0) {
            networkStatus.textContent = 'Active';
            networkStatus.style.color = '#28a745';
        } else {
            networkStatus.textContent = 'No devices';
            networkStatus.style.color = '#6c757d';
        }
    }

    updateDevices(devices) {
        const container = document.getElementById('devices-container');

        if (!devices || devices.length === 0) {
            container.innerHTML = '<div class="no-devices">No devices currently connected</div>';
            return;
        }

        // Create device list
        let html = `
            <ul class="device-list">
                <li class="device-item device-header">
                    <div>Device</div>
                    <div>IP Address</div>
                    <div>Vendor</div>
                    <div>Connected</div>
                    <div>Status</div>
                </li>
        `;

        devices.forEach(device => {
            const isActive = device.duration_seconds < 3600; // Active in last hour
            const statusClass = isActive ? 'status-active' : 'status-inactive';
            const statusText = isActive ? 'Active' : 'Inactive';

            html += `
                <li class="device-item">
                    <div class="device-info">
                        <div class="device-name">${this.escapeHtml(device.hostname || 'Unknown')}</div>
                        <div class="device-mac">${device.mac}</div>
                    </div>
                    <div class="device-ip">${device.ip}</div>
                    <div class="device-vendor">${this.escapeHtml(device.vendor)}</div>
                    <div class="device-duration">${device.duration}</div>
                    <span class="device-status ${statusClass}">${statusText}</span>
                </li>
            `;
        });

        html += '</ul>';
        container.innerHTML = html;
    }

    updateLastUpdate() {
        this.lastUpdate = new Date();
        const lastUpdateElement = document.getElementById('last-update');
        lastUpdateElement.textContent = `Last updated: ${this.formatTime(this.lastUpdate)}`;
    }

    setLoadingState(loading) {
        const refreshBtn = document.getElementById('refresh-btn');
        const container = document.getElementById('devices-container');

        if (loading) {
            refreshBtn.disabled = true;
            refreshBtn.textContent = 'Refreshing...';
            if (!container.querySelector('.loading')) {
                container.innerHTML = '<div class="loading">Loading devices...</div>';
            }
        } else {
            refreshBtn.disabled = false;
            refreshBtn.textContent = 'Refresh';
        }
    }

    showError(message) {
        const container = document.getElementById('devices-container');
        container.innerHTML = `<div class="error">${this.escapeHtml(message)}</div>`;
    }

    startAutoRefresh() {
        this.intervalId = setInterval(() => {
            this.refreshData();
        }, this.refreshInterval);
    }

    stopAutoRefresh() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    getAuthHeaders() {
        const credentials = sessionStorage.getItem('pidns_auth');
        if (credentials) {
            return {
                'Authorization': `Basic ${credentials}`
            };
        }
        return {};
    }

    handleAuthRequired() {
        const username = prompt('Enter username:');
        const password = prompt('Enter password:');
        
        if (username && password) {
            const credentials = btoa(`${username}:${password}`);
            sessionStorage.setItem('pidns_auth', credentials);
            this.refreshData();
        } else {
            this.showError('Authentication required to access the dashboard');
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.piDNSDashboard = new PiDNSDashboard();
});

// Handle page visibility changes to pause/resume auto-refresh
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        if (window.piDNSDashboard) {
            window.piDNSDashboard.stopAutoRefresh();
        }
    } else {
        if (window.piDNSDashboard) {
            window.piDNSDashboard.startAutoRefresh();
        }
    }
});
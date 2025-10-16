/**
 * PiDNS Ad-Blocker Common JavaScript
 * Shared utilities and functionality for all pages
 */

class AdBlockerCommon {
    constructor() {
        this.baseURL = '';
        this.credentials = null;
        this.refreshInterval = 30000; // 30 seconds
        
        this.init();
    }
    
    init() {
        // Get stored credentials
        this.credentials = sessionStorage.getItem('adblocker_auth');
        
        // Bind global event listeners
        this.bindEventListeners();
        
        // Initialize page-specific functionality
        this.initPageSpecific();
        
        // Start auto-refresh
        this.startAutoRefresh();
        
        // Update last update time
        this.updateLastUpdateTime();
    }
    
    bindEventListeners() {
        // Refresh button
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshPage());
        }
        
        // Close notifications
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('notification')) {
                this.hideNotification(e.target);
            }
        });
    }
    
    initPageSpecific() {
        // Page-specific initialization
        const pageClass = document.body.getAttribute('data-page');
        if (pageClass && typeof this[`init${pageClass}`] === 'function') {
            this[`init${pageClass}`]();
        }
    }
    
    // Authentication
    getAuthHeaders() {
        const headers = {};
        if (this.credentials) {
            headers['Authorization'] = `Basic ${this.credentials}`;
        }
        return headers;
    }
    
    requireAuth() {
        if (!this.credentials) {
            this.showAuthDialog();
            return false;
        }
        return true;
    }
    
    showAuthDialog() {
        const username = prompt('Enter username:');
        const password = prompt('Enter password:');
        
        if (username && password) {
            const credentials = btoa(`${username}:${password}`);
            sessionStorage.setItem('adblocker_auth', credentials);
            this.credentials = credentials;
            this.refreshPage();
        } else {
            this.showNotification('Authentication required', 'Please provide valid credentials to access the ad-blocker interface.', 'error');
        }
    }
    
    // API requests
    async apiRequest(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const fetchOptions = {
            headers: this.getAuthHeaders(),
            ...options
        };
        
        try {
            const response = await fetch(url, fetchOptions);
            
            if (response.status === 401) {
                // Clear credentials and show auth dialog
                sessionStorage.removeItem('adblocker_auth');
                this.credentials = null;
                this.showAuthDialog();
                return null;
            }
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            this.showNotification('API Error', `Failed to fetch data: ${error.message}`, 'error');
            return null;
        }
    }
    
    async get(endpoint) {
        return this.apiRequest(endpoint);
    }
    
    async post(endpoint, data) {
        return this.apiRequest(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...this.getAuthHeaders()
            },
            body: JSON.stringify(data)
        });
    }
    
    async put(endpoint, data) {
        return this.apiRequest(endpoint, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                ...this.getAuthHeaders()
            },
            body: JSON.stringify(data)
        });
    }
    
    async delete(endpoint) {
        return this.apiRequest(endpoint, {
            method: 'DELETE'
        });
    }
    
    // UI utilities
    showLoading(show = true) {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.toggle('active', show);
        }
    }
    
    showNotification(title, message, type = 'info', autoHide = true) {
        const container = document.getElementById('notification-container');
        if (!container) return;
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-title">${this.escapeHtml(title)}</div>
            <div class="notification-message">${this.escapeHtml(message)}</div>
        `;
        
        container.appendChild(notification);
        
        if (autoHide) {
            setTimeout(() => this.hideNotification(notification), 5000);
        }
    }
    
    hideNotification(notification) {
        if (notification && notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }
    
    showSuccess(message) {
        this.showNotification('Success', message, 'success');
    }
    
    showError(message) {
        this.showNotification('Error', message, 'error');
    }
    
    showWarning(message) {
        this.showNotification('Warning', message, 'warning');
    }
    
    showInfo(message) {
        this.showNotification('Info', message, 'info');
    }
    
    // Modal utilities
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
            // Focus first input in modal
            const firstInput = modal.querySelector('input, select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        }
    }
    
    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
        }
    }
    
    // Form utilities
    serializeForm(form) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                // Handle multiple values with same name
                if (!Array.isArray(data[key])) {
                    data[key] = [data[key]];
                }
                data[key].push(value);
            } else {
                data[key] = value;
            }
        }
        
        return data;
    }
    
    // Date utilities
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }
    
    formatRelativeTime(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffSecs = Math.floor(diffMs / 1000);
        const diffMins = Math.floor(diffSecs / 60);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);
        
        if (diffSecs < 60) {
            return 'Just now';
        } else if (diffMins < 60) {
            return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
        } else if (diffHours < 24) {
            return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        } else if (diffDays < 7) {
            return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
        } else {
            return this.formatDate(dateString);
        }
    }
    
    // Auto-refresh
    startAutoRefresh() {
        this.stopAutoRefresh();
        this.refreshIntervalId = setInterval(() => {
            this.refreshPage();
        }, this.refreshInterval);
    }
    
    stopAutoRefresh() {
        if (this.refreshIntervalId) {
            clearInterval(this.refreshIntervalId);
            this.refreshIntervalId = null;
        }
    }
    
    refreshPage() {
        // Check if there's a page-specific refresh function
        const pageClass = document.body.getAttribute('data-page');
        if (pageClass && typeof this[`refresh${pageClass}`] === 'function') {
            this[`refresh${pageClass}`]();
        } else {
            // Default reload
            location.reload();
        }
        
        this.updateLastUpdateTime();
    }
    
    updateLastUpdateTime() {
        const lastUpdateElement = document.getElementById('last-update');
        if (lastUpdateElement) {
            lastUpdateElement.textContent = `Last updated: ${this.formatTime(new Date())}`;
        }
    }
    
    formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }
    
    // Utility functions
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }
    
    formatPercentage(value) {
        return (value * 100).toFixed(1) + '%';
    }
    
    // Copy to clipboard
    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showSuccess('Copied to clipboard');
            }).catch(err => {
                console.error('Failed to copy: ', err);
                this.showError('Failed to copy to clipboard');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
                this.showSuccess('Copied to clipboard');
            } catch (err) {
                console.error('Failed to copy: ', err);
                this.showError('Failed to copy to clipboard');
            }
            
            document.body.removeChild(textArea);
        }
    }
    
    // Export data
    exportData(data, filename, type = 'json') {
        let content, mimeType;
        
        if (type === 'json') {
            content = JSON.stringify(data, null, 2);
            mimeType = 'application/json';
        } else if (type === 'csv') {
            content = this.convertToCSV(data);
            mimeType = 'text/csv';
        }
        
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `${filename}.${type}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    convertToCSV(data) {
        if (!Array.isArray(data) || data.length === 0) {
            return '';
        }
        
        const headers = Object.keys(data[0]);
        const csvHeaders = headers.join(',');
        const csvRows = data.map(row => {
            return headers.map(header => {
                const value = row[header];
                return typeof value === 'string' && value.includes(',') 
                    ? `"${value}"` 
                    : value;
            }).join(',');
        });
        
        return [csvHeaders, ...csvRows].join('\n');
    }
}

// Initialize common functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.adBlockerCommon = new AdBlockerCommon();
});

// Handle page visibility changes to pause/resume auto-refresh
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        if (window.adBlockerCommon) {
            window.adBlockerCommon.stopAutoRefresh();
        }
    } else {
        if (window.adBlockerCommon) {
            window.adBlockerCommon.startAutoRefresh();
        }
    }
});
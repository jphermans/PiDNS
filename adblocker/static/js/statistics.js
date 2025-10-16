/**
 * PiDNS Ad-Blocker Statistics JavaScript
 * Handles statistics display and visualization
 */

class StatisticsManager {
    constructor() {
        this.currentTab = 'overview';
        this.period = 7; // days
        this.currentPage = 1;
        this.pageSize = 50;
        this.hourlyChart = null;
        
        this.init();
    }
    
    init() {
        // Bind event listeners
        this.bindEventListeners();
        
        // Load initial data
        this.loadOverview();
    }
    
    bindEventListeners() {
        // Control buttons
        document.getElementById('refresh-btn').addEventListener('click', () => this.refreshCurrentTab());
        document.getElementById('export-btn').addEventListener('click', () => this.showExportModal());
        document.getElementById('clear-btn').addEventListener('click', () => this.showClearModal());
        
        // Period selector
        document.getElementById('period-select').addEventListener('change', (e) => {
            this.period = parseInt(e.target.value);
            this.refreshCurrentTab();
        });
        
        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.target.getAttribute('data-tab');
                this.switchTab(tab);
            });
        });
        
        // Export modal
        document.getElementById('export-confirm-btn').addEventListener('click', () => this.exportData());
        document.getElementById('cancel-export-btn').addEventListener('click', () => this.hideExportModal());
        document.getElementById('close-export-modal').addEventListener('click', () => this.hideExportModal());
        
        // Clear modal
        document.getElementById('clear-confirm-btn').addEventListener('click', () => this.clearData());
        document.getElementById('cancel-clear-btn').addEventListener('click', () => this.hideClearModal());
        document.getElementById('close-clear-modal').addEventListener('click', () => this.hideClearModal());
        
        // Queries tab controls
        document.getElementById('blocked-only-checkbox').addEventListener('change', () => this.loadQueries());
        document.getElementById('limit-select').addEventListener('change', (e) => {
            this.pageSize = parseInt(e.target.value);
            this.currentPage = 1;
            this.loadQueries();
        });
        
        // Domains tab controls
        document.getElementById('blocked-domains-checkbox').addEventListener('change', () => this.loadTopDomains());
        document.getElementById('domains-limit-select').addEventListener('change', () => this.loadTopDomains());
        
        // Clients tab controls
        document.getElementById('clients-limit-select').addEventListener('change', () => this.loadTopClients());
        
        // Hourly tab controls
        document.getElementById('hours-select').addEventListener('change', () => this.loadHourlyStats());
        
        // Pagination
        document.getElementById('prev-page-btn').addEventListener('click', () => this.previousPage());
        document.getElementById('next-page-btn').addEventListener('click', () => this.nextPage());
    }
    
    switchTab(tab) {
        // Update active tab
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(`${tab}-tab`).classList.add('active');
        
        this.currentTab = tab;
        
        // Load tab data
        switch (tab) {
            case 'overview':
                this.loadOverview();
                break;
            case 'queries':
                this.loadQueries();
                break;
            case 'domains':
                this.loadTopDomains();
                break;
            case 'clients':
                this.loadTopClients();
                break;
            case 'hourly':
                this.loadHourlyStats();
                break;
        }
    }
    
    refreshCurrentTab() {
        switch (this.currentTab) {
            case 'overview':
                this.loadOverview();
                break;
            case 'queries':
                this.loadQueries();
                break;
            case 'domains':
                this.loadTopDomains();
                break;
            case 'clients':
                this.loadTopClients();
                break;
            case 'hourly':
                this.loadHourlyStats();
                break;
        }
    }
    
    async loadOverview() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.get(`/api/statistics/overview?days=${this.period}`);
            
            if (response && response.success) {
                this.renderOverview(response.statistics);
            } else {
                window.adBlockerCommon.showError('Failed to load overview statistics');
            }
        } catch (error) {
            console.error('Error loading overview:', error);
            window.adBlockerCommon.showError('Failed to load overview statistics');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    renderOverview(stats) {
        document.getElementById('total-queries').textContent = window.adBlockerCommon.formatNumber(stats.total_queries);
        document.getElementById('blocked-queries').textContent = window.adBlockerCommon.formatNumber(stats.blocked_queries);
        document.getElementById('block-rate').textContent = `${stats.block_percentage}%`;
        document.getElementById('unique-domains').textContent = window.adBlockerCommon.formatNumber(stats.unique_domains);
        document.getElementById('dnsmasq-status').textContent = stats.dnsmasq_status;
        document.getElementById('active-blocklists').textContent = stats.active_blocklists;
        document.getElementById('unique-clients').textContent = window.adBlockerCommon.formatNumber(stats.unique_clients);
        document.getElementById('period-days').textContent = `${stats.period_days} days`;
    }
    
    async loadQueries() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const blockedOnly = document.getElementById('blocked-only-checkbox').checked;
            const offset = (this.currentPage - 1) * this.pageSize;
            
            const response = await window.adBlockerCommon.get(
                `/api/statistics/recent-queries?limit=${this.pageSize}&offset=${offset}&blocked_only=${blockedOnly}`
            );
            
            if (response && response.success) {
                this.renderQueries(response.queries);
                this.updatePagination(response.total);
            } else {
                window.adBlockerCommon.showError('Failed to load queries');
            }
        } catch (error) {
            console.error('Error loading queries:', error);
            window.adBlockerCommon.showError('Failed to load queries');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    renderQueries(queries) {
        const tbody = document.getElementById('queries-tbody');
        
        if (!queries || queries.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="no-data">No queries found</td></tr>';
            return;
        }
        
        let html = '';
        queries.forEach(query => {
            html += this.renderQueryRow(query);
        });
        
        tbody.innerHTML = html;
    }
    
    renderQueryRow(query) {
        const blockedClass = query.blocked ? 'blocked' : 'allowed';
        const blockedText = query.blocked ? 'Blocked' : 'Allowed';
        const blockListText = query.block_list_name || '-';
        
        return `
            <tr>
                <td class="timestamp">${window.adBlockerCommon.formatDateTime(query.timestamp)}</td>
                <td class="domain">${window.adBlockerCommon.escapeHtml(query.domain)}</td>
                <td class="client-ip">${query.client_ip}</td>
                <td class="type">
                    <span class="query-type ${blockedClass}">${blockedText}</span>
                </td>
                <td class="block-list">${window.adBlockerCommon.escapeHtml(blockListText)}</td>
            </tr>
        `;
    }
    
    async loadTopDomains() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const blockedOnly = document.getElementById('blocked-domains-checkbox').checked;
            const limit = parseInt(document.getElementById('domains-limit-select').value);
            
            const response = await window.adBlockerCommon.get(
                `/api/statistics/top-domains?limit=${limit}&blocked_only=${blockedOnly}&days=${this.period}`
            );
            
            if (response && response.success) {
                this.renderTopDomains(response.domains);
            } else {
                window.adBlockerCommon.showError('Failed to load top domains');
            }
        } catch (error) {
            console.error('Error loading top domains:', error);
            window.adBlockerCommon.showError('Failed to load top domains');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    renderTopDomains(domains) {
        const tbody = document.getElementById('domains-tbody');
        
        if (!domains || domains.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="no-data">No domains found</td></tr>';
            return;
        }
        
        let html = '';
        domains.forEach(domain => {
            html += `
                <tr>
                    <td class="domain">${window.adBlockerCommon.escapeHtml(domain.domain)}</td>
                    <td class="count">${window.adBlockerCommon.formatNumber(domain.count)}</td>
                    <td class="blocked">${window.adBlockerCommon.formatNumber(domain.count)}</td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
    }
    
    async loadTopClients() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const limit = parseInt(document.getElementById('clients-limit-select').value);
            
            const response = await window.adBlockerCommon.get(
                `/api/statistics/top-clients?limit=${limit}&days=${this.period}`
            );
            
            if (response && response.success) {
                this.renderTopClients(response.clients);
            } else {
                window.adBlockerCommon.showError('Failed to load top clients');
            }
        } catch (error) {
            console.error('Error loading top clients:', error);
            window.adBlockerCommon.showError('Failed to load top clients');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    renderTopClients(clients) {
        const tbody = document.getElementById('clients-tbody');
        
        if (!clients || clients.length === 0) {
            tbody.innerHTML = '<tr><td colspan="2" class="no-data">No clients found</td></tr>';
            return;
        }
        
        let html = '';
        clients.forEach(client => {
            html += `
                <tr>
                    <td class="client-ip">${client.client_ip}</td>
                    <td class="count">${window.adBlockerCommon.formatNumber(client.count)}</td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
    }
    
    async loadHourlyStats() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const hours = parseInt(document.getElementById('hours-select').value);
            
            const response = await window.adBlockerCommon.get(
                `/api/statistics/hourly?hours=${hours}`
            );
            
            if (response && response.success) {
                this.renderHourlyStats(response.hourly_stats);
            } else {
                window.adBlockerCommon.showError('Failed to load hourly statistics');
            }
        } catch (error) {
            console.error('Error loading hourly stats:', error);
            window.adBlockerCommon.showError('Failed to load hourly statistics');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    renderHourlyStats(hourlyStats) {
        const canvas = document.getElementById('hourly-chart');
        const ctx = canvas.getContext('2d');
        
        // Prepare data
        const labels = hourlyStats.map(stat => {
            const date = new Date(stat.hour);
            return date.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
        });
        
        const totalData = hourlyStats.map(stat => stat.total_queries);
        const blockedData = hourlyStats.map(stat => stat.blocked_queries);
        
        // Destroy existing chart
        if (this.hourlyChart) {
            this.hourlyChart.destroy();
        }
        
        // Create new chart
        this.hourlyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Total Queries',
                        data: totalData,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.1
                    },
                    {
                        label: 'Blocked Queries',
                        data: blockedData,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                }
            }
        });
    }
    
    updatePagination(total) {
        const totalPages = Math.ceil(total / this.pageSize);
        const pageInfo = document.getElementById('page-info');
        const prevBtn = document.getElementById('prev-page-btn');
        const nextBtn = document.getElementById('next-page-btn');
        
        pageInfo.textContent = `Page ${this.currentPage} of ${totalPages}`;
        
        prevBtn.disabled = this.currentPage <= 1;
        nextBtn.disabled = this.currentPage >= totalPages;
    }
    
    previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.loadQueries();
        }
    }
    
    nextPage() {
        const totalPages = Math.ceil(this.total / this.pageSize);
        if (this.currentPage < totalPages) {
            this.currentPage++;
            this.loadQueries();
        }
    }
    
    showExportModal() {
        window.adBlockerCommon.showModal('export-modal');
    }
    
    hideExportModal() {
        window.adBlockerCommon.hideModal('export-modal');
    }
    
    async exportData() {
        const format = document.getElementById('export-format').value;
        const days = parseInt(document.getElementById('export-days').value);
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.get(
                `/api/statistics/export?format=${format}&days=${days}`
            );
            
            if (response && response.success) {
                window.adBlockerCommon.exportData(response.data, 'statistics', format);
                window.adBlockerCommon.showSuccess('Statistics exported successfully');
                this.hideExportModal();
            } else {
                window.adBlockerCommon.showError('Failed to export statistics');
            }
        } catch (error) {
            console.error('Error exporting statistics:', error);
            window.adBlockerCommon.showError('Failed to export statistics');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    showClearModal() {
        window.adBlockerCommon.showModal('clear-modal');
    }
    
    hideClearModal() {
        window.adBlockerCommon.hideModal('clear-modal');
    }
    
    async clearData() {
        const days = document.getElementById('clear-days').value;
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.post(
                `/api/statistics/clear${days ? `?days=${days}` : ''}`
            );
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.hideClearModal();
                this.refreshCurrentTab();
            } else {
                window.adBlockerCommon.showError('Failed to clear statistics');
            }
        } catch (error) {
            console.error('Error clearing statistics:', error);
            window.adBlockerCommon.showError('Failed to clear statistics');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
}

// Initialize statistics manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.statisticsManager = new StatisticsManager();
});

// Page-specific refresh function
window.adBlockerCommon.refreshStatistics = function() {
    if (window.statisticsManager) {
        window.statisticsManager.refreshCurrentTab();
    }
};
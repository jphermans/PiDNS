/**
 * PiDNS Ad-Blocker Block Lists JavaScript
 * Handles block list management functionality
 */

class BlocklistsManager {
    constructor() {
        this.blocklists = [];
        this.predefinedLists = [];
        this.filters = {
            category: '',
            status: ''
        };
        
        this.init();
    }
    
    init() {
        // Bind event listeners
        this.bindEventListeners();
        
        // Load initial data
        this.loadBlocklists();
    }
    
    bindEventListeners() {
        // Control buttons
        document.getElementById('add-blocklist-btn').addEventListener('click', () => this.showAddModal());
        document.getElementById('update-all-btn').addEventListener('click', () => this.updateAllBlocklists());
        
        // Filters
        document.getElementById('category-filter').addEventListener('change', (e) => {
            this.filters.category = e.target.value;
            this.applyFilters();
        });
        
        document.getElementById('status-filter').addEventListener('change', (e) => {
            this.filters.status = e.target.value;
            this.applyFilters();
        });
        
        // Add modal
        document.getElementById('save-blocklist-btn').addEventListener('click', () => this.saveBlocklist());
        document.getElementById('cancel-add-btn').addEventListener('click', () => this.hideAddModal());
        document.getElementById('close-add-modal').addEventListener('click', () => this.hideAddModal());
        
        // Predefined modal
        document.getElementById('close-predefined-modal').addEventListener('click', () => this.hidePredefinedModal());
        document.getElementById('close-predefined-btn').addEventListener('click', () => this.hidePredefinedModal());
        
        // Form submission
        document.getElementById('add-blocklist-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveBlocklist();
        });
    }
    
    async loadBlocklists() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.get('/api/blocklists');
            if (response && response.success) {
                this.blocklists = response.blocklists;
                this.renderBlocklists();
            } else {
                window.adBlockerCommon.showError('Failed to load block lists');
            }
        } catch (error) {
            console.error('Error loading block lists:', error);
            window.adBlockerCommon.showError('Failed to load block lists');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async loadPredefinedLists() {
        try {
            const response = await window.adBlockerCommon.get('/api/blocklists/predefined');
            if (response && response.success) {
                this.predefinedLists = response.predefined_blocklists;
                this.renderPredefinedLists();
            } else {
                window.adBlockerCommon.showError('Failed to load predefined block lists');
            }
        } catch (error) {
            console.error('Error loading predefined block lists:', error);
            window.adBlockerCommon.showError('Failed to load predefined block lists');
        }
    }
    
    renderBlocklists() {
        const container = document.getElementById('blocklist-grid');
        
        if (!this.blocklists || this.blocklists.length === 0) {
            container.innerHTML = '<div class="no-data">No block lists found</div>';
            return;
        }
        
        const filteredLists = this.getFilteredBlocklists();
        
        let html = '';
        filteredLists.forEach(blocklist => {
            html += this.renderBlocklistCard(blocklist);
        });
        
        container.innerHTML = html;
        
        // Bind event listeners to the new elements
        this.bindCardEventListeners();
    }
    
    renderBlocklistCard(blocklist) {
        const lastUpdated = blocklist.last_updated 
            ? window.adBlockerCommon.formatRelativeTime(blocklist.last_updated)
            : 'Never';
        
        const needsUpdate = this.needsUpdate(blocklist);
        
        return `
            <div class="blocklist-card" data-id="${blocklist.id}">
                <div class="blocklist-header">
                    <div class="blocklist-title">${window.adBlockerCommon.escapeHtml(blocklist.name)}</div>
                    <div class="blocklist-status ${blocklist.enabled ? 'active' : 'inactive'}"></div>
                </div>
                
                <div class="blocklist-info">
                    <div class="blocklist-info-item">
                        <span>Category:</span>
                        <span class="category">${blocklist.category}</span>
                    </div>
                    <div class="blocklist-info-item">
                        <span>Entries:</span>
                        <span>${window.adBlockerCommon.formatNumber(blocklist.entry_count || 0)}</span>
                    </div>
                    <div class="blocklist-info-item">
                        <span>Last Updated:</span>
                        <span>${lastUpdated}</span>
                    </div>
                    <div class="blocklist-info-item">
                        <span>Status:</span>
                        <span class="${needsUpdate ? 'warning' : 'success'}">
                            ${needsUpdate ? 'Needs Update' : 'Up to Date'}
                        </span>
                    </div>
                </div>
                
                <div class="blocklist-description">
                    ${window.adBlockerCommon.escapeHtml(blocklist.description || 'No description')}
                </div>
                
                <div class="blocklist-actions">
                    <button class="btn btn-sm ${blocklist.enabled ? 'btn-warning' : 'btn-success'} toggle-btn" 
                            data-id="${blocklist.id}">
                        ${blocklist.enabled ? 'Disable' : 'Enable'}
                    </button>
                    <button class="btn btn-sm btn-primary update-btn" data-id="${blocklist.id}">
                        Update
                    </button>
                    <button class="btn btn-sm btn-danger delete-btn" data-id="${blocklist.id}">
                        Delete
                    </button>
                </div>
            </div>
        `;
    }
    
    renderPredefinedLists() {
        const container = document.getElementById('predefined-lists');
        
        if (!this.predefinedLists || this.predefinedLists.length === 0) {
            container.innerHTML = '<div class="no-data">No predefined block lists available</div>';
            return;
        }
        
        let html = '<div class="predefined-grid">';
        this.predefinedLists.forEach(list => {
            html += this.renderPredefinedCard(list);
        });
        html += '</div>';
        
        container.innerHTML = html;
        
        // Bind event listeners
        this.bindPredefinedEventListeners();
    }
    
    renderPredefinedCard(list) {
        const isInDatabase = list.in_database;
        const isEnabled = list.database_enabled;
        
        return `
            <div class="predefined-card">
                <div class="predefined-header">
                    <div class="predefined-title">${window.adBlockerCommon.escapeHtml(list.name)}</div>
                    <div class="predefined-category">${list.category}</div>
                </div>
                
                <div class="predefined-info">
                    <div class="predefined-info-item">
                        <span>URL:</span>
                        <span class="url">${window.adBlockerCommon.escapeHtml(list.url)}</span>
                    </div>
                    <div class="predefined-info-item">
                        <span>Description:</span>
                        <span>Predefined ${list.category} block list</span>
                    </div>
                </div>
                
                <div class="predefined-actions">
                    ${isInDatabase 
                        ? `<div class="in-db">Already in database (${isEnabled ? 'enabled' : 'disabled'})</div>`
                        : `<button class="btn btn-sm btn-primary add-predefined-btn" data-url="${list.url}">
                            Add to Database
                        </button>`
                    }
                </div>
            </div>
        `;
    }
    
    bindCardEventListeners() {
        // Toggle buttons
        document.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                this.toggleBlocklist(id);
            });
        });
        
        // Update buttons
        document.querySelectorAll('.update-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                this.updateBlocklist(id);
            });
        });
        
        // Delete buttons
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                this.deleteBlocklist(id);
            });
        });
    }
    
    bindPredefinedEventListeners() {
        document.querySelectorAll('.add-predefined-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const url = e.target.getAttribute('data-url');
                this.addPredefinedBlocklist(url);
            });
        });
    }
    
    getFilteredBlocklists() {
        let filtered = [...this.blocklists];
        
        if (this.filters.category) {
            filtered = filtered.filter(bl => bl.category === this.filters.category);
        }
        
        if (this.filters.status) {
            enabled = this.filters.status === 'enabled';
            filtered = filtered.filter(bl => bl.enabled === enabled);
        }
        
        return filtered;
    }
    
    applyFilters() {
        this.renderBlocklists();
    }
    
    needsUpdate(blocklist) {
        if (!blocklist.last_updated) return true;
        
        const updateTime = new Date(blocklist.last_updated);
        const now = new Date();
        const diffHours = (now - updateTime) / (1000 * 60 * 60);
        
        return diffHours > 24; // Needs update if older than 24 hours
    }
    
    showAddModal() {
        window.adBlockerCommon.showModal('add-blocklist-modal');
        document.getElementById('blocklist-name').focus();
    }
    
    hideAddModal() {
        window.adBlockerCommon.hideModal('add-blocklist-modal');
        document.getElementById('add-blocklist-form').reset();
    }
    
    showPredefinedModal() {
        window.adBlockerCommon.showModal('predefined-modal');
        this.loadPredefinedLists();
    }
    
    hidePredefinedModal() {
        window.adBlockerCommon.hideModal('predefined-modal');
    }
    
    async saveBlocklist() {
        const form = document.getElementById('add-blocklist-form');
        const formData = window.adBlockerCommon.serializeForm(form);
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.post('/api/blocklists', formData);
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.hideAddModal();
                this.loadBlocklists();
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to save block list');
            }
        } catch (error) {
            console.error('Error saving block list:', error);
            window.adBlockerCommon.showError('Failed to save block list');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async toggleBlocklist(id) {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.post(`/api/blocklists/${id}/toggle`);
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.loadBlocklists();
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to toggle block list');
            }
        } catch (error) {
            console.error('Error toggling block list:', error);
            window.adBlockerCommon.showError('Failed to toggle block list');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async updateBlocklist(id) {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.post(`/api/blocklists/${id}/update`);
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.loadBlocklists();
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to update block list');
            }
        } catch (error) {
            console.error('Error updating block list:', error);
            window.adBlockerCommon.showError('Failed to update block list');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async deleteBlocklist(id) {
        if (!confirm('Are you sure you want to delete this block list?')) {
            return;
        }
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.delete(`/api/blocklists/${id}`);
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.loadBlocklists();
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to delete block list');
            }
        } catch (error) {
            console.error('Error deleting block list:', error);
            window.adBlockerCommon.showError('Failed to delete block list');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async updateAllBlocklists() {
        if (!confirm('Update all enabled block lists? This may take a few minutes.')) {
            return;
        }
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.post('/api/blocklists/update-all');
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.loadBlocklists();
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to update block lists');
            }
        } catch (error) {
            console.error('Error updating block lists:', error);
            window.adBlockerCommon.showError('Failed to update block lists');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async addPredefinedBlocklist(url) {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.post('/api/blocklists/predefined', { url });
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.loadPredefinedLists();
                this.loadBlocklists();
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to add predefined block list');
            }
        } catch (error) {
            console.error('Error adding predefined block list:', error);
            window.adBlockerCommon.showError('Failed to add predefined block list');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
}

// Initialize blocklists manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.blocklistsManager = new BlocklistsManager();
});

// Page-specific refresh function
window.adBlockerCommon.refreshBlocklists = function() {
    if (window.blocklistsManager) {
        window.blocklistsManager.loadBlocklists();
    }
};
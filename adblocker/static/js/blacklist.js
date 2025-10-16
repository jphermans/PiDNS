/**
 * PiDNS Ad-Blocker Blacklist JavaScript
 * Handles blacklist management functionality
 */

class BlacklistManager {
    constructor() {
        this.entries = [];
        this.filters = {
            category: '',
            status: '',
            search: ''
        };
        
        this.init();
    }
    
    init() {
        // Bind event listeners
        this.bindEventListeners();
        
        // Load initial data
        this.loadBlacklist();
    }
    
    bindEventListeners() {
        // Control buttons
        document.getElementById('add-blacklist-btn').addEventListener('click', () => this.showAddModal());
        document.getElementById('import-blacklist-btn').addEventListener('click', () => this.showImportModal());
        document.getElementById('export-blacklist-btn').addEventListener('click', () => this.exportBlacklist());
        document.getElementById('cleanup-btn').addEventListener('click', () => this.cleanupExpired());
        
        // Filters
        document.getElementById('category-filter').addEventListener('change', (e) => {
            this.filters.category = e.target.value;
            this.applyFilters();
        });
        
        document.getElementById('status-filter').addEventListener('change', (e) => {
            this.filters.status = e.target.value;
            this.applyFilters();
        });
        
        document.getElementById('search-input').addEventListener('input', (e) => {
            this.filters.search = e.target.value.toLowerCase();
            this.applyFilters();
        });
        
        // Blacklist modal
        document.getElementById('save-blacklist-btn').addEventListener('click', () => this.saveEntry());
        document.getElementById('cancel-blacklist-btn').addEventListener('click', () => this.hideBlacklistModal());
        document.getElementById('close-blacklist-modal').addEventListener('click', () => this.hideBlacklistModal());
        
        // Import modal
        document.getElementById('import-blacklist-confirm-btn').addEventListener('click', () => this.importEntries());
        document.getElementById('cancel-import-btn').addEventListener('click', () => this.hideImportModal());
        document.getElementById('close-import-modal').addEventListener('click', () => this.hideImportModal());
        
        // Import inputs
        document.getElementById('import-file').addEventListener('change', (e) => this.handleFileUpload(e));
        document.getElementById('import-data').addEventListener('input', () => this.updateImportPreview());
        
        // Form submission
        document.getElementById('blacklist-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveEntry();
        });
    }
    
    async loadBlacklist() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.get('/api/blacklist');
            if (response && response.success) {
                this.entries = response.entries;
                this.renderBlacklist();
            } else {
                window.adBlockerCommon.showError('Failed to load blacklist entries');
            }
        } catch (error) {
            console.error('Error loading blacklist:', error);
            window.adBlockerCommon.showError('Failed to load blacklist entries');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    renderBlacklist() {
        const tbody = document.getElementById('blacklist-tbody');
        
        if (!this.entries || this.entries.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="no-data">No blacklist entries found</td></tr>';
            return;
        }
        
        const filteredEntries = this.getFilteredEntries();
        
        if (filteredEntries.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="no-data">No entries match the current filters</td></tr>';
            return;
        }
        
        let html = '';
        filteredEntries.forEach(entry => {
            html += this.renderEntryRow(entry);
        });
        
        tbody.innerHTML = html;
        
        // Bind event listeners to the new elements
        this.bindRowEventListeners();
    }
    
    renderEntryRow(entry) {
        const isExpired = entry.expires_at && new Date(entry.expires_at) < new Date();
        const statusClass = isExpired ? 'expired' : 'active';
        const statusText = isExpired ? 'Expired' : 'Active';
        
        const expiresText = entry.expires_at 
            ? window.adBlockerCommon.formatDate(entry.expires_at)
            : 'Never';
        
        const createdText = entry.created_at 
            ? window.adBlockerCommon.formatDate(entry.created_at)
            : 'Unknown';
        
        return `
            <tr data-id="${entry.id}">
                <td class="domain">${window.adBlockerCommon.escapeHtml(entry.domain)}</td>
                <td class="category">${entry.category}</td>
                <td class="created">${createdText}</td>
                <td class="expires">${expiresText}</td>
                <td class="status">
                    <span class="status-badge ${statusClass}">${statusText}</span>
                </td>
                <td class="notes">${window.adBlockerCommon.escapeHtml(entry.notes || '')}</td>
                <td class="actions">
                    <button class="btn btn-sm btn-primary edit-btn" data-id="${entry.id}">Edit</button>
                    <button class="btn btn-sm btn-danger delete-btn" data-id="${entry.id}">Delete</button>
                </td>
            </tr>
        `;
    }
    
    bindRowEventListeners() {
        // Edit buttons
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                this.editEntry(id);
            });
        });
        
        // Delete buttons
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                this.deleteEntry(id);
            });
        });
    }
    
    getFilteredEntries() {
        let filtered = [...this.entries];
        
        if (this.filters.category) {
            filtered = filtered.filter(entry => entry.category === this.filters.category);
        }
        
        if (this.filters.status) {
            if (this.filters.status === 'active') {
                filtered = filtered.filter(entry => {
                    return !entry.expires_at || new Date(entry.expires_at) >= new Date();
                });
            } else if (this.filters.status === 'expired') {
                filtered = filtered.filter(entry => {
                    return entry.expires_at && new Date(entry.expires_at) < new Date();
                });
            }
        }
        
        if (this.filters.search) {
            filtered = filtered.filter(entry => 
                entry.domain.toLowerCase().includes(this.filters.search) ||
                (entry.notes && entry.notes.toLowerCase().includes(this.filters.search))
            );
        }
        
        return filtered;
    }
    
    applyFilters() {
        this.renderBlacklist();
    }
    
    showAddModal() {
        document.getElementById('modal-title').textContent = 'Add Blacklist Entry';
        document.getElementById('blacklist-form').reset();
        document.getElementById('entry-id').value = '';
        window.adBlockerCommon.showModal('blacklist-modal');
        document.getElementById('domain-input').focus();
    }
    
    hideBlacklistModal() {
        window.adBlockerCommon.hideModal('blacklist-modal');
        document.getElementById('blacklist-form').reset();
    }
    
    showImportModal() {
        window.adBlockerCommon.showModal('import-modal');
        this.updateImportPreview();
    }
    
    hideImportModal() {
        window.adBlockerCommon.hideModal('import-modal');
        document.getElementById('import-file').value = '';
        document.getElementById('import-data').value = '';
        document.getElementById('preview-content').textContent = 'No entries to preview';
    }
    
    async editEntry(id) {
        try {
            const entry = this.entries.find(e => e.id == id);
            if (!entry) {
                window.adBlockerCommon.showError('Entry not found');
                return;
            }
            
            // Populate form
            document.getElementById('modal-title').textContent = 'Edit Blacklist Entry';
            document.getElementById('entry-id').value = entry.id;
            document.getElementById('domain-input').value = entry.domain;
            document.getElementById('category-input').value = entry.category;
            
            if (entry.expires_at) {
                // Format datetime-local input value
                const date = new Date(entry.expires_at);
                const year = date.getFullYear();
                const month = String(date.getMonth() + 1).padStart(2, '0');
                const day = String(date.getDate()).padStart(2, '0');
                const hours = String(date.getHours()).padStart(2, '0');
                const minutes = String(date.getMinutes()).padStart(2, '0');
                
                document.getElementById('expires-input').value = `${year}-${month}-${day}T${hours}:${minutes}`;
            }
            
            document.getElementById('notes-input').value = entry.notes || '';
            
            window.adBlockerCommon.showModal('blacklist-modal');
            document.getElementById('domain-input').focus();
            
        } catch (error) {
            console.error('Error editing entry:', error);
            window.adBlockerCommon.showError('Failed to edit entry');
        }
    }
    
    async saveEntry() {
        const form = document.getElementById('blacklist-form');
        const formData = window.adBlockerCommon.serializeForm(form);
        const entryId = formData.id;
        
        // Format expiration date
        if (formData.expires_at) {
            const date = new Date(formData.expires_at);
            formData.expires_at = date.toISOString();
        } else {
            delete formData.expires_at;
        }
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            let response;
            if (entryId) {
                // Update existing entry
                response = await window.adBlockerCommon.put(`/api/blacklist/${entryId}`, formData);
            } else {
                // Create new entry
                response = await window.adBlockerCommon.post('/api/blacklist', formData);
            }
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.hideBlacklistModal();
                this.loadBlacklist();
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to save entry');
            }
        } catch (error) {
            console.error('Error saving entry:', error);
            window.adBlockerCommon.showError('Failed to save entry');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async deleteEntry(id) {
        if (!confirm('Are you sure you want to delete this blacklist entry?')) {
            return;
        }
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.delete(`/api/blacklist/${id}`);
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.loadBlacklist();
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to delete entry');
            }
        } catch (error) {
            console.error('Error deleting entry:', error);
            window.adBlockerCommon.showError('Failed to delete entry');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async exportBlacklist() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.get('/api/blacklist/export');
            
            if (response && response.success) {
                window.adBlockerCommon.exportData(response.entries, 'blacklist', 'json');
                window.adBlockerCommon.showSuccess('Blacklist exported successfully');
            } else {
                window.adBlockerCommon.showError('Failed to export blacklist');
            }
        } catch (error) {
            console.error('Error exporting blacklist:', error);
            window.adBlockerCommon.showError('Failed to export blacklist');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async cleanupExpired() {
        if (!confirm('Are you sure you want to remove all expired blacklist entries?')) {
            return;
        }
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.post('/api/blacklist/cleanup');
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.loadBlacklist();
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to cleanup expired entries');
            }
        } catch (error) {
            console.error('Error cleaning up expired entries:', error);
            window.adBlockerCommon.showError('Failed to cleanup expired entries');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('import-data').value = e.target.result;
            this.updateImportPreview();
        };
        reader.readAsText(file);
    }
    
    updateImportPreview() {
        const data = document.getElementById('import-data').value;
        const previewContent = document.getElementById('preview-content');
        
        if (!data.trim()) {
            previewContent.textContent = 'No entries to preview';
            return;
        }
        
        // Parse entries
        const lines = data.split('\n').filter(line => line.trim());
        const entries = lines.map(line => {
            const domain = line.trim().toLowerCase();
            return { domain };
        });
        
        // Show preview
        if (entries.length > 0) {
            const previewHtml = entries.slice(0, 10).map(entry => 
                `<div>${window.adBlockerCommon.escapeHtml(entry.domain)}</div>`
            ).join('');
            
            previewContent.innerHTML = previewHtml + 
                (entries.length > 10 ? `<div class="preview-more">... and ${entries.length - 10} more</div>` : '');
        } else {
            previewContent.textContent = 'No valid entries found';
        }
    }
    
    async importEntries() {
        const data = document.getElementById('import-data').value;
        const category = document.getElementById('import-category').value;
        
        if (!data.trim()) {
            window.adBlockerCommon.showError('No entries to import');
            return;
        }
        
        // Parse entries
        const lines = data.split('\n').filter(line => line.trim());
        const entries = lines.map(line => {
            const domain = line.trim().toLowerCase();
            return { domain, category };
        });
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.post('/api/blacklist/batch', {
                entries: entries,
                category: category
            });
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.hideImportModal();
                this.loadBlacklist();
                
                // Show import statistics
                const result = response.result;
                if ((result.errors && result.errors.length > 0) || result.skipped > 0) {
                    let message = `Imported ${result.added} entries`;
                    if (result.skipped > 0) {
                        message += `, skipped ${result.skipped}`;
                    }
                    if (result.errors && result.errors.length > 0) {
                        message += `, errors: ${result.errors.slice(0, 3).join(', ')}`;
                        if (result.errors.length > 3) {
                            message += ` and ${result.errors.length - 3} more`;
                        }
                    }
                    window.adBlockerCommon.showInfo(message);
                }
            } else {
                window.adBlockerCommon.showError(response.error || 'Failed to import entries');
            }
        } catch (error) {
            console.error('Error importing entries:', error);
            window.adBlockerCommon.showError('Failed to import entries');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
}

// Initialize blacklist manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.blacklistManager = new BlacklistManager();
});

// Page-specific refresh function
window.adBlockerCommon.refreshBlacklist = function() {
    if (window.blacklistManager) {
        window.blacklistManager.loadBlacklist();
    }
};
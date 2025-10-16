/**
 * PiDNS Ad-Blocker Whitelist JavaScript
 * Handles whitelist management functionality
 */

class WhitelistManager {
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
        this.loadWhitelist();
    }
    
    bindEventListeners() {
        // Control buttons
        document.getElementById('add-whitelist-btn').addEventListener('click', () => this.showAddModal());
        document.getElementById('import-whitelist-btn').addEventListener('click', () => this.showImportModal());
        document.getElementById('export-whitelist-btn').addEventListener('click', () => this.exportWhitelist());
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
        
        // Whitelist modal
        document.getElementById('save-whitelist-btn').addEventListener('click', () => this.saveEntry());
        document.getElementById('cancel-whitelist-btn').addEventListener('click', () => this.hideWhitelistModal());
        document.getElementById('close-whitelist-modal').addEventListener('click', () => this.hideWhitelistModal());
        
        // Import modal
        document.getElementById('import-whitelist-confirm-btn').addEventListener('click', () => this.importEntries());
        document.getElementById('cancel-import-btn').addEventListener('click', () => this.hideImportModal());
        document.getElementById('close-import-modal').addEventListener('click', () => this.hideImportModal());
        
        // Import inputs
        document.getElementById('import-file').addEventListener('change', (e) => this.handleFileUpload(e));
        document.getElementById('import-data').addEventListener('input', () => this.updateImportPreview());
        
        // Form submission
        document.getElementById('whitelist-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveEntry();
        });
    }
    
    async loadWhitelist() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.get('/api/whitelist');
            if (response && response.success) {
                this.entries = response.entries;
                this.renderWhitelist();
            } else {
                window.adBlockerCommon.showError('Failed to load whitelist entries');
            }
        } catch (error) {
            console.error('Error loading whitelist:', error);
            window.adBlockerCommon.showError('Failed to load whitelist entries');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    renderWhitelist() {
        const tbody = document.getElementById('whitelist-tbody');
        
        if (!this.entries || this.entries.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="no-data">No whitelist entries found</td></tr>';
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
        this.renderWhitelist();
    }
    
    showAddModal() {
        document.getElementById('modal-title').textContent = 'Add Whitelist Entry';
        document.getElementById('whitelist-form').reset();
        document.getElementById('entry-id').value = '';
        window.adBlockerCommon.showModal('whitelist-modal');
        document.getElementById('domain-input').focus();
    }
    
    hideWhitelistModal() {
        window.adBlockerCommon.hideModal('whitelist-modal');
        document.getElementById('whitelist-form').reset();
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
            document.getElementById('modal-title').textContent = 'Edit Whitelist Entry';
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
            
            window.adBlockerCommon.showModal('whitelist-modal');
            document.getElementById('domain-input').focus();
            
        } catch (error) {
            console.error('Error editing entry:', error);
            window.adBlockerCommon.showError('Failed to edit entry');
        }
    }
    
    async saveEntry() {
        const form = document.getElementById('whitelist-form');
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
                response = await window.adBlockerCommon.put(`/api/whitelist/${entryId}`, formData);
            } else {
                // Create new entry
                response = await window.adBlockerCommon.post('/api/whitelist', formData);
            }
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.hideWhitelistModal();
                this.loadWhitelist();
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
        if (!confirm('Are you sure you want to delete this whitelist entry?')) {
            return;
        }
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.delete(`/api/whitelist/${id}`);
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.loadWhitelist();
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
    
    async exportWhitelist() {
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.get('/api/whitelist/export');
            
            if (response && response.success) {
                window.adBlockerCommon.exportData(response.entries, 'whitelist', 'json');
                window.adBlockerCommon.showSuccess('Whitelist exported successfully');
            } else {
                window.adBlockerCommon.showError('Failed to export whitelist');
            }
        } catch (error) {
            console.error('Error exporting whitelist:', error);
            window.adBlockerCommon.showError('Failed to export whitelist');
        } finally {
            window.adBlockerCommon.showLoading(false);
        }
    }
    
    async cleanupExpired() {
        if (!confirm('Are you sure you want to remove all expired whitelist entries?')) {
            return;
        }
        
        try {
            window.adBlockerCommon.showLoading(true);
            
            const response = await window.adBlockerCommon.post('/api/whitelist/cleanup');
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.loadWhitelist();
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
            
            const response = await window.adBlockerCommon.post('/api/whitelist/batch', {
                entries: entries,
                category: category
            });
            
            if (response && response.success) {
                window.adBlockerCommon.showSuccess(response.message);
                this.hideImportModal();
                this.loadWhitelist();
                
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

// Initialize whitelist manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.whitelistManager = new WhitelistManager();
});

// Page-specific refresh function
window.adBlockerCommon.refreshWhitelist = function() {
    if (window.whitelistManager) {
        window.whitelistManager.loadWhitelist();
    }
};
"""
Whitelist and Blacklist manager for PiDNS Ad-Blocker
Handles management of custom whitelist and blacklist entries
"""

import logging
from datetime import datetime, timedelta

from adblocker.models.database import Whitelist, Blacklist, db
from adblocker.services.dnsmasq_manager import DnsmasqManager

logger = logging.getLogger(__name__)

class ListManager:
    """Manages whitelist and blacklist entries"""
    
    def __init__(self, config):
        self.config = config
        self.dnsmasq_manager = DnsmasqManager(config)
    
    def add_whitelist_entry(self, domain, category='custom', expires_at=None, notes=''):
        """Add a domain to the whitelist"""
        try:
            # Check if domain already exists
            existing = Whitelist.query.filter_by(domain=domain.lower()).first()
            if existing:
                return False, "Domain already in whitelist"
            
            # Create new whitelist entry
            entry = Whitelist(
                domain=domain.lower(),
                category=category,
                expires_at=expires_at,
                notes=notes
            )
            
            db.session.add(entry)
            db.session.commit()
            
            # Update configuration
            self.update_whitelist_config()
            
            logger.info(f"Added {domain} to whitelist")
            return True, "Domain added to whitelist successfully"
            
        except Exception as e:
            logger.error(f"Failed to add whitelist entry: {e}")
            db.session.rollback()
            return False, str(e)
    
    def remove_whitelist_entry(self, entry_id):
        """Remove a domain from the whitelist"""
        try:
            entry = Whitelist.query.get(entry_id)
            if not entry:
                return False, "Whitelist entry not found"
            
            domain = entry.domain
            db.session.delete(entry)
            db.session.commit()
            
            # Update configuration
            self.update_whitelist_config()
            
            logger.info(f"Removed {domain} from whitelist")
            return True, "Domain removed from whitelist successfully"
            
        except Exception as e:
            logger.error(f"Failed to remove whitelist entry: {e}")
            db.session.rollback()
            return False, str(e)
    
    def update_whitelist_entry(self, entry_id, category=None, expires_at=None, notes=None):
        """Update a whitelist entry"""
        try:
            entry = Whitelist.query.get(entry_id)
            if not entry:
                return False, "Whitelist entry not found"
            
            # Update fields if provided
            if category is not None:
                entry.category = category
            if expires_at is not None:
                entry.expires_at = expires_at
            if notes is not None:
                entry.notes = notes
            
            entry.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Update configuration
            self.update_whitelist_config()
            
            logger.info(f"Updated whitelist entry for {entry.domain}")
            return True, "Whitelist entry updated successfully"
            
        except Exception as e:
            logger.error(f"Failed to update whitelist entry: {e}")
            db.session.rollback()
            return False, str(e)
    
    def get_whitelist_entries(self, category=None, include_expired=False):
        """Get whitelist entries"""
        try:
            query = Whitelist.query
            
            if category:
                query = query.filter_by(category=category)
            
            entries = query.all()
            
            # Filter expired entries if requested
            if not include_expired:
                entries = [entry for entry in entries if not entry.is_expired()]
            
            return [entry.to_dict() for entry in entries]
            
        except Exception as e:
            logger.error(f"Failed to get whitelist entries: {e}")
            return []
    
    def add_blacklist_entry(self, domain, category='custom', expires_at=None, notes=''):
        """Add a domain to the blacklist"""
        try:
            # Check if domain already exists
            existing = Blacklist.query.filter_by(domain=domain.lower()).first()
            if existing:
                return False, "Domain already in blacklist"
            
            # Create new blacklist entry
            entry = Blacklist(
                domain=domain.lower(),
                category=category,
                expires_at=expires_at,
                notes=notes
            )
            
            db.session.add(entry)
            db.session.commit()
            
            # Update configuration
            self.update_blacklist_config()
            
            logger.info(f"Added {domain} to blacklist")
            return True, "Domain added to blacklist successfully"
            
        except Exception as e:
            logger.error(f"Failed to add blacklist entry: {e}")
            db.session.rollback()
            return False, str(e)
    
    def remove_blacklist_entry(self, entry_id):
        """Remove a domain from the blacklist"""
        try:
            entry = Blacklist.query.get(entry_id)
            if not entry:
                return False, "Blacklist entry not found"
            
            domain = entry.domain
            db.session.delete(entry)
            db.session.commit()
            
            # Update configuration
            self.update_blacklist_config()
            
            logger.info(f"Removed {domain} from blacklist")
            return True, "Domain removed from blacklist successfully"
            
        except Exception as e:
            logger.error(f"Failed to remove blacklist entry: {e}")
            db.session.rollback()
            return False, str(e)
    
    def update_blacklist_entry(self, entry_id, category=None, expires_at=None, notes=None):
        """Update a blacklist entry"""
        try:
            entry = Blacklist.query.get(entry_id)
            if not entry:
                return False, "Blacklist entry not found"
            
            # Update fields if provided
            if category is not None:
                entry.category = category
            if expires_at is not None:
                entry.expires_at = expires_at
            if notes is not None:
                entry.notes = notes
            
            entry.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Update configuration
            self.update_blacklist_config()
            
            logger.info(f"Updated blacklist entry for {entry.domain}")
            return True, "Blacklist entry updated successfully"
            
        except Exception as e:
            logger.error(f"Failed to update blacklist entry: {e}")
            db.session.rollback()
            return False, str(e)
    
    def get_blacklist_entries(self, category=None, include_expired=False):
        """Get blacklist entries"""
        try:
            query = Blacklist.query
            
            if category:
                query = query.filter_by(category=category)
            
            entries = query.all()
            
            # Filter expired entries if requested
            if not include_expired:
                entries = [entry for entry in entries if not entry.is_expired()]
            
            return [entry.to_dict() for entry in entries]
            
        except Exception as e:
            logger.error(f"Failed to get blacklist entries: {e}")
            return []
    
    def update_whitelist_config(self):
        """Update dnsmasq whitelist configuration"""
        try:
            # Get all non-expired whitelist entries
            entries = Whitelist.query.all()
            whitelist_domains = [entry.domain for entry in entries if not entry.is_expired()]
            
            # Generate configuration
            self.dnsmasq_manager.generate_whitelist_config(whitelist_domains)
            
            # Reload dnsmasq
            self.dnsmasq_manager.reload_dnsmasq()
            
            logger.info(f"Updated whitelist configuration with {len(whitelist_domains)} domains")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update whitelist configuration: {e}")
            return False
    
    def update_blacklist_config(self):
        """Update dnsmasq blacklist configuration"""
        try:
            # Get all non-expired blacklist entries
            entries = Blacklist.query.all()
            blacklist_domains = [entry.domain for entry in entries if not entry.is_expired()]
            
            # Generate configuration
            self.dnsmasq_manager.generate_blacklist_config(blacklist_domains)
            
            # Reload dnsmasq
            self.dnsmasq_manager.reload_dnsmasq()
            
            logger.info(f"Updated blacklist configuration with {len(blacklist_domains)} domains")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update blacklist configuration: {e}")
            return False
    
    def cleanup_expired_entries(self):
        """Clean up expired whitelist and blacklist entries"""
        try:
            current_time = datetime.utcnow()
            
            # Clean expired whitelist entries
            expired_whitelist = Whitelist.query.filter(
                Whitelist.expires_at.isnot(None),
                Whitelist.expires_at < current_time
            ).all()
            
            for entry in expired_whitelist:
                db.session.delete(entry)
                logger.info(f"Removed expired whitelist entry: {entry.domain}")
            
            # Clean expired blacklist entries
            expired_blacklist = Blacklist.query.filter(
                Blacklist.expires_at.isnot(None),
                Blacklist.expires_at < current_time
            ).all()
            
            for entry in expired_blacklist:
                db.session.delete(entry)
                logger.info(f"Removed expired blacklist entry: {entry.domain}")
            
            db.session.commit()
            
            # Update configurations if entries were removed
            if expired_whitelist or expired_blacklist:
                self.update_whitelist_config()
                self.update_blacklist_config()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired entries: {e}")
            db.session.rollback()
            return False
    
    def get_statistics(self):
        """Get whitelist and blacklist statistics"""
        try:
            # Get whitelist statistics
            whitelist_total = Whitelist.query.count()
            whitelist_active = len([e for e in Whitelist.query.all() if not e.is_expired()])
            
            # Get blacklist statistics
            blacklist_total = Blacklist.query.count()
            blacklist_active = len([e for e in Blacklist.query.all() if not e.is_expired()])
            
            # Get category statistics
            whitelist_categories = {}
            for entry in Whitelist.query.all():
                if not entry.is_expired():
                    category = entry.category
                    whitelist_categories[category] = whitelist_categories.get(category, 0) + 1
            
            blacklist_categories = {}
            for entry in Blacklist.query.all():
                if not entry.is_expired():
                    category = entry.category
                    blacklist_categories[category] = blacklist_categories.get(category, 0) + 1
            
            return {
                'whitelist': {
                    'total': whitelist_total,
                    'active': whitelist_active,
                    'expired': whitelist_total - whitelist_active,
                    'categories': whitelist_categories
                },
                'blacklist': {
                    'total': blacklist_total,
                    'active': blacklist_active,
                    'expired': blacklist_total - blacklist_active,
                    'categories': blacklist_categories
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get list statistics: {e}")
            return {}
    
    def import_entries(self, entries, list_type='whitelist', category='custom'):
        """Import multiple entries to whitelist or blacklist"""
        try:
            added_count = 0
            skipped_count = 0
            errors = []
            
            for entry_data in entries:
                domain = entry_data.get('domain', '').strip().lower()
                if not domain:
                    skipped_count += 1
                    continue
                
                # Check if domain already exists
                if list_type == 'whitelist':
                    existing = Whitelist.query.filter_by(domain=domain).first()
                else:
                    existing = Blacklist.query.filter_by(domain=domain).first()
                
                if existing:
                    skipped_count += 1
                    continue
                
                # Parse expiration date if provided
                expires_at = None
                if entry_data.get('expires_at'):
                    try:
                        expires_at = datetime.fromisoformat(entry_data['expires_at'])
                    except ValueError:
                        errors.append(f"Invalid expiration date for {domain}")
                        continue
                
                # Add entry
                if list_type == 'whitelist':
                    entry = Whitelist(
                        domain=domain,
                        category=entry_data.get('category', category),
                        expires_at=expires_at,
                        notes=entry_data.get('notes', '')
                    )
                else:
                    entry = Blacklist(
                        domain=domain,
                        category=entry_data.get('category', category),
                        expires_at=expires_at,
                        notes=entry_data.get('notes', '')
                    )
                
                db.session.add(entry)
                added_count += 1
            
            db.session.commit()
            
            # Update configuration
            if list_type == 'whitelist':
                self.update_whitelist_config()
            else:
                self.update_blacklist_config()
            
            result = {
                'added': added_count,
                'skipped': skipped_count,
                'errors': errors
            }
            
            logger.info(f"Imported {added_count} entries to {list_type}")
            return True, result
            
        except Exception as e:
            logger.error(f"Failed to import entries: {e}")
            db.session.rollback()
            return False, str(e)
    
    def export_entries(self, list_type='whitelist', category=None):
        """Export whitelist or blacklist entries"""
        try:
            if list_type == 'whitelist':
                entries = self.get_whitelist_entries(category=category)
            else:
                entries = self.get_blacklist_entries(category=category)
            
            return entries
            
        except Exception as e:
            logger.error(f"Failed to export entries: {e}")
            return []
    
    def is_domain_whitelisted(self, domain):
        """Check if a domain is whitelisted"""
        try:
            entry = Whitelist.query.filter_by(domain=domain.lower()).first()
            if entry and not entry.is_expired():
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to check whitelist status: {e}")
            return False
    
    def is_domain_blacklisted(self, domain):
        """Check if a domain is blacklisted"""
        try:
            entry = Blacklist.query.filter_by(domain=domain.lower()).first()
            if entry and not entry.is_expired():
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to check blacklist status: {e}")
            return False
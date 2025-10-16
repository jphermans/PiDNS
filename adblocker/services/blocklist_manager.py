"""
Block list manager for PiDNS Ad-Blocker
Handles downloading, processing, and updating of block lists
"""

import os
import re
import requests
import logging
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlparse
import gzip

from adblocker.models.database import BlockList, db
from adblocker.services.dnsmasq_manager import DnsmasqManager

logger = logging.getLogger(__name__)

class BlockListManager:
    """Manages block lists for ad-blocking"""
    
    def __init__(self, config):
        self.config = config
        self.blocklists_dir = Path(config.BLOCKLISTS_DIR)
        self.blocklists_dir.mkdir(parents=True, exist_ok=True)
        self.dnsmasq_manager = DnsmasqManager(config)
        
        # Domain patterns for different file formats
        self.domain_patterns = [
            # Standard hosts file format
            r'^0\.0\.0\.0\s+([^\s]+)',
            r'^127\.0\.0\.1\s+([^\s]+)',
            r'^::\s+([^\s]+)',
            # Plain domain lists
            r'^([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\s*$',
            # AdBlock format (||domain.com^)
            r'^\|\|([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\^',
            # Other common formats
            r'^([^\s]+\.[a-zA-Z]{2,})\s+',
        ]
    
    def download_blocklist(self, blocklist_id):
        """Download a specific block list"""
        blocklist = BlockList.query.get(blocklist_id)
        if not blocklist or not blocklist.url:
            logger.error(f"Block list {blocklist_id} not found or no URL")
            return False
        
        try:
            logger.info(f"Downloading block list: {blocklist.name}")
            
            # Download the block list
            response = requests.get(
                blocklist.url,
                timeout=30,
                headers={'User-Agent': 'PiDNS-AdBlocker/1.0'}
            )
            response.raise_for_status()
            
            # Check if content is gzipped
            content = response.content
            if response.headers.get('content-encoding') == 'gzip':
                try:
                    content = gzip.decompress(content)
                except:
                    logger.warning(f"Failed to decompress gzipped content for {blocklist.name}")
            
            # Save to file
            file_path = self.blocklists_dir / f"blocklist_{blocklist_id}.txt"
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # Parse and count domains
            domains = self.parse_blocklist_content(content.decode('utf-8', errors='ignore'))
            
            # Update block list info
            blocklist.last_updated = datetime.utcnow()
            blocklist.entry_count = len(domains)
            db.session.commit()
            
            logger.info(f"Downloaded block list {blocklist.name} with {len(domains)} domains")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download block list {blocklist.name}: {e}")
            return False
    
    def parse_blocklist_content(self, content):
        """Parse block list content and extract domains"""
        domains = set()
        
        for line in content.splitlines():
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#') or line.startswith('!'):
                continue
            
            # Try to extract domain using various patterns
            for pattern in self.domain_patterns:
                match = re.search(pattern, line)
                if match:
                    domain = match.group(1).lower().strip()
                    
                    # Validate domain
                    if self.is_valid_domain(domain):
                        domains.add(domain)
                    break
        
        return list(domains)
    
    def is_valid_domain(self, domain):
        """Check if a domain is valid"""
        if not domain or len(domain) < 4:
            return False
        
        # Skip localhost and local domains
        if domain.endswith('.local') or domain.endswith('.localhost'):
            return False
        
        # Skip IP addresses
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
            return False
        
        # Basic domain validation
        if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain):
            return False
        
        # Skip domains with too many subdomains
        if domain.count('.') > 5:
            return False
        
        return True
    
    def update_all_blocklists(self):
        """Update all enabled block lists"""
        enabled_blocklists = BlockList.query.filter_by(enabled=True).all()
        updated_count = 0
        
        for blocklist in enabled_blocklists:
            if self.download_blocklist(blocklist.id):
                updated_count += 1
        
        # Generate combined configuration
        self.generate_combined_config()
        
        # Reload dnsmasq
        self.dnsmasq_manager.reload_dnsmasq()
        
        logger.info(f"Updated {updated_count} block lists")
        return updated_count
    
    def generate_combined_config(self):
        """Generate combined block list configuration"""
        try:
            # Get all domains from enabled block lists
            all_domains = set()
            
            enabled_blocklists = BlockList.query.filter_by(enabled=True).all()
            for blocklist in enabled_blocklists:
                file_path = self.blocklists_dir / f"blocklist_{blocklist.id}.txt"
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        domains = self.parse_blocklist_content(content)
                        all_domains.update(domains)
            
            # Generate dnsmasq configuration
            self.dnsmasq_manager.generate_adblock_config(list(all_domains))
            
            logger.info(f"Generated combined config with {len(all_domains)} domains")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate combined config: {e}")
            return False
    
    def get_blocklist_status(self, blocklist_id):
        """Get status of a specific block list"""
        blocklist = BlockList.query.get(blocklist_id)
        if not blocklist:
            return None
        
        file_path = self.blocklists_dir / f"blocklist_{blocklist_id}.txt"
        exists = file_path.exists()
        
        return {
            'id': blocklist.id,
            'name': blocklist.name,
            'enabled': blocklist.enabled,
            'url': blocklist.url,
            'category': blocklist.category,
            'last_updated': blocklist.last_updated.isoformat() if blocklist.last_updated else None,
            'entry_count': blocklist.entry_count,
            'file_exists': exists,
            'needs_update': self.needs_update(blocklist)
        }
    
    def needs_update(self, blocklist):
        """Check if block list needs updating"""
        if not blocklist.last_updated:
            return True
        
        # Check if it's been more than the update interval since last update
        update_interval = timedelta(hours=self.config.BLOCKLIST_UPDATE_INTERVAL)
        return datetime.utcnow() - blocklist.last_updated > update_interval
    
    def add_custom_blocklist(self, name, url, category='custom', description=''):
        """Add a custom block list"""
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False, "Invalid URL"
            
            # Check if URL already exists
            existing = BlockList.query.filter_by(url=url).first()
            if existing:
                return False, "Block list with this URL already exists"
            
            # Create new block list
            blocklist = BlockList(
                name=name,
                url=url,
                category=category,
                enabled=True,
                description=description
            )
            
            db.session.add(blocklist)
            db.session.commit()
            
            # Download the block list
            if self.download_blocklist(blocklist.id):
                self.generate_combined_config()
                self.dnsmasq_manager.reload_dnsmasq()
                return True, "Block list added successfully"
            else:
                return False, "Failed to download block list"
                
        except Exception as e:
            logger.error(f"Failed to add custom block list: {e}")
            return False, str(e)
    
    def remove_blocklist(self, blocklist_id):
        """Remove a block list"""
        try:
            blocklist = BlockList.query.get(blocklist_id)
            if not blocklist:
                return False, "Block list not found"
            
            # Don't allow removing predefined block lists
            from adblocker.config.flask_config import get_config
            config = get_config()
            for predefined in config.PREDEFINED_BLOCKLISTS:
                if predefined['url'] == blocklist.url:
                    return False, "Cannot remove predefined block list"
            
            # Remove block list file
            file_path = self.blocklists_dir / f"blocklist_{blocklist_id}.txt"
            if file_path.exists():
                file_path.unlink()
            
            # Remove from database
            db.session.delete(blocklist)
            db.session.commit()
            
            # Regenerate configuration
            self.generate_combined_config()
            self.dnsmasq_manager.reload_dnsmasq()
            
            return True, "Block list removed successfully"
            
        except Exception as e:
            logger.error(f"Failed to remove block list: {e}")
            return False, str(e)
    
    def toggle_blocklist(self, blocklist_id):
        """Toggle block list enabled status"""
        try:
            blocklist = BlockList.query.get(blocklist_id)
            if not blocklist:
                return False, "Block list not found"
            
            blocklist.enabled = not blocklist.enabled
            db.session.commit()
            
            # Regenerate configuration
            self.generate_combined_config()
            self.dnsmasq_manager.reload_dnsmasq()
            
            status = "enabled" if blocklist.enabled else "disabled"
            return True, f"Block list {status} successfully"
            
        except Exception as e:
            logger.error(f"Failed to toggle block list: {e}")
            return False, str(e)
    
    def update_blocklist(self, blocklist_id):
        """Update a specific block list"""
        try:
            if self.download_blocklist(blocklist_id):
                self.generate_combined_config()
                self.dnsmasq_manager.reload_dnsmasq()
                return True, "Block list updated successfully"
            else:
                return False, "Failed to update block list"
                
        except Exception as e:
            logger.error(f"Failed to update block list: {e}")
            return False, str(e)
    
    def get_statistics(self):
        """Get block list statistics"""
        try:
            total_blocklists = BlockList.query.count()
            enabled_blocklists = BlockList.query.filter_by(enabled=True).count()
            
            total_domains = 0
            for blocklist in BlockList.query.filter_by(enabled=True).all():
                total_domains += blocklist.entry_count or 0
            
            # Get last update time
            last_update = None
            for blocklist in BlockList.query.filter_by(enabled=True).all():
                if blocklist.last_updated:
                    if not last_update or blocklist.last_updated > last_update:
                        last_update = blocklist.last_updated
            
            # Get category statistics
            category_stats = {}
            for blocklist in BlockList.query.filter_by(enabled=True).all():
                category = blocklist.category
                if category not in category_stats:
                    category_stats[category] = {
                        'count': 0,
                        'domains': 0
                    }
                category_stats[category]['count'] += 1
                category_stats[category]['domains'] += blocklist.entry_count or 0
            
            return {
                'total_blocklists': total_blocklists,
                'enabled_blocklists': enabled_blocklists,
                'total_domains': total_domains,
                'last_update': last_update.isoformat() if last_update else None,
                'category_stats': category_stats
            }
            
        except Exception as e:
            logger.error(f"Failed to get block list statistics: {e}")
            return {}
    
    def cleanup_old_files(self):
        """Clean up old block list files"""
        try:
            # Get all block list IDs from database
            blocklist_ids = {str(bl.id) for bl in BlockList.query.all()}
            
            # Remove files for non-existent block lists
            for file_path in self.blocklists_dir.glob("blocklist_*.txt"):
                blocklist_id = file_path.stem.replace("blocklist_", "")
                if blocklist_id not in blocklist_ids:
                    file_path.unlink()
                    logger.info(f"Removed old block list file: {file_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to cleanup old files: {e}")
            return False

def schedule_blocklist_updates(app):
    """Schedule automatic block list updates"""
    from apscheduler.schedulers.background import BackgroundScheduler
    
    def update_job():
        with app.app_context():
            try:
                manager = BlockListManager(app.config)
                manager.update_all_blocklists()
                logger.info("Scheduled block list update completed")
            except Exception as e:
                logger.error(f"Scheduled block list update failed: {e}")
    
    scheduler = BackgroundScheduler()
    
    # Schedule updates every 24 hours
    scheduler.add_job(
        func=update_job,
        trigger='cron',
        hour=2,
        minute=0,
        id='update_blocklists'
    )
    
    scheduler.start()
    logger.info("Scheduled block list updates (daily at 2:00 AM)")
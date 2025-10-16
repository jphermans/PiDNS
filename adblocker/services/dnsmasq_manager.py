"""
dnsmasq configuration manager for PiDNS Ad-Blocker
Handles generation and management of dnsmasq configuration files
"""

import os
import subprocess
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class DnsmasqManager:
    """Manages dnsmasq configuration for ad-blocking"""
    
    def __init__(self, config):
        self.config = config
        self.config_dir = Path(config.DNSMASQ_CONFIG_DIR)
        self.adblock_config = Path(config.ADBLOCK_CONFIG_FILE)
        self.whitelist_config = Path(config.WHITELIST_CONFIG_FILE)
        self.blacklist_config = Path(config.BLACKLIST_CONFIG_FILE)
        self.service_name = config.DNSMASQ_SERVICE
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_adblock_config(self, blocked_domains):
        """Generate dnsmasq configuration for blocked domains"""
        try:
            with open(self.adblock_config, 'w') as f:
                f.write("# PiDNS Ad-Blocker Configuration\n")
                f.write(f"# Generated on {datetime.now().isoformat()}\n\n")
                
                # Add sinkhole IP configuration
                f.write("# Sinkhole IP address\n")
                f.write("address=/#/0.0.0.0\n")
                f.write("address=/#/::\n\n")
                
                # Add blocked domains
                f.write("# Blocked domains\n")
                for domain in sorted(set(blocked_domains)):
                    if domain and not domain.startswith('#'):
                        f.write(f"address=/{domain}/0.0.0.0\n")
                        f.write(f"address=/{domain}/::\n")
                
                logger.info(f"Generated adblock config with {len(blocked_domains)} domains")
                return True
                
        except Exception as e:
            logger.error(f"Failed to generate adblock config: {e}")
            return False
    
    def generate_whitelist_config(self, whitelist_domains):
        """Generate dnsmasq configuration for whitelisted domains"""
        try:
            with open(self.whitelist_config, 'w') as f:
                f.write("# PiDNS Ad-Blocker Whitelist Configuration\n")
                f.write(f"# Generated on {datetime.now().isoformat()}\n\n")
                
                # Add whitelist entries
                f.write("# Whitelisted domains (bypass ad-blocking)\n")
                for domain in sorted(set(whitelist_domains)):
                    if domain and not domain.startswith('#'):
                        f.write(f"server=/{domain}/#\n")
                
                logger.info(f"Generated whitelist config with {len(whitelist_domains)} domains")
                return True
                
        except Exception as e:
            logger.error(f"Failed to generate whitelist config: {e}")
            return False
    
    def generate_blacklist_config(self, blacklist_domains):
        """Generate dnsmasq configuration for blacklisted domains"""
        try:
            with open(self.blacklist_config, 'w') as f:
                f.write("# PiDNS Ad-Blocker Blacklist Configuration\n")
                f.write(f"# Generated on {datetime.now().isoformat()}\n\n")
                
                # Add blacklist entries
                f.write("# Explicitly blacklisted domains\n")
                for domain in sorted(set(blacklist_domains)):
                    if domain and not domain.startswith('#'):
                        f.write(f"address=/{domain}/0.0.0.0\n")
                        f.write(f"address=/{domain}/::\n")
                
                logger.info(f"Generated blacklist config with {len(blacklist_domains)} domains")
                return True
                
        except Exception as e:
            logger.error(f"Failed to generate blacklist config: {e}")
            return False
    
    def reload_dnsmasq(self):
        """Reload dnsmasq service to apply configuration changes"""
        try:
            # Test configuration first
            result = subprocess.run(
                ['dnsmasq', '--test'],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"dnsmasq configuration test failed: {result.stderr}")
                return False
            
            # Reload service
            result = subprocess.run(
                ['systemctl', 'reload', self.service_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"Failed to reload dnsmasq: {result.stderr}")
                return False
            
            logger.info("dnsmasq reloaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to reload dnsmasq: {e}")
            return False
    
    def restart_dnsmasq(self):
        """Restart dnsmasq service"""
        try:
            result = subprocess.run(
                ['systemctl', 'restart', self.service_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"Failed to restart dnsmasq: {result.stderr}")
                return False
            
            logger.info("dnsmasq restarted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restart dnsmasq: {e}")
            return False
    
    def get_dnsmasq_status(self):
        """Get dnsmasq service status"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', self.service_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return 'active'
            else:
                return 'inactive'
                
        except Exception as e:
            logger.error(f"Failed to get dnsmasq status: {e}")
            return 'unknown'
    
    def get_dnsmasq_info(self):
        """Get detailed dnsmasq service information"""
        try:
            result = subprocess.run(
                ['systemctl', 'show', self.service_name, '--property=ActiveState,SubState,MainPID'],
                capture_output=True,
                text=True
            )
            
            info = {}
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if '=' in line:
                        key, value = line.split('=', 1)
                        info[key] = value
            
            return info
            
        except Exception as e:
            logger.error(f"Failed to get dnsmasq info: {e}")
            return {}
    
    def enable_query_logging(self, log_file=None):
        """Enable dnsmasq query logging"""
        try:
            log_file = log_file or self.config.DNSMASQ_LOG_FILE
            
            # Create log directory if it doesn't exist
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Add logging configuration to main dnsmasq config
            main_config = Path('/etc/dnsmasq.conf')
            
            # Check if logging is already enabled
            with open(main_config, 'r') as f:
                config_content = f.read()
            
            if 'log-queries' not in config_content:
                # Add logging configuration
                with open(main_config, 'a') as f:
                    f.write("\n# PiDNS Ad-Blocker Query Logging\n")
                    f.write(f"log-queries\n")
                    f.write(f"log-facility={log_file}\n")
                
                logger.info("Enabled dnsmasq query logging")
                return True
            else:
                logger.info("dnsmasq query logging already enabled")
                return True
                
        except Exception as e:
            logger.error(f"Failed to enable dnsmasq query logging: {e}")
            return False
    
    def disable_query_logging(self):
        """Disable dnsmasq query logging"""
        try:
            main_config = Path('/etc/dnsmasq.conf')
            
            # Read and modify configuration
            with open(main_config, 'r') as f:
                lines = f.readlines()
            
            # Remove logging configuration lines
            filtered_lines = []
            skip_next = False
            for line in lines:
                if 'PiDNS Ad-Blocker Query Logging' in line:
                    skip_next = True
                    continue
                elif skip_next and ('log-queries' in line or 'log-facility' in line):
                    continue
                else:
                    skip_next = False
                    filtered_lines.append(line)
            
            # Write back configuration
            with open(main_config, 'w') as f:
                f.writelines(filtered_lines)
            
            logger.info("Disabled dnsmasq query logging")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disable dnsmasq query logging: {e}")
            return False
    
    def get_config_files(self):
        """Get list of dnsmasq configuration files"""
        try:
            result = subprocess.run(
                ['dnsmasq', '--test', '--conf-dir', str(self.config_dir)],
                capture_output=True,
                text=True
            )
            
            config_files = []
            if result.returncode == 0:
                # Parse output to find configuration files
                for line in result.stdout.splitlines():
                    if 'reading' in line and '.conf' in line:
                        file_path = line.split('reading')[-1].strip()
                        config_files.append(file_path)
            
            return config_files
            
        except Exception as e:
            logger.error(f"Failed to get dnsmasq config files: {e}")
            return []
    
    def backup_config(self):
        """Backup current dnsmasq configuration"""
        try:
            backup_dir = self.config_dir / 'backups'
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backup_dir / f'dnsmasq_backup_{timestamp}.tar.gz'
            
            # Create backup of configuration files
            result = subprocess.run(
                ['tar', '-czf', str(backup_file), '-C', str(self.config_dir), '.'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Created dnsmasq config backup: {backup_file}")
                return str(backup_file)
            else:
                logger.error(f"Failed to create dnsmasq config backup: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to backup dnsmasq config: {e}")
            return None
    
    def restore_config(self, backup_file):
        """Restore dnsmasq configuration from backup"""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_file}")
                return False
            
            # Extract backup
            result = subprocess.run(
                ['tar', '-xzf', str(backup_path), '-C', str(self.config_dir)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"Failed to restore dnsmasq config: {result.stderr}")
                return False
            
            # Reload dnsmasq
            return self.reload_dnsmasq()
            
        except Exception as e:
            logger.error(f"Failed to restore dnsmasq config: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count=5):
        """Clean up old configuration backups"""
        try:
            backup_dir = self.config_dir / 'backups'
            if not backup_dir.exists():
                return True
            
            # List backup files sorted by modification time
            backup_files = sorted(
                backup_dir.glob('dnsmasq_backup_*.tar.gz'),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # Remove old backups
            for backup_file in backup_files[keep_count:]:
                backup_file.unlink()
                logger.info(f"Removed old backup: {backup_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to cleanup old backups: {e}")
            return False
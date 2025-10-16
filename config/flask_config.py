"""
Flask configuration for PiDNS dashboard
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings
    HOST = '0.0.0.0'
    PORT = 8080

    # DNS and DHCP settings
    DNSMASQ_LEASE_FILE = '/var/lib/misc/dnsmasq.leases'
    DNSMASQ_CONFIG_FILE = '/etc/dnsmasq.conf'

    # MAC vendor database
    MAC_VENDORS_FILE = BASE_DIR / 'data' / 'mac-vendors.json'

    # Dashboard settings
    DASHBOARD_TITLE = 'PiDNS Network Dashboard'
    REFRESH_INTERVAL = 30  # seconds

    # Authentication (must be provided via environment variables in production)
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SECRET_KEY = 'dev-secret-key'
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME') or 'dev-admin'
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD') or 'dev-change-me-now!'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD')

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration class based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV') or 'default'
    return config.get(config_name, config['default'])
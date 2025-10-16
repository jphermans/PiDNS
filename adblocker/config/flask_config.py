"""
Flask configuration for PiDNS Ad-Blocker
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('ADBLOCKER_SECRET_KEY') or 'adblocker-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings
    HOST = '0.0.0.0'
    PORT = 8081

    # Database settings
    DATABASE_PATH = BASE_DIR / 'data' / 'adblocker.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ad-blocker settings
    ADBLOCKER_TITLE = 'PiDNS Ad-Blocker Management'
    REFRESH_INTERVAL = 30  # seconds

    # dnsmasq settings
    DNSMASQ_CONFIG_DIR = '/etc/dnsmasq.d'
    ADBLOCK_CONFIG_FILE = os.path.join(DNSMASQ_CONFIG_DIR, 'adblock.conf')
    WHITELIST_CONFIG_FILE = os.path.join(DNSMASQ_CONFIG_DIR, 'whitelist.conf')
    BLACKLIST_CONFIG_FILE = os.path.join(DNSMASQ_CONFIG_DIR, 'blacklist.conf')
    DNSMASQ_SERVICE = 'dnsmasq'
    
    # Block list settings
    BLOCKLISTS_DIR = BASE_DIR / 'data' / 'blocklists'
    BLOCKLIST_UPDATE_INTERVAL = 24  # hours
    
    # Predefined block list categories
    BLOCKLIST_CATEGORIES = {
        'ads': {
            'name': 'Advertisements',
            'description': 'Block advertisements and promotional content',
            'enabled': True
        },
        'trackers': {
            'name': 'Trackers',
            'description': 'Block tracking and analytics services',
            'enabled': True
        },
        'malware': {
            'name': 'Malware',
            'description': 'Block known malicious domains',
            'enabled': True
        },
        'phishing': {
            'name': 'Phishing',
            'description': 'Block phishing domains',
            'enabled': True
        },
        'social': {
            'name': 'Social Media',
            'description': 'Block social media platforms',
            'enabled': False
        },
        'adult': {
            'name': 'Adult Content',
            'description': 'Block adult content',
            'enabled': False
        }
    }
    
    # Predefined block list sources
    PREDEFINED_BLOCKLISTS = [
        {
            'name': 'StevenBlack\'s Ad Block List',
            'url': 'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts',
            'category': 'ads',
            'enabled': True
        },
        {
            'name': 'EasyList',
            'url': 'https://easylist.to/easylist/easylist.txt',
            'category': 'ads',
            'enabled': True
        },
        {
            'name': 'EasyPrivacy',
            'url': 'https://easylist.to/easylist/easyprivacy.txt',
            'category': 'trackers',
            'enabled': True
        },
        {
            'name': 'Malware Domain List',
            'url': 'https://badsites.com/badlist/hosts.txt',
            'category': 'malware',
            'enabled': True
        },
        {
            'name': 'PhishTank',
            'url': 'https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt',
            'category': 'phishing',
            'enabled': True
        }
    ]
    
    # Authentication
    BASIC_AUTH_USERNAME = os.environ.get('ADBLOCKER_USERNAME') or 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('ADBLOCKER_PASSWORD') or 'password'
    
    # Logging
    DNSMASQ_LOG_FILE = '/var/log/dnsmasq.log'
    QUERY_LOG_RETENTION_DAYS = 30
    
    # Statistics
    STATS_RETENTION_DAYS = 90
    MAX_LOG_ENTRIES_PER_PAGE = 100

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SECRET_KEY = 'dev-adblocker-secret-key'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('ADBLOCKER_SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("ADBLOCKER_SECRET_KEY environment variable must be set in production")

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
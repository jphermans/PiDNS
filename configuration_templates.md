# PiDNS Configuration Templates

## 1. Configuration Template Overview

### Template Structure
1. **Base Configuration**: Common settings for all device types
2. **Device-Specific Configuration**: Settings specific to each device type
3. **Container-Specific Configuration**: Settings specific to each container type
4. **Environment-Specific Configuration**: Settings specific to each environment (development, testing, production)

### Template Variables
1. **Device Type Variables**: Variables that change based on device type
2. **Container Type Variables**: Variables that change based on container type
3. **Environment Variables**: Variables that change based on environment
4. **User-Defined Variables**: Variables that can be customized by users

### Template Generation
1. **Template Engine**: Use Jinja2 for template rendering
2. **Variable Substitution**: Replace variables with actual values
3. **Validation**: Validate generated configuration files
4. **Installation**: Install generated configuration files

## 2. Flask Configuration Templates

### Base Flask Configuration
```python
# templates/flask_config_base.py.j2
# Base Flask configuration template for PiDNS
# This template contains common settings for all device types

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration for PiDNS"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings
    HOST = '0.0.0.0'
    PORT = 8080
    
    # Performance optimizations
    THREADS_PER_PAGE = {{ threads_per_page }}
    PROCESSES = {{ processes }}
    
    # DNS and DHCP settings
    DNSMASQ_LEASE_FILE = '/var/lib/misc/dnsmasq.leases'
    DNSMASQ_CONFIG_FILE = '/etc/dnsmasq.conf'
    
    # MAC vendor database
    MAC_VENDORS_FILE = BASE_DIR / 'data' / 'mac-vendors.json'
    
    # Dashboard settings
    DASHBOARD_TITLE = 'PiDNS Network Dashboard ({{ device_name }})'
    REFRESH_INTERVAL = {{ refresh_interval }}  # seconds
    
    # Authentication
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME') or 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD') or 'password'
    
    # Memory optimization settings
    MAX_DEVICES = {{ max_devices }}
    LOG_LEVEL = '{{ log_level }}'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(BASE_DIR / 'data' / 'pidns.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cache settings
    CACHE_TYPE = '{{ cache_type }}'
    CACHE_DEFAULT_TIMEOUT = {{ cache_timeout }}
    
    # Security settings
    SESSION_COOKIE_SECURE = {{ session_cookie_secure }}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = {{ session_lifetime }}
    
    # API settings
    API_KEY = os.environ.get('PIDNS_API_KEY') or 'default-api-key-change-in-production'
    API_RATE_LIMIT = '{{ api_rate_limit }}'
    
    # Ad-blocker settings
    AD_BLOCKER_ENABLED = {{ ad_blocker_enabled }}
    AD_BLOCKER_PORT = 8081
    AD_BLOCKER_API_KEY = os.environ.get('PIDNS_AD_BLOCKER_API_KEY') or 'default-ad-blocker-api-key-change-in-production'
    
    # Container settings
    CONTAINER_TYPE = '{{ container_type }}'
    CONTAINER_NAME = '{{ container_name }}'
    
    # Device-specific settings
    DEVICE_TYPE = '{{ device_type }}'
    DEVICE_NAME = '{{ device_name }}'
    DEVICE_MEMORY = '{{ device_memory }}'
    DEVICE_CPU_CORES = {{ device_cpu_cores }}
    
    # Environment-specific settings
    ENVIRONMENT = '{{ environment }}'
    LOG_FILE = '{{ log_file }}'
    LOG_MAX_SIZE = {{ log_max_size }}
    LOG_BACKUP_COUNT = {{ log_backup_count }}
```

### Raspberry Pi Zero W Flask Configuration
```python
# templates/flask_config_pi_zero.py.j2
# Flask configuration template for Raspberry Pi Zero W
# This template contains settings optimized for Raspberry Pi Zero W

{% extends "flask_config_base.py.j2" %}

{% block config %}
class Config:
    """Configuration optimized for Raspberry Pi Zero W"""
    
    # Performance optimizations for Pi Zero W
    THREADS_PER_PAGE = 1  # Limited threading for Pi Zero W
    PROCESSES = 1         # Single process
    
    # Dashboard settings for Pi Zero W
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Raspberry Pi Zero W)'
    REFRESH_INTERVAL = 60  # seconds (slower refresh for resource constraints)
    
    # Memory optimization settings for Pi Zero W
    MAX_DEVICES = 25  # Limited device count for Pi Zero W
    LOG_LEVEL = 'WARNING'  # Reduced logging to save resources
    
    # Cache settings for Pi Zero W
    CACHE_TYPE = 'simple'  # Simple cache for Pi Zero W
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes
    
    # Security settings for Pi Zero W
    SESSION_COOKIE_SECURE = False  # Disable with HTTP (no HTTPS on Pi Zero W)
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    
    # API settings for Pi Zero W
    API_RATE_LIMIT = '30/hour'  # Reduced rate limit for Pi Zero W
    
    # Ad-blocker settings for Pi Zero W
    AD_BLOCKER_ENABLED = False  # Disabled by default for Pi Zero W
    
    # Device-specific settings for Pi Zero W
    DEVICE_TYPE = 'pi-zero'
    DEVICE_NAME = 'Raspberry Pi Zero W'
    DEVICE_MEMORY = '512MB'
    DEVICE_CPU_CORES = 1
    
    # Environment-specific settings for Pi Zero W
    LOG_FILE = '/var/log/pidns/app.log'
    LOG_MAX_SIZE = 5 * 1024 * 1024  # 5MB
    LOG_BACKUP_COUNT = 2
{% endblock %}
```

### Raspberry Pi Zero 2W Flask Configuration
```python
# templates/flask_config_pi_zero_2w.py.j2
# Flask configuration template for Raspberry Pi Zero 2W
# This template contains settings optimized for Raspberry Pi Zero 2W

{% extends "flask_config_base.py.j2" %}

{% block config %}
class Config:
    """Configuration optimized for Raspberry Pi Zero 2W"""
    
    # Performance optimizations for Pi Zero 2W
    THREADS_PER_PAGE = 1  # Limited threading for Pi Zero 2W
    PROCESSES = 1         # Single process
    
    # Dashboard settings for Pi Zero 2W
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Raspberry Pi Zero 2W)'
    REFRESH_INTERVAL = 60  # seconds (slower refresh for resource constraints)
    
    # Memory optimization settings for Pi Zero 2W
    MAX_DEVICES = 25  # Limited device count for Pi Zero 2W
    LOG_LEVEL = 'WARNING'  # Reduced logging to save resources
    
    # Cache settings for Pi Zero 2W
    CACHE_TYPE = 'simple'  # Simple cache for Pi Zero 2W
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes
    
    # Security settings for Pi Zero 2W
    SESSION_COOKIE_SECURE = False  # Disable with HTTP (no HTTPS on Pi Zero 2W)
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    
    # API settings for Pi Zero 2W
    API_RATE_LIMIT = '30/hour'  # Reduced rate limit for Pi Zero 2W
    
    # Ad-blocker settings for Pi Zero 2W
    AD_BLOCKER_ENABLED = False  # Disabled by default for Pi Zero 2W
    
    # Device-specific settings for Pi Zero 2W
    DEVICE_TYPE = 'pi-zero-2w'
    DEVICE_NAME = 'Raspberry Pi Zero 2W'
    DEVICE_MEMORY = '512MB'
    DEVICE_CPU_CORES = 1
    
    # Environment-specific settings for Pi Zero 2W
    LOG_FILE = '/var/log/pidns/app.log'
    LOG_MAX_SIZE = 5 * 1024 * 1024  # 5MB
    LOG_BACKUP_COUNT = 2
{% endblock %}
```

### Raspberry Pi 3 Flask Configuration
```python
# templates/flask_config_pi_3.py.j2
# Flask configuration template for Raspberry Pi 3
# This template contains settings optimized for Raspberry Pi 3

{% extends "flask_config_base.py.j2" %}

{% block config %}
class Config:
    """Configuration optimized for Raspberry Pi 3"""
    
    # Performance optimizations for Pi 3
    THREADS_PER_PAGE = 2  # Moderate threading for Pi 3
    PROCESSES = 1         # Single process
    
    # Dashboard settings for Pi 3
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Raspberry Pi 3)'
    REFRESH_INTERVAL = 30  # seconds (moderate refresh for Pi 3)
    
    # Memory optimization settings for Pi 3
    MAX_DEVICES = 50  # Moderate device count for Pi 3
    LOG_LEVEL = 'INFO'  # Standard logging for Pi 3
    
    # Cache settings for Pi 3
    CACHE_TYPE = 'simple'  # Simple cache for Pi 3
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Security settings for Pi 3
    SESSION_COOKIE_SECURE = False  # Disable with HTTP (no HTTPS on Pi 3)
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # API settings for Pi 3
    API_RATE_LIMIT = '60/hour'  # Moderate rate limit for Pi 3
    
    # Ad-blocker settings for Pi 3
    AD_BLOCKER_ENABLED = True  # Enabled by default for Pi 3
    
    # Device-specific settings for Pi 3
    DEVICE_TYPE = 'pi-3'
    DEVICE_NAME = 'Raspberry Pi 3'
    DEVICE_MEMORY = '1GB'
    DEVICE_CPU_CORES = 4
    
    # Environment-specific settings for Pi 3
    LOG_FILE = '/var/log/pidns/app.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 3
{% endblock %}
```

### Raspberry Pi 4/5 Flask Configuration
```python
# templates/flask_config_pi_4_5.py.j2
# Flask configuration template for Raspberry Pi 4/5
# This template contains settings optimized for Raspberry Pi 4/5

{% extends "flask_config_base.py.j2" %}

{% block config %}
class Config:
    """Configuration optimized for Raspberry Pi 4/5"""
    
    # Performance optimizations for Pi 4/5
    THREADS_PER_PAGE = 4  # More threading for Pi 4/5
    PROCESSES = 1         # Single process
    
    # Dashboard settings for Pi 4/5
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Raspberry Pi 4/5)'
    REFRESH_INTERVAL = 15  # seconds (faster refresh for better UX)
    
    # Memory optimization settings for Pi 4/5
    MAX_DEVICES = 250  # Higher device limit for Pi 4/5
    LOG_LEVEL = 'DEBUG'  # Full logging for debugging
    
    # Cache settings for Pi 4/5
    CACHE_TYPE = 'filesystem'  # Filesystem cache for Pi 4/5
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Security settings for Pi 4/5
    SESSION_COOKIE_SECURE = False  # Disable with HTTP (no HTTPS on Pi 4/5)
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # API settings for Pi 4/5
    API_RATE_LIMIT = '100/hour'  # Higher rate limit for Pi 4/5
    
    # Ad-blocker settings for Pi 4/5
    AD_BLOCKER_ENABLED = True  # Enabled by default for Pi 4/5
    
    # Device-specific settings for Pi 4/5
    DEVICE_TYPE = 'pi-4'  # Will be set to pi-5 for Pi 5
    DEVICE_NAME = 'Raspberry Pi 4/5'
    DEVICE_MEMORY = '2-8GB'  # Will be set to 4-8GB for Pi 5
    DEVICE_CPU_CORES = 4
    
    # Environment-specific settings for Pi 4/5
    LOG_FILE = '/var/log/pidns/app.log'
    LOG_MAX_SIZE = 20 * 1024 * 1024  # 20MB
    LOG_BACKUP_COUNT = 5
{% endblock %}
```

### Low-Resource PC Flask Configuration
```python
# templates/flask_config_low_resource_pc.py.j2
# Flask configuration template for Low-Resource PC
# This template contains settings optimized for Low-Resource PC

{% extends "flask_config_base.py.j2" %}

{% block config %}
class Config:
    """Configuration optimized for Low-Resource PC"""
    
    # Performance optimizations for Low-Resource PC
    THREADS_PER_PAGE = 2  # Limited threading for resource constraints
    PROCESSES = 1         # Single process
    
    # Dashboard settings for Low-Resource PC
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Low-Resource PC)'
    REFRESH_INTERVAL = 45  # seconds (increased to reduce CPU usage)
    
    # Memory optimization settings for Low-Resource PC
    MAX_DEVICES = 75  # Limited device count for resource constraints
    LOG_LEVEL = 'WARNING'  # Reduced logging to save resources
    
    # Cache settings for Low-Resource PC
    CACHE_TYPE = 'simple'  # Simple cache for Low-Resource PC
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes
    
    # Security settings for Low-Resource PC
    SESSION_COOKIE_SECURE = False  # Disable with HTTP (no HTTPS on Low-Resource PC)
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # API settings for Low-Resource PC
    API_RATE_LIMIT = '60/hour'  # Moderate rate limit for Low-Resource PC
    
    # Ad-blocker settings for Low-Resource PC
    AD_BLOCKER_ENABLED = True  # Enabled by default for Low-Resource PC
    
    # Device-specific settings for Low-Resource PC
    DEVICE_TYPE = 'low-resource-pc'
    DEVICE_NAME = 'Low-Resource PC'
    DEVICE_MEMORY = '≤1GB'
    DEVICE_CPU_CORES = '≤2'
    
    # Environment-specific settings for Low-Resource PC
    LOG_FILE = '/var/log/pidns/app.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 3
{% endblock %}
```

### Standard PC Flask Configuration
```python
# templates/flask_config_standard_pc.py.j2
# Flask configuration template for Standard PC
# This template contains settings optimized for Standard PC

{% extends "flask_config_base.py.j2" %}

{% block config %}
class Config:
    """Configuration optimized for Standard PC"""
    
    # Performance optimizations for Standard PC
    THREADS_PER_PAGE = 4  # Standard threading for PC
    PROCESSES = 1         # Single process
    
    # Dashboard settings for Standard PC
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Standard PC)'
    REFRESH_INTERVAL = 10  # seconds (fast refresh for better UX)
    
    # Memory optimization settings for Standard PC
    MAX_DEVICES = 500  # High device limit for PC
    LOG_LEVEL = 'DEBUG'  # Full logging for debugging
    
    # Cache settings for Standard PC
    CACHE_TYPE = 'redis'  # Redis cache for Standard PC
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Security settings for Standard PC
    SESSION_COOKIE_SECURE = True  # Enable with HTTPS
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # API settings for Standard PC
    API_RATE_LIMIT = '100/hour'  # Higher rate limit for Standard PC
    
    # Ad-blocker settings for Standard PC
    AD_BLOCKER_ENABLED = True  # Enabled by default for Standard PC
    
    # Device-specific settings for Standard PC
    DEVICE_TYPE = 'standard-pc'
    DEVICE_NAME = 'Standard PC'
    DEVICE_MEMORY = '>1GB'
    DEVICE_CPU_CORES = '>2'
    
    # Environment-specific settings for Standard PC
    LOG_FILE = '/var/log/pidns/app.log'
    LOG_MAX_SIZE = 20 * 1024 * 1024  # 20MB
    LOG_BACKUP_COUNT = 5
{% endblock %}
```

## 3. dnsmasq Configuration Templates

### Base dnsmasq Configuration
```conf
# templates/dnsmasq_base.conf.j2
# Base dnsmasq configuration template for PiDNS
# This template contains common settings for all device types

# Interface configuration
interface={{ interface }}
# Uncomment the line below if using Ethernet instead of WiFi
# interface=eth0

# DHCP server configuration
dhcp-range={{ dhcp_range_start }},{{ dhcp_range_end }},{{ dhcp_netmask }},{{ dhcp_lease_time }}
dhcp-option=option:router,{{ dhcp_router }}
dhcp-option=option:dns-server,{{ dhcp_dns_server }}
dhcp-authoritative

# DNS configuration
domain-needed
bogus-priv
no-resolv
server={{ dns_server_1 }}
server={{ dns_server_2 }}
server={{ dns_server_3 }}

# Lease file location
dhcp-leasefile=/var/lib/misc/dnsmasq.leases

# Logging
{% if enable_logging %}
log-queries
log-dhcp
{% if log_async %}
log-async={{ log_async_queue_size }}
{% endif %}
{% endif %}

# Performance optimizations
cache-size={{ cache_size }}
dns-forward-max={{ dns_forward_max }}
min-port={{ min_port }}
max-port={{ max_port }}

# Security
no-ping
dhcp-name-match=set:hostname-ignore,wpad
dhcp-ignore-names=tag:hostname-ignore

# Local domain
local=/local/
domain=local

# Static leases (examples - customize as needed)
# dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1
# dhcp-host=11:22:33:44:55:66,192.168.1.11,device2

# Time-to-live settings
local-ttl={{ local_ttl }}
neg-ttl={{ neg_ttl }}
max-ttl={{ max_ttl }}
min-cache-ttl={{ min_cache_ttl }}

# Resource optimization settings
max-cache-ttl={{ max_cache_ttl }}
min-cache-ttl={{ min_cache_ttl }}
cache-lim={{ cache_limit }}
```

### Raspberry Pi Zero W dnsmasq Configuration
```conf
# templates/dnsmasq_pi_zero.conf.j2
# dnsmasq configuration template for Raspberry Pi Zero W
# This template contains settings optimized for Raspberry Pi Zero W

{% extends "dnsmasq_base.conf.j2" %}

{% block config %}
# Interface configuration
interface=wlan0
# Uncomment the line below if using Ethernet instead of WiFi
# interface=eth0

# DHCP server configuration
dhcp-range=192.168.1.100,192.168.1.120,255.255.255.0,24h
dhcp-option=option:router,192.168.1.1
dhcp-option=option:dns-server,192.168.1.1
dhcp-authoritative

# DNS configuration
domain-needed
bogus-priv
no-resolv
server=8.8.8.8
server=8.8.4.4
server=1.1.1.1

# Lease file location
dhcp-leasefile=/var/lib/misc/dnsmasq.leases

# Logging (minimal for Pi Zero W)
# log-queries  # Commented out to save resources
# log-dhcp     # Commented out to save resources

# Performance optimizations for Pi Zero W
cache-size=50
dns-forward-max=50
min-port=4096
max-port=65535

# Security
no-ping
dhcp-name-match=set:hostname-ignore,wpad
dhcp-ignore-names=tag:hostname-ignore

# Local domain
local=/local/
domain=local

# Static leases (examples - customize as needed)
# dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1
# dhcp-host=11:22:33:44:55:66,192.168.1.11,device2

# Time-to-live settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=50
{% endblock %}
```

### Raspberry Pi Zero 2W dnsmasq Configuration
```conf
# templates/dnsmasq_pi_zero_2w.conf.j2
# dnsmasq configuration template for Raspberry Pi Zero 2W
# This template contains settings optimized for Raspberry Pi Zero 2W

{% extends "dnsmasq_base.conf.j2" %}

{% block config %}
# Interface configuration
interface=wlan0
# Uncomment the line below if using Ethernet instead of WiFi
# interface=eth0

# DHCP server configuration
dhcp-range=192.168.1.100,192.168.1.120,255.255.255.0,24h
dhcp-option=option:router,192.168.1.1
dhcp-option=option:dns-server,192.168.1.1
dhcp-authoritative

# DNS configuration
domain-needed
bogus-priv
no-resolv
server=8.8.8.8
server=8.8.4.4
server=1.1.1.1

# Lease file location
dhcp-leasefile=/var/lib/misc/dnsmasq.leases

# Logging (minimal for Pi Zero 2W)
# log-queries  # Commented out to save resources
# log-dhcp     # Commented out to save resources

# Performance optimizations for Pi Zero 2W
cache-size=50
dns-forward-max=50
min-port=4096
max-port=65535

# Security
no-ping
dhcp-name-match=set:hostname-ignore,wpad
dhcp-ignore-names=tag:hostname-ignore

# Local domain
local=/local/
domain=local

# Static leases (examples - customize as needed)
# dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1
# dhcp-host=11:22:33:44:55:66,192.168.1.11,device2

# Time-to-live settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=50
{% endblock %}
```

### Raspberry Pi 3 dnsmasq Configuration
```conf
# templates/dnsmasq_pi_3.conf.j2
# dnsmasq configuration template for Raspberry Pi 3
# This template contains settings optimized for Raspberry Pi 3

{% extends "dnsmasq_base.conf.j2" %}

{% block config %}
# Interface configuration
interface=wlan0
# Uncomment the line below if using Ethernet instead of WiFi
# interface=eth0

# DHCP server configuration
dhcp-range=192.168.1.100,192.168.1.200,255.255.255.0,24h
dhcp-option=option:router,192.168.1.1
dhcp-option=option:dns-server,192.168.1.1
dhcp-authoritative

# DNS configuration
domain-needed
bogus-priv
no-resolv
server=8.8.8.8
server=8.8.4.4
server=1.1.1.1

# Lease file location
dhcp-leasefile=/var/lib/misc/dnsmasq.leases

# Logging (moderate for Pi 3)
log-queries
log-dhcp

# Performance optimizations for Pi 3
cache-size=200
dns-forward-max=200
min-port=4096
max-port=65535

# Security
no-ping
dhcp-name-match=set:hostname-ignore,wpad
dhcp-ignore-names=tag:hostname-ignore

# Local domain
local=/local/
domain=local

# Static leases (examples - customize as needed)
# dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1
# dhcp-host=11:22:33:44:55:66,192.168.1.11,device2

# Time-to-live settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=200
{% endblock %}
```

### Raspberry Pi 4/5 dnsmasq Configuration
```conf
# templates/dnsmasq_pi_4_5.conf.j2
# dnsmasq configuration template for Raspberry Pi 4/5
# This template contains settings optimized for Raspberry Pi 4/5

{% extends "dnsmasq_base.conf.j2" %}

{% block config %}
# Interface configuration
interface=wlan0
# Uncomment the line below if using Ethernet instead of WiFi
# interface=eth0

# DHCP server configuration
dhcp-range=192.168.1.100,192.168.1.250,255.255.255.0,24h
dhcp-option=option:router,192.168.1.1
dhcp-option=option:dns-server,192.168.1.1
dhcp-authoritative

# DNS configuration
domain-needed
bogus-priv
no-resolv
server=8.8.8.8
server=8.8.4.4
server=1.1.1.1

# Lease file location
dhcp-leasefile=/var/lib/misc/dnsmasq.leases

# Logging (full for Pi 4/5)
log-queries
log-dhcp
log-async=50  # Async logging for better performance

# Performance optimizations for Pi 4/5
cache-size=500
dns-forward-max=500
min-port=4096
max-port=65535

# Security
no-ping
dhcp-name-match=set:hostname-ignore,wpad
dhcp-ignore-names=tag:hostname-ignore

# Local domain
local=/local/
domain=local

# Static leases (examples - customize as needed)
# dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1
# dhcp-host=11:22:33:44:55:66,192.168.1.11,device2

# Time-to-live settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=500

# Additional features for Pi 4/5
dhcp-rapid-commit
dhcp-option=option:ntp-server,0.0.0.0
{% endblock %}
```

### Low-Resource PC dnsmasq Configuration
```conf
# templates/dnsmasq_low_resource_pc.conf.j2
# dnsmasq configuration template for Low-Resource PC
# This template contains settings optimized for Low-Resource PC

{% extends "dnsmasq_base.conf.j2" %}

{% block config %}
# Interface configuration
interface=eth0
# Uncomment the line below if using WiFi instead of Ethernet
# interface=wlan0

# DHCP server configuration
dhcp-range=192.168.1.100,192.168.1.180,255.255.255.0,24h
dhcp-option=option:router,192.168.1.1
dhcp-option=option:dns-server,192.168.1.1
dhcp-authoritative

# DNS configuration
domain-needed
bogus-priv
no-resolv
server=8.8.8.8
server=8.8.4.4
server=1.1.1.1

# Lease file location
dhcp-leasefile=/var/lib/misc/dnsmasq.leases

# Logging (minimal for resource constraints)
# log-queries  # Commented out to save resources
# log-dhcp     # Commented out to save resources

# Performance optimizations for Low-Resource PC
cache-size=300
dns-forward-max=300
min-port=4096
max-port=65535

# Security
no-ping
dhcp-name-match=set:hostname-ignore,wpad
dhcp-ignore-names=tag:hostname-ignore

# Local domain
local=/local/
domain=local

# Static leases (examples - customize as needed)
# dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1
# dhcp-host=11:22:33:44:55:66,192.168.1.11,device2

# Time-to-live settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=300
{% endblock %}
```

### Standard PC dnsmasq Configuration
```conf
# templates/dnsmasq_standard_pc.conf.j2
# dnsmasq configuration template for Standard PC
# This template contains settings optimized for Standard PC

{% extends "dnsmasq_base.conf.j2" %}

{% block config %}
# Interface configuration
interface=eth0
# Uncomment the line below if using WiFi instead of Ethernet
# interface=wlan0

# DHCP server configuration
dhcp-range=192.168.1.100,192.168.1.250,255.255.255.0,24h
dhcp-option=option:router,192.168.1.1
dhcp-option=option:dns-server,192.168.1.1
dhcp-authoritative

# DNS configuration
domain-needed
bogus-priv
no-resolv
server=8.8.8.8
server=8.8.4.4
server=1.1.1.1

# Lease file location
dhcp-leasefile=/var/lib/misc/dnsmasq.leases

# Logging (full for Standard PC)
log-queries
log-dhcp
log-async=100  # Async logging for better performance

# Performance optimizations for Standard PC
cache-size=1000
dns-forward-max=1000
min-port=4096
max-port=65535

# Security
no-ping
dhcp-name-match=set:hostname-ignore,wpad
dhcp-ignore-names=tag:hostname-ignore

# Local domain
local=/local/
domain=local

# Static leases (examples - customize as needed)
# dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1
# dhcp-host=11:22:33:44:55:66,192.168.1.11,device2

# Time-to-live settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=1000

# Additional features for Standard PC
dhcp-rapid-commit
dhcp-option=option:ntp-server,0.0.0.0
dhcp-option=option:domain-search,local
{% endblock %}
```

## 4. Systemd Service Templates

### Base Systemd Service Template
```ini
# templates/pidns_base.service.j2
# Base systemd service template for PiDNS
# This template contains common settings for all device types

[Unit]
Description=PiDNS Dashboard - Network monitoring dashboard
After=network.target dnsmasq.service
Wants=network.target dnsmasq.service

[Service]
Type=simple
User={{ service_user }}
Group={{ service_group }}
WorkingDirectory={{ working_directory }}
Environment=FLASK_ENV={{ flask_env }}
Environment=PYTHONPATH={{ python_path }}
ExecStart={{ exec_start }}
ExecReload={{ exec_reload }}
Restart=on-failure
RestartSec={{ restart_sec }}
StandardOutput={{ standard_output }}
StandardError={{ standard_error }}

# Resource limits
MemoryLimit={{ memory_limit }}
CPUQuota={{ cpu_quota }}
TasksMax={{ tasks_max }}
LimitNOFILE={{ limit_nofile }}

# Security settings
NoNewPrivileges={{ no_new_privileges }}
PrivateTmp={{ private_tmp }}
ProtectSystem={{ protect_system }}
ProtectHome={{ protect_home }}
ReadWritePaths={{ read_write_paths }}

[Install]
WantedBy={{ wanted_by }}
```

### Raspberry Pi Zero W Systemd Service Template
```ini
# templates/pidns_pi_zero.service.j2
# Systemd service template for Raspberry Pi Zero W
# This template contains settings optimized for Raspberry Pi Zero W

{% extends "pidns_base.service.j2" %}

{% block config %}
[Unit]
Description=PiDNS Dashboard - Network monitoring dashboard
After=network.target dnsmasq.service
Wants=network.target dnsmasq.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/app/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Pi Zero W
MemoryLimit=256M
CPUQuota=50%
TasksMax=50
LimitNOFILE=1024

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /var/lib/misc

[Install]
WantedBy=multi-user.target
{% endblock %}
```

### Raspberry Pi Zero 2W Systemd Service Template
```ini
# templates/pidns_pi_zero_2w.service.j2
# Systemd service template for Raspberry Pi Zero 2W
# This template contains settings optimized for Raspberry Pi Zero 2W

{% extends "pidns_base.service.j2" %}

{% block config %}
[Unit]
Description=PiDNS Dashboard - Network monitoring dashboard
After=network.target dnsmasq.service
Wants=network.target dnsmasq.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/app/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Pi Zero 2W
MemoryLimit=256M
CPUQuota=50%
TasksMax=50
LimitNOFILE=1024

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /var/lib/misc

[Install]
WantedBy=multi-user.target
{% endblock %}
```

### Raspberry Pi 3 Systemd Service Template
```ini
# templates/pidns_pi_3.service.j2
# Systemd service template for Raspberry Pi 3
# This template contains settings optimized for Raspberry Pi 3

{% extends "pidns_base.service.j2" %}

{% block config %}
[Unit]
Description=PiDNS Dashboard - Network monitoring dashboard
After=network.target dnsmasq.service
Wants=network.target dnsmasq.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/app/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Pi 3
MemoryLimit=512M
CPUQuota=75%
TasksMax=100
LimitNOFILE=2048

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /var/lib/misc

[Install]
WantedBy=multi-user.target
{% endblock %}
```

### Raspberry Pi 4/5 Systemd Service Template
```ini
# templates/pidns_pi_4_5.service.j2
# Systemd service template for Raspberry Pi 4/5
# This template contains settings optimized for Raspberry Pi 4/5

{% extends "pidns_base.service.j2" %}

{% block config %}
[Unit]
Description=PiDNS Dashboard - Network monitoring dashboard
After=network.target dnsmasq.service
Wants=network.target dnsmasq.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/app/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Pi 4/5
MemoryLimit=1024M
CPUQuota=100%
TasksMax=200
LimitNOFILE=4096

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /var/lib/misc

[Install]
WantedBy=multi-user.target
{% endblock %}
```

### Low-Resource PC Systemd Service Template
```ini
# templates/pidns_low_resource_pc.service.j2
# Systemd service template for Low-Resource PC
# This template contains settings optimized for Low-Resource PC

{% extends "pidns_base.service.j2" %}

{% block config %}
[Unit]
Description=PiDNS Dashboard - Network monitoring dashboard
After=network.target dnsmasq.service
Wants=network.target dnsmasq.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/app/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Low-Resource PC
MemoryLimit=512M
CPUQuota=75%
TasksMax=100
LimitNOFILE=2048

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /var/lib/misc

[Install]
WantedBy=multi-user.target
{% endblock %}
```

### Standard PC Systemd Service Template
```ini
# templates/pidns_standard_pc.service.j2
# Systemd service template for Standard PC
# This template contains settings optimized for Standard PC

{% extends "pidns_base.service.j2" %}

{% block config %}
[Unit]
Description=PiDNS Dashboard - Network monitoring dashboard
After=network.target dnsmasq.service
Wants=network.target dnsmasq.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/app/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Standard PC
MemoryLimit=2048M
CPUQuota=100%
TasksMax=500
LimitNOFILE=8192

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /var/lib/misc

[Install]
WantedBy=multi-user.target
{% endblock %}
```

## 5. Container Configuration Templates

### Docker Compose Base Template
```yaml
# templates/docker-compose_base.yml.j2
# Base Docker Compose template for PiDNS
# This template contains common settings for all device types

version: '3.8'

services:
  pidns:
    build: 
      context: .
      dockerfile: Dockerfile
    image: pidns:latest
    container_name: pidns
    restart: unless-stopped
    network_mode: host
    cap_add:
      - NET_ADMIN
    volumes:
      - pidns-data:/app/data
      - pidns-logs:/var/log/pidns
      - pidns-config:/app/config
      - /var/lib/misc:/var/lib/misc:rw
      - /etc/dnsmasq.conf:/etc/dnsmasq.conf:rw
    environment:
      - FLASK_ENV={{ flask_env }}
      - PIDNS_USERNAME={{ pidns_username }}
      - PIDNS_PASSWORD={{ pidns_password }}
      - DEVICE_TYPE={{ device_type }}
    depends_on:
      - dnsmasq

  dnsmasq:
    image: andyshinn/dnsmasq:latest
    container_name: pidns-dnsmasq
    restart: unless-stopped
    network_mode: host
    cap_add:
      - NET_ADMIN
    volumes:
      - ./config/dnsmasq.{{ device_type }}.conf:/etc/dnsmasq.conf:ro
      - /var/lib/misc:/var/lib/misc:rw
    command: --log-queries --log-dhcp

volumes:
  pidns-data:
  pidns-logs:
  pidns-config:
```

### Docker Compose Override Templates
```yaml
# templates/docker-compose_override_pi_zero.yml.j2
# Docker Compose override template for Raspberry Pi Zero W
# This template contains settings optimized for Raspberry Pi Zero W

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: pi-zero
    environment:
      - DEVICE_TYPE=pi-zero
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
        reservations:
          memory: 128M
          cpus: '0.25'
    volumes:
      - ./config/flask_config.pi_zero.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi_zero.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/docker-compose_override_pi_zero_2w.yml.j2
# Docker Compose override template for Raspberry Pi Zero 2W
# This template contains settings optimized for Raspberry Pi Zero 2W

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: pi-zero-2w
    environment:
      - DEVICE_TYPE=pi-zero-2w
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
        reservations:
          memory: 128M
          cpus: '0.25'
    volumes:
      - ./config/flask_config.pi_zero_2w.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi_zero_2w.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/docker-compose_override_pi_3.yml.j2
# Docker Compose override template for Raspberry Pi 3
# This template contains settings optimized for Raspberry Pi 3

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: pi-3
    environment:
      - DEVICE_TYPE=pi-3
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
    volumes:
      - ./config/flask_config.pi_3.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi_3.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/docker-compose_override_pi_4_5.yml.j2
# Docker Compose override template for Raspberry Pi 4/5
# This template contains settings optimized for Raspberry Pi 4/5

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: pi-4
    environment:
      - DEVICE_TYPE=pi-4
    deploy:
      resources:
        limits:
          memory: 1024M
          cpus: '2.0'
        reservations:
          memory: 512M
          cpus: '1.0'
    volumes:
      - ./config/flask_config.pi_4_5.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi_4_5.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/docker-compose_override_low_resource_pc.yml.j2
# Docker Compose override template for Low-Resource PC
# This template contains settings optimized for Low-Resource PC

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: low-resource-pc
    environment:
      - DEVICE_TYPE=low-resource-pc
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
    volumes:
      - ./config/flask_config.low_resource_pc.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.low_resource_pc.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/docker-compose_override_standard_pc.yml.j2
# Docker Compose override template for Standard PC
# This template contains settings optimized for Standard PC

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: standard-pc
    environment:
      - DEVICE_TYPE=standard-pc
    deploy:
      resources:
        limits:
          memory: 2048M
          cpus: '4.0'
        reservations:
          memory: 1024M
          cpus: '2.0'
    volumes:
      - ./config/flask_config.standard_pc.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.standard_pc.conf:/etc/dnsmasq.conf:ro
```

### Podman Compose Base Template
```yaml
# templates/podman-compose_base.yml.j2
# Base Podman Compose template for PiDNS
# This template contains common settings for all device types

version: '3.8'

services:
  pidns:
    build: 
      context: .
      dockerfile: Containerfile
    image: pidns:latest
    container_name: pidns
    restart: unless-stopped
    network_mode: host
    cap_add:
      - NET_ADMIN
    volumes:
      - pidns-data:/app/data:z
      - pidns-logs:/var/log/pidns:z
      - pidns-config:/app/config:z
      - /var/lib/misc:/var/lib/misc:rw,z
      - /etc/dnsmasq.conf:/etc/dnsmasq.conf:rw,z
    environment:
      - FLASK_ENV={{ flask_env }}
      - PIDNS_USERNAME={{ pidns_username }}
      - PIDNS_PASSWORD={{ pidns_password }}
      - DEVICE_TYPE={{ device_type }}
    userns: keep-id

  dnsmasq:
    image: andyshinn/dnsmasq:latest
    container_name: pidns-dnsmasq
    restart: unless-stopped
    network_mode: host
    cap_add:
      - NET_ADMIN
    volumes:
      - ./config/dnsmasq.{{ device_type }}.conf:/etc/dnsmasq.conf:ro,z
      - /var/lib/misc:/var/lib/misc:rw,z
    command: --log-queries --log-dhcp
    userns: keep-id

volumes:
  pidns-data:
  pidns-logs:
  pidns-config:
```

### Podman Compose Override Templates
```yaml
# templates/podman-compose_override_pi_zero.yml.j2
# Podman Compose override template for Raspberry Pi Zero W
# This template contains settings optimized for Raspberry Pi Zero W

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: pi-zero
    environment:
      - DEVICE_TYPE=pi-zero
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
        reservations:
          memory: 128M
          cpus: '0.25'
    volumes:
      - ./config/flask_config.pi_zero.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi_zero.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/podman-compose_override_pi_zero_2w.yml.j2
# Podman Compose override template for Raspberry Pi Zero 2W
# This template contains settings optimized for Raspberry Pi Zero 2W

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: pi-zero-2w
    environment:
      - DEVICE_TYPE=pi-zero-2w
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
        reservations:
          memory: 128M
          cpus: '0.25'
    volumes:
      - ./config/flask_config.pi_zero_2w.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi_zero_2w.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/podman-compose_override_pi_3.yml.j2
# Podman Compose override template for Raspberry Pi 3
# This template contains settings optimized for Raspberry Pi 3

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: pi-3
    environment:
      - DEVICE_TYPE=pi-3
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
    volumes:
      - ./config/flask_config.pi_3.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi_3.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/podman-compose_override_pi_4_5.yml.j2
# Podman Compose override template for Raspberry Pi 4/5
# This template contains settings optimized for Raspberry Pi 4/5

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: pi-4
    environment:
      - DEVICE_TYPE=pi-4
    deploy:
      resources:
        limits:
          memory: 1024M
          cpus: '2.0'
        reservations:
          memory: 512M
          cpus: '1.0'
    volumes:
      - ./config/flask_config.pi_4_5.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi_4_5.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/podman-compose_override_low_resource_pc.yml.j2
# Podman Compose override template for Low-Resource PC
# This template contains settings optimized for Low-Resource PC

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: low-resource-pc
    environment:
      - DEVICE_TYPE=low-resource-pc
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
    volumes:
      - ./config/flask_config.low_resource_pc.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.low_resource_pc.conf:/etc/dnsmasq.conf:ro
```

```yaml
# templates/podman-compose_override_standard_pc.yml.j2
# Podman Compose override template for Standard PC
# This template contains settings optimized for Standard PC

version: '3.8'

services:
  pidns:
    build:
      args:
        DEVICE_TYPE: standard-pc
    environment:
      - DEVICE_TYPE=standard-pc
    deploy:
      resources:
        limits:
          memory: 2048M
          cpus: '4.0'
        reservations:
          memory: 1024M
          cpus: '2.0'
    volumes:
      - ./config/flask_config.standard_pc.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.standard_pc.conf:/etc/dnsmasq.conf:ro
```

### LXC Configuration Templates
```conf
# templates/lxc_base.conf.j2
# Base LXC configuration template for PiDNS
# This template contains common settings for all device types

lxc.uts.name = pidns
lxc.arch = {{ lxc_arch }}

# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx

# Root filesystem
lxc.rootfs.path = dir:/var/lib/lxc/pidns/rootfs

# Mounts
lxc.mount.entry = /var/lib/misc var/lib/misc none bind,create=dir
lxc.mount.entry = /etc/dnsmasq.conf etc/dnsmasq.conf none bind,create=file
lxc.mount.entry = /var/log/pidns var/log/pidns none bind,create=dir

# Autostart
lxc.start.auto = 1
lxc.start.delay = 5

# Resource limits
lxc.cgroup.memory.limit_in_bytes = {{ memory_limit }}
lxc.cgroup.memory.swappiness = {{ memory_swappiness }}
lxc.cgroup.cpu.shares = {{ cpu_shares }}

# Capabilities
lxc.cap.drop = {{ dropped_capabilities }}

# Console settings
lxc.tty.max = {{ tty_max }}
lxc.pts = {{ pts }}

# AppArmor profile
lxc.apparmor.profile = {{ apparmor_profile }}
```

```conf
# templates/lxc_pi_zero.conf.j2
# LXC configuration template for Raspberry Pi Zero W
# This template contains settings optimized for Raspberry Pi Zero W

{% extends "lxc_base.conf.j2" %}

{% block config %}
lxc.uts.name = pidns
lxc.arch = linuxarm

# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx

# Root filesystem
lxc.rootfs.path = dir:/var/lib/lxc/pidns/rootfs

# Mounts
lxc.mount.entry = /var/lib/misc var/lib/misc none bind,create=dir
lxc.mount.entry = /etc/dnsmasq.conf etc/dnsmasq.conf none bind,create=file
lxc.mount.entry = /var/log/pidns var/log/pidns none bind,create=dir

# Autostart
lxc.start.auto = 1
lxc.start.delay = 5

# Resource limits for Pi Zero W
lxc.cgroup.memory.limit_in_bytes = 256M
lxc.cgroup.memory.swappiness = 10
lxc.cgroup.cpu.shares = 128

# Capabilities
lxc.cap.drop = sys_admin sys_module sys_rawio

# Console settings
lxc.tty.max = 2
lxc.pts = 64

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
{% endblock %}
```

```conf
# templates/lxc_pi_zero_2w.conf.j2
# LXC configuration template for Raspberry Pi Zero 2W
# This template contains settings optimized for Raspberry Pi Zero 2W

{% extends "lxc_base.conf.j2" %}

{% block config %}
lxc.uts.name = pidns
lxc.arch = linuxarm

# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx

# Root filesystem
lxc.rootfs.path = dir:/var/lib/lxc/pidns/rootfs

# Mounts
lxc.mount.entry = /var/lib/misc var/lib/misc none bind,create=dir
lxc.mount.entry = /etc/dnsmasq.conf etc/dnsmasq.conf none bind,create=file
lxc.mount.entry = /var/log/pidns var/log/pidns none bind,create=dir

# Autostart
lxc.start.auto = 1
lxc.start.delay = 5

# Resource limits for Pi Zero 2W
lxc.cgroup.memory.limit_in_bytes = 256M
lxc.cgroup.memory.swappiness = 10
lxc.cgroup.cpu.shares = 128

# Capabilities
lxc.cap.drop = sys_admin sys_module sys_rawio

# Console settings
lxc.tty.max = 2
lxc.pts = 64

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
{% endblock %}
```

```conf
# templates/lxc_pi_3.conf.j2
# LXC configuration template for Raspberry Pi 3
# This template contains settings optimized for Raspberry Pi 3

{% extends "lxc_base.conf.j2" %}

{% block config %}
lxc.uts.name = pidns
lxc.arch = linuxarm

# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx

# Root filesystem
lxc.rootfs.path = dir:/var/lib/lxc/pidns/rootfs

# Mounts
lxc.mount.entry = /var/lib/misc var/lib/misc none bind,create=dir
lxc.mount.entry = /etc/dnsmasq.conf etc/dnsmasq.conf none bind,create=file
lxc.mount.entry = /var/log/pidns var/log/pidns none bind,create=dir

# Autostart
lxc.start.auto = 1
lxc.start.delay = 5

# Resource limits for Pi 3
lxc.cgroup.memory.limit_in_bytes = 512M
lxc.cgroup.memory.swappiness = 10
lxc.cgroup.cpu.shares = 256

# Capabilities
lxc.cap.drop = sys_admin sys_module sys_rawio

# Console settings
lxc.tty.max = 4
lxc.pts = 128

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
{% endblock %}
```

```conf
# templates/lxc_pi_4_5.conf.j2
# LXC configuration template for Raspberry Pi 4/5
# This template contains settings optimized for Raspberry Pi 4/5

{% extends "lxc_base.conf.j2" %}

{% block config %}
lxc.uts.name = pidns
lxc.arch = linuxarm

# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx

# Root filesystem
lxc.rootfs.path = dir:/var/lib/lxc/pidns/rootfs

# Mounts
lxc.mount.entry = /var/lib/misc var/lib/misc none bind,create=dir
lxc.mount.entry = /etc/dnsmasq.conf etc/dnsmasq.conf none bind,create=file
lxc.mount.entry = /var/log/pidns var/log/pidns none bind,create=dir

# Autostart
lxc.start.auto = 1
lxc.start.delay = 5

# Resource limits for Pi 4/5
lxc.cgroup.memory.limit_in_bytes = 2048M
lxc.cgroup.memory.swappiness = 5
lxc.cgroup.cpu.shares = 512

# Capabilities
lxc.cap.drop = sys_admin sys_module sys_rawio

# Console settings
lxc.tty.max = 4
lxc.pts = 256

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
{% endblock %}
```

```conf
# templates/lxc_low_resource_pc.conf.j2
# LXC configuration template for Low-Resource PC
# This template contains settings optimized for Low-Resource PC

{% extends "lxc_base.conf.j2" %}

{% block config %}
lxc.uts.name = pidns
lxc.arch = linuxamd64

# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx

# Root filesystem
lxc.rootfs.path = dir:/var/lib/lxc/pidns/rootfs

# Mounts
lxc.mount.entry = /var/lib/misc var/lib/misc none bind,create=dir
lxc.mount.entry = /etc/dnsmasq.conf etc/dnsmasq.conf none bind,create=file
lxc.mount.entry = /var/log/pidns var/log/pidns none bind,create=dir

# Autostart
lxc.start.auto = 1
lxc.start.delay = 5

# Resource limits for Low-Resource PC
lxc.cgroup.memory.limit_in_bytes = 512M
lxc.cgroup.memory.swappiness = 10
lxc.cgroup.cpu.shares = 256

# Capabilities
lxc.cap.drop = sys_admin sys_module sys_rawio

# Console settings
lxc.tty.max = 4
lxc.pts = 128

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
{% endblock %}
```

```conf
# templates/lxc_standard_pc.conf.j2
# LXC configuration template for Standard PC
# This template contains settings optimized for Standard PC

{% extends "lxc_base.conf.j2" %}

{% block config %}
lxc.uts.name = pidns
lxc.arch = linuxamd64

# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx

# Root filesystem
lxc.rootfs.path = dir:/var/lib/lxc/pidns/rootfs

# Mounts
lxc.mount.entry = /var/lib/misc var/lib/misc none bind,create=dir
lxc.mount.entry = /etc/dnsmasq.conf etc/dnsmasq.conf none bind,create=file
lxc.mount.entry = /var/log/pidns var/log/pidns none bind,create=dir

# Autostart
lxc.start.auto = 1
lxc.start.delay = 5

# Resource limits for Standard PC
lxc.cgroup.memory.limit_in_bytes = 2048M
lxc.cgroup.memory.swappiness = 5
lxc.cgroup.cpu.shares = 512

# Capabilities
lxc.cap.drop = sys_admin sys_module sys_rawio

# Console settings
lxc.tty.max = 4
lxc.pts = 256

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
{% endblock %}
```

## 6. Template Variables

### Device Type Variables
```python
# templates/variables/device_types.py
# Device type variables for PiDNS configuration templates

DEVICE_TYPES = {
    "pi-zero": {
        "name": "Raspberry Pi Zero W",
        "memory": "512MB",
        "cpu_cores": 1,
        "threads_per_page": 1,
        "processes": 1,
        "refresh_interval": 60,
        "max_devices": 25,
        "log_level": "WARNING",
        "cache_type": "simple",
        "cache_timeout": 600,
        "session_cookie_secure": False,
        "session_lifetime": 1800,
        "api_rate_limit": "30/hour",
        "ad_blocker_enabled": False,
        "cache_size": 50,
        "dns_forward_max": 50,
        "memory_limit": "256M",
        "cpu_quota": "50%",
        "tasks_max": 50,
        "limit_nofile": 1024,
        "tty_max": 2,
        "pts": 64,
        "memory_swappiness": 10,
        "cpu_shares": 128,
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping",
        "log_max_size": "5MB",
        "log_backup_count": 2
    },
    "pi-zero-2w": {
        "name": "Raspberry Pi Zero 2W",
        "memory": "512MB",
        "cpu_cores": 1,
        "threads_per_page": 1,
        "processes": 1,
        "refresh_interval": 60,
        "max_devices": 25,
        "log_level": "WARNING",
        "cache_type": "simple",
        "cache_timeout": 600,
        "session_cookie_secure": False,
        "session_lifetime": 1800,
        "api_rate_limit": "30/hour",
        "ad_blocker_enabled": False,
        "cache_size": 50,
        "dns_forward_max": 50,
        "memory_limit": "256M",
        "cpu_quota": "50%",
        "tasks_max": 50,
        "limit_nofile": 1024,
        "tty_max": 2,
        "pts": 64,
        "memory_swappiness": 10,
        "cpu_shares": 128,
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping",
        "log_max_size": "5MB",
        "log_backup_count": 2
    },
    "pi-3": {
        "name": "Raspberry Pi 3",
        "memory": "1GB",
        "cpu_cores": 4,
        "threads_per_page": 2,
        "processes": 1,
        "refresh_interval": 30,
        "max_devices": 50,
        "log_level": "INFO",
        "cache_type": "simple",
        "cache_timeout": 300,
        "session_cookie_secure": False,
        "session_lifetime": 3600,
        "api_rate_limit": "60/hour",
        "ad_blocker_enabled": True,
        "cache_size": 200,
        "dns_forward_max": 200,
        "memory_limit": "512M",
        "cpu_quota": "75%",
        "tasks_max": 100,
        "limit_nofile": 2048,
        "tty_max": 4,
        "pts": 128,
        "memory_swappiness": 10,
        "cpu_shares": 256,
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping",
        "log_max_size": "10MB",
        "log_backup_count": 3
    },
    "pi-4": {
        "name": "Raspberry Pi 4",
        "memory": "2-8GB",
        "cpu_cores": 4,
        "threads_per_page": 4,
        "processes": 1,
        "refresh_interval": 15,
        "max_devices": 250,
        "log_level": "DEBUG",
        "cache_type": "filesystem",
        "cache_timeout": 300,
        "session_cookie_secure": False,
        "session_lifetime": 3600,
        "api_rate_limit": "100/hour",
        "ad_blocker_enabled": True,
        "cache_size": 500,
        "dns_forward_max": 500,
        "memory_limit": "1024M",
        "cpu_quota": "100%",
        "tasks_max": 200,
        "limit_nofile": 4096,
        "tty_max": 4,
        "pts": 256,
        "memory_swappiness": 5,
        "cpu_shares": 512,
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping",
        "log_max_size": "20MB",
        "log_backup_count": 5
    },
    "pi-5": {
        "name": "Raspberry Pi 5",
        "memory": "4-8GB",
        "cpu_cores": 4,
        "threads_per_page": 4,
        "processes": 1,
        "refresh_interval": 15,
        "max_devices": 250,
        "log_level": "DEBUG",
        "cache_type": "filesystem",
        "cache_timeout": 300,
        "session_cookie_secure": False,
        "session_lifetime": 3600,
        "api_rate_limit": "100/hour",
        "ad_blocker_enabled": True,
        "cache_size": 500,
        "dns_forward_max": 500,
        "memory_limit": "1024M",
        "cpu_quota": "100%",
        "tasks_max": 200,
        "limit_nofile": 4096,
        "tty_max": 4,
        "pts": 256,
        "memory_swappiness": 5,
        "cpu_shares": 512,
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping",
        "log_max_size": "20MB",
        "log_backup_count": 5
    },
    "low-resource-pc": {
        "name": "Low-Resource PC",
        "memory": "≤1GB",
        "cpu_cores": "≤2",
        "threads_per_page": 2,
        "processes": 1,
        "refresh_interval": 45,
        "max_devices": 75,
        "log_level": "WARNING",
        "cache_type": "simple",
        "cache_timeout": 600,
        "session_cookie_secure": False,
        "session_lifetime": 3600,
        "api_rate_limit": "60/hour",
        "ad_blocker_enabled": True,
        "cache_size": 300,
        "dns_forward_max": 300,
        "memory_limit": "512M",
        "cpu_quota": "75%",
        "tasks_max": 100,
        "limit_nofile": 2048,
        "tty_max": 4,
        "pts": 128,
        "memory_swappiness": 10,
        "cpu_shares": 256,
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping",
        "log_max_size": "10MB",
        "log_backup_count": 3
    },
    "standard-pc": {
        "name": "Standard PC",
        "memory": ">1GB",
        "cpu_cores": ">2",
        "threads_per_page": 4,
        "processes": 1,
        "refresh_interval": 10,
        "max_devices": 500,
        "log_level": "DEBUG",
        "cache_type": "redis",
        "cache_timeout": 300,
        "session_cookie_secure": True,
        "session_lifetime": 3600,
        "api_rate_limit": "100/hour",
        "ad_blocker_enabled": True,
        "cache_size": 1000,
        "dns_forward_max": 1000,
        "memory_limit": "2048M",
        "cpu_quota": "100%",
        "tasks_max": 500,
        "limit_nofile": 8192,
        "tty_max": 4,
        "pts": 256,
        "memory_swappiness": 5,
        "cpu_shares": 512,
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping",
        "log_max_size": "20MB",
        "log_backup_count": 5
    }
}
```

### Container Type Variables
```python
# templates/variables/container_types.py
# Container type variables for PiDNS configuration templates

CONTAINER_TYPES = {
    "docker": {
        "name": "Docker",
        "description": "Most popular container platform with wide community support",
        "compose_file": "docker-compose.yml",
        "override_file": "docker-compose.override.{device_type}.yml",
        "service_file": "pidns-docker.service",
        "build_file": "Dockerfile",
        "network_mode": "host",
        "cap_add": ["NET_ADMIN"],
        "volumes": [
            "pidns-data:/app/data",
            "pidns-logs:/var/log/pidns",
            "pidns-config:/app/config",
            "/var/lib/misc:/var/lib/misc:rw",
            "/etc/dnsmasq.conf:/etc/dnsmasq.conf:rw"
        ],
        "environment": [
            "FLASK_ENV=production",
            "PIDNS_USERNAME=admin",
            "PIDNS_PASSWORD=password",
            "DEVICE_TYPE={device_type}"
        ],
        "depends_on": ["dnsmasq"],
        "security": {
            "non_root_user": True,
            "read_only_filesystem": False,
            "resource_limits": True,
            "health_checks": True,
            "seccomp_profiles": True,
            "apparmor_profiles": False
        },
        "performance": {
            "multi_stage_build": True,
            "resource_limits": True,
            "health_checks": True,
            "volume_management": True,
            "caching": True,
            "parallel_builds": True
        }
    },
    "podman": {
        "name": "Podman",
        "description": "Daemonless, rootless containers with better security",
        "compose_file": "podman-compose.yml",
        "override_file": "podman-compose.override.{device_type}.yml",
        "service_file": "pidns-podman.service",
        "build_file": "Containerfile",
        "network_mode": "host",
        "cap_add": ["NET_ADMIN"],
        "volumes": [
            "pidns-data:/app/data:z",
            "pidns-logs:/var/log/pidns:z",
            "pidns-config:/app/config:z",
            "/var/lib/misc:/var/lib/misc:rw,z",
            "/etc/dnsmasq.conf:/etc/dnsmasq.conf:rw,z"
        ],
        "environment": [
            "FLASK_ENV=production",
            "PIDNS_USERNAME=admin",
            "PIDNS_PASSWORD=password",
            "DEVICE_TYPE={device_type}"
        ],
        "userns": "keep-id",
        "depends_on": ["dnsmasq"],
        "security": {
            "non_root_user": True,
            "read_only_filesystem": False,
            "resource_limits": True,
            "health_checks": False,
            "seccomp_profiles": True,
            "apparmor_profiles": False,
            "selinux_labeling": True,
            "user_namespace_mapping": True,
            "no_new_privileges": True
        },
        "performance": {
            "slim_base_image": True,
            "resource_limits": True,
            "quadlet_integration": True,
            "volume_management": True,
            "caching": True,
            "parallel_builds": True
        }
    },
    "lxc": {
        "name": "LXC",
        "description": "Lightweight OS-level virtualization with better performance",
        "config_file": "lxc-{device_type}.conf",
        "service_file": "pidns-lxc.service",
        "setup_script": "lxc-setup.sh",
        "network_mode": "veth",
        "cap_add": ["NET_ADMIN"],
        "mounts": [
            "/var/lib/misc var/lib/misc none bind,create=dir",
            "/etc/dnsmasq.conf etc/dnsmasq.conf none bind,create=file",
            "/var/log/pidns var/log/pidns none bind,create=dir"
        ],
        "environment": [
            "FLASK_ENV=production",
            "PIDNS_USERNAME=admin",
            "PIDNS_PASSWORD=password",
            "DEVICE_TYPE={device_type}"
        ],
        "autostart": True,
        "security": {
            "capability_dropping": True,
            "apparmor_profiles": True,
            "device_restrictions": True,
            "resource_limits": True,
            "network_isolation": True,
            "control_groups": True,
            "namespace_isolation": True
        },
        "performance": {
            "resource_limits": True,
            "filesystem_mounts": True,
            "network_configuration": True,
            "autostart_configuration": True,
            "memory_management": True,
            "cpu_management": True
        }
    },
    "none": {
        "name": "None (Bare Metal)",
        "description": "Install directly on the host system without containers",
        "service_file": "pidns.service",
        "dnsmasq_service_file": "dnsmasq.service",
        "environment": [
            "FLASK_ENV=production",
            "PIDNS_USERNAME=admin",
            "PIDNS_PASSWORD=password",
            "DEVICE_TYPE={device_type}"
        ],
        "security": {
            "systemd_security": True,
            "file_permissions": True,
            "user_permissions": True,
            "service_isolation": True
        },
        "performance": {
            "direct_hardware_access": True,
            "no_container_overhead": True,
            "system_optimization": True
        }
    }
}
```

### Environment Variables
```python
# templates/variables/environments.py
# Environment variables for PiDNS configuration templates

ENVIRONMENTS = {
    "development": {
        "name": "Development",
        "flask_env": "development",
        "debug": True,
        "testing": False,
        "log_level": "DEBUG",
        "session_cookie_secure": False,
        "cache_type": "simple",
        "cache_timeout": 60,
        "api_rate_limit": "1000/hour",
        "ad_blocker_enabled": True,
        "log_file": "/var/log/pidns/app-dev.log",
        "log_max_size": "50MB",
        "log_backup_count": 10
    },
    "testing": {
        "name": "Testing",
        "flask_env": "testing",
        "debug": True,
        "testing": True,
        "log_level": "DEBUG",
        "session_cookie_secure": False,
        "cache_type": "simple",
        "cache_timeout": 60,
        "api_rate_limit": "1000/hour",
        "ad_blocker_enabled": True,
        "log_file": "/var/log/pidns/app-test.log",
        "log_max_size": "50MB",
        "log_backup_count": 10
    },
    "production": {
        "name": "Production",
        "flask_env": "production",
        "debug": False,
        "testing": False,
        "log_level": "INFO",
        "session_cookie_secure": False,
        "cache_type": "filesystem",
        "cache_timeout": 300,
        "api_rate_limit": "100/hour",
        "ad_blocker_enabled": True,
        "log_file": "/var/log/pidns/app.log",
        "log_max_size": "20MB",
        "log_backup_count": 5
    }
}
```

## 7. Template Generation Script

### Template Generation Script
```python
# scripts/generate_config.py
#!/usr/bin/env python3
"""
Configuration generation script for PiDNS
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from jinja2 import Environment, FileSystemLoader, Template

# Import template variables
sys.path.append('templates/variables')
from device_types import DEVICE_TYPES
from container_types import CONTAINER_TYPES
from environments import ENVIRONMENTS

def create_output_directory(output_dir: str) -> bool:
    """Create output directory if it doesn't exist"""
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        return True
    except (OSError, PermissionError):
        print(f"Error: Cannot create output directory: {output_dir}")
        return False

def load_template(template_path: str) -> Optional[Template]:
    """Load a Jinja2 template"""
    try:
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template(template_path)
        return template
    except Exception as e:
        print(f"Error: Cannot load template {template_path}: {e}")
        return None

def generate_flask_config(device_type: str, output_dir: str) -> bool:
    """Generate Flask configuration file"""
    template_path = f"flask_config_{device_type}.py.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Add common variables
    common_vars = {
        "base_dir": str(Path.cwd()),
        "environment": "production"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / f"flask_config.{device_type}.py"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated Flask configuration: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render Flask configuration template: {e}")
        return False

def generate_dnsmasq_config(device_type: str, output_dir: str) -> bool:
    """Generate dnsmasq configuration file"""
    template_path = f"dnsmasq_{device_type}.conf.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Add common variables
    common_vars = {
        "interface": "wlan0",
        "dhcp_range_start": "192.168.1.100",
        "dhcp_range_end": "192.168.1.200",
        "dhcp_netmask": "255.255.255.0",
        "dhcp_lease_time": "24h",
        "dhcp_router": "192.168.1.1",
        "dhcp_dns_server": "192.168.1.1",
        "dns_server_1": "8.8.8.8",
        "dns_server_2": "8.8.4.4",
        "dns_server_3": "1.1.1.1",
        "enable_logging": True,
        "log_async": True,
        "log_async_queue_size": 50,
        "min_port": 4096,
        "max_port": 65535,
        "local_ttl": 1,
        "neg_ttl": 900,
        "max_ttl": 86400,
        "min_cache_ttl": 3600,
        "max_cache_ttl": 86400,
        "cache_limit": 100
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / f"dnsmasq.{device_type}.conf"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated dnsmasq configuration: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render dnsmasq configuration template: {e}")
        return False

def generate_systemd_service(device_type: str, output_dir: str) -> bool:
    """Generate systemd service file"""
    template_path = f"pidns_{device_type}.service.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Add common variables
    common_vars = {
        "service_user": "pi",
        "service_group": "pi",
        "working_directory": "/home/pi/PiDNS",
        "flask_env": "production",
        "python_path": "/home/pi/PiDNS",
        "exec_start": "/usr/bin/python3 /home/pi/PiDNS/app/app.py",
        "exec_reload": "/bin/kill -HUP $MAINPID",
        "restart_sec": 10,
        "standard_output": "journal",
        "standard_error": "journal",
        "no_new_privileges": True,
        "private_tmp": True,
        "protect_system": "strict",
        "protect_home": True,
        "read_write_paths": "/home/pi/PiDNS/data /var/lib/misc",
        "wanted_by": "multi-user.target"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / f"pidns.{device_type}.service"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated systemd service: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render systemd service template: {e}")
        return False

def generate_docker_compose(device_type: str, output_dir: str) -> bool:
    """Generate Docker Compose files"""
    # Generate base Docker Compose file
    base_template_path = "docker-compose_base.yml.j2"
    base_template = load_template(base_template_path)
    
    if not base_template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Add common variables
    common_vars = {
        "flask_env": "production",
        "pidns_username": "admin",
        "pidns_password": "password"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars}
    
    # Render base template
    try:
        output = base_template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / "docker-compose.yml"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated Docker Compose base file: {output_file}")
    except Exception as e:
        print(f"Error: Cannot render Docker Compose base template: {e}")
        return False
    
    # Generate Docker Compose override file
    override_template_path = f"docker-compose_override_{device_type}.yml.j2"
    override_template = load_template(override_template_path)
    
    if not override_template:
        return False
    
    # Render override template
    try:
        output = override_template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / f"docker-compose.override.{device_type}.yml"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated Docker Compose override file: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render Docker Compose override template: {e}")
        return False

def generate_podman_compose(device_type: str, output_dir: str) -> bool:
    """Generate Podman Compose files"""
    # Generate base Podman Compose file
    base_template_path = "podman-compose_base.yml.j2"
    base_template = load_template(base_template_path)
    
    if not base_template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Add common variables
    common_vars = {
        "flask_env": "production",
        "pidns_username": "admin",
        "pidns_password": "password"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars}
    
    # Render base template
    try:
        output = base_template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / "podman-compose.yml"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated Podman Compose base file: {output_file}")
    except Exception as e:
        print(f"Error: Cannot render Podman Compose base template: {e}")
        return False
    
    # Generate Podman Compose override file
    override_template_path = f"podman-compose_override_{device_type}.yml.j2"
    override_template = load_template(override_template_path)
    
    if not override_template:
        return False
    
    # Render override template
    try:
        output = override_template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / f"podman-compose.override.{device_type}.yml"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated Podman Compose override file: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render Podman Compose override template: {e}")
        return False

def generate_lxc_config(device_type: str, output_dir: str) -> bool:
    """Generate LXC configuration file"""
    template_path = f"lxc_{device_type}.conf.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Add common variables
    common_vars = {
        "lxc_arch": "linuxarm" if device_type.startswith("pi") else "linuxamd64",
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / f"lxc.{device_type}.conf"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated LXC configuration: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render LXC configuration template: {e}")
        return False

def generate_container_config(container_type: str, device_type: str, output_dir: str) -> bool:
    """Generate container configuration files"""
    if container_type == "docker":
        return generate_docker_compose(device_type, output_dir)
    elif container_type == "podman":
        return generate_podman_compose(device_type, output_dir)
    elif container_type == "lxc":
        return generate_lxc_config(device_type, output_dir)
    else:
        print(f"Error: Unknown container type: {container_type}")
        return False

def generate_all_configs(device_type: str, container_type: str, output_dir: str) -> bool:
    """Generate all configuration files"""
    # Create output directory
    if not create_output_directory(output_dir):
        return False
    
    # Generate Flask configuration
    if not generate_flask_config(device_type, output_dir):
        return False
    
    # Generate dnsmasq configuration
    if not generate_dnsmasq_config(device_type, output_dir):
        return False
    
    # Generate systemd service
    if not generate_systemd_service(device_type, output_dir):
        return False
    
    # Generate container configuration if container type is not "none"
    if container_type != "none":
        if not generate_container_config(container_type, device_type, output_dir):
            return False
    
    return True

def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate PiDNS configuration files')
    parser.add_argument('--device', type=str, required=True,
                        choices=['pi-zero', 'pi-zero-2w', 'pi-3', 'pi-4', 'pi-5', 'low-resource-pc', 'standard-pc'],
                        help='Device type')
    parser.add_argument('--container', type=str, default='none',
                        choices=['docker', 'podman', 'lxc', 'none'],
                        help='Container type')
    parser.add_argument('--output', type=str, default='./config',
                        help='Output directory')
    
    args = parser.parse_args()
    
    # Generate all configuration files
    if generate_all_configs(args.device, args.container, args.output):
        print(f"Successfully generated configuration files for {args.device} with {args.container} container")
        return 0
    else:
        print(f"Failed to generate configuration files for {args.device} with {args.container} container")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

## 8. Template Validation Script

### Template Validation Script
```python
# scripts/validate_config.py
#!/usr/bin/env python3
"""
Configuration validation script for PiDNS
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def validate_flask_config(config_file: str) -> bool:
    """Validate Flask configuration file"""
    print(f"Validating Flask configuration: {config_file}")
    
    # Check if file exists
    if not os.path.exists(config_file):
        print(f"Error: Configuration file does not exist: {config_file}")
        return False
    
    # Check Python syntax
    try:
        with open(config_file, 'r') as f:
            code = f.read()
        compile(code, config_file, 'exec')
    except SyntaxError as e:
        print(f"Error: Syntax error in configuration file: {e}")
        return False
    
    print("Flask configuration is valid")
    return True

def validate_dnsmasq_config(config_file: str) -> bool:
    """Validate dnsmasq configuration file"""
    print(f"Validating dnsmasq configuration: {config_file}")
    
    # Check if file exists
    if not os.path.exists(config_file):
        print(f"Error: Configuration file does not exist: {config_file}")
        return False
    
    # Check dnsmasq configuration syntax
    try:
        result = subprocess.run(['dnsmasq', '--test', '-C', config_file], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: dnsmasq configuration is invalid: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: dnsmasq is not installed")
        return False
    
    print("dnsmasq configuration is valid")
    return True

def validate_systemd_service(service_file: str) -> bool:
    """Validate systemd service file"""
    print(f"Validating systemd service: {service_file}")
    
    # Check if file exists
    if not os.path.exists(service_file):
        print(f"Error: Service file does not exist: {service_file}")
        return False
    
    # Check systemd service syntax
    try:
        result = subprocess.run(['systemd-analyze', 'verify', service_file], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: systemd service is invalid: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: systemd is not available")
        return False
    
    print("systemd service is valid")
    return True

def validate_docker_compose(compose_file: str) -> bool:
    """Validate Docker Compose file"""
    print(f"Validating Docker Compose file: {compose_file}")
    
    # Check if file exists
    if not os.path.exists(compose_file):
        print(f"Error: Docker Compose file does not exist: {compose_file}")
        return False
    
    # Check Docker Compose syntax
    try:
        result = subprocess.run(['docker-compose', '-f', compose_file, 'config'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: Docker Compose file is invalid: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: docker-compose is not installed")
        return False
    
    print("Docker Compose file is valid")
    return True

def validate_podman_compose(compose_file: str) -> bool:
    """Validate Podman Compose file"""
    print(f"Validating Podman Compose file: {compose_file}")
    
    # Check if file exists
    if not os.path.exists(compose_file):
        print(f"Error: Podman Compose file does not exist: {compose_file}")
        return False
    
    # Check Podman Compose syntax
    try:
        result = subprocess.run(['podman-compose', '-f', compose_file, 'config'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: Podman Compose file is invalid: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: podman-compose is not installed")
        return False
    
    print("Podman Compose file is valid")
    return True

def validate_lxc_config(config_file: str) -> bool:
    """Validate LXC configuration file"""
    print(f"Validating LXC configuration: {config_file}")
    
    # Check if file exists
    if not os.path.exists(config_file):
        print(f"Error: LXC configuration file does not exist: {config_file}")
        return False
    
    # Check LXC configuration syntax
    try:
        result = subprocess.run(['lxc-checkconfig', config_file], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: LXC configuration is invalid: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: lxc-checkconfig is not installed")
        return False
    
    print("LXC configuration is valid")
    return True

def validate_container_config(container_type: str, config_file: str) -> bool:
    """Validate container configuration file"""
    if container_type == "docker":
        return validate_docker_compose(config_file)
    elif container_type == "podman":
        return validate_podman_compose(config_file)
    elif container_type == "lxc":
        return validate_lxc_config(config_file)
    else:
        print(f"Error: Unknown container type: {container_type}")
        return False

def validate_all_configs(device_type: str, container_type: str, config_dir: str) -> bool:
    """Validate all configuration files"""
    # Validate Flask configuration
    flask_config = os.path.join(config_dir, f"flask_config.{device_type}.py")
    if not validate_flask_config(flask_config):
        return False
    
    # Validate dnsmasq configuration
    dnsmasq_config = os.path.join(config_dir, f"dnsmasq.{device_type}.conf")
    if not validate_dnsmasq_config(dnsmasq_config):
        return False
    
    # Validate systemd service
    systemd_service = os.path.join(config_dir, f"pidns.{device_type}.service")
    if not validate_systemd_service(systemd_service):
        return False
    
    # Validate container configuration if container type is not "none"
    if container_type != "none":
        if container_type == "docker":
            container_config = os.path.join(config_dir, "docker-compose.yml")
            if not validate_container_config(container_type, container_config):
                return False
            
            container_override = os.path.join(config_dir, f"docker-compose.override.{device_type}.yml")
            if not validate_container_config(container_type, container_override):
                return False
        elif container_type == "podman":
            container_config = os.path.join(config_dir, "podman-compose.yml")
            if not validate_container_config(container_type, container_config):
                return False
            
            container_override = os.path.join(config_dir, f"podman-compose.override.{device_type}.yml")
            if not validate_container_config(container_type, container_override):
                return False
        elif container_type == "lxc":
            container_config = os.path.join(config_dir, f"lxc.{device_type}.conf")
            if not validate_container_config(container_type, container_config):
                return False
    
    return True

def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Validate PiDNS configuration files')
    parser.add_argument('--device', type=str, required=True,
                        choices=['pi-zero', 'pi-zero-2w', 'pi-3', 'pi-4', 'pi-5', 'low-resource-pc', 'standard-pc'],
                        help='Device type')
    parser.add_argument('--container', type=str, default='none',
                        choices=['docker', 'podman', 'lxc', 'none'],
                        help='Container type')
    parser.add_argument('--config', type=str, default='./config',
                        help='Configuration directory')
    
    args = parser.parse_args()
    
    # Validate all configuration files
    if validate_all_configs(args.device, args.container, args.config):
        print(f"All configuration files for {args.device} with {args.container} container are valid")
        return 0
    else:
        print(f"Some configuration files for {args.device} with {args.container} container are invalid")
        return 1

if __name__ == '__main__':
    sys.exit(main())
# PiDNS Device-Specific Optimization Settings Plan

## 1. Device Optimization Overview

### Optimization Goals
1. **Resource Efficiency**: Optimize for limited RAM and CPU resources
2. **Performance**: Ensure responsive dashboard and DNS resolution
3. **Stability**: Prevent crashes and memory exhaustion
4. **Power Efficiency**: Reduce power consumption where possible

### Device Categories
1. **Raspberry Pi Zero W**: 512MB RAM, 1-core CPU
2. **Raspberry Pi Zero 2W**: 512MB RAM, 1-core CPU
3. **Raspberry Pi 3**: 1GB RAM, 4-core CPU
4. **Raspberry Pi 4**: 2-8GB RAM, 4-core CPU
5. **Raspberry Pi 5**: 4-8GB RAM, 4-core CPU
6. **Low-Resource PC**: ≤1GB RAM, ≤2 cores
7. **Standard PC**: >1GB RAM, >2 cores

## 2. System-Level Optimizations

### Kernel Parameter Optimizations

#### Raspberry Pi Zero W / Zero 2W
```bash
# sysctl optimizations for Pi Zero
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_ratio=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_background_ratio=5' | sudo tee -a /etc/sysctl.conf

# Network optimizations
echo 'net.core.rmem_max=4194304' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max=4194304' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem=4096 65536 4194304' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem=4096 65536 4194304' | sudo tee -a /etc/sysctl.conf
echo 'net.core.netdev_max_backlog=1000' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf

# Apply settings
sudo sysctl -p
```

#### Raspberry Pi 3
```bash
# sysctl optimizations for Pi 3
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_ratio=15' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_background_ratio=10' | sudo tee -a /etc/sysctl.conf

# Network optimizations
echo 'net.core.rmem_max=8388608' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max=8388608' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem=4096 87380 8388608' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem=4096 65536 8388608' | sudo tee -a /etc/sysctl.conf
echo 'net.core.netdev_max_backlog=2000' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf

# Apply settings
sudo sysctl -p
```

#### Raspberry Pi 4/5
```bash
# sysctl optimizations for Pi 4/5
echo 'vm.swappiness=5' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_ratio=20' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_background_ratio=15' | sudo tee -a /etc/sysctl.conf

# Network optimizations
echo 'net.core.rmem_max=16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max=16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem=4096 87380 16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem=4096 65536 16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.core.netdev_max_backlog=5000' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf

# Apply settings
sudo sysctl -p
```

#### Low-Resource PC
```bash
# sysctl optimizations for Low-Resource PC
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_ratio=15' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_background_ratio=10' | sudo tee -a /etc/sysctl.conf

# Network optimizations
echo 'net.core.rmem_max=8388608' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max=8388608' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem=4096 87380 8388608' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem=4096 65536 8388608' | sudo tee -a /etc/sysctl.conf
echo 'net.core.netdev_max_backlog=2000' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf

# Apply settings
sudo sysctl -p
```

#### Standard PC
```bash
# sysctl optimizations for Standard PC
echo 'vm.swappiness=1' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_ratio=20' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_background_ratio=15' | sudo tee -a /etc/sysctl.conf

# Network optimizations
echo 'net.core.rmem_max=16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max=16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem=4096 87380 16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem=4096 65536 16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.core.netdev_max_backlog=10000' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf

# Apply settings
sudo sysctl -p
```

### Swap Configuration

#### Raspberry Pi Zero W / Zero 2W
```bash
# Create and configure swap file for Pi Zero
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Configure swap usage
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

#### Raspberry Pi 3
```bash
# Create and configure swap file for Pi 3
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Configure swap usage
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

#### Raspberry Pi 4/5
```bash
# Create and configure swap file for Pi 4/5
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Configure swap usage
echo 'vm.swappiness=5' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

#### Low-Resource PC
```bash
# Create and configure swap file for Low-Resource PC
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Configure swap usage
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

#### Standard PC
```bash
# Create and configure swap file for Standard PC
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Configure swap usage
echo 'vm.swappiness=1' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 3. dnsmasq Optimizations

### Raspberry Pi Zero W / Zero 2W
```conf
# dnsmasq optimizations for Pi Zero
# Cache settings
cache-size=100
dns-forward-max=100
min-port=4096
max-port=65535

# TTL settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=100

# Logging (minimal for resource constraints)
# log-queries  # Commented out to save resources
# log-dhcp     # Commented out to save resources

# Connection settings
max-connections=50
max-dns-connections=50
```

### Raspberry Pi 3
```conf
# dnsmasq optimizations for Pi 3
# Cache settings
cache-size=200
dns-forward-max=200
min-port=4096
max-port=65535

# TTL settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=200

# Logging (moderate for Pi 3)
log-queries
log-dhcp

# Connection settings
max-connections=100
max-dns-connections=100
```

### Raspberry Pi 4/5
```conf
# dnsmasq optimizations for Pi 4/5
# Cache settings
cache-size=500
dns-forward-max=500
min-port=4096
max-port=65535

# TTL settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=500

# Logging (full for Pi 4/5)
log-queries
log-dhcp
log-async=50  # Async logging for better performance

# Connection settings
max-connections=200
max-dns-connections=200

# Additional features for Pi 4/5
dhcp-rapid-commit
dhcp-option=option:ntp-server,0.0.0.0
```

### Low-Resource PC
```conf
# dnsmasq optimizations for Low-Resource PC
# Cache settings
cache-size=300
dns-forward-max=300
min-port=4096
max-port=65535

# TTL settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=300

# Logging (minimal for resource constraints)
# log-queries  # Commented out to save resources
# log-dhcp     # Commented out to save resources

# Connection settings
max-connections=150
max-dns-connections=150
```

### Standard PC
```conf
# dnsmasq optimizations for Standard PC
# Cache settings
cache-size=1000
dns-forward-max=1000
min-port=4096
max-port=65535

# TTL settings
local-ttl=1
neg-ttl=900
max-ttl=86400
min-cache-ttl=3600

# Resource optimization settings
max-cache-ttl=86400
min-cache-ttl=3600
cache-lim=1000

# Logging (full for Standard PC)
log-queries
log-dhcp
log-async=100  # Async logging for better performance

# Connection settings
max-connections=500
max-dns-connections=500

# Additional features for Standard PC
dhcp-rapid-commit
dhcp-option=option:ntp-server,0.0.0.0
dhcp-option=option:domain-search,local
```

## 4. Flask Application Optimizations

### Raspberry Pi Zero W / Zero 2W
```python
"""
Flask configuration for PiDNS dashboard on Raspberry Pi Zero W/2W
Optimized for minimal resources (512MB RAM, 1-core CPU)
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration optimized for Pi Zero W/2W"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings - reduced timeouts for resource constraints
    HOST = '0.0.0.0'
    PORT = 8080
    
    # Performance optimizations
    THREADS_PER_PAGE = 1  # Single thread for minimal resource usage
    PROCESSES = 1         # Single process
    
    # Request/response optimizations
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max content length
    SEND_FILE_MAX_AGE_DEFAULT = 60  # 1 minute cache for static files
    TEMPLATES_AUTO_RELOAD = False  # Disable template auto-reload
    
    # Session optimizations
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    SESSION_COOKIE_SECURE = False  # Disable for simplicity (enable with HTTPS)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # DNS and DHCP settings
    DNSMASQ_LEASE_FILE = '/var/lib/misc/dnsmasq.leases'
    DNSMASQ_CONFIG_FILE = '/etc/dnsmasq.conf'
    
    # MAC vendor database
    MAC_VENDORS_FILE = BASE_DIR / 'data' / 'mac-vendors.json'
    
    # Dashboard settings - reduced refresh rate for resource constraints
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Zero W)'
    REFRESH_INTERVAL = 60  # seconds (increased from 30 to reduce CPU usage)
    
    # Authentication
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME') or 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD') or 'password'
    
    # Memory optimization settings
    MAX_DEVICES = 50  # Limit number of devices displayed
    LOG_LEVEL = 'WARNING'  # Reduce logging overhead
    
    # Caching optimizations
    CACHE_TYPE = 'simple'  # Simple in-memory cache
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Database optimizations (for ad-blocker)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'data' / 'adblocker' / 'adblocker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600
    }
```

### Raspberry Pi 3
```python
"""
Flask configuration for PiDNS dashboard on Raspberry Pi 3
Optimized for moderate resources (1GB RAM, 4-core CPU)
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration optimized for Pi 3"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings
    HOST = '0.0.0.0'
    PORT = 8080
    
    # Performance optimizations
    THREADS_PER_PAGE = 2  # Moderate threading for Pi 3
    PROCESSES = 1         # Single process
    
    # Request/response optimizations
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB max content length
    SEND_FILE_MAX_AGE_DEFAULT = 60  # 1 minute cache for static files
    TEMPLATES_AUTO_RELOAD = False  # Disable template auto-reload
    
    # Session optimizations
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_COOKIE_SECURE = False  # Disable for simplicity (enable with HTTPS)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # DNS and DHCP settings
    DNSMASQ_LEASE_FILE = '/var/lib/misc/dnsmasq.leases'
    DNSMASQ_CONFIG_FILE = '/etc/dnsmasq.conf'
    
    # MAC vendor database
    MAC_VENDORS_FILE = BASE_DIR / 'data' / 'mac-vendors.json'
    
    # Dashboard settings
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Pi 3)'
    REFRESH_INTERVAL = 30  # seconds
    
    # Authentication
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME') or 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD') or 'password'
    
    # Memory optimization settings
    MAX_DEVICES = 100  # Moderate device limit
    LOG_LEVEL = 'INFO'  # Standard logging level
    
    # Caching optimizations
    CACHE_TYPE = 'simple'  # Simple in-memory cache
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Database optimizations (for ad-blocker)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'data' / 'adblocker' / 'adblocker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 3600
    }
```

### Raspberry Pi 4/5
```python
"""
Flask configuration for PiDNS dashboard on Raspberry Pi 4/5
Optimized for higher resources (2-8GB RAM, 4-core CPU)
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration optimized for Pi 4/5"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings
    HOST = '0.0.0.0'
    PORT = 8080
    
    # Performance optimizations
    THREADS_PER_PAGE = 4  # More threading for Pi 4/5
    PROCESSES = 1         # Single process
    
    # Request/response optimizations
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024  # 64MB max content length
    SEND_FILE_MAX_AGE_DEFAULT = 60  # 1 minute cache for static files
    TEMPLATES_AUTO_RELOAD = False  # Disable template auto-reload
    
    # Session optimizations
    PERMANENT_SESSION_LIFETIME = 7200  # 2 hours
    SESSION_COOKIE_SECURE = False  # Disable for simplicity (enable with HTTPS)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # DNS and DHCP settings
    DNSMASQ_LEASE_FILE = '/var/lib/misc/dnsmasq.leases'
    DNSMASQ_CONFIG_FILE = '/etc/dnsmasq.conf'
    
    # MAC vendor database
    MAC_VENDORS_FILE = BASE_DIR / 'data' / 'mac-vendors.json'
    
    # Dashboard settings
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Pi 4/5)'
    REFRESH_INTERVAL = 15  # seconds (faster refresh for better UX)
    
    # Authentication
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME') or 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD') or 'password'
    
    # Memory optimization settings
    MAX_DEVICES = 250  # Higher device limit
    LOG_LEVEL = 'DEBUG'  # Full logging for debugging
    
    # Caching optimizations
    CACHE_TYPE = 'simple'  # Simple in-memory cache
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Database optimizations (for ad-blocker)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'data' / 'adblocker' / 'adblocker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 40,
        'pool_timeout': 30,
        'pool_recycle': 3600
    }
```

### Low-Resource PC
```python
"""
Flask configuration for PiDNS dashboard on Low-Resource PC
Optimized for minimal resources (≤1GB RAM, ≤2 cores)
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration optimized for Low-Resource PC"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings - reduced timeouts for resource constraints
    HOST = '0.0.0.0'
    PORT = 8080
    
    # Performance optimizations
    THREADS_PER_PAGE = 2  # Limited threading for resource constraints
    PROCESSES = 1         # Single process
    
    # Request/response optimizations
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB max content length
    SEND_FILE_MAX_AGE_DEFAULT = 60  # 1 minute cache for static files
    TEMPLATES_AUTO_RELOAD = False  # Disable template auto-reload
    
    # Session optimizations
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_COOKIE_SECURE = False  # Disable for simplicity (enable with HTTPS)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # DNS and DHCP settings
    DNSMASQ_LEASE_FILE = '/var/lib/misc/dnsmasq.leases'
    DNSMASQ_CONFIG_FILE = '/etc/dnsmasq.conf'
    
    # MAC vendor database
    MAC_VENDORS_FILE = BASE_DIR / 'data' / 'mac-vendors.json'
    
    # Dashboard settings - reduced refresh rate for resource constraints
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Low-Resource PC)'
    REFRESH_INTERVAL = 45  # seconds (increased to reduce CPU usage)
    
    # Authentication
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME') or 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD') or 'password'
    
    # Memory optimization settings
    MAX_DEVICES = 75  # Limited device count for resource constraints
    LOG_LEVEL = 'WARNING'  # Reduced logging to save resources
    
    # Caching optimizations
    CACHE_TYPE = 'simple'  # Simple in-memory cache
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Database optimizations (for ad-blocker)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'data' / 'adblocker' / 'adblocker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600
    }
```

### Standard PC
```python
"""
Flask configuration for PiDNS dashboard on Standard PC
Optimized for standard resources (>1GB RAM, >2 cores)
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration optimized for Standard PC"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings
    HOST = '0.0.0.0'
    PORT = 8080
    
    # Performance optimizations
    THREADS_PER_PAGE = 4  # Standard threading for PC
    PROCESSES = 1         # Single process
    
    # Request/response optimizations
    MAX_CONTENT_LENGTH = 128 * 1024 * 1024  # 128MB max content length
    SEND_FILE_MAX_AGE_DEFAULT = 60  # 1 minute cache for static files
    TEMPLATES_AUTO_RELOAD = False  # Disable template auto-reload
    
    # Session optimizations
    PERMANENT_SESSION_LIFETIME = 7200  # 2 hours
    SESSION_COOKIE_SECURE = False  # Disable for simplicity (enable with HTTPS)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # DNS and DHCP settings
    DNSMASQ_LEASE_FILE = '/var/lib/misc/dnsmasq.leases'
    DNSMASQ_CONFIG_FILE = '/etc/dnsmasq.conf'
    
    # MAC vendor database
    MAC_VENDORS_FILE = BASE_DIR / 'data' / 'mac-vendors.json'
    
    # Dashboard settings
    DASHBOARD_TITLE = 'PiDNS Network Dashboard (Standard PC)'
    REFRESH_INTERVAL = 10  # seconds (fast refresh for better UX)
    
    # Authentication
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME') or 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD') or 'password'
    
    # Memory optimization settings
    MAX_DEVICES = 500  # High device limit for PC
    LOG_LEVEL = 'DEBUG'  # Full logging for debugging
    
    # Caching optimizations
    CACHE_TYPE = 'simple'  # Simple in-memory cache
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Database optimizations (for ad-blocker)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'data' / 'adblocker' / 'adblocker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 40,
        'pool_timeout': 30,
        'pool_recycle': 3600
    }
```

## 5. Systemd Service Optimizations

### Raspberry Pi Zero W / Zero 2W
```ini
# pidns.service for Pi Zero W/2W
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

# Resource limits for Pi Zero W/2W
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
```

### Raspberry Pi 3
```ini
# pidns.service for Pi 3
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
```

### Raspberry Pi 4/5
```ini
# pidns.service for Pi 4/5
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
```

### Low-Resource PC
```ini
# pidns.service for Low-Resource PC
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
```

### Standard PC
```ini
# pidns.service for Standard PC
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
```

## 6. Ad-Blocker Service Optimizations

### Raspberry Pi Zero W / Zero 2W
```ini
# adblocker.service for Pi Zero W/2W
[Unit]
Description=PiDNS Ad-Blocker Service
After=network.target dnsmasq.service pidns.service
Wants=network.target dnsmasq.service pidns.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/adblocker/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Pi Zero W/2W
MemoryLimit=128M
CPUQuota=50%
TasksMax=50
LimitNOFILE=1024

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /home/pi/PiDNS/data/adblocker /var/log/pidns-adblocker

[Install]
WantedBy=multi-user.target
```

### Raspberry Pi 3
```ini
# adblocker.service for Pi 3
[Unit]
Description=PiDNS Ad-Blocker Service
After=network.target dnsmasq.service pidns.service
Wants=network.target dnsmasq.service pidns.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/adblocker/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Pi 3
MemoryLimit=256M
CPUQuota=75%
TasksMax=100
LimitNOFILE=2048

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /home/pi/PiDNS/data/adblocker /var/log/pidns-adblocker

[Install]
WantedBy=multi-user.target
```

### Raspberry Pi 4/5
```ini
# adblocker.service for Pi 4/5
[Unit]
Description=PiDNS Ad-Blocker Service
After=network.target dnsmasq.service pidns.service
Wants=network.target dnsmasq.service pidns.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/adblocker/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Pi 4/5
MemoryLimit=512M
CPUQuota=100%
TasksMax=200
LimitNOFILE=4096

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /home/pi/PiDNS/data/adblocker /var/log/pidns-adblocker

[Install]
WantedBy=multi-user.target
```

### Low-Resource PC
```ini
# adblocker.service for Low-Resource PC
[Unit]
Description=PiDNS Ad-Blocker Service
After=network.target dnsmasq.service pidns.service
Wants=network.target dnsmasq.service pidns.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/adblocker/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Low-Resource PC
MemoryLimit=256M
CPUQuota=75%
TasksMax=100
LimitNOFILE=2048

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /home/pi/PiDNS/data/adblocker /var/log/pidns-adblocker

[Install]
WantedBy=multi-user.target
```

### Standard PC
```ini
# adblocker.service for Standard PC
[Unit]
Description=PiDNS Ad-Blocker Service
After=network.target dnsmasq.service pidns.service
Wants=network.target dnsmasq.service pidns.service

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/PiDNS
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/home/pi/PiDNS
ExecStart=/usr/bin/python3 /home/pi/PiDNS/adblocker/app.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits for Standard PC
MemoryLimit=1024M
CPUQuota=100%
TasksMax=500
LimitNOFILE=8192

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/pi/PiDNS/data /home/pi/PiDNS/data/adblocker /var/log/pidns-adblocker

[Install]
WantedBy=multi-user.target
```

## 7. Python Virtual Environment Optimizations

### Raspberry Pi Zero W / Zero 2W
```bash
# Create optimized Python virtual environment for Pi Zero W/2W
python3 -m venv --without-pip --system-site-packages venv

# Activate virtual environment
source venv/bin/activate

# Install pip with optimizations
curl -s https://bootstrap.pypa.io/get-pip.py | python - --no-setuptools --no-wheel

# Install setuptools and wheel with optimizations
pip install --no-cache-dir --no-compile --upgrade setuptools wheel

# Install requirements with optimizations
pip install --no-cache-dir --no-compile -r requirements.txt
pip install --no-cache-dir --no-compile -r requirements_adblocker.txt

# Pre-compile Python bytecode to reduce runtime overhead
python -m compileall -q .
python -m compileall -q -f .
```

### Raspberry Pi 3
```bash
# Create optimized Python virtual environment for Pi 3
python3 -m venv --without-pip --system-site-packages venv

# Activate virtual environment
source venv/bin/activate

# Install pip with optimizations
curl -s https://bootstrap.pypa.io/get-pip.py | python - --no-setuptools --no-wheel

# Install setuptools and wheel with optimizations
pip install --no-cache-dir --upgrade setuptools wheel

# Install requirements with optimizations
pip install --no-cache-dir -r requirements.txt
pip install --no-cache-dir -r requirements_adblocker.txt

# Pre-compile Python bytecode to reduce runtime overhead
python -m compileall -q .
python -m compileall -q -f .
```

### Raspberry Pi 4/5
```bash
# Create optimized Python virtual environment for Pi 4/5
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install pip with optimizations
curl -s https://bootstrap.pypa.io/get-pip.py | python - --no-setuptools --no-wheel

# Install setuptools and wheel with optimizations
pip install --upgrade setuptools wheel

# Install requirements with optimizations
pip install -r requirements.txt
pip install -r requirements_adblocker.txt

# Pre-compile Python bytecode to reduce runtime overhead
python -m compileall -q .
python -m compileall -q -f .
```

### Low-Resource PC
```bash
# Create optimized Python virtual environment for Low-Resource PC
python3 -m venv --without-pip --system-site-packages venv

# Activate virtual environment
source venv/bin/activate

# Install pip with optimizations
curl -s https://bootstrap.pypa.io/get-pip.py | python - --no-setuptools --no-wheel

# Install setuptools and wheel with optimizations
pip install --no-cache-dir --upgrade setuptools wheel

# Install requirements with optimizations
pip install --no-cache-dir -r requirements.txt
pip install --no-cache-dir -r requirements_adblocker.txt

# Pre-compile Python bytecode to reduce runtime overhead
python -m compileall -q .
python -m compileall -q -f .
```

### Standard PC
```bash
# Create optimized Python virtual environment for Standard PC
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install pip with optimizations
curl -s https://bootstrap.pypa.io/get-pip.py | python - --no-setuptools --no-wheel

# Install setuptools and wheel with optimizations
pip install --upgrade setuptools wheel

# Install requirements with optimizations
pip install -r requirements.txt
pip install -r requirements_adblocker.txt

# Pre-compile Python bytecode to reduce runtime overhead
python -m compileall -q .
python -m compileall -q -f .
```

## 8. Filesystem Optimizations

### Raspberry Pi Zero W / Zero 2W
```bash
# Filesystem optimizations for Pi Zero W/2W

# Disable atime updates to reduce disk I/O
sudo mount -o remount,noatime /

# Configure tmpfs for /tmp
echo 'tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=128M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/log
echo 'tmpfs /var/log tmpfs defaults,noatime,mode=1777,size=64M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/tmp
echo 'tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=64M 0 0' | sudo tee -a /etc/fstab

# Apply fstab changes
sudo mount -a

# Configure log rotation for PiDNS
sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 2
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 10M
}
EOF

# Configure log rotation for ad-blocker
sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
/var/log/pidns-adblocker/*.log {
    weekly
    rotate 2
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 10M
}
EOF
```

### Raspberry Pi 3
```bash
# Filesystem optimizations for Pi 3

# Disable atime updates to reduce disk I/O
sudo mount -o remount,noatime /

# Configure tmpfs for /tmp
echo 'tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=256M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/log
echo 'tmpfs /var/log tmpfs defaults,noatime,mode=1777,size=128M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/tmp
echo 'tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=128M 0 0' | sudo tee -a /etc/fstab

# Apply fstab changes
sudo mount -a

# Configure log rotation for PiDNS
sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 20M
}
EOF

# Configure log rotation for ad-blocker
sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
/var/log/pidns-adblocker/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 20M
}
EOF
```

### Raspberry Pi 4/5
```bash
# Filesystem optimizations for Pi 4/5

# Disable atime updates to reduce disk I/O
sudo mount -o remount,noatime /

# Configure tmpfs for /tmp
echo 'tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=512M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/log
echo 'tmpfs /var/log tmpfs defaults,noatime,mode=1777,size=256M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/tmp
echo 'tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=256M 0 0' | sudo tee -a /etc/fstab

# Apply fstab changes
sudo mount -a

# Configure log rotation for PiDNS
sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 8
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 50M
}
EOF

# Configure log rotation for ad-blocker
sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
/var/log/pidns-adblocker/*.log {
    weekly
    rotate 8
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 50M
}
EOF
```

### Low-Resource PC
```bash
# Filesystem optimizations for Low-Resource PC

# Disable atime updates to reduce disk I/O
sudo mount -o remount,noatime /

# Configure tmpfs for /tmp
echo 'tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=256M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/log
echo 'tmpfs /var/log tmpfs defaults,noatime,mode=1777,size=128M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/tmp
echo 'tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=128M 0 0' | sudo tee -a /etc/fstab

# Apply fstab changes
sudo mount -a

# Configure log rotation for PiDNS
sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 20M
}
EOF

# Configure log rotation for ad-blocker
sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
/var/log/pidns-adblocker/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 20M
}
EOF
```

### Standard PC
```bash
# Filesystem optimizations for Standard PC

# Disable atime updates to reduce disk I/O
sudo mount -o remount,noatime /

# Configure tmpfs for /tmp
echo 'tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=1024M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/log
echo 'tmpfs /var/log tmpfs defaults,noatime,mode=1777,size=512M 0 0' | sudo tee -a /etc/fstab

# Configure tmpfs for /var/tmp
echo 'tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=512M 0 0' | sudo tee -a /etc/fstab

# Apply fstab changes
sudo mount -a

# Configure log rotation for PiDNS
sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 12
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 100M
}
EOF

# Configure log rotation for ad-blocker
sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
/var/log/pidns-adblocker/*.log {
    weekly
    rotate 12
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 100M
}
EOF
```

## 9. Optimization Application Script

### Optimization Script
```bash
#!/bin/bash
# apply_optimizations.sh - Apply device-specific optimizations

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Function to apply kernel parameter optimizations
apply_kernel_optimizations() {
    print_step "Applying kernel parameter optimizations..."
    
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            # Pi Zero W/2W optimizations
            echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
            echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_ratio=10' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_background_ratio=5' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.rmem_max=4194304' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.wmem_max=4194304' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_rmem=4096 65536 4194304' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_wmem=4096 65536 4194304' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.netdev_max_backlog=1000' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf
            ;;
        "pi-3")
            # Pi 3 optimizations
            echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
            echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_ratio=15' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_background_ratio=10' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.rmem_max=8388608' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.wmem_max=8388608' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_rmem=4096 87380 8388608' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_wmem=4096 65536 8388608' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.netdev_max_backlog=2000' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf
            ;;
        "pi-4"|"pi-5")
            # Pi 4/5 optimizations
            echo 'vm.swappiness=5' | sudo tee -a /etc/sysctl.conf
            echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_ratio=20' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_background_ratio=15' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.rmem_max=16777216' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.wmem_max=16777216' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_rmem=4096 87380 16777216' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_wmem=4096 65536 16777216' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.netdev_max_backlog=5000' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf
            ;;
        "low-resource-pc")
            # Low-Resource PC optimizations
            echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
            echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_ratio=15' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_background_ratio=10' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.rmem_max=8388608' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.wmem_max=8388608' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_rmem=4096 87380 8388608' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_wmem=4096 65536 8388608' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.netdev_max_backlog=2000' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf
            ;;
        "standard-pc")
            # Standard PC optimizations
            echo 'vm.swappiness=1' | sudo tee -a /etc/sysctl.conf
            echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_ratio=20' | sudo tee -a /etc/sysctl.conf
            echo 'vm.dirty_background_ratio=15' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.rmem_max=16777216' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.wmem_max=16777216' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_rmem=4096 87380 16777216' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_wmem=4096 65536 16777216' | sudo tee -a /etc/sysctl.conf
            echo 'net.core.netdev_max_backlog=10000' | sudo tee -a /etc/sysctl.conf
            echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf
            ;;
    esac
    
    # Apply sysctl changes
    sudo sysctl -p
    
    print_status "Kernel parameter optimizations applied."
}

# Function to configure swap
configure_swap() {
    print_step "Configuring swap..."
    
    # Remove existing swap file if it exists
    if [ -f /swapfile ]; then
        sudo swapoff /swapfile
        sudo rm /swapfile
    fi
    
    # Remove swap entry from fstab if it exists
    sudo sed -i '/\/swapfile/d' /etc/fstab
    
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            # Create 1GB swap file for Pi Zero W/2W
            sudo fallocate -l 1G /swapfile
            sudo chmod 600 /swapfile
            sudo mkswap /swapfile
            sudo swapon /swapfile
            echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
            ;;
        "pi-3"|"low-resource-pc")
            # Create 2GB swap file for Pi 3/Low-Resource PC
            sudo fallocate -l 2G /swapfile
            sudo chmod 600 /swapfile
            sudo mkswap /swapfile
            sudo swapon /swapfile
            echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
            ;;
        "pi-4"|"pi-5"|"standard-pc")
            # Create 4GB swap file for Pi 4/5/Standard PC
            sudo fallocate -l 4G /swapfile
            sudo chmod 600 /swapfile
            sudo mkswap /swapfile
            sudo swapon /swapfile
            echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
            ;;
    esac
    
    print_status "Swap configured."
}

# Function to configure dnsmasq
configure_dnsmasq() {
    print_step "Configuring dnsmasq..."
    
    # Create device-specific dnsmasq configuration
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            # Pi Zero W/2W dnsmasq configuration
            sed "s/CACHE_SIZE/100/g; s/DNS_CACHE/100/g" config/dnsmasq.conf > /tmp/dnsmasq.conf
            ;;
        "pi-3")
            # Pi 3 dnsmasq configuration
            sed "s/CACHE_SIZE/200/g; s/DNS_CACHE/200/g" config/dnsmasq.conf > /tmp/dnsmasq.conf
            ;;
        "pi-4"|"pi-5")
            # Pi 4/5 dnsmasq configuration
            sed "s/CACHE_SIZE/500/g; s/DNS_CACHE/500/g" config/dnsmasq.conf > /tmp/dnsmasq.conf
            ;;
        "low-resource-pc")
            # Low-Resource PC dnsmasq configuration
            sed "s/CACHE_SIZE/300/g; s/DNS_CACHE/300/g" config/dnsmasq.conf > /tmp/dnsmasq.conf
            ;;
        "standard-pc")
            # Standard PC dnsmasq configuration
            sed "s/CACHE_SIZE/1000/g; s/DNS_CACHE/1000/g" config/dnsmasq.conf > /tmp/dnsmasq.conf
            ;;
    esac
    
    # Install configuration
    sudo cp /tmp/dnsmasq.conf /etc/dnsmasq.conf
    sudo systemctl restart dnsmasq
    
    print_status "dnsmasq configured."
}

# Function to configure systemd services
configure_systemd_services() {
    print_step "Configuring systemd services..."
    
    # Create device-specific systemd service files
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            # Pi Zero W/2W systemd service configuration
            sed 's/MemoryLimit=.*$/MemoryLimit=256M/' services/pidns.service > /tmp/pidns.service
            sed 's/CPUQuota=.*$/CPUQuota=50%/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            sed 's/TasksMax=.*$/TasksMax=50/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            sed 's/LimitNOFILE=.*$/LimitNOFILE=1024/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            
            sed 's/MemoryLimit=.*$/MemoryLimit=128M/' services/adblocker.service > /tmp/adblocker.service
            sed 's/CPUQuota=.*$/CPUQuota=50%/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            sed 's/TasksMax=.*$/TasksMax=50/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            sed 's/LimitNOFILE=.*$/LimitNOFILE=1024/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            ;;
        "pi-3"|"low-resource-pc")
            # Pi 3/Low-Resource PC systemd service configuration
            sed 's/MemoryLimit=.*$/MemoryLimit=512M/' services/pidns.service > /tmp/pidns.service
            sed 's/CPUQuota=.*$/CPUQuota=75%/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            sed 's/TasksMax=.*$/TasksMax=100/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            sed 's/LimitNOFILE=.*$/LimitNOFILE=2048/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            
            sed 's/MemoryLimit=.*$/MemoryLimit=256M/' services/adblocker.service > /tmp/adblocker.service
            sed 's/CPUQuota=.*$/CPUQuota=75%/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            sed 's/TasksMax=.*$/TasksMax=100/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            sed 's/LimitNOFILE=.*$/LimitNOFILE=2048/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            ;;
        "pi-4"|"pi-5")
            # Pi 4/5 systemd service configuration
            sed 's/MemoryLimit=.*$/MemoryLimit=1024M/' services/pidns.service > /tmp/pidns.service
            sed 's/CPUQuota=.*$/CPUQuota=100%/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            sed 's/TasksMax=.*$/TasksMax=200/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            sed 's/LimitNOFILE=.*$/LimitNOFILE=4096/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            
            sed 's/MemoryLimit=.*$/MemoryLimit=512M/' services/adblocker.service > /tmp/adblocker.service
            sed 's/CPUQuota=.*$/CPUQuota=100%/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            sed 's/TasksMax=.*$/TasksMax=200/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            sed 's/LimitNOFILE=.*$/LimitNOFILE=4096/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            ;;
        "standard-pc")
            # Standard PC systemd service configuration
            sed 's/MemoryLimit=.*$/MemoryLimit=2048M/' services/pidns.service > /tmp/pidns.service
            sed 's/CPUQuota=.*$/CPUQuota=100%/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            sed 's/TasksMax=.*$/TasksMax=500/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            sed 's/LimitNOFILE=.*$/LimitNOFILE=8192/' /tmp/pidns.service > /tmp/pidns.service.tmp && mv /tmp/pidns.service.tmp /tmp/pidns.service
            
            sed 's/MemoryLimit=.*$/MemoryLimit=1024M/' services/adblocker.service > /tmp/adblocker.service
            sed 's/CPUQuota=.*$/CPUQuota=100%/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            sed 's/TasksMax=.*$/TasksMax=500/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            sed 's/LimitNOFILE=.*$/LimitNOFILE=8192/' /tmp/adblocker.service > /tmp/adblocker.service.tmp && mv /tmp/adblocker.service.tmp /tmp/adblocker.service
            ;;
    esac
    
    # Install service files
    sudo cp /tmp/pidns.service /etc/systemd/system/
    sudo cp /tmp/adblocker.service /etc/systemd/system/
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Restart services
    sudo systemctl restart pidns.service
    sudo systemctl restart adblocker.service
    
    print_status "Systemd services configured."
}

# Function to configure filesystem
configure_filesystem() {
    print_step "Configuring filesystem..."
    
    # Disable atime updates to reduce disk I/O
    sudo mount -o remount,noatime /
    
    # Remove existing tmpfs entries from fstab
    sudo sed -i '/tmpfs \/tmp/d' /etc/fstab
    sudo sed -i '/tmpfs \/var\/log/d' /etc/fstab
    sudo sed -i '/tmpfs \/var\/tmp/d' /etc/fstab
    
    # Configure tmpfs based on device type
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            # Pi Zero W/2W tmpfs configuration
            echo 'tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=128M 0 0' | sudo tee -a /etc/fstab
            echo 'tmpfs /var/log tmpfs defaults,noatime,mode=1777,size=64M 0 0' | sudo tee -a /etc/fstab
            echo 'tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=64M 0 0' | sudo tee -a /etc/fstab
            
            # Configure log rotation for PiDNS
            sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 2
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 10M
}
EOF

            # Configure log rotation for ad-blocker
            sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
/var/log/pidns-adblocker/*.log {
    weekly
    rotate 2
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 10M
}
EOF
            ;;
        "pi-3"|"low-resource-pc")
            # Pi 3/Low-Resource PC tmpfs configuration
            echo 'tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=256M 0 0' | sudo tee -a /etc/fstab
            echo 'tmpfs /var/log tmpfs defaults,noatime,mode=1777,size=128M 0 0' | sudo tee -a /etc/fstab
            echo 'tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=128M 0 0' | sudo tee -a /etc/fstab
            
            # Configure log rotation for PiDNS
            sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 20M
}
EOF

            # Configure log rotation for ad-blocker
            sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
/var/log/pidns-adblocker/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 20M
}
EOF
            ;;
        "pi-4"|"pi-5")
            # Pi 4/5 tmpfs configuration
            echo 'tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=512M 0 0' | sudo tee -a /etc/fstab
            echo 'tmpfs /var/log tmpfs defaults,noatime,mode=1777,size=256M 0 0' | sudo tee -a /etc/fstab
            echo 'tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=256M 0 0' | sudo tee -a /etc/fstab
            
            # Configure log rotation for PiDNS
            sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 8
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 50M
}
EOF

            # Configure log rotation for ad-blocker
            sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
/var/log/pidns-adblocker/*.log {
    weekly
    rotate 8
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 50M
}
EOF
            ;;
        "standard-pc")
            # Standard PC tmpfs configuration
            echo 'tmpfs /tmp tmpfs defaults,noatime,mode=1777,size=1024M 0 0' | sudo tee -a /etc/fstab
            echo 'tmpfs /var/log tmpfs defaults,noatime,mode=1777,size=512M 0 0' | sudo tee -a /etc/fstab
            echo 'tmpfs /var/tmp tmpfs defaults,noatime,mode=1777,size=512M 0 0' | sudo tee -a /etc/fstab
            
            # Configure log rotation for PiDNS
            sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 12
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 100M
}
EOF

            # Configure log rotation for ad-blocker
            sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
/var/log/pidns-adblocker/*.log {
    weekly
    rotate 12
    compress
    delaycompress
    missingok
    notifempty
    create 644 pi pi
    size 100M
}
EOF
            ;;
    esac
    
    # Apply fstab changes
    sudo mount -a
    
    print_status "Filesystem configured."
}

# Function to configure Flask
configure_flask() {
    print_step "Configuring Flask..."
    
    # Create device-specific Flask configuration
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            # Pi Zero W/2W Flask configuration
            cp config/flask_config.pi-zero.py config/flask_config.py
            ;;
        "pi-3")
            # Pi 3 Flask configuration
            cp config/flask_config.pi-3.py config/flask_config.py
            ;;
        "pi-4"|"pi-5")
            # Pi 4/5 Flask configuration
            cp config/flask_config.pi-4-5.py config/flask_config.py
            ;;
        "low-resource-pc")
            # Low-Resource PC Flask configuration
            cp config/flask_config.low-resource-pc.py config/flask_config.py
            ;;
        "standard-pc")
            # Standard PC Flask configuration
            cp config/flask_config.standard-pc.py config/flask_config.py
            ;;
    esac
    
    print_status "Flask configured."
}

# Function to optimize Python virtual environment
optimize_python_venv() {
    print_step "Optimizing Python virtual environment..."
    
    # Remove existing virtual environment
    if [ -d "venv" ]; then
        rm -rf venv
    fi
    
    # Create optimized Python virtual environment based on device type
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w"|"low-resource-pc")
            # Pi Zero W/2W/Low-Resource PC Python virtual environment
            python3 -m venv --without-pip --system-site-packages venv
            ;;
        "pi-3"|"pi-4"|"pi-5"|"standard-pc")
            # Pi 3/4/5/Standard PC Python virtual environment
            python3 -m venv venv
            ;;
    esac
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install pip with optimizations
    curl -s https://bootstrap.pypa.io/get-pip.py | python - --no-setuptools --no-wheel
    
    # Install setuptools and wheel with optimizations
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w"|"low-resource-pc")
            # Pi Zero W/2W/Low-Resource PC pip optimizations
            pip install --no-cache-dir --no-compile --upgrade setuptools wheel
            pip install --no-cache-dir --no-compile -r requirements.txt
            pip install --no-cache-dir --no-compile -r requirements_adblocker.txt
            ;;
        "pi-3"|"pi-4"|"pi-5"|"standard-pc")
            # Pi 3/4/5/Standard PC pip optimizations
            pip install --no-cache-dir --upgrade setuptools wheel
            pip install --no-cache-dir -r requirements.txt
            pip install --no-cache-dir -r requirements_adblocker.txt
            ;;
    esac
    
    # Pre-compile Python bytecode to reduce runtime overhead
    python -m compileall -q .
    python -m compileall -q -f .
    
    print_status "Python virtual environment optimized."
}

# Main optimization function
main() {
    # Check if device type is provided
    if [ -z "$1" ]; then
        print_error "Device type not provided."
        echo "Usage: $0 <device_type>"
        echo "Supported device types: pi-zero, pi-zero-2w, pi-3, pi-4, pi-5, low-resource-pc, standard-pc"
        exit 1
    fi
    
    DEVICE_TYPE=$1
    
    print_status "Applying optimizations for $DEVICE_TYPE..."
    
    # Apply kernel parameter optimizations
    apply_kernel_optimizations
    
    # Configure swap
    configure_swap
    
    # Configure dnsmasq
    configure_dnsmasq
    
    # Configure systemd services
    configure_systemd_services
    
    # Configure filesystem
    configure_filesystem
    
    # Configure Flask
    configure_flask
    
    # Optimize Python virtual environment
    optimize_python_venv
    
    print_status "Optimizations applied successfully for $DEVICE_TYPE."
    print_warning "Please reboot your system for all optimizations to take effect."
}

# Run main function with device type parameter
main "$@"
```

## 10. Optimization Verification

### Verification Script
```bash
#!/bin/bash
# verify_optimizations.sh - Verify device-specific optimizations

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Function to verify kernel parameter optimizations
verify_kernel_optimizations() {
    print_step "Verifying kernel parameter optimizations..."
    
    local verification_passed=true
    
    # Check swappiness
    local swappiness=$(cat /proc/sys/vm/swappiness)
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w"|"pi-3"|"low-resource-pc")
            if [ "$swappiness" -ne 10 ]; then
                print_error "Incorrect swappiness: $swappiness (expected: 10)"
                verification_passed=false
            else
                print_status "Correct swappiness: $swappiness"
            fi
            ;;
        "pi-4"|"pi-5")
            if [ "$swappiness" -ne 5 ]; then
                print_error "Incorrect swappiness: $swappiness (expected: 5)"
                verification_passed=false
            else
                print_status "Correct swappiness: $swappiness"
            fi
            ;;
        "standard-pc")
            if [ "$swappiness" -ne 1 ]; then
                print_error "Incorrect swappiness: $swappiness (expected: 1)"
                verification_passed=false
            else
                print_status "Correct swappiness: $swappiness"
            fi
            ;;
    esac
    
    # Check network buffer sizes
    local rmem_max=$(cat /proc/sys/net/core/rmem_max)
    local wmem_max=$(cat /proc/sys/net/core/wmem_max)
    
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            if [ "$rmem_max" -ne 4194304 ]; then
                print_error "Incorrect rmem_max: $rmem_max (expected: 4194304)"
                verification_passed=false
            else
                print_status "Correct rmem_max: $rmem_max"
            fi
            
            if [ "$wmem_max" -ne 4194304 ]; then
                print_error "Incorrect wmem_max: $wmem_max (expected: 4194304)"
                verification_passed=false
            else
                print_status "Correct wmem_max: $wmem_max"
            fi
            ;;
        "pi-3"|"low-resource-pc")
            if [ "$rmem_max" -ne 8388608 ]; then
                print_error "Incorrect rmem_max: $rmem_max (expected: 8388608)"
                verification_passed=false
            else
                print_status "Correct rmem_max: $rmem_max"
            fi
            
            if [ "$wmem_max" -ne 8388608 ]; then
                print_error "Incorrect wmem_max: $wmem_max (expected: 8388608)"
                verification_passed=false
            else
                print_status "Correct wmem_max: $wmem_max"
            fi
            ;;
        "pi-4"|"pi-5"|"standard-pc")
            if [ "$rmem_max" -ne 16777216 ]; then
                print_error "Incorrect rmem_max: $rmem_max (expected: 16777216)"
                verification_passed=false
            else
                print_status "Correct rmem_max: $rmem_max"
            fi
            
            if [ "$wmem_max" -ne 16777216 ]; then
                print_error "Incorrect wmem_max: $wmem_max (expected: 16777216)"
                verification_passed=false
            else
                print_status "Correct wmem_max: $wmem_max"
            fi
            ;;
    esac
    
    # Print verification result
    if [ "$verification_passed" = true ]; then
        print_status "Kernel parameter optimizations verified."
        return 0
    else
        print_error "Kernel parameter optimizations verification failed."
        return 1
    fi
}

# Function to verify swap configuration
verify_swap_configuration() {
    print_step "Verifying swap configuration..."
    
    local verification_passed=true
    
    # Check if swap file exists
    if [ ! -f /swapfile ]; then
        print_error "Swap file does not exist."
        verification_passed=false
    else
        print_status "Swap file exists."
    fi
    
    # Check if swap is active
    if ! swapon --show=NAME | grep -q "^/swapfile$"; then
        print_error "Swap is not active."
        verification_passed=false
    else
        print_status "Swap is active."
    fi
    
    # Check swap size
    local swap_size=$(swapon --show=SIZE --bytes | grep "^/swapfile$" | awk '{print $2}')
    
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            if [ "$swap_size" -ne 1073741824 ]; then
                print_error "Incorrect swap size: $swap_size bytes (expected: 1073741824 bytes)"
                verification_passed=false
            else
                print_status "Correct swap size: $swap_size bytes"
            fi
            ;;
        "pi-3"|"low-resource-pc")
            if [ "$swap_size" -ne 2147483648 ]; then
                print_error "Incorrect swap size: $swap_size bytes (expected: 2147483648 bytes)"
                verification_passed=false
            else
                print_status "Correct swap size: $swap_size bytes"
            fi
            ;;
        "pi-4"|"pi-5"|"standard-pc")
            if [ "$swap_size" -ne 4294967296 ]; then
                print_error "Incorrect swap size: $swap_size bytes (expected: 4294967296 bytes)"
                verification_passed=false
            else
                print_status "Correct swap size: $swap_size bytes"
            fi
            ;;
    esac
    
    # Print verification result
    if [ "$verification_passed" = true ]; then
        print_status "Swap configuration verified."
        return 0
    else
        print_error "Swap configuration verification failed."
        return 1
    fi
}

# Function to verify dnsmasq configuration
verify_dnsmasq_configuration() {
    print_step "Verifying dnsmasq configuration..."
    
    local verification_passed=true
    
    # Check if dnsmasq is running
    if ! systemctl is-active --quiet dnsmasq; then
        print_error "dnsmasq is not running."
        verification_passed=false
    else
        print_status "dnsmasq is running."
    fi
    
    # Check dnsmasq configuration syntax
    if ! dnsmasq --test; then
        print_error "dnsmasq configuration syntax is invalid."
        verification_passed=false
    else
        print_status "dnsmasq configuration syntax is valid."
    fi
    
    # Check cache size
    local cache_size=$(grep "^cache-size=" /etc/dnsmasq.conf | cut -d'=' -f2)
    
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            if [ "$cache_size" -ne 100 ]; then
                print_error "Incorrect cache size: $cache_size (expected: 100)"
                verification_passed=false
            else
                print_status "Correct cache size: $cache_size"
            fi
            ;;
        "pi-3")
            if [ "$cache_size" -ne 200 ]; then
                print_error "Incorrect cache size: $cache_size (expected: 200)"
                verification_passed=false
            else
                print_status "Correct cache size: $cache_size"
            fi
            ;;
        "pi-4"|"pi-5")
            if [ "$cache_size" -ne 500 ]; then
                print_error "Incorrect cache size: $cache_size (expected: 500)"
                verification_passed=false
            else
                print_status "Correct cache size: $cache_size"
            fi
            ;;
        "low-resource-pc")
            if [ "$cache_size" -ne 300 ]; then
                print_error "Incorrect cache size: $cache_size (expected: 300)"
                verification_passed=false
            else
                print_status "Correct cache size: $cache_size"
            fi
            ;;
        "standard-pc")
            if [ "$cache_size" -ne 1000 ]; then
                print_error "Incorrect cache size: $cache_size (expected: 1000)"
                verification_passed=false
            else
                print_status "Correct cache size: $cache_size"
            fi
            ;;
    esac
    
    # Print verification result
    if [ "$verification_passed" = true ]; then
        print_status "dnsmasq configuration verified."
        return 0
    else
        print_error "dnsmasq configuration verification failed."
        return 1
    fi
}

# Function to verify systemd services
verify_systemd_services() {
    print_step "Verifying systemd services..."
    
    local verification_passed=true
    
    # Check if PiDNS service is running
    if ! systemctl is-active --quiet pidns.service; then
        print_error "PiDNS service is not running."
        verification_passed=false
    else
        print_status "PiDNS service is running."
    fi
    
    # Check if ad-blocker service is running
    if ! systemctl is-active --quiet adblocker.service; then
        print_error "Ad-blocker service is not running."
        verification_passed=false
    else
        print_status "Ad-blocker service is running."
    fi
    
    # Check PiDNS service resource limits
    local memory_limit=$(systemctl show pidns.service | grep MemoryLimit | cut -d'=' -f2)
    local cpu_quota=$(systemctl show pidns.service | grep CPUQuota | cut -d'=' -f2)
    
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            if [ "$memory_limit" != "268435456" ]; then
                print_error "Incorrect PiDNS memory limit: $memory_limit (expected: 268435456)"
                verification_passed=false
            else
                print_status "Correct PiDNS memory limit: $memory_limit"
            fi
            
            if [ "$cpu_quota" != "50%" ]; then
                print_error "Incorrect PiDNS CPU quota: $cpu_quota (expected: 50%)"
                verification_passed=false
            else
                print_status "Correct PiDNS CPU quota: $cpu_quota"
            fi
            ;;
        "pi-3"|"low-resource-pc")
            if [ "$memory_limit" != "536870912" ]; then
                print_error "Incorrect PiDNS memory limit: $memory_limit (expected: 536870912)"
                verification_passed=false
            else
                print_status "Correct PiDNS memory limit: $memory_limit"
            fi
            
            if [ "$cpu_quota" != "75%" ]; then
                print_error "Incorrect PiDNS CPU quota: $cpu_quota (expected: 75%)"
                verification_passed=false
            else
                print_status "Correct PiDNS CPU quota: $cpu_quota"
            fi
            ;;
        "pi-4"|"pi-5")
            if [ "$memory_limit" != "1073741824" ]; then
                print_error "Incorrect PiDNS memory limit: $memory_limit (expected: 1073741824)"
                verification_passed=false
            else
                print_status "Correct PiDNS memory limit: $memory_limit"
            fi
            
            if [ "$cpu_quota" != "100%" ]; then
                print_error "Incorrect PiDNS CPU quota: $cpu_quota (expected: 100%)"
                verification_passed=false
            else
                print_status "Correct PiDNS CPU quota: $cpu_quota"
            fi
            ;;
        "standard-pc")
            if [ "$memory_limit" != "2147483648" ]; then
                print_error "Incorrect PiDNS memory limit: $memory_limit (expected: 2147483648)"
                verification_passed=false
            else
                print_status "Correct PiDNS memory limit: $memory_limit"
            fi
            
            if [ "$cpu_quota" != "100%" ]; then
                print_error "Incorrect PiDNS CPU quota: $cpu_quota (expected: 100%)"
                verification_passed=false
            else
                print_status "Correct PiDNS CPU quota: $cpu_quota"
            fi
            ;;
    esac
    
    # Print verification result
    if [ "$verification_passed" = true ]; then
        print_status "Systemd services verified."
        return 0
    else
        print_error "Systemd services verification failed."
        return 1
    fi
}

# Function to verify filesystem configuration
verify_filesystem_configuration() {
    print_step "Verifying filesystem configuration..."
    
    local verification_passed=true
    
    # Check if root filesystem is mounted with noatime
    if ! mount | grep " on / " | grep -q noatime; then
        print_error "Root filesystem is not mounted with noatime."
        verification_passed=false
    else
        print_status "Root filesystem is mounted with noatime."
    fi
    
    # Check if tmpfs is configured for /tmp
    if ! mount | grep " on /tmp " | grep -q tmpfs; then
        print_error "tmpfs is not configured for /tmp."
        verification_passed=false
    else
        print_status "tmpfs is configured for /tmp."
    fi
    
    # Check if tmpfs is configured for /var/log
    if ! mount | grep " on /var/log " | grep -q tmpfs; then
        print_error "tmpfs is not configured for /var/log."
        verification_passed=false
    else
        print_status "tmpfs is configured for /var/log."
    fi
    
    # Check if logrotate is configured for PiDNS
    if [ ! -f /etc/logrotate.d/pidns ]; then
        print_error "logrotate is not configured for PiDNS."
        verification_passed=false
    else
        print_status "logrotate is configured for PiDNS."
    fi
    
    # Check if logrotate is configured for ad-blocker
    if [ ! -f /etc/logrotate.d/pidns-adblocker ]; then
        print_error "logrotate is not configured for ad-blocker."
        verification_passed=false
    else
        print_status "logrotate is configured for ad-blocker."
    fi
    
    # Print verification result
    if [ "$verification_passed" = true ]; then
        print_status "Filesystem configuration verified."
        return 0
    else
        print_error "Filesystem configuration verification failed."
        return 1
    fi
}

# Function to verify Flask configuration
verify_flask_configuration() {
    print_step "Verifying Flask configuration..."
    
    local verification_passed=true
    
    # Check if Flask configuration file exists
    if [ ! -f config/flask_config.py ]; then
        print_error "Flask configuration file does not exist."
        verification_passed=false
    else
        print_status "Flask configuration file exists."
    fi
    
    # Check Flask configuration syntax
    if ! python3 -m py_compile config/flask_config.py; then
        print_error "Flask configuration has syntax errors."
        verification_passed=false
    else
        print_status "Flask configuration syntax is valid."
    fi
    
    # Check if PiDNS service is running
    if ! systemctl is-active --quiet pidns.service; then
        print_error "PiDNS service is not running."
        verification_passed=false
    else
        print_status "PiDNS service is running."
    fi
    
    # Check if dashboard is accessible
    if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
        print_error "Main dashboard is not accessible."
        verification_passed=false
    else
        print_status "Main dashboard is accessible."
    fi
    
    # Print verification result
    if [ "$verification_passed" = true ]; then
        print_status "Flask configuration verified."
        return 0
    else
        print_error "Flask configuration verification failed."
        return 1
    fi
}

# Function to verify Python virtual environment
verify_python_venv() {
    print_step "Verifying Python virtual environment..."
    
    local verification_passed=true
    
    # Check if Python virtual environment exists
    if [ ! -d venv ]; then
        print_error "Python virtual environment does not exist."
        verification_passed=false
    else
        print_status "Python virtual environment exists."
    fi
    
    # Check if Python virtual environment is properly set up
    if [ ! -f venv/bin/python ]; then
        print_error "Python virtual environment is not properly set up."
        verification_passed=false
    else
        print_status "Python virtual environment is properly set up."
    fi
    
    # Check if required packages are installed
    source venv/bin/activate
    if ! python -c "import flask" 2>/dev/null; then
        print_error "Flask is not installed in virtual environment."
        verification_passed=false
    else
        print_status "Flask is installed in virtual environment."
    fi
    
    if ! python -c "import jinja2" 2>/dev/null; then
        print_error "Jinja2 is not installed in virtual environment."
        verification_passed=false
    else
        print_status "Jinja2 is installed in virtual environment."
    fi
    
    # Print verification result
    if [ "$verification_passed" = true ]; then
        print_status "Python virtual environment verified."
        return 0
    else
        print_error "Python virtual environment verification failed."
        return 1
    fi
}

# Main verification function
main() {
    # Check if device type is provided
    if [ -z "$1" ]; then
        print_error "Device type not provided."
        echo "Usage: $0 <device_type>"
        echo "Supported device types: pi-zero, pi-zero-2w, pi-3, pi-4, pi-5, low-resource-pc, standard-pc"
        exit 1
    fi
    
    DEVICE_TYPE=$1
    
    print_status "Verifying optimizations for $DEVICE_TYPE..."
    
    # Verify kernel parameter optimizations
    verify_kernel_optimizations
    local kernel_result=$?
    
    # Verify swap configuration
    verify_swap_configuration
    local swap_result=$?
    
    # Verify dnsmasq configuration
    verify_dnsmasq_configuration
    local dnsmasq_result=$?
    
    # Verify systemd services
    verify_systemd_services
    local systemd_result=$?
    
    # Verify filesystem configuration
    verify_filesystem_configuration
    local filesystem_result=$?
    
    # Verify Flask configuration
    verify_flask_configuration
    local flask_result=$?
    
    # Verify Python virtual environment
    verify_python_venv
    local python_result=$?
    
    # Print overall verification result
    if [ $kernel_result -eq 0 ] && [ $swap_result -eq 0 ] && [ $dnsmasq_result -eq 0 ] && [ $systemd_result -eq 0 ] && [ $filesystem_result -eq 0 ] && [ $flask_result -eq 0 ] && [ $python_result -eq 0 ]; then
        print_status "All optimizations verified successfully for $DEVICE_TYPE."
        return 0
    else
        print_error "Some optimizations verification failed for $DEVICE_TYPE."
        return 1
    fi
}

# Run main function with device type parameter
main "$@"
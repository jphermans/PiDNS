# PiDNS Configuration Templates Plan

## 1. Device-Specific Configuration Templates

### Raspberry Pi Zero W Configuration

#### dnsmasq.pi-zero.conf
```conf
# PiDNS dnsmasq configuration for Raspberry Pi Zero W
# Optimized for minimal resources (512MB RAM, 1-core CPU)

# Interface configuration
interface=wlan0
# Uncomment the line below if using Ethernet instead of WiFi
# interface=eth0

# DHCP server configuration - reduced range for limited resources
dhcp-range=192.168.1.100,192.168.1.150,255.255.255.0,24h
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

# Performance optimizations for Pi Zero W
cache-size=100
dns-forward-max=100
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
cache-lim=100
```

#### flask_config.pi-zero.py
```python
"""
Flask configuration for PiDNS dashboard on Raspberry Pi Zero W
Optimized for minimal resources (512MB RAM, 1-core CPU)
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration optimized for Pi Zero W"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings - reduced timeouts for resource constraints
    HOST = '0.0.0.0'
    PORT = 8080
    
    # Performance optimizations
    THREADS_PER_PAGE = 1  # Single thread for minimal resource usage
    PROCESSES = 1         # Single process

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
```

### Raspberry Pi 3 Configuration

#### dnsmasq.pi-3.conf
```conf
# PiDNS dnsmasq configuration for Raspberry Pi 3
# Optimized for moderate resources (1GB RAM, 4-core CPU)

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
```

#### flask_config.pi-3.py
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
```

### Raspberry Pi 4/5 Configuration

#### dnsmasq.pi-4-5.conf
```conf
# PiDNS dnsmasq configuration for Raspberry Pi 4/5
# Optimized for higher resources (2-8GB RAM, 4-core CPU)

# Interface configuration
interface=wlan0
# Uncomment the line below if using Ethernet instead of WiFi
# interface=eth0

# DHCP server configuration - expanded range for more devices
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
```

#### flask_config.pi-4-5.py
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
```

### Low-Resource PC Configuration

#### dnsmasq.low-resource-pc.conf
```conf
# PiDNS dnsmasq configuration for Low-Resource PC
# Optimized for minimal resources (≤1GB RAM, ≤2 cores)

# Interface configuration
interface=eth0
# Uncomment the line below if using WiFi instead of Ethernet
# interface=wlan0

# DHCP server configuration - reduced range for limited resources
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
```

#### flask_config.low-resource-pc.py
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
```

### Standard PC Configuration

#### dnsmasq.standard-pc.conf
```conf
# PiDNS dnsmasq configuration for Standard PC
# Optimized for standard resources (>1GB RAM, >2 cores)

# Interface configuration
interface=eth0
# Uncomment the line below if using WiFi instead of Ethernet
# interface=wlan0

# DHCP server configuration - expanded range for more devices
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
```

#### flask_config.standard-pc.py
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
```

## 2. Container-Specific Configuration Templates

### Docker Configuration

#### docker-compose.yml
```yaml
version: '3.8'

services:
  pidns:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: pidns
    restart: unless-stopped
    network_mode: host
    cap_add:
      - NET_ADMIN
    volumes:
      - ./config:/app/config:ro
      - ./data:/app/data
      - /var/lib/misc:/var/lib/misc:rw
      - /etc/dnsmasq.conf:/etc/dnsmasq.conf:rw
      - /var/log/pidns:/var/log/pidns:rw
    environment:
      - FLASK_ENV=production
      - PIDNS_USERNAME=admin
      - PIDNS_PASSWORD=${PIDNS_PASSWORD:-password}
      - DEVICE_TYPE=${DEVICE_TYPE:-standard-pc}
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
      - ./config/dnsmasq.${DEVICE_TYPE:-standard-pc}.conf:/etc/dnsmasq.conf:ro
      - /var/lib/misc:/var/lib/misc:rw
    command: --log-queries --log-dhcp
```

#### Dockerfile
```dockerfile
# Multi-stage build for optimized image size
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY requirements_adblocker.txt .
RUN pip install --user -r requirements_adblocker.txt

# Final stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    dnsmasq \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 pidns && \
    chown -R pidns:pidns /app
USER pidns

# Expose ports
EXPOSE 8080 8081 53 67/udp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Start command
CMD ["python3", "app/app.py"]
```

### Podman Configuration

#### podman-compose.yml
```yaml
version: '3.8'

services:
  pidns:
    build: 
      context: .
      dockerfile: Containerfile
    container_name: pidns
    restart: unless-stopped
    network_mode: host
    cap_add:
      - NET_ADMIN
    volumes:
      - ./config:/app/config:ro,z
      - ./data:/app/data:z
      - /var/lib/misc:/var/lib/misc:rw,z
      - /etc/dnsmasq.conf:/etc/dnsmasq.conf:rw,z
      - /var/log/pidns:/var/log/pidns:rw,z
    environment:
      - FLASK_ENV=production
      - PIDNS_USERNAME=admin
      - PIDNS_PASSWORD=${PIDNS_PASSWORD:-password}
      - DEVICE_TYPE=${DEVICE_TYPE:-standard-pc}
    userns: keep-id

  dnsmasq:
    image: andyshinn/dnsmasq:latest
    container_name: pidns-dnsmasq
    restart: unless-stopped
    network_mode: host
    cap_add:
      - NET_ADMIN
    volumes:
      - ./config/dnsmasq.${DEVICE_TYPE:-standard-pc}.conf:/etc/dnsmasq.conf:ro,z
      - /var/lib/misc:/var/lib/misc:rw,z
    command: --log-queries --log-dhcp
    userns: keep-id
```

#### Containerfile
```containerfile
# Podman Containerfile for PiDNS
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    dnsmasq \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY requirements_adblocker.txt .
RUN pip install --user -r requirements_adblocker.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 pidns && \
    chown -R pidns:pidns /app
USER pidns

# Expose ports
EXPOSE 8080 8081 53 67/udp

# Start command
CMD ["python3", "app/app.py"]
```

### LXC Configuration

#### lxc-config.conf
```conf
# LXC configuration for PiDNS container

# Container name
lxc.uts.name = pidns

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
lxc.start.order = 100

# Resource limits based on device type
# These will be adjusted during installation based on selected device type
lxc.cgroup.memory.limit_in_bytes = 512M
lxc.cgroup.memory.swappiness = 10
lxc.cgroup.cpu.shares = 256

# Capabilities
lxc.cap.drop = sys_admin sys_module sys_rawio

# Console settings
lxc.tty.max = 4
lxc.pts = 1024

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
```

#### lxc-setup.sh
```bash
#!/bin/bash
# LXC setup script for PiDNS

# Device type parameter
DEVICE_TYPE=${1:-standard-pc}

# Create container
lxc-create -n pidns -t download -- -d debian -r bullseye -a armhf

# Start container
lxc-start -n pidns -d

# Wait for container to start
sleep 10

# Copy PiDNS files into container
lxc-attach -n pidns -- mkdir -p /app
tar -cf - . | lxc-attach -n pidns -- tar -xf - -C /app

# Install dependencies in container
lxc-attach -n pidns -- apt-get update
lxc-attach -n pidns -- apt-get install -y python3 python3-pip dnsmasq curl wget
lxc-attach -n pidns -- pip3 install -r /app/requirements.txt
lxc-attach -n pidns -- pip3 install -r /app/requirements_adblocker.txt

# Configure dnsmasq based on device type
lxc-attach -n pidns -- cp /app/config/dnsmasq.$DEVICE_TYPE.conf /etc/dnsmasq.conf

# Create startup script
cat > /tmp/start-pidns.sh << 'EOF'
#!/bin/bash
cd /app
python3 app/app.py &
dnsmasq
EOF
lxc-file-push /tmp/start-pidns.sh pidns/usr/local/bin/start-pidns.sh
lxc-attach -n pidns -- chmod +x /usr/local/bin/start-pidns.sh

# Configure autostart
cat > /tmp/lxc-pidns.conf << EOF
lxc.start.auto = 1
lxc.start.delay = 5
lxc.start.order = 100
EOF
lxc-config -n pidns -s lxc.start.auto -v 1
lxc-config -n pidns -s lxc.start.delay -v 5

# Set resource limits based on device type
case $DEVICE_TYPE in
    "pi-zero"|"pi-zero-2w")
        lxc-config -n pidns -s lxc.cgroup.memory.limit_in_bytes -v 512M
        lxc-config -n pidns -s lxc.cgroup.memory.swappiness -v 10
        lxc-config -n pidns -s lxc.cgroup.cpu.shares -v 128
        ;;
    "pi-3")
        lxc-config -n pidns -s lxc.cgroup.memory.limit_in_bytes -v 1024M
        lxc-config -n pidns -s lxc.cgroup.memory.swappiness -v 10
        lxc-config -n pidns -s lxc.cgroup.cpu.shares -v 256
        ;;
    "pi-4"|"pi-5")
        lxc-config -n pidns -s lxc.cgroup.memory.limit_in_bytes -v 2048M
        lxc-config -n pidns -s lxc.cgroup.memory.swappiness -v 5
        lxc-config -n pidns -s lxc.cgroup.cpu.shares -v 512
        ;;
    "low-resource-pc")
        lxc-config -n pidns -s lxc.cgroup.memory.limit_in_bytes -v 1024M
        lxc-config -n pidns -s lxc.cgroup.memory.swappiness -v 10
        lxc-config -n pidns -s lxc.cgroup.cpu.shares -v 256
        ;;
    "standard-pc")
        lxc-config -n pidns -s lxc.cgroup.memory.limit_in_bytes -v 2048M
        lxc-config -n pidns -s lxc.cgroup.memory.swappiness -v 5
        lxc-config -n pidns -s lxc.cgroup.cpu.shares -v 512
        ;;
esac

# Start services
echo "Starting PiDNS services..."
lxc-attach -n pidns -- /usr/local/bin/start-pidns.sh

echo "PiDNS is now running in LXC container."
echo "Container IP: $(lxc-info -n pidns -iH)"
echo "Dashboard URL: http://$(lxc-info -n pidns -iH):8080"
```

## 3. Systemd Service Templates

### Docker Service Template

#### pidns-docker.service
```ini
[Unit]
Description=PiDNS Docker Container
After=docker.service network-online.target
Requires=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/PiDNS
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Podman Service Template

#### pidns-podman.service
```ini
[Unit]
Description=PiDNS Podman Container
After=network-online.target
Requires=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/PiDNS
ExecStart=/usr/bin/podman-compose up -d
ExecStop=/usr/bin/podman-compose down
TimeoutStartSec=0
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### LXC Service Template

#### pidns-lxc.service
```ini
[Unit]
Description=PiDNS LXC Container
After=lxc.service network-online.target
Requires=lxc.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/PiDNS
ExecStart=/usr/bin/lxc-start -n pidns -d
ExecStop=/usr/bin/lxc-stop -n pidns
TimeoutStartSec=0
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 4. Configuration Selection Logic

### Configuration Selection Script
```bash
#!/bin/bash
# select_config.sh - Select appropriate configuration based on device type

# Function to select dnsmasq configuration
select_dnsmasq_config() {
    local device_type=$1
    local container_type=$2
    
    if [ "$container_type" != "none" ]; then
        # Container deployment - use device-specific config
        echo "config/dnsmasq.$device_type.conf"
    else
        # Bare metal deployment - use device-specific config
        echo "config/dnsmasq.$device_type.conf"
    fi
}

# Function to select Flask configuration
select_flask_config() {
    local device_type=$1
    local container_type=$2
    
    if [ "$container_type" != "none" ]; then
        # Container deployment - use device-specific config
        echo "config/flask_$device_type.py"
    else
        # Bare metal deployment - use device-specific config
        echo "config/flask_$device_type.py"
    fi
}

# Function to select systemd service
select_systemd_service() {
    local container_type=$1
    
    case $container_type in
        "docker")
            echo "services/pidns-docker.service"
            ;;
        "podman")
            echo "services/pidns-podman.service"
            ;;
        "lxc")
            echo "services/pidns-lxc.service"
            ;;
        *)
            echo "services/pidns.service"
            ;;
    esac
}

# Example usage
DEVICE_TYPE="pi-4"
CONTAINER_TYPE="docker"

DNSMASQ_CONFIG=$(select_dnsmasq_config $DEVICE_TYPE $CONTAINER_TYPE)
FLASK_CONFIG=$(select_flask_config $DEVICE_TYPE $CONTAINER_TYPE)
SYSTEMD_SERVICE=$(select_systemd_service $CONTAINER_TYPE)

echo "Selected dnsmasq config: $DNSMASQ_CONFIG"
echo "Selected Flask config: $FLASK_CONFIG"
echo "Selected systemd service: $SYSTEMD_SERVICE"
```

## 5. Configuration Validation

### Configuration Validation Script
```bash
#!/bin/bash
# validate_config.sh - Validate configuration files

# Function to validate dnsmasq configuration
validate_dnsmasq_config() {
    local config_file=$1
    
    if [ ! -f "$config_file" ]; then
        echo "Error: dnsmasq configuration file $config_file not found"
        return 1
    fi
    
    # Test dnsmasq configuration syntax
    if ! dnsmasq --test -C "$config_file"; then
        echo "Error: dnsmasq configuration $config_file is invalid"
        return 1
    fi
    
    echo "dnsmasq configuration $config_file is valid"
    return 0
}

# Function to validate Flask configuration
validate_flask_config() {
    local config_file=$1
    
    if [ ! -f "$config_file" ]; then
        echo "Error: Flask configuration file $config_file not found"
        return 1
    fi
    
    # Test Python syntax
    if ! python3 -m py_compile "$config_file"; then
        echo "Error: Flask configuration $config_file has syntax errors"
        return 1
    fi
    
    echo "Flask configuration $config_file is valid"
    return 0
}

# Function to validate systemd service
validate_systemd_service() {
    local service_file=$1
    
    if [ ! -f "$service_file" ]; then
        echo "Error: systemd service file $service_file not found"
        return 1
    fi
    
    # Test systemd service syntax
    if ! systemd-analyze verify "$service_file"; then
        echo "Error: systemd service $service_file is invalid"
        return 1
    fi
    
    echo "systemd service $service_file is valid"
    return 0
}

# Example usage
validate_dnsmasq_config "config/dnsmasq.pi-4.conf"
validate_flask_config "config/flask_pi-4.py"
validate_systemd_service "services/pidns-docker.service"
```

## 6. Configuration Migration

### Configuration Migration Script
```bash
#!/bin/bash
# migrate_config.sh - Migrate configuration between device types

# Function to migrate dnsmasq configuration
migrate_dnsmasq_config() {
    local source_device=$1
    local target_device=$2
    
    local source_config="config/dnsmasq.$source_device.conf"
    local target_config="config/dnsmasq.$target_device.conf"
    
    if [ ! -f "$source_config" ]; then
        echo "Error: Source configuration $source_config not found"
        return 1
    fi
    
    # Copy source configuration to target
    cp "$source_config" "$target_config"
    
    # Update device-specific settings
    case $target_device in
        "pi-zero"|"pi-zero-2w")
            sed -i 's/cache-size=[0-9]*/cache-size=100/g' "$target_config"
            sed -i 's/dns-forward-max=[0-9]*/dns-forward-max=100/g' "$target_config"
            ;;
        "pi-3")
            sed -i 's/cache-size=[0-9]*/cache-size=200/g' "$target_config"
            sed -i 's/dns-forward-max=[0-9]*/dns-forward-max=200/g' "$target_config"
            ;;
        "pi-4"|"pi-5")
            sed -i 's/cache-size=[0-9]*/cache-size=500/g' "$target_config"
            sed -i 's/dns-forward-max=[0-9]*/dns-forward-max=500/g' "$target_config"
            ;;
        "low-resource-pc")
            sed -i 's/cache-size=[0-9]*/cache-size=300/g' "$target_config"
            sed -i 's/dns-forward-max=[0-9]*/dns-forward-max=300/g' "$target_config"
            ;;
        "standard-pc")
            sed -i 's/cache-size=[0-9]*/cache-size=1000/g' "$target_config"
            sed -i 's/dns-forward-max=[0-9]*/dns-forward-max=1000/g' "$target_config"
            ;;
    esac
    
    echo "Migrated dnsmasq configuration from $source_device to $target_device"
    return 0
}

# Function to migrate Flask configuration
migrate_flask_config() {
    local source_device=$1
    local target_device=$2
    
    local source_config="config/flask_$source_device.py"
    local target_config="config/flask_$target_device.py"
    
    if [ ! -f "$source_config" ]; then
        echo "Error: Source configuration $source_config not found"
        return 1
    fi
    
    # Copy source configuration to target
    cp "$source_config" "$target_config"
    
    # Update device-specific settings
    case $target_device in
        "pi-zero"|"pi-zero-2w")
            sed -i "s/REFRESH_INTERVAL = [0-9]*/REFRESH_INTERVAL = 60/g" "$target_config"
            sed -i "s/MAX_DEVICES = [0-9]*/MAX_DEVICES = 50/g" "$target_config"
            sed -i "s/THREADS_PER_PAGE = [0-9]*/THREADS_PER_PAGE = 1/g" "$target_config"
            ;;
        "pi-3")
            sed -i "s/REFRESH_INTERVAL = [0-9]*/REFRESH_INTERVAL = 30/g" "$target_config"
            sed -i "s/MAX_DEVICES = [0-9]*/MAX_DEVICES = 100/g" "$target_config"
            sed -i "s/THREADS_PER_PAGE = [0-9]*/THREADS_PER_PAGE = 2/g" "$target_config"
            ;;
        "pi-4"|"pi-5")
            sed -i "s/REFRESH_INTERVAL = [0-9]*/REFRESH_INTERVAL = 15/g" "$target_config"
            sed -i "s/MAX_DEVICES = [0-9]*/MAX_DEVICES = 250/g" "$target_config"
            sed -i "s/THREADS_PER_PAGE = [0-9]*/THREADS_PER_PAGE = 4/g" "$target_config"
            ;;
        "low-resource-pc")
            sed -i "s/REFRESH_INTERVAL = [0-9]*/REFRESH_INTERVAL = 45/g" "$target_config"
            sed -i "s/MAX_DEVICES = [0-9]*/MAX_DEVICES = 75/g" "$target_config"
            sed -i "s/THREADS_PER_PAGE = [0-9]*/THREADS_PER_PAGE = 2/g" "$target_config"
            ;;
        "standard-pc")
            sed -i "s/REFRESH_INTERVAL = [0-9]*/REFRESH_INTERVAL = 10/g" "$target_config"
            sed -i "s/MAX_DEVICES = [0-9]*/MAX_DEVICES = 500/g" "$target_config"
            sed -i "s/THREADS_PER_PAGE = [0-9]*/THREADS_PER_PAGE = 4/g" "$target_config"
            ;;
    esac
    
    echo "Migrated Flask configuration from $source_device to $target_device"
    return 0
}

# Example usage
migrate_dnsmasq_config "pi-3" "pi-4"
migrate_flask_config "pi-3" "pi-4"
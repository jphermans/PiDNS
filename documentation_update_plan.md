# PiDNS Documentation Update Plan

## 1. Documentation Overview

### Documentation Goals
1. **Comprehensive Coverage**: Document all new installation options and features
2. **User-Friendly**: Make documentation easy to understand and follow
3. **Maintainable**: Keep documentation up-to-date with code changes
4. **Accessible**: Provide documentation in multiple formats (Markdown, HTML, PDF)

### Documentation Structure
1. **README.md**: Main project documentation
2. **INSTALLATION.md**: Detailed installation guide
3. **CONFIGURATION.md**: Configuration options and examples
4. **TROUBLESHOOTING.md**: Common issues and solutions
5. **DEVELOPMENT.md**: Developer guide
6. **CHANGELOG.md**: Version history and changes
7. **CONTRIBUTING.md**: Contribution guidelines

## 2. README.md Updates

### Updated README.md Structure
```markdown
# PiDNS

![PiDNS Logo](https://raw.githubusercontent.com/yourusername/PiDNS/main/docs/images/pidns-logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Docker Pulls](https://img.shields.io/docker/pulls/yourusername/pidns)](https://hub.docker.com/r/yourusername/pidns)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/PiDNS)](https://github.com/yourusername/PiDNS/issues)

PiDNS is a lightweight, easy-to-use DNS and DHCP server with an integrated ad-blocker. It's designed to run on Raspberry Pi devices and low-resource PCs, providing network-wide ad blocking and DNS management through a user-friendly web dashboard.

## Features

- **DNS Server**: Lightweight DNS server with caching capabilities
- **DHCP Server**: Automatic IP address assignment for network devices
- **Ad-Blocker**: Network-wide ad blocking with customizable block lists
- **Web Dashboard**: User-friendly interface for managing DNS, DHCP, and ad-blocking settings
- **Device Discovery**: Automatic detection and identification of network devices
- **Multi-Platform Support**: Runs on Raspberry Pi (Zero W, 3, 4, 5) and low-resource PCs
- **Container Support**: Run in Docker, Podman, or LXC containers
- **Device-Specific Optimizations**: Automatically optimized for your hardware

## Quick Start

### Prerequisites

- Raspberry Pi (Zero W, 3, 4, 5) or low-resource PC
- Raspberry Pi OS (Bullseye or later) or Debian-based Linux distribution
- Internet connection for downloading dependencies

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PiDNS.git
   cd PiDNS
   ```

2. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

3. Follow the interactive prompts to:
   - Select your device type
   - Choose container options (Docker, Podman, LXC, or bare metal)
   - Configure basic settings

4. Access the web dashboard:
   - Main Dashboard: `http://<your-pi-ip>:8080`
   - Ad-Blocker Dashboard: `http://<your-pi-ip>:8081`

### Default Credentials

- Username: `admin`
- Password: `password`

**Important**: Change the default password immediately after installation!

## Screenshots

### Main Dashboard
![Main Dashboard](https://raw.githubusercontent.com/yourusername/PiDNS/main/docs/screenshots/main-dashboard.png)

### Ad-Blocker Dashboard
![Ad-Blocker Dashboard](https://raw.githubusercontent.com/yourusername/PiDNS/main/docs/screenshots/adblocker-dashboard.png)

### Device Management
![Device Management](https://raw.githubusercontent.com/yourusername/PiDNS/main/docs/screenshots/device-management.png)

## Supported Devices

### Raspberry Pi
- **Raspberry Pi Zero W**: 512MB RAM, 1-core CPU
- **Raspberry Pi Zero 2W**: 512MB RAM, 1-core CPU
- **Raspberry Pi 3**: 1GB RAM, 4-core CPU
- **Raspberry Pi 4**: 2-8GB RAM, 4-core CPU
- **Raspberry Pi 5**: 4-8GB RAM, 4-core CPU

### Low-Resource PCs
- **Low-Resource PC**: ≤1GB RAM, ≤2 cores
- **Standard PC**: >1GB RAM, >2 cores

## Container Support

PiDNS supports running in the following container types:

### Docker
- Most popular container platform with wide community support
- Easy to use with Docker Compose
- Supports resource limits and health checks

### Podman
- Daemonless, rootless containers with better security
- Compatible with Docker CLI
- No central daemon required

### LXC
- Lightweight OS-level virtualization with better performance
- Lower overhead than Docker or Podman
- Direct access to host kernel features

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Developer Guide](docs/DEVELOPMENT.md)
- [Changelog](docs/CHANGELOG.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## Community

- [GitHub Issues](https://github.com/yourusername/PiDNS/issues): Bug reports and feature requests
- [GitHub Discussions](https://github.com/yourusername/PiDNS/discussions): General discussions and questions
- [Wiki](https://github.com/yourusername/PiDNS/wiki): Community-contributed documentation

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

## License

PiDNS is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [dnsmasq](https://dnsmasq.org/): Lightweight DNS, DHCP, and TFTP server
- [Flask](https://flask.palletsprojects.com/): Web framework for Python
- [Bootstrap](https://getbootstrap.com/): Frontend component library
- [jQuery](https://jquery.com/): JavaScript library
```

## 3. Installation Guide Updates

### Updated INSTALLATION.md Structure
```markdown
# PiDNS Installation Guide

This guide provides detailed instructions for installing PiDNS on various devices and in different container environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Device-Specific Installation](#device-specific-installation)
4. [Container Installation](#container-installation)
5. [Post-Installation](#post-installation)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Hardware Requirements

#### Raspberry Pi
- **Raspberry Pi Zero W**: 512MB RAM, 1-core CPU
- **Raspberry Pi Zero 2W**: 512MB RAM, 1-core CPU
- **Raspberry Pi 3**: 1GB RAM, 4-core CPU
- **Raspberry Pi 4**: 2-8GB RAM, 4-core CPU
- **Raspberry Pi 5**: 4-8GB RAM, 4-core CPU

#### Low-Resource PCs
- **Low-Resource PC**: ≤1GB RAM, ≤2 cores
- **Standard PC**: >1GB RAM, >2 cores

### Software Requirements

#### Raspberry Pi
- Raspberry Pi OS (Bullseye or later)
- Python 3.9 or later
- Git

#### Low-Resource PCs
- Debian-based Linux distribution (Debian, Ubuntu, etc.)
- Python 3.9 or later
- Git

#### Container Environments
- Docker (version 20.10 or later)
- Podman (version 3.0 or later)
- LXC (version 4.0 or later)

## Installation Methods

### Interactive Installation (Recommended)

The interactive installation method guides you through the installation process with prompts for device type and container options.

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PiDNS.git
   cd PiDNS
   ```

2. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

3. Follow the interactive prompts:
   - Select your device type
   - Choose container options (Docker, Podman, LXC, or bare metal)
   - Configure basic settings

### Silent Installation

For automated installations, you can use command line arguments to specify installation options:

```bash
./scripts/install.sh --device pi-4 --container docker --silent
```

Available options:
- `--device DEVICE_TYPE`: Specify device type (pi-zero, pi-zero-2w, pi-3, pi-4, pi-5, low-resource-pc, standard-pc)
- `--container CONTAINER_TYPE`: Specify container type (docker, podman, lxc, none)
- `--silent`: Run in silent mode with no interactive prompts

## Device-Specific Installation

### Raspberry Pi Zero W / Zero 2W

#### Interactive Installation
1. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

2. When prompted, select:
   - Device type: `Raspberry Pi Zero W` or `Raspberry Pi Zero 2W`
   - Container type: Choose based on your preference

#### Silent Installation
```bash
./scripts/install.sh --device pi-zero --container docker --silent
```

#### Optimizations Applied
- Reduced cache sizes for DNS and DHCP
- Limited memory usage for Flask application
- Disabled logging to reduce I/O
- Configured swap file for memory management

### Raspberry Pi 3

#### Interactive Installation
1. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

2. When prompted, select:
   - Device type: `Raspberry Pi 3`
   - Container type: Choose based on your preference

#### Silent Installation
```bash
./scripts/install.sh --device pi-3 --container docker --silent
```

#### Optimizations Applied
- Moderate cache sizes for DNS and DHCP
- Balanced memory usage for Flask application
- Enabled basic logging
- Configured swap file for memory management

### Raspberry Pi 4 / 5

#### Interactive Installation
1. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

2. When prompted, select:
   - Device type: `Raspberry Pi 4` or `Raspberry Pi 5`
   - Container type: Choose based on your preference

#### Silent Installation
```bash
./scripts/install.sh --device pi-4 --container docker --silent
```

#### Optimizations Applied
- Increased cache sizes for DNS and DHCP
- Higher memory limits for Flask application
- Enabled full logging with async logging
- Configured swap file for memory management

### Low-Resource PC

#### Interactive Installation
1. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

2. When prompted, select:
   - Device type: `Low-Resource PC`
   - Container type: Choose based on your preference

#### Silent Installation
```bash
./scripts/install.sh --device low-resource-pc --container docker --silent
```

#### Optimizations Applied
- Moderate cache sizes for DNS and DHCP
- Balanced memory usage for Flask application
- Enabled basic logging
- Configured swap file for memory management

### Standard PC

#### Interactive Installation
1. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

2. When prompted, select:
   - Device type: `Standard PC`
   - Container type: Choose based on your preference

#### Silent Installation
```bash
./scripts/install.sh --device standard-pc --container docker --silent
```

#### Optimizations Applied
- Maximum cache sizes for DNS and DHCP
- High memory limits for Flask application
- Enabled full logging with async logging
- Configured swap file for memory management

## Container Installation

### Docker Installation

#### Prerequisites
- Docker (version 20.10 or later)
- Docker Compose (version 1.29 or later)

#### Interactive Installation
1. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

2. When prompted, select:
   - Device type: Choose based on your hardware
   - Container type: `Docker`

#### Silent Installation
```bash
./scripts/install.sh --device pi-4 --container docker --silent
```

#### Manual Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PiDNS.git
   cd PiDNS
   ```

2. Build the Docker image:
   ```bash
   docker build -t pidns:latest .
   ```

3. Create a docker-compose.yml file:
   ```yaml
   version: '3.8'
   
   services:
     pidns:
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
         - FLASK_ENV=production
         - PIDNS_USERNAME=admin
         - PIDNS_PASSWORD=${PIDNS_PASSWORD:-password}
         - DEVICE_TYPE=pi-4
   
   volumes:
     pidns-data:
     pidns-logs:
     pidns-config:
   ```

4. Start the container:
   ```bash
   docker-compose up -d
   ```

#### Docker Management
```bash
# View container status
docker ps

# View container logs
docker logs pidns

# Stop container
docker stop pidns

# Start container
docker start pidns

# Restart container
docker restart pidns

# Remove container
docker stop pidns && docker rm pidns
```

### Podman Installation

#### Prerequisites
- Podman (version 3.0 or later)
- Podman Compose (version 1.0 or later)

#### Interactive Installation
1. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

2. When prompted, select:
   - Device type: Choose based on your hardware
   - Container type: `Podman`

#### Silent Installation
```bash
./scripts/install.sh --device pi-4 --container podman --silent
```

#### Manual Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PiDNS.git
   cd PiDNS
   ```

2. Build the Podman image:
   ```bash
   podman build -t pidns:latest .
   ```

3. Create a podman-compose.yml file:
   ```yaml
   version: '3.8'
   
   services:
     pidns:
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
         - FLASK_ENV=production
         - PIDNS_USERNAME=admin
         - PIDNS_PASSWORD=${PIDNS_PASSWORD:-password}
         - DEVICE_TYPE=pi-4
       userns: keep-id
   
   volumes:
     pidns-data:
     pidns-logs:
     pidns-config:
   ```

4. Start the container:
   ```bash
   podman-compose up -d
   ```

#### Podman Management
```bash
# View container status
podman ps

# View container logs
podman logs pidns

# Stop container
podman stop pidns

# Start container
podman start pidns

# Restart container
podman restart pidns

# Remove container
podman stop pidns && podman rm pidns
```

### LXC Installation

#### Prerequisites
- LXC (version 4.0 or later)
- LXC templates

#### Interactive Installation
1. Run the installation script:
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

2. When prompted, select:
   - Device type: Choose based on your hardware
   - Container type: `LXC`

#### Silent Installation
```bash
./scripts/install.sh --device pi-4 --container lxc --silent
```

#### Manual Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PiDNS.git
   cd PiDNS
   ```

2. Create an LXC container:
   ```bash
   lxc-create -n pidns -t download -- -d debian -r bullseye -a armhf
   ```

3. Start the container:
   ```bash
   lxc-start -n pidns -d
   ```

4. Wait for the container to start:
   ```bash
   sleep 10
   ```

5. Copy PiDNS files into the container:
   ```bash
   lxc-attach -n pidns -- mkdir -p /app
   tar -cf - . | lxc-attach -n pidns -- tar -xf - -C /app
   ```

6. Install dependencies in the container:
   ```bash
   lxc-attach -n pidns -- apt-get update
   lxc-attach -n pidns -- apt-get install -y python3 python3-pip dnsmasq curl wget
   lxc-attach -n pidns -- pip3 install -r /app/requirements.txt
   lxc-attach -n pidns -- pip3 install -r /app/requirements_adblocker.txt
   ```

7. Configure dnsmasq:
   ```bash
   lxc-attach -n pidns -- cp /app/config/dnsmasq.pi-4.conf /etc/dnsmasq.conf
   ```

8. Create a startup script:
   ```bash
   cat > /tmp/start-pidns.sh << 'EOF'
   #!/bin/bash
   cd /app
   python3 app/app.py &
   dnsmasq
   EOF
   lxc-file-push /tmp/start-pidns.sh pidns/usr/local/bin/start-pidns.sh
   lxc-attach -n pidns -- chmod +x /usr/local/bin/start-pidns.sh
   ```

9. Start PiDNS services:
   ```bash
   lxc-attach -n pidns -- /usr/local/bin/start-pidns.sh
   ```

#### LXC Management
```bash
# View container status
lxc-info -n pidns

# View container logs
lxc-attach -n pidns -- tail -f /var/log/pidns.log

# Stop container
lxc-stop -n pidns

# Start container
lxc-start -n pidns -d

# Restart container
lxc-stop -n pidns && lxc-start -n pidns -d

# Remove container
lxc-stop -n pidns && lxc-destroy -n pidns
```

## Post-Installation

### Accessing the Dashboard

After installation, you can access the PiDNS dashboards at:

- **Main Dashboard**: `http://<your-pi-ip>:8080`
- **Ad-Blocker Dashboard**: `http://<your-pi-ip>:8081`

Default credentials:
- Username: `admin`
- Password: `password`

**Important**: Change the default password immediately after installation!

### Changing Default Password

1. Access the main dashboard at `http://<your-pi-ip>:8080`
2. Log in with the default credentials
3. Navigate to Settings > Security
4. Enter a new password and confirm
5. Click Save

### Configuring Your Router

To use PiDNS as your network's DNS and DHCP server:

1. Log in to your router's admin interface
2. Navigate to the DHCP/DNS settings
3. Disable the router's DHCP server
4. Set the DNS server to your Pi's IP address
5. Save and apply the changes

### Updating PiDNS

#### Bare Metal Installation
```bash
cd /home/pi/PiDNS
git pull origin main
./scripts/update.sh
```

#### Docker Installation
```bash
cd /home/pi/PiDNS
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

#### Podman Installation
```bash
cd /home/pi/PiDNS
git pull origin main
podman-compose down
podman-compose build
podman-compose up -d
```

#### LXC Installation
```bash
cd /home/pi/PiDNS
git pull origin main
lxc-stop -n pidns
tar -cf - . | lxc-attach -n pidns -- tar -xf - -C /app
lxc-start -n pidns -d
```

## Troubleshooting

### Common Issues

#### Installation Fails
- Ensure you have enough disk space (at least 1GB free)
- Check your internet connection
- Verify you're running as the correct user (not root)

#### Container Won't Start
- Check container logs for error messages
- Verify all required volumes are mounted correctly
- Ensure port 8080, 8081, 53, and 67 are not in use by other services

#### Dashboard Not Accessible
- Verify the container is running
- Check your firewall settings
- Ensure you're using the correct IP address

#### DNS Not Working
- Verify dnsmasq is running
- Check dnsmasq configuration for errors
- Ensure your router is configured to use PiDNS as the DNS server

### Getting Help

If you encounter issues not covered in this guide:

1. Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Search existing [GitHub Issues](https://github.com/yourusername/PiDNS/issues)
3. Create a new issue with detailed information about your problem
4. Join our [GitHub Discussions](https://github.com/yourusername/PiDNS/discussions) for community support
```

## 4. Configuration Guide Updates

### Updated CONFIGURATION.md Structure
```markdown
# PiDNS Configuration Guide

This guide provides detailed information about configuring PiDNS for different use cases and environments.

## Table of Contents

1. [Configuration Files](#configuration-files)
2. [Device-Specific Configuration](#device-specific-configuration)
3. [Container-Specific Configuration](#container-specific-configuration)
4. [DNS Configuration](#dns-configuration)
5. [DHCP Configuration](#dhcp-configuration)
6. [Ad-Blocker Configuration](#ad-blocker-configuration)
7. [Dashboard Configuration](#dashboard-configuration)
8. [Security Configuration](#security-configuration)
9. [Performance Configuration](#performance-configuration)
10. [Advanced Configuration](#advanced-configuration)

## Configuration Files

### Main Configuration Files

#### Flask Configuration (`config/flask_config.py`)
The Flask configuration file contains settings for the web dashboard, including:

- Server settings (host, port, threading)
- Database settings
- Authentication settings
- Logging settings
- Performance settings

#### dnsmasq Configuration (`config/dnsmasq.conf`)
The dnsmasq configuration file contains settings for the DNS and DHCP server, including:

- Interface settings
- DHCP range settings
- DNS server settings
- Cache settings
- Logging settings

#### Systemd Service Files (`services/`)
The systemd service files contain settings for running PiDNS as a system service, including:

- Service dependencies
- Resource limits
- Restart policies
- Security settings

### Device-Specific Configuration Files

#### Raspberry Pi Zero W / Zero 2W
- `config/flask_config.pi-zero.py`
- `config/dnsmasq.pi-zero.conf`
- `services/pidns.pi-zero.service`

#### Raspberry Pi 3
- `config/flask_config.pi-3.py`
- `config/dnsmasq.pi-3.conf`
- `services/pidns.pi-3.service`

#### Raspberry Pi 4 / 5
- `config/flask_config.pi-4-5.py`
- `config/dnsmasq.pi-4-5.conf`
- `services/pidns.pi-4-5.service`

#### Low-Resource PC
- `config/flask_config.low-resource-pc.py`
- `config/dnsmasq.low-resource-pc.conf`
- `services/pidns.low-resource-pc.service`

#### Standard PC
- `config/flask_config.standard-pc.py`
- `config/dnsmasq.standard-pc.conf`
- `services/pidns.standard-pc.service`

### Container-Specific Configuration Files

#### Docker
- `Dockerfile`
- `docker-compose.yml`
- `docker-compose.override.{device_type}.yml`
- `services/pidns-docker.service`

#### Podman
- `Containerfile`
- `podman-compose.yml`
- `podman-compose.override.{device_type}.yml`
- `services/pidns-podman.service`
- `~/.config/containers/systemd/pidns.container`

#### LXC
- `lxc/lxc-{device_type}.conf`
- `services/pidns-lxc.service`

## Device-Specific Configuration

### Raspberry Pi Zero W / Zero 2W

#### Flask Configuration
```python
# config/flask_config.pi-zero.py
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

#### dnsmasq Configuration
```conf
# config/dnsmasq.pi-zero.conf
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

#### Systemd Service Configuration
```ini
# services/pidns.pi-zero.service
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
```

### Raspberry Pi 3

#### Flask Configuration
```python
# config/flask_config.pi-3.py
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

#### dnsmasq Configuration
```conf
# config/dnsmasq.pi-3.conf
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

#### Systemd Service Configuration
```ini
# services/pidns.pi-3.service
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

### Raspberry Pi 4 / 5

#### Flask Configuration
```python
# config/flask_config.pi-4-5.py
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

#### dnsmasq Configuration
```conf
# config/dnsmasq.pi-4-5.conf
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

#### Systemd Service Configuration
```ini
# services/pidns.pi-4-5.service
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

#### Flask Configuration
```python
# config/flask_config.low-resource-pc.py
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

#### dnsmasq Configuration
```conf
# config/dnsmasq.low-resource-pc.conf
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

#### Systemd Service Configuration
```ini
# services/pidns.low-resource-pc.service
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

#### Flask Configuration
```python
# config/flask_config.standard-pc.py
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

#### dnsmasq Configuration
```conf
# config/dnsmasq.standard-pc.conf
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

#### Systemd Service Configuration
```ini
# services/pidns.standard-pc.service
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

## Container-Specific Configuration

### Docker Configuration

#### Dockerfile
```dockerfile
# Dockerfile for PiDNS
# Multi-stage build for optimized image size

# Builder stage
FROM python:3.11-slim-bullseye as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
COPY requirements_adblocker.txt .

# Install Python dependencies
RUN pip install --user -r requirements.txt
RUN pip install --user -r requirements_adblocker.txt

# Final stage
FROM python:3.11-slim-bullseye

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    dnsmasq \
    curl \
    wget \
    supervisor \
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

# Default command
CMD ["python3", "app/app.py"]
```

#### Docker Compose Configuration
```yaml
# docker-compose.yml
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

volumes:
  pidns-data:
  pidns-logs:
  pidns-config:
```

#### Docker Compose Override for Pi 4/5
```yaml
# docker-compose.override.pi-4-5.yml
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
      - ./config/flask_config.pi-4-5.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi-4-5.conf:/etc/dnsmasq.conf:ro
```

### Podman Configuration

#### Containerfile
```containerfile
# Containerfile for PiDNS
# Optimized for Podman

FROM python:3.11-slim-bullseye

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    dnsmasq \
    curl \
    wget \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
COPY requirements_adblocker.txt .

# Install Python dependencies
RUN pip install --user -r requirements.txt
RUN pip install --user -r requirements_adblocker.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 pidns && \
    chown -R pidns:pidns /app
USER pidns

# Expose ports
EXPOSE 8080 8081 53 67/udp

# Default command
CMD ["python3", "app/app.py"]
```

#### Podman Compose Configuration
```yaml
# podman-compose.yml
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

volumes:
  pidns-data:
  pidns-logs:
  pidns-config:
```

#### Podman Quadlet Configuration
```ini
# ~/.config/containers/systemd/pidns.container
[Unit]
Description=PiDNS Container
After=network-online.target

[Container]
Image=localhost/pidns:latest
ContainerName=pidns
Network=host
PublishPort=8080:8080
PublishPort=8081:8081
PublishPort=53:53
PublishPort=67:67/udp
Volume=pidns-data:/app/data:z
Volume=pidns-logs:/var/log/pidns:z
Volume=pidns-config:/app/config:z
Volume=/var/lib/misc:/var/lib/misc:rw,z
Volume=/etc/dnsmasq.conf:/etc/dnsmasq.conf:rw,z
Environment=FLASK_ENV=production
Environment=PIDNS_USERNAME=admin
Environment=PIDNS_PASSWORD=password
Environment=DEVICE_TYPE=standard-pc
UserNS=keep-id

[Service]
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

### LXC Configuration

#### LXC Configuration for Pi 4/5
```conf
# lxc/lxc-pi-4-5.conf
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
lxc.pts = 1024

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
```

#### LXC Systemd Service Configuration
```ini
# services/pidns-lxc.service
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

## DNS Configuration

### Basic DNS Configuration

#### Forwarding DNS Queries
```conf
# Forward DNS queries to upstream servers
server=8.8.8.8
server=8.8.4.4
server=1.1.1.1
```

#### Local DNS Resolution
```conf
# Enable local DNS resolution
domain-needed
bogus-priv
local=/local/
domain=local
```

#### DNS Cache Configuration
```conf
# DNS cache configuration
cache-size=500
dns-forward-max=500
min-cache-ttl=3600
max-cache-ttl=86400
```

### Advanced DNS Configuration

#### Conditional Forwarding
```conf
# Forward specific domains to specific servers
server=/example.com/192.168.1.100
server=/internal.local/192.168.1.101
```

#### DNSSEC Configuration
```conf
# Enable DNSSEC validation
dnssec
trust-anchor=.,20326,8,2,e06d44b80b8f1d39a95c0cf0dd1971bae9c9d9e7e3341d9c9f2b3d1e7b6d1
```

#### DNS Filtering
```conf
# Block specific domains
address=/doubleclick.net/127.0.0.1
address=/facebook.com/127.0.0.1
```

## DHCP Configuration

### Basic DHCP Configuration

#### DHCP Range Configuration
```conf
# DHCP range configuration
dhcp-range=192.168.1.100,192.168.1.200,255.255.255.0,24h
```

#### DHCP Options
```conf
# DHCP options
dhcp-option=option:router,192.168.1.1
dhcp-option=option:dns-server,192.168.1.1
dhcp-option=option:ntp-server,192.168.1.1
```

#### DHCP Static Leases
```conf
# Static DHCP leases
dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1,infinite
dhcp-host=11:22:33:44:55:66,192.168.1.11,device2,infinite
```

### Advanced DHCP Configuration

#### Multiple DHCP Ranges
```conf
# Multiple DHCP ranges for different subnets
dhcp-range=192.168.1.100,192.168.1.200,255.255.255.0,24h
dhcp-range=192.168.2.100,192.168.2.200,255.255.255.0,24h
```

#### DHCP Vendor Classes
```conf
# Vendor-specific DHCP options
dhcp-vendorclass=set:android,android-dhcp
dhcp-option=tag:android,option:dns-server,192.168.1.1
```

#### DHCP User Classes
```conf
# User-specific DHCP options
dhcp-userclass=set:printers,printers
dhcp-option=tag:printers,option:router,192.168.1.1
```

## Ad-Blocker Configuration

### Basic Ad-Blocker Configuration

#### Enable Ad-Blocking
```python
# adblocker/config/flask_config.py
class Config:
    # Enable ad-blocking
    AD_BLOCKING_ENABLED = True
    
    # Block list categories
    BLOCKLIST_CATEGORIES = [
        'ads',
        'tracking',
        'malware',
        'phishing',
        'social'
    ]
```

#### Custom Block Lists
```python
# adblocker/config/flask_config.py
class Config:
    # Custom block lists
    CUSTOM_BLOCKLISTS = [
        'https://example.com/custom-blocklist.txt',
        'https://example.com/another-blocklist.txt'
    ]
```

#### Whitelist Configuration
```python
# adblocker/config/flask_config.py
class Config:
    # Whitelist configuration
    WHITELIST = [
        'example.com',
        'subdomain.example.com'
    ]
```

### Advanced Ad-Blocker Configuration

#### Scheduled Block List Updates
```python
# adblocker/config/flask_config.py
class Config:
    # Scheduled block list updates
    BLOCKLIST_UPDATE_SCHEDULE = {
        'enabled': True,
        'interval': 'daily',  # hourly, daily, weekly
        'time': '03:00'  # Time of day for updates
    }
```

#### Block List Categories
```python
# adblocker/config/flask_config.py
class Config:
    # Block list categories with URLs
    BLOCKLIST_CATEGORIES = {
        'ads': [
            'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts',
            'https://adaway.org/hosts.txt'
        ],
        'tracking': [
            'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/tracking/hosts',
            'https://gitlab.com/quidsup/notrack-blocklists/raw/master/notrack-blocklist.txt'
        ],
        'malware': [
            'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews/hosts',
            'https://gitlab.com/quidsup/notrack-blocklists/raw/master/notrack-malware.txt'
        ],
        'phishing': [
            'https://phishing.army/download/phishing_army_blocklist_extended.txt',
            'https://gitlab.com/quidsup/notrack-blocklists/raw/master/notrack-phishing.txt'
        ],
        'social': [
            'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/social/hosts',
            'https://gitlab.com/quidsup/notrack-blocklists/raw/master/notrack-social.txt'
        ]
    }
```

#### Custom Block List Rules
```python
# adblocker/config/flask_config.py
class Config:
    # Custom block list rules
    CUSTOM_BLOCKLIST_RULES = [
        {
            'pattern': '.*\\.example\\.com',
            'type': 'regex',
            'category': 'ads',
            'enabled': True
        },
        {
            'pattern': 'tracking\\.example\\.com',
            'type': 'domain',
            'category': 'tracking',
            'enabled': True
        }
    ]
```

## Dashboard Configuration

### Basic Dashboard Configuration

#### Dashboard Title
```python
# config/flask_config.py
class Config:
    # Dashboard title
    DASHBOARD_TITLE = 'PiDNS Network Dashboard'
```

#### Refresh Interval
```python
# config/flask_config.py
class Config:
    # Dashboard refresh interval (in seconds)
    REFRESH_INTERVAL = 30
```

#### Device Display Limit
```python
# config/flask_config.py
class Config:
    # Maximum number of devices to display
    MAX_DEVICES = 100
```

### Advanced Dashboard Configuration

#### Custom Theme
```python
# config/flask_config.py
class Config:
    # Custom theme configuration
    THEME = {
        'primary_color': '#007bff',
        'secondary_color': '#6c757d',
        'success_color': '#28a745',
        'danger_color': '#dc3545',
        'warning_color': '#ffc107',
        'info_color': '#17a2b8',
        'light_color': '#f8f9fa',
        'dark_color': '#343a40'
    }
```

#### Dashboard Widgets
```python
# config/flask_config.py
class Config:
    # Dashboard widgets configuration
    DASHBOARD_WIDGETS = [
        {
            'name': 'device_list',
            'title': 'Connected Devices',
            'enabled': True,
            'position': 'top-left'
        },
        {
            'name': 'dns_stats',
            'title': 'DNS Statistics',
            'enabled': True,
            'position': 'top-right'
        },
        {
            'name': 'dhcp_stats',
            'title': 'DHCP Statistics',
            'enabled': True,
            'position': 'bottom-left'
        },
        {
            'name': 'adblocker_stats',
            'title': 'Ad-Blocker Statistics',
            'enabled': True,
            'position': 'bottom-right'
        }
    ]
```

#### Custom Dashboard Layout
```python
# config/flask_config.py
class Config:
    # Custom dashboard layout
    DASHBOARD_LAYOUT = {
        'rows': 2,
        'columns': 2,
        'widgets': {
            'top-left': 'device_list',
            'top-right': 'dns_stats',
            'bottom-left': 'dhcp_stats',
            'bottom-right': 'adblocker_stats'
        }
    }
```

## Security Configuration

### Basic Security Configuration

#### Authentication
```python
# config/flask_config.py
class Config:
    # Authentication configuration
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME') or 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD') or 'password'
```

#### Session Security
```python
# config/flask_config.py
class Config:
    # Session security configuration
    SESSION_COOKIE_SECURE = False  # Enable with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
```

#### API Security
```python
# config/flask_config.py
class Config:
    # API security configuration
    API_KEY = os.environ.get('PIDNS_API_KEY') or 'default-api-key-change-in-production'
    API_RATE_LIMIT = '100/hour'
```

### Advanced Security Configuration

#### Two-Factor Authentication
```python
# config/flask_config.py
class Config:
    # Two-factor authentication configuration
    TWO_FACTOR_AUTH = {
        'enabled': False,
        'issuer': 'PiDNS',
        'token_validity': 30  # seconds
    }
```

#### IP Whitelisting
```python
# config/flask_config.py
class Config:
    # IP whitelisting configuration
    IP_WHITELIST = [
        '192.168.1.0/24',
        '10.0.0.0/8'
    ]
```

#### Access Control
```python
# config/flask_config.py
class Config:
    # Access control configuration
    ACCESS_CONTROL = {
        'enabled': False,
        'default_role': 'viewer',
        'roles': {
            'viewer': {
                'permissions': ['read']
            },
            'editor': {
                'permissions': ['read', 'write']
            },
            'admin': {
                'permissions': ['read', 'write', 'admin']
            }
        }
    }
```

## Performance Configuration

### Basic Performance Configuration

#### Threading Configuration
```python
# config/flask_config.py
class Config:
    # Threading configuration
    THREADS_PER_PAGE = 4
    PROCESSES = 1
```

#### Caching Configuration
```python
# config/flask_config.py
class Config:
    # Caching configuration
    CACHE_TYPE = 'simple'  # simple, filesystem, redis
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
```

#### Logging Configuration
```python
# config/flask_config.py
class Config:
    # Logging configuration
    LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE = '/var/log/pidns/app.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
```

### Advanced Performance Configuration

#### Database Connection Pooling
```python
# config/flask_config.py
class Config:
    # Database connection pooling
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 3600
    }
```

#### Request Optimization
```python
# config/flask_config.py
class Config:
    # Request optimization
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024  # 64MB
    SEND_FILE_MAX_AGE_DEFAULT = 60  # 1 minute
    TEMPLATES_AUTO_RELOAD = False
```

#### System Resource Limits
```python
# config/flask_config.py
class Config:
    # System resource limits
    SYSTEM_RESOURCE_LIMITS = {
        'memory_limit': '1024M',
        'cpu_quota': '100%',
        'max_tasks': 200,
        'max_open_files': 4096
    }
```

## Advanced Configuration

### Custom dnsmasq Scripts
```bash
#!/bin/bash
# /etc/dnsmasq.d/01-custom.conf

# Custom dnsmasq configuration
# This file is loaded after the main configuration file

# Add custom DNS entries
address=/custom.local/192.168.1.100

# Add custom DHCP options
dhcp-option=option:domain-search,local

# Add custom DHCP host mappings
dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.200,custom-device
```

### Custom Systemd Service Overrides
```ini
# /etc/systemd/system/pidns.service.d/override.conf
[Service]
# Custom systemd service overrides
Environment=PIDNS_CUSTOM_SETTING=value
RestartSec=5
```

### Custom Environment Variables
```bash
# /etc/default/pidns
# Custom environment variables for PiDNS

# PiDNS configuration
PIDNS_USERNAME=admin
PIDNS_PASSWORD=secure-password
PIDNS_API_KEY=custom-api-key

# Device type
DEVICE_TYPE=pi-4

# Container type
CONTAINER_TYPE=docker
```

### Configuration Validation
```python
# scripts/validate_config.py
#!/usr/bin/env python3
"""
Configuration validation script for PiDNS
"""

import os
import sys
import configparser
import json
from pathlib import Path

def validate_flask_config(config_file):
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

def validate_dnsmasq_config(config_file):
    """Validate dnsmasq configuration file"""
    print(f"Validating dnsmasq configuration: {config_file}")
    
    # Check if file exists
    if not os.path.exists(config_file):
        print(f"Error: Configuration file does not exist: {config_file}")
        return False
    
    # Check dnsmasq configuration syntax
    import subprocess
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

def validate_systemd_service(service_file):
    """Validate systemd service file"""
    print(f"Validating systemd service: {service_file}")
    
    # Check if file exists
    if not os.path.exists(service_file):
        print(f"Error: Service file does not exist: {service_file}")
        return False
    
    # Check systemd service syntax
    import subprocess
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

def main():
    """Main validation function"""
    print("PiDNS Configuration Validation")
    print("=" * 40)
    
    # Validate Flask configuration
    flask_config = 'config/flask_config.py'
    if not validate_flask_config(flask_config):
        sys.exit(1)
    
    # Validate dnsmasq configuration
    dnsmasq_config = '/etc/dnsmasq.conf'
    if not validate_dnsmasq_config(dnsmasq_config):
        sys.exit(1)
    
    # Validate systemd service
    systemd_service = '/etc/systemd/system/pidns.service'
    if not validate_systemd_service(systemd_service):
        sys.exit(1)
    
    print("=" * 40)
    print("All configurations are valid")
    return 0

if __name__ == '__main__':
    sys.exit(main())
```

### Configuration Migration
```python
# scripts/migrate_config.py
#!/usr/bin/env python3
"""
Configuration migration script for PiDNS
"""

import os
import sys
import shutil
from pathlib import Path

def migrate_flask_config(source_device, target_device):
    """Migrate Flask configuration from source device to target device"""
    print(f"Migrating Flask configuration from {source_device} to {target_device}")
    
    source_config = f'config/flask_config.{source_device}.py'
    target_config = f'config/flask_config.{target_device}.py'
    
    # Check if source configuration exists
    if not os.path.exists(source_config):
        print(f"Error: Source configuration does not exist: {source_config}")
        return False
    
    # Copy source configuration to target
    shutil.copy(source_config, target_config)
    
    # Update device-specific settings
    with open(target_config, 'r') as f:
        content = f.read()
    
    # Update device type
    content = content.replace(f"DEVICE_TYPE = '{source_device}'", f"DEVICE_TYPE = '{target_device}'")
    
    # Update dashboard title
    content = content.replace(f"DASHBOARD_TITLE = 'PiDNS Network Dashboard ({source_device})'", 
                           f"DASHBOARD_TITLE = 'PiDNS Network Dashboard ({target_device})'")
    
    # Write updated content
    with open(target_config, 'w') as f:
        f.write(content)
    
    print(f"Flask configuration migrated from {source_device} to {target_device}")
    return True

def migrate_dnsmasq_config(source_device, target_device):
    """Migrate dnsmasq configuration from source device to target device"""
    print(f"Migrating dnsmasq configuration from {source_device} to {target_device}")
    
    source_config = f'config/dnsmasq.{source_device}.conf'
    target_config = f'config/dnsmasq.{target_device}.conf'
    
    # Check if source configuration exists
    if not os.path.exists(source_config):
        print(f"Error: Source configuration does not exist: {source_config}")
        return False
    
    # Copy source configuration to target
    shutil.copy(source_config, target_config)
    
    # Update device-specific settings
    with open(target_config, 'r') as f:
        content = f.read()
    
    # Update cache size based on device type
    cache_sizes = {
        'pi-zero': 100,
        'pi-zero-2w': 100,
        'pi-3': 200,
        'pi-4': 500,
        'pi-5': 500,
        'low-resource-pc': 300,
        'standard-pc': 1000
    }
    
    cache_size = cache_sizes.get(target_device, 100)
    content = content.replace(f"cache-size={cache_sizes.get(source_device, 100)}", 
                           f"cache-size={cache_size}")
    
    # Write updated content
    with open(target_config, 'w') as f:
        f.write(content)
    
    print(f"dnsmasq configuration migrated from {source_device} to {target_device}")
    return True

def migrate_systemd_service(source_device, target_device):
    """Migrate systemd service from source device to target device"""
    print(f"Migrating systemd service from {source_device} to {target_device}")
    
    source_service = f'services/pidns.{source_device}.service'
    target_service = f'services/pidns.{target_device}.service'
    
    # Check if source service exists
    if not os.path.exists(source_service):
        print(f"Error: Source service does not exist: {source_service}")
        return False
    
    # Copy source service to target
    shutil.copy(source_service, target_service)
    
    # Update device-specific settings
    with open(target_service, 'r') as f:
        content = f.read()
    
    # Update memory limit based on device type
    memory_limits = {
        'pi-zero': '256M',
        'pi-zero-2w': '256M',
        'pi-3': '512M',
        'pi-4': '1024M',
        'pi-5': '1024M',
        'low-resource-pc': '512M',
        'standard-pc': '2048M'
    }
    
    memory_limit = memory_limits.get(target_device, '256M')
    content = content.replace(f"MemoryLimit={memory_limits.get(source_device, '256M')}", 
                           f"MemoryLimit={memory_limit}")
    
    # Write updated content
    with open(target_service, 'w') as f:
        f.write(content)
    
    print(f"systemd service migrated from {source_device} to {target_device}")
    return True

def main():
    """Main migration function"""
    if len(sys.argv) != 3:
        print("Usage: python migrate_config.py <source_device> <target_device>")
        print("Supported devices: pi-zero, pi-zero-2w, pi-3, pi-4, pi-5, low-resource-pc, standard-pc")
        sys.exit(1)
    
    source_device = sys.argv[1]
    target_device = sys.argv[2]
    
    print("PiDNS Configuration Migration")
    print("=" * 40)
    
    # Migrate Flask configuration
    if not migrate_flask_config(source_device, target_device):
        sys.exit(1)
    
    # Migrate dnsmasq configuration
    if not migrate_dnsmasq_config(source_device, target_device):
        sys.exit(1)
    
    # Migrate systemd service
    if not migrate_systemd_service(source_device, target_device):
        sys.exit(1)
    
    print("=" * 40)
    print(f"Configuration migrated from {source_device} to {target_device}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
# PiDNS Comprehensive Documentation

## 1. Project Overview

### What is PiDNS?
PiDNS is a lightweight, easy-to-use DNS and DHCP server solution designed for Raspberry Pi and other low-resource devices. It provides a web-based dashboard for monitoring and managing network devices, with support for ad-blocking capabilities.

### Key Features
1. **DNS and DHCP Server**: Provides DNS and DHCP services for local networks
2. **Web Dashboard**: User-friendly web interface for monitoring and management
3. **Device Monitoring**: Real-time monitoring of connected devices
4. **Ad-blocking**: Built-in ad-blocking capabilities
5. **Container Support**: Support for Docker, Podman, and LXC containers
6. **Multi-Device Support**: Optimized for various Raspberry Pi models and PCs
7. **Resource Optimization**: Configurable resource usage based on device capabilities

### Target Audience
1. **Home Users**: Individuals looking for a simple DNS/DHCP solution for their home network
2. **Small Businesses**: Small businesses needing a cost-effective network management solution
3. **Developers**: Developers interested in networking and container technologies
4. **Educators**: Educators teaching networking concepts

## 2. Architecture

### System Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    PiDNS System                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Flask App   │  │   dnsmasq     │  │  Ad-blocker │ │
│  │   Dashboard   │  │   Service      │  │   Service   │ │
│  │             │  │               │  │             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│           │                     │                     │    │
│           └─────────────────────┼─────────────────────┘    │
│                                 │                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Container Runtime                │ │
│  │  (Docker/Podman/LXC/Bare Metal)          │ │
│  │                                             │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                 │                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                Host System                   │ │
│  │  (Raspberry Pi/PC)                          │ │
│  │                                             │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Component Architecture
1. **Flask Dashboard**: Web-based dashboard for monitoring and management
2. **dnsmasq Service**: DNS and DHCP server
3. **Ad-blocker Service**: Optional ad-blocking service
4. **Container Runtime**: Docker, Podman, LXC, or bare metal
5. **Host System**: Raspberry Pi or PC

### Data Flow
1. **Device Connection**: Devices connect to the network via DHCP
2. **DNS Queries**: Devices send DNS queries to dnsmasq
3. **Ad-blocking**: Ad-blocker filters DNS queries if enabled
4. **Dashboard Updates**: Flask dashboard updates with device information
5. **User Interaction**: Users interact with the dashboard to manage devices

## 3. Installation

### Prerequisites
1. **Operating System**: Raspberry Pi OS (formerly Raspbian) or Debian-based Linux distribution
2. **Python**: Python 3.7 or higher
3. **Memory**: Minimum 512MB RAM (1GB recommended)
4. **Storage**: Minimum 4GB free space (8GB recommended)
5. **Network**: Ethernet or Wi-Fi connection

### Installation Methods
1. **Interactive Installation**: Guided installation with prompts
2. **Silent Installation**: Automated installation with command-line arguments
3. **Manual Installation**: Step-by-step manual installation

### Interactive Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/PiDNS.git
cd PiDNS

# Run the installation script
./scripts/install.sh

# Follow the prompts to select device type and container type
```

### Silent Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/PiDNS.git
cd PiDNS

# Run the installation script with specified options
./scripts/install.sh --device pi-4 --container docker --silent
```

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/PiDNS.git
cd PiDNS

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip dnsmasq curl wget supervisor

# Install Python dependencies
pip3 install -r requirements.txt
pip3 install -r requirements_adblocker.txt

# Generate configuration files
python3 scripts/generate_config.py --device pi-4 --container docker

# Copy configuration files
sudo cp config/flask_config.pi-4.py config/flask_config.py
sudo cp config/dnsmasq.pi-4.conf /etc/dnsmasq.conf
sudo cp services/pidns.pi-4.service /etc/systemd/system/pidns.service

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable pidns.service
sudo systemctl enable dnsmasq.service
sudo systemctl start pidns.service
sudo systemctl start dnsmasq.service
```

## 4. Configuration

### Device Types
1. **Raspberry Pi Zero W**: 512MB RAM, 1-core CPU
2. **Raspberry Pi Zero 2W**: 512MB RAM, 1-core CPU
3. **Raspberry Pi 3**: 1GB RAM, 4-core CPU
4. **Raspberry Pi 4**: 2-8GB RAM, 4-core CPU
5. **Raspberry Pi 5**: 4-8GB RAM, 4-core CPU
6. **Low-Resource PC**: ≤1GB RAM, ≤2 cores
7. **Standard PC**: >1GB RAM, >2 cores

### Container Types
1. **Docker**: Most popular container platform with wide community support
2. **Podman**: Daemonless, rootless containers with better security
3. **LXC**: Lightweight OS-level virtualization with better performance
4. **None**: Install directly on the host system without containers

### Configuration Files
1. **Flask Configuration**: `config/flask_config.py`
2. **dnsmasq Configuration**: `/etc/dnsmasq.conf`
3. **Systemd Service**: `/etc/systemd/system/pidns.service`
4. **Docker Compose**: `docker-compose.yml` and `docker-compose.override.{device_type}.yml`
5. **Podman Compose**: `podman-compose.yml` and `podman-compose.override.{device_type}.yml`
6. **LXC Configuration**: `lxc.{device_type}.conf`

### Flask Configuration
```python
# config/flask_config.py
# Flask configuration for PiDNS

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Configuration for PiDNS"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # Flask settings
    HOST = '0.0.0.0'
    PORT = 8080
    
    # Performance optimizations
    THREADS_PER_PAGE = 4
    PROCESSES = 1
    
    # DNS and DHCP settings
    DNSMASQ_LEASE_FILE = '/var/lib/misc/dnsmasq.leases'
    DNSMASQ_CONFIG_FILE = '/etc/dnsmasq.conf'
    
    # MAC vendor database
    MAC_VENDORS_FILE = BASE_DIR / 'data' / 'mac-vendors.json'
    
    # Dashboard settings
    DASHBOARD_TITLE = 'PiDNS Network Dashboard'
    REFRESH_INTERVAL = 15  # seconds
    
    # Authentication
    BASIC_AUTH_USERNAME = os.environ.get('PIDNS_USERNAME') or 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('PIDNS_PASSWORD') or 'password'
    
    # Memory optimization settings
    MAX_DEVICES = 250
    LOG_LEVEL = 'DEBUG'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(BASE_DIR / 'data' / 'pidns.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cache settings
    CACHE_TYPE = 'filesystem'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Security settings
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # API settings
    API_KEY = os.environ.get('PIDNS_API_KEY') or 'default-api-key-change-in-production'
    API_RATE_LIMIT = '100/hour'
    
    # Ad-blocker settings
    AD_BLOCKER_ENABLED = True
    AD_BLOCKER_PORT = 8081
    AD_BLOCKER_API_KEY = os.environ.get('PIDNS_AD_BLOCKER_API_KEY') or 'default-ad-blocker-api-key-change-in-production'
    
    # Container settings
    CONTAINER_TYPE = 'docker'
    CONTAINER_NAME = 'pidns'
    
    # Device-specific settings
    DEVICE_TYPE = 'pi-4'
    DEVICE_NAME = 'Raspberry Pi 4'
    DEVICE_MEMORY = '2-8GB'
    DEVICE_CPU_CORES = 4
    
    # Environment-specific settings
    ENVIRONMENT = 'production'
    LOG_FILE = '/var/log/pidns/app.log'
    LOG_MAX_SIZE = 20 * 1024 * 1024  # 20MB
    LOG_BACKUP_COUNT = 5
```

### dnsmasq Configuration
```conf
# /etc/dnsmasq.conf
# dnsmasq configuration for PiDNS

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

# Logging
log-queries
log-dhcp
log-async=50  # Async logging for better performance

# Performance optimizations
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

# Additional features
dhcp-rapid-commit
dhcp-option=option:ntp-server,0.0.0.0
```

## 5. Usage

### Accessing the Dashboard
1. **URL**: Open a web browser and navigate to `http://<pi-ip-address>:8080`
2. **Login**: Use the default username `admin` and password `password`
3. **Change Password**: It is recommended to change the default password after first login

### Dashboard Features
1. **Device List**: View all connected devices with their IP addresses, MAC addresses, and hostnames
2. **Device Details**: Click on a device to view more details
3. **DHCP Leases**: View all DHCP leases
4. **DNS Queries**: View recent DNS queries
5. **Ad-blocking**: Enable/disable ad-blocking and view blocked domains
6. **Settings**: Configure PiDNS settings

### Managing Devices
1. **View Devices**: The dashboard shows all connected devices
2. **Device Details**: Click on a device to view more details
3. **Reserve IP**: Reserve an IP address for a device by adding a static lease
4. **Block Device**: Block a device from connecting to the network

### Managing DNS
1. **View DNS Queries**: The dashboard shows recent DNS queries
2. **Add Custom DNS**: Add custom DNS entries
3. **Block Domains**: Block specific domains
4. **Enable Ad-blocking**: Enable or disable ad-blocking

### Managing DHCP
1. **View DHCP Leases**: The dashboard shows all DHCP leases
2. **Configure DHCP Range**: Configure the DHCP range
3. **Add Static Lease**: Add a static lease for a device
4. **Configure DHCP Options**: Configure DHCP options such as DNS server and router

## 6. Container Management

### Docker Management
```bash
# Start Docker containers
./scripts/container-management.sh start pi-4

# Stop Docker containers
./scripts/container-management.sh stop

# Restart Docker containers
./scripts/container-management.sh restart pi-4

# View Docker container status
./scripts/container-management.sh status

# View Docker container logs
./scripts/container-management.sh logs

# Backup Docker containers
./scripts/container-management.sh backup ./backup

# Restore Docker containers
./scripts/container-management.sh restore ./backup

# Migrate from Docker to Podman
./scripts/container-management.sh migrate docker podman pi-4
```

### Podman Management
```bash
# Start Podman containers
./scripts/container-management.sh start pi-4

# Stop Podman containers
./scripts/container-management.sh stop

# Restart Podman containers
./scripts/container-management.sh restart pi-4

# View Podman container status
./scripts/container-management.sh status

# View Podman container logs
./scripts/container-management.sh logs

# Backup Podman containers
./scripts/container-management.sh backup ./backup

# Restore Podman containers
./scripts/container-management.sh restore ./backup

# Migrate from Podman to Docker
./scripts/container-management.sh migrate podman docker pi-4
```

### LXC Management
```bash
# Start LXC container
./scripts/container-management.sh start pi-4

# Stop LXC container
./scripts/container-management.sh stop

# Restart LXC container
./scripts/container-management.sh restart pi-4

# View LXC container status
./scripts/container-management.sh status

# View LXC container logs
./scripts/container-management.sh logs

# Backup LXC container
./scripts/container-management.sh backup ./backup

# Restore LXC container
./scripts/container-management.sh restore ./backup

# Migrate from LXC to Docker
./scripts/container-management.sh migrate lxc docker pi-4
```

## 7. Troubleshooting

### Common Issues
1. **Dashboard Not Accessible**: Check if the Flask app is running and if the port is open
2. **DNS Not Working**: Check if dnsmasq is running and if the configuration is correct
3. **DHCP Not Working**: Check if dnsmasq is running and if the DHCP range is correct
4. **Ad-blocking Not Working**: Check if the ad-blocker service is running and if the configuration is correct
5. **Container Issues**: Check if the container runtime is installed and if the container is running

### Log Files
1. **Flask App Logs**: `/var/log/pidns/app.log`
2. **dnsmasq Logs**: `/var/log/syslog` (or use `journalctl -u dnsmasq`)
3. **Systemd Service Logs**: `journalctl -u pidns`
4. **Docker Logs**: `docker logs pidns`
5. **Podman Logs**: `podman logs pidns`
6. **LXC Logs**: `lxc-attach -n pidns -- tail -f /var/log/pidns/app.log`

### Debugging Steps
1. **Check Service Status**: Use `systemctl status` to check if services are running
2. **Check Logs**: Use `journalctl` or check log files for error messages
3. **Check Configuration**: Verify that configuration files are correct
4. **Check Network**: Use `ping` and `nslookup` to test network connectivity
5. **Check Containers**: Use container-specific commands to check container status

### Resetting PiDNS
```bash
# Stop PiDNS services
sudo systemctl stop pidns
sudo systemctl stop dnsmasq

# Remove configuration files
sudo rm /etc/dnsmasq.conf
sudo rm /etc/systemd/system/pidns.service

# Remove data files
sudo rm -rf /var/lib/misc/dnsmasq.leases
sudo rm -rf /var/log/pidns

# Reload systemd
sudo systemctl daemon-reload

# Reinstall PiDNS
./scripts/install.sh
```

## 8. Development

### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/PiDNS.git
cd PiDNS

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements_adblocker.txt
pip install -r requirements_dev.txt

# Generate configuration files
python3 scripts/generate_config.py --device standard-pc --container none

# Copy configuration files
cp config/flask_config.standard_pc.py config/flask_config.py
cp config/dnsmasq.standard_pc.conf /etc/dnsmasq.conf
cp services/pidns.standard_pc.service /etc/systemd/system/pidns.service

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable pidns.service
sudo systemctl enable dnsmasq.service
sudo systemctl start pidns.service
sudo systemctl start dnsmasq.service
```

### Running Tests
```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Run all tests
python -m pytest tests/

# Run tests with coverage
python -m pytest --cov=app tests/
```

### Building Documentation
```bash
# Install documentation dependencies
pip install -r requirements_docs.txt

# Build documentation
cd docs
make html

# View documentation
open _build/html/index.html
```

### Contributing
1. **Fork the Repository**: Fork the repository on GitHub
2. **Create a Branch**: Create a new branch for your changes
3. **Make Changes**: Make your changes and test them
4. **Submit a Pull Request**: Submit a pull request to the main repository

### Code Style
1. **Python**: Follow PEP 8 style guidelines
2. **JavaScript**: Follow ESLint style guidelines
3. **HTML**: Follow W3C standards
4. **CSS**: Follow BEM methodology

## 9. Security

### Authentication
1. **Default Credentials**: The default username is `admin` and password is `password`
2. **Change Password**: It is recommended to change the default password after first login
3. **Password Strength**: Use a strong password with at least 8 characters, including uppercase, lowercase, numbers, and special characters

### Network Security
1. **Firewall**: Configure a firewall to restrict access to the dashboard
2. **HTTPS**: Use HTTPS to encrypt traffic to the dashboard
3. **VPN**: Use a VPN to access the dashboard remotely
4. **Network Segmentation**: Use network segmentation to isolate the PiDNS server

### Container Security
1. **Non-root User**: Run containers as a non-root user
2. **Capability Management**: Limit capabilities to only what's needed
3. **Read-only Filesystem**: Use read-only filesystem where possible
4. **Resource Limits**: Set appropriate memory and CPU limits
5. **Network Isolation**: Use appropriate network settings

### System Security
1. **System Updates**: Keep the system up to date with security patches
2. **User Permissions**: Use appropriate user permissions
3. **Service Isolation**: Isolate services from each other
4. **Log Monitoring**: Monitor logs for suspicious activity

## 10. Performance Optimization

### Device-Specific Optimization
1. **Raspberry Pi Zero W/2W**: Use minimal configuration to conserve resources
2. **Raspberry Pi 3**: Use moderate configuration for balanced performance
3. **Raspberry Pi 4/5**: Use full configuration for maximum performance
4. **Low-Resource PC**: Use moderate configuration for balanced performance
5. **Standard PC**: Use full configuration for maximum performance

### Flask Optimization
1. **Threading**: Use appropriate number of threads based on device capabilities
2. **Caching**: Use caching to reduce database queries
3. **Static Files**: Serve static files efficiently
4. **Database Optimization**: Use database indexes and query optimization

### dnsmasq Optimization
1. **Cache Size**: Use appropriate cache size based on device capabilities
2. **Logging**: Use appropriate logging level based on device capabilities
3. **DNS Forwarding**: Use appropriate DNS forwarding settings based on device capabilities
4. **DHCP Range**: Use appropriate DHCP range based on network size

### Container Optimization
1. **Resource Limits**: Set appropriate memory and CPU limits
2. **Image Size**: Use minimal base images to reduce image size
3. **Volume Management**: Use appropriate volume types for data persistence
4. **Network Configuration**: Use appropriate network settings

## 11. Backup and Recovery

### Backup Strategies
1. **Configuration Backup**: Backup configuration files regularly
2. **Data Backup**: Backup data files regularly
3. **Container Backup**: Backup containers regularly
4. **System Backup**: Backup the entire system regularly

### Backup Tools
```bash
# Backup configuration files
sudo tar -czf pidns-config-$(date +%Y%m%d).tar.gz /etc/dnsmasq.conf /etc/systemd/system/pidns.service

# Backup data files
sudo tar -czf pidns-data-$(date +%Y%m%d).tar.gz /var/lib/misc/dnsmasq.leases /var/log/pidns

# Backup Docker containers
./scripts/container-management.sh backup ./backup

# Backup the entire system
sudo dd if=/dev/mmcblk0 of=pidns-system-$(date +%Y%m%d).img bs=4M status=progress
```

### Recovery Strategies
1. **Configuration Recovery**: Restore configuration files from backup
2. **Data Recovery**: Restore data files from backup
3. **Container Recovery**: Restore containers from backup
4. **System Recovery**: Restore the entire system from backup

### Recovery Tools
```bash
# Restore configuration files
sudo tar -xzf pidns-config-$(date +%Y%m%d).tar.gz -C /

# Restore data files
sudo tar -xzf pidns-data-$(date +%Y%m%d).tar.gz -C /

# Restore Docker containers
./scripts/container-management.sh restore ./backup

# Restore the entire system
sudo dd if=pidns-system-$(date +%Y%m%d).img of=/dev/mmcblk0 bs=4M status=progress
```

## 12. Frequently Asked Questions (FAQ)

### General Questions
1. **What is PiDNS?**
   PiDNS is a lightweight, easy-to-use DNS and DHCP server solution designed for Raspberry Pi and other low-resource devices.

2. **What are the system requirements for PiDNS?**
   PiDNS requires a Raspberry Pi or PC with at least 512MB RAM and 4GB free storage.

3. **Is PiDNS free?**
   Yes, PiDNS is open-source software released under the MIT license.

4. **How do I get support for PiDNS?**
   You can get support by creating an issue on the GitHub repository or by joining the PiDNS community forum.

### Installation Questions
1. **How do I install PiDNS?**
   You can install PiDNS by running the installation script: `./scripts/install.sh`

2. **Can I install PiDNS on a PC?**
   Yes, PiDNS can be installed on a PC running a Debian-based Linux distribution.

3. **Can I install PiDNS without containers?**
   Yes, PiDNS can be installed without containers by selecting the "none" container type during installation.

4. **How do I uninstall PiDNS?**
   You can uninstall PiDNS by running the uninstallation script: `./scripts/uninstall.sh`

### Configuration Questions
1. **How do I change the default password?**
   You can change the default password by logging in to the dashboard and navigating to the settings page.

2. **How do I configure the DHCP range?**
   You can configure the DHCP range by editing the dnsmasq configuration file: `/etc/dnsmasq.conf`

3. **How do I add a static DHCP lease?**
   You can add a static DHCP lease by adding a line to the dnsmasq configuration file: `dhcp-host=<mac-address>,<ip-address>,<hostname>`

4. **How do I enable ad-blocking?**
   You can enable ad-blocking by navigating to the ad-blocking page in the dashboard and clicking the "Enable" button.

### Troubleshooting Questions
1. **Why can't I access the dashboard?**
   There are several reasons why you might not be able to access the dashboard:
   - The Flask app is not running
   - The port is blocked by a firewall
   - The IP address has changed
   - The device is not connected to the network

2. **Why is DNS not working?**
   There are several reasons why DNS might not be working:
   - The dnsmasq service is not running
   - The dnsmasq configuration is incorrect
   - The DNS servers are not reachable
   - The network is not configured correctly

3. **Why is DHCP not working?**
   There are several reasons why DHCP might not be working:
   - The dnsmasq service is not running
   - The dnsmasq configuration is incorrect
   - The DHCP range is exhausted
   - The network is not configured correctly

4. **Why is ad-blocking not working?**
   There are several reasons why ad-blocking might not be working:
   - The ad-blocker service is not running
   - The ad-blocker configuration is incorrect
   - The ad-blocker lists are not up to date
   - The DNS queries are not being routed through the ad-blocker

## 13. Glossary

### Terms
1. **DNS**: Domain Name System, a hierarchical decentralized naming system for computers, services, or any resource connected to the Internet or a private network.
2. **DHCP**: Dynamic Host Configuration Protocol, a network management protocol used to automate the process of configuring devices on IP networks.
3. **Dashboard**: A web-based user interface for monitoring and managing PiDNS.
4. **Container**: A lightweight, standalone, executable package of software that includes everything needed to run it.
5. **Docker**: A platform for developing, shipping, and running applications in containers.
6. **Podman**: A daemonless container engine for developing, managing, and running OCI Containers on your Linux System.
7. **LXC**: Linux Containers, an operating-system-level virtualization method for running multiple isolated Linux systems on a single control host.
8. **Systemd**: A system and service manager for Linux operating systems.
9. **dnsmasq**: A lightweight, easy to configure DNS forwarder, DHCP server, and router advertisement subsystem.
10. **Flask**: A micro web framework for Python.

### Acronyms
1. **PiDNS**: Private DNS
2. **DNS**: Domain Name System
3. **DHCP**: Dynamic Host Configuration Protocol
4. **IP**: Internet Protocol
5. **MAC**: Media Access Control
6. **HTTP**: Hypertext Transfer Protocol
7. **HTTPS**: Hypertext Transfer Protocol Secure
8. **API**: Application Programming Interface
9. **CLI**: Command Line Interface
10. **GUI**: Graphical User Interface

## 14. References

### Documentation
1. **dnsmasq Documentation**: http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html
2. **Flask Documentation**: https://flask.palletsprojects.com/
3. **Docker Documentation**: https://docs.docker.com/
4. **Podman Documentation**: https://podman.io/
5. **LXC Documentation**: https://linuxcontainers.org/lxc/introduction/

### Community
1. **PiDNS GitHub Repository**: https://github.com/yourusername/PiDNS
2. **PiDNS Community Forum**: https://forum.pidns.org/
3. **PiDNS Discord Server**: https://discord.gg/pidns
4. **PiDNS Reddit**: https://www.reddit.com/r/pidns/

### Related Projects
1. **Pi-hole**: A network-wide ad blocking DNS server
2. **AdGuard Home**: A network-wide ad and tracker blocking DNS server
3. **BIND**: A widely used DNS server software
4. **Unbound**: A validating, recursive, and caching DNS resolver
5. **Kea**: A high-performance, open source DHCP server
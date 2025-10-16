# PiDNS Container Support Design

## 1. Container Support Overview

### Design Goals
1. **Flexibility**: Support multiple container types (Docker, Podman, LXC)
2. **Consistency**: Ensure consistent behavior across container types
3. **Performance**: Optimize for each container type's strengths
4. **Portability**: Allow easy migration between container types
5. **Security**: Implement appropriate security measures for each container type

### Container Types
1. **Docker**: Most popular container platform with wide community support
2. **Podman**: Daemonless, rootless containers with better security
3. **LXC**: Lightweight OS-level virtualization with better performance

### Container Selection Criteria
1. **Resource Constraints**: Choose container type based on available resources
2. **Security Requirements**: Select container type based on security needs
3. **Performance Needs**: Optimize for performance requirements
4. **User Preference**: Allow users to choose based on familiarity

## 2. Docker Support Design

### Docker Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Host                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Docker CLI   │  │  Docker Daemon  │  │  Container  │ │
│  │                │  │                │  │   Runtime   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│           │                     │                     │    │
│           └─────────────────────┼─────────────────────┘    │
│                                 │                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 PiDNS Container                     │ │
│  │                                                     │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │ │
│  │  │   Flask     │  │   dnsmasq   │  │  Ad-blocker │ │ │
│  │  │  Dashboard   │  │   Service   │  │   Service   │ │ │
│  │  │             │  │             │  │             │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Docker Components
1. **Dockerfile**: Multi-stage build for optimized image size
2. **docker-compose.yml**: Main compose file for service orchestration
3. **docker-compose.override.{device_type}.yml**: Device-specific overrides
4. **pidns-docker.service**: Systemd service for Docker containers

### Docker Configuration
```dockerfile
# Dockerfile
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

```yaml
# docker-compose.override.pi-4.yml
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

```ini
# pidns-docker.service
[Unit]
Description=PiDNS Docker Container
After=docker.service network-online.target
Requires=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/PiDNS
ExecStart=/usr/bin/docker-compose -f docker-compose.yml -f docker-compose.override.${DEVICE_TYPE}.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.yml -f docker-compose.override.${DEVICE_TYPE}.yml down
TimeoutStartSec=0
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Docker Security Configuration
1. **Non-root User**: Run containers as non-root user
2. **Capability Management**: Limit capabilities to only what's needed
3. **Read-only Filesystem**: Use read-only filesystem where possible
4. **Resource Limits**: Set appropriate memory and CPU limits
5. **Network Isolation**: Use appropriate network settings

### Docker Performance Optimization
1. **Multi-stage Build**: Reduce image size
2. **Resource Limits**: Set appropriate limits for each device type
3. **Health Checks**: Monitor container health
4. **Volume Management**: Use appropriate volume types for data persistence

### Docker Management Commands
```bash
# Build Docker image
docker build -t pidns:latest .

# Run Docker container
docker run -d \
    --name pidns \
    --network host \
    --cap-add NET_ADMIN \
    -v pidns-data:/app/data \
    -v pidns-logs:/var/log/pidns \
    -v pidns-config:/app/config \
    -v /var/lib/misc:/var/lib/misc:rw \
    -v /etc/dnsmasq.conf:/etc/dnsmasq.conf:rw \
    -e FLASK_ENV=production \
    -e PIDNS_USERNAME=admin \
    -e PIDNS_PASSWORD=password \
    -e DEVICE_TYPE=pi-4 \
    pidns:latest

# Start Docker Compose
docker-compose -f docker-compose.yml -f docker-compose.override.pi-4.yml up -d

# Stop Docker Compose
docker-compose -f docker-compose.yml -f docker-compose.override.pi-4.yml down

# View Docker logs
docker logs pidns

# Restart Docker container
docker restart pidns

# Remove Docker container
docker stop pidns && docker rm pidns
```

## 3. Podman Support Design

### Podman Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    Podman Host                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Podman CLI  │  │  Podman Service│  │  Container  │ │
│  │                │  │                │  │   Runtime   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│           │                     │                     │    │
│           └─────────────────────┼─────────────────────┘    │
│                                 │                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 PiDNS Container                     │ │
│  │                                                     │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │ │
│  │  │   Flask     │  │   dnsmasq   │  │  Ad-blocker │ │ │
│  │  │  Dashboard   │  │   Service   │  │   Service   │ │ │
│  │  │             │  │             │  │             │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Podman Components
1. **Containerfile**: Build file for Podman images
2. **podman-compose.yml**: Main compose file for service orchestration
3. **podman-compose.override.{device_type}.yml**: Device-specific overrides
4. **pidns-podman.service**: Systemd service for Podman containers
5. **pidns.container**: Quadlet file for rootless containers

### Podman Configuration
```containerfile
# Containerfile
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

```yaml
# podman-compose.override.pi-4.yml
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

```ini
# pidns-podman.service
[Unit]
Description=PiDNS Podman Container
After=network-online.target
Requires=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/PiDNS
ExecStart=/usr/bin/podman-compose -f podman-compose.yml -f podman-compose.override.${DEVICE_TYPE}.yml up -d
ExecStop=/usr/bin/podman-compose -f podman-compose.yml -f podman-compose.override.${DEVICE_TYPE}.yml down
TimeoutStartSec=0
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

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
Environment=DEVICE_TYPE=pi-4
UserNS=keep-id

[Service]
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

### Podman Security Configuration
1. **Rootless Containers**: Run containers without root privileges
2. **SELinux Labeling**: Use SELinux labels for file access control
3. **Capability Management**: Limit capabilities to only what's needed
4. **User Namespace Mapping**: Map container user to host user
5. **Network Isolation**: Use appropriate network settings

### Podman Performance Optimization
1. **Slim Base Image**: Use minimal base image
2. **Resource Limits**: Set appropriate limits for each device type
3. **Quadlet Integration**: Use systemd for better service management
4. **Volume Management**: Use appropriate volume types for data persistence

### Podman Management Commands
```bash
# Build Podman image
podman build -t pidns:latest .

# Run Podman container
podman run -d \
    --name pidns \
    --network host \
    --cap-add NET_ADMIN \
    -v pidns-data:/app/data:z \
    -v pidns-logs:/var/log/pidns:z \
    -v pidns-config:/app/config:z \
    -v /var/lib/misc:/var/lib/misc:rw,z \
    -v /etc/dnsmasq.conf:/etc/dnsmasq.conf:rw,z \
    -e FLASK_ENV=production \
    -e PIDNS_USERNAME=admin \
    -e PIDNS_PASSWORD=password \
    -e DEVICE_TYPE=pi-4 \
    --userns keep-id \
    pidns:latest

# Start Podman Compose
podman-compose -f podman-compose.yml -f podman-compose.override.pi-4.yml up -d

# Stop Podman Compose
podman-compose -f podman-compose.yml -f podman-compose.override.pi-4.yml down

# View Podman logs
podman logs pidns

# Restart Podman container
podman restart pidns

# Remove Podman container
podman stop pidns && podman rm pidns

# Generate Quadlet file
podman generate systemd --name pidns --files
```

## 4. LXC Support Design

### LXC Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    LXC Host                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │    LXC CLI    │  │   LXC Daemon   │  │  Container  │ │
│  │                │  │                │  │   Runtime   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│           │                     │                     │    │
│           └─────────────────────┼─────────────────────┘    │
│                                 │                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 PiDNS Container                     │ │
│  │                                                     │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │ │
│  │  │   Flask     │  │   dnsmasq   │  │  Ad-blocker │ │ │
│  │  │  Dashboard   │  │   Service   │  │   Service   │ │ │
│  │  │             │  │             │  │             │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### LXC Components
1. **lxc-{device_type}.conf**: LXC configuration files for each device type
2. **lxc-setup.sh**: Setup script for LXC containers
3. **pidns-lxc.service**: Systemd service for LXC containers

### LXC Configuration
```conf
# lxc-pi-4.conf
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

```bash
#!/bin/bash
# lxc-setup.sh - LXC setup script for PiDNS

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

```ini
# pidns-lxc.service
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

### LXC Security Configuration
1. **Capability Dropping**: Drop unnecessary capabilities
2. **AppArmor Profiles**: Use AppArmor for additional security
3. **Device Restrictions**: Limit access to devices
4. **Resource Limits**: Set appropriate resource limits
5. **Network Isolation**: Use appropriate network settings

### LXC Performance Optimization
1. **Resource Limits**: Set appropriate limits for each device type
2. **Filesystem Mounts**: Use bind mounts for better performance
3. **Network Configuration**: Use appropriate network settings
4. **Autostart Configuration**: Configure container to start automatically

### LXC Management Commands
```bash
# Create LXC container
lxc-create -n pidns -t download -- -d debian -r bullseye -a armhf

# Start LXC container
lxc-start -n pidns -d

# Stop LXC container
lxc-stop -n pidns

# Restart LXC container
lxc-stop -n pidns && lxc-start -n pidns -d

# View LXC container info
lxc-info -n pidns

# Access LXC container shell
lxc-attach -n pidns

# Copy files to LXC container
lxc-file-push /path/to/local/file pidns /path/to/container/file

# Copy files from LXC container
lxc-file-pull pidns /path/to/container/file /path/to/local/file

# Remove LXC container
lxc-stop -n pidns && lxc-destroy -n pidns
```

## 5. Container Selection Logic

### Container Selection Criteria
1. **Device Type**: Different containers work better on different devices
2. **Resource Availability**: Choose container based on available resources
3. **Security Requirements**: Select container based on security needs
4. **User Preference**: Allow users to choose based on familiarity

### Container Selection Algorithm
```python
# scripts/container_selection.py
#!/usr/bin/env python3
"""
Container selection logic for PiDNS
"""

import os
import sys
import subprocess
from typing import Dict, List, Optional, Tuple

def check_container_availability(container_type: str) -> bool:
    """Check if a container type is available on the system"""
    try:
        if container_type == "docker":
            subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif container_type == "podman":
            subprocess.run(["podman", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif container_type == "lxc":
            subprocess.run(["lxc-info", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            return False
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_system_resources() -> Dict[str, int]:
    """Get system resources (memory in MB, CPU cores)"""
    try:
        # Get total memory in MB
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemTotal:'):
                    total_mem_kb = int(line.split()[1])
                    total_mem_mb = total_mem_kb // 1024
                    break
        
        # Get CPU cores
        cpu_cores = os.cpu_count()
        
        return {
            'memory_mb': total_mem_mb,
            'cpu_cores': cpu_cores
        }
    except (FileNotFoundError, ValueError, IndexError):
        # Default values if unable to determine
        return {
            'memory_mb': 1024,
            'cpu_cores': 2
        }

def get_device_type() -> str:
    """Get the device type"""
    try:
        # Check if we're running on a Raspberry Pi
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip()
        
        if "Raspberry Pi Zero W" in model:
            return "pi-zero"
        elif "Raspberry Pi Zero 2 W" in model:
            return "pi-zero-2w"
        elif "Raspberry Pi 3" in model:
            return "pi-3"
        elif "Raspberry Pi 4" in model:
            return "pi-4"
        elif "Raspberry Pi 5" in model:
            return "pi-5"
        else:
            # Not a Raspberry Pi, determine based on resources
            resources = get_system_resources()
            
            if resources['memory_mb'] <= 1024 and resources['cpu_cores'] <= 2:
                return "low-resource-pc"
            else:
                return "standard-pc"
    except FileNotFoundError:
        # Not a Raspberry Pi, determine based on resources
        resources = get_system_resources()
        
        if resources['memory_mb'] <= 1024 and resources['cpu_cores'] <= 2:
            return "low-resource-pc"
        else:
            return "standard-pc"

def get_recommended_container(device_type: str) -> List[str]:
    """Get recommended container types for a device type"""
    recommendations = {
        "pi-zero": ["docker", "lxc"],
        "pi-zero-2w": ["docker", "lxc"],
        "pi-3": ["docker", "podman", "lxc"],
        "pi-4": ["docker", "podman", "lxc"],
        "pi-5": ["docker", "podman", "lxc"],
        "low-resource-pc": ["docker", "podman", "lxc"],
        "standard-pc": ["docker", "podman", "lxc"]
    }
    
    return recommendations.get(device_type, ["docker", "podman", "lxc"])

def get_available_containers() -> List[str]:
    """Get list of available container types"""
    available = []
    
    for container_type in ["docker", "podman", "lxc"]:
        if check_container_availability(container_type):
            available.append(container_type)
    
    return available

def select_container(device_type: str, preferred_container: Optional[str] = None) -> str:
    """Select the best container type for the device"""
    # Get recommended containers for the device type
    recommended = get_recommended_container(device_type)
    
    # Get available containers on the system
    available = get_available_containers()
    
    # Find intersection of recommended and available
    candidates = [c for c in recommended if c in available]
    
    # If no candidates, use any available container
    if not candidates:
        candidates = available
    
    # If no containers available, return None
    if not candidates:
        return None
    
    # If preferred container is specified and available, use it
    if preferred_container and preferred_container in candidates:
        return preferred_container
    
    # Otherwise, use the first candidate
    return candidates[0]

def main():
    """Main function for testing"""
    device_type = get_device_type()
    print(f"Device type: {device_type}")
    
    recommended = get_recommended_container(device_type)
    print(f"Recommended containers: {', '.join(recommended)}")
    
    available = get_available_containers()
    print(f"Available containers: {', '.join(available)}")
    
    selected = select_container(device_type)
    print(f"Selected container: {selected}")

if __name__ == "__main__":
    main()
```

### Container Selection UI
```python
# scripts/container_selection_ui.py
#!/usr/bin/env python3
"""
Container selection UI for PiDNS installation
"""

import os
import sys
from typing import Dict, List, Optional

from container_selection import (
    check_container_availability,
    get_device_type,
    get_recommended_container,
    get_available_containers,
    select_container,
    get_system_resources
)

def display_container_info(container_type: str) -> None:
    """Display information about a container type"""
    info = {
        "docker": {
            "name": "Docker",
            "description": "Most popular container platform with wide community support",
            "pros": [
                "Wide community support",
                "Easy to use with Docker Compose",
                "Supports resource limits and health checks"
            ],
            "cons": [
                "Requires Docker daemon",
                "Runs as root by default"
            ]
        },
        "podman": {
            "name": "Podman",
            "description": "Daemonless, rootless containers with better security",
            "pros": [
                "Daemonless architecture",
                "Rootless containers by default",
                "Compatible with Docker CLI",
                "Better security model"
            ],
            "cons": [
                "Smaller community than Docker",
                "Fewer third-party tools"
            ]
        },
        "lxc": {
            "name": "LXC",
            "description": "Lightweight OS-level virtualization with better performance",
            "pros": [
                "Lightweight with low overhead",
                "Direct access to host kernel features",
                "Better performance for some workloads"
            ],
            "cons": [
                "More complex setup",
                "Fewer management tools"
            ]
        }
    }
    
    if container_type not in info:
        print(f"Unknown container type: {container_type}")
        return
    
    container = info[container_type]
    
    print(f"\n{container['name']}")
    print("=" * len(container['name']))
    print(f"Description: {container['description']}")
    print("\nPros:")
    for pro in container['pros']:
        print(f"  - {pro}")
    print("\nCons:")
    for con in container['cons']:
        print(f"  - {con}")

def display_device_info(device_type: str) -> None:
    """Display information about a device type"""
    info = {
        "pi-zero": {
            "name": "Raspberry Pi Zero W",
            "memory": "512MB",
            "cpu": "1-core ARM",
            "recommended_containers": ["Docker", "LXC"]
        },
        "pi-zero-2w": {
            "name": "Raspberry Pi Zero 2W",
            "memory": "512MB",
            "cpu": "1-core ARM",
            "recommended_containers": ["Docker", "LXC"]
        },
        "pi-3": {
            "name": "Raspberry Pi 3",
            "memory": "1GB",
            "cpu": "4-core ARM",
            "recommended_containers": ["Docker", "Podman", "LXC"]
        },
        "pi-4": {
            "name": "Raspberry Pi 4",
            "memory": "2-8GB",
            "cpu": "4-core ARM",
            "recommended_containers": ["Docker", "Podman", "LXC"]
        },
        "pi-5": {
            "name": "Raspberry Pi 5",
            "memory": "4-8GB",
            "cpu": "4-core ARM",
            "recommended_containers": ["Docker", "Podman", "LXC"]
        },
        "low-resource-pc": {
            "name": "Low-Resource PC",
            "memory": "≤1GB",
            "cpu": "≤2 cores",
            "recommended_containers": ["Docker", "Podman", "LXC"]
        },
        "standard-pc": {
            "name": "Standard PC",
            "memory": ">1GB",
            "cpu": ">2 cores",
            "recommended_containers": ["Docker", "Podman", "LXC"]
        }
    }
    
    if device_type not in info:
        print(f"Unknown device type: {device_type}")
        return
    
    device = info[device_type]
    
    print(f"\n{device['name']}")
    print("=" * len(device['name']))
    print(f"Memory: {device['memory']}")
    print(f"CPU: {device['cpu']}")
    print(f"Recommended containers: {', '.join(device['recommended_containers'])}")

def interactive_container_selection(device_type: str) -> str:
    """Interactively select a container type"""
    # Get available containers
    available = get_available_containers()
    
    # Get recommended containers for the device type
    recommended = get_recommended_container(device_type)
    
    # Filter recommended containers to only include available ones
    available_recommended = [c for c in recommended if c in available]
    
    print("\nContainer Selection")
    print("==================")
    
    # Display device information
    display_device_info(device_type)
    
    # Display available containers
    print("\nAvailable container types:")
    for i, container_type in enumerate(available, 1):
        marker = " (recommended)" if container_type in available_recommended else ""
        print(f"  {i}. {container_type.capitalize()}{marker}")
    
    # Get user selection
    while True:
        try:
            choice = input(f"\nSelect a container type (1-{len(available)}): ")
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(available):
                selected = available[choice_num - 1]
                
                # Display information about selected container
                display_container_info(selected)
                
                # Confirm selection
                confirm = input(f"\nUse {selected.capitalize()}? (y/n): ")
                if confirm.lower() in ['y', 'yes']:
                    return selected
            else:
                print(f"Please enter a number between 1 and {len(available)}")
        except ValueError:
            print("Please enter a valid number")

def main():
    """Main function for testing"""
    # Get device type
    device_type = get_device_type()
    
    # Interactively select container type
    selected = interactive_container_selection(device_type)
    
    print(f"\nSelected container: {selected}")
    print(f"Device type: {device_type}")

if __name__ == "__main__":
    main()
```

## 6. Container Migration

### Migration Strategy
1. **Data Migration**: Ensure data can be migrated between container types
2. **Configuration Migration**: Ensure configuration can be migrated between container types
3. **Service Migration**: Ensure services can be migrated between container types
4. **Rollback Plan**: Provide a way to rollback if migration fails

### Migration Tools
```python
# scripts/container_migration.py
#!/usr/bin/env python3
"""
Container migration tools for PiDNS
"""

import os
import sys
import subprocess
import shutil
import tarfile
import tempfile
from typing import Dict, List, Optional, Tuple

from container_selection import (
    check_container_availability,
    get_device_type,
    get_recommended_container,
    get_available_containers,
    select_container,
    get_system_resources
)

def backup_docker_data(backup_path: str) -> bool:
    """Backup Docker data"""
    try:
        # Create backup directory
        os.makedirs(backup_path, exist_ok=True)
        
        # Backup Docker volumes
        volumes = ["pidns-data", "pidns-logs", "pidns-config"]
        
        for volume in volumes:
            # Create a temporary container to backup the volume
            subprocess.run([
                "docker", "run", "--rm",
                "-v", f"{volume}:/data",
                "-v", f"{backup_path}:/backup",
                "alpine", "tar", "czf", f"/backup/{volume}.tar.gz", "-C", "/data", "."
            ], check=True)
        
        # Backup Docker container configuration
        subprocess.run([
            "docker", "inspect", "pidns"
        ], check=True, stdout=open(f"{backup_path}/pidns-inspect.json", "w"))
        
        return True
    except subprocess.CalledProcessError:
        return False

def restore_docker_data(backup_path: str) -> bool:
    """Restore Docker data"""
    try:
        # Restore Docker volumes
        volumes = ["pidns-data", "pidns-logs", "pidns-config"]
        
        for volume in volumes:
            # Create a temporary container to restore the volume
            subprocess.run([
                "docker", "run", "--rm",
                "-v", f"{volume}:/data",
                "-v", f"{backup_path}:/backup",
                "alpine", "tar", "xzf", f"/backup/{volume}.tar.gz", "-C", "/data"
            ], check=True)
        
        return True
    except subprocess.CalledProcessError:
        return False

def backup_podman_data(backup_path: str) -> bool:
    """Backup Podman data"""
    try:
        # Create backup directory
        os.makedirs(backup_path, exist_ok=True)
        
        # Backup Podman volumes
        volumes = ["pidns-data", "pidns-logs", "pidns-config"]
        
        for volume in volumes:
            # Create a temporary container to backup the volume
            subprocess.run([
                "podman", "run", "--rm",
                "-v", f"{volume}:/data:z",
                "-v", f"{backup_path}:/backup:z",
                "alpine", "tar", "czf", f"/backup/{volume}.tar.gz", "-C", "/data", "."
            ], check=True)
        
        # Backup Podman container configuration
        subprocess.run([
            "podman", "inspect", "pidns"
        ], check=True, stdout=open(f"{backup_path}/pidns-inspect.json", "w"))
        
        return True
    except subprocess.CalledProcessError:
        return False

def restore_podman_data(backup_path: str) -> bool:
    """Restore Podman data"""
    try:
        # Restore Podman volumes
        volumes = ["pidns-data", "pidns-logs", "pidns-config"]
        
        for volume in volumes:
            # Create a temporary container to restore the volume
            subprocess.run([
                "podman", "run", "--rm",
                "-v", f"{volume}:/data:z",
                "-v", f"{backup_path}:/backup:z",
                "alpine", "tar", "xzf", f"/backup/{volume}.tar.gz", "-C", "/data"
            ], check=True)
        
        return True
    except subprocess.CalledProcessError:
        return False

def backup_lxc_data(backup_path: str) -> bool:
    """Backup LXC data"""
    try:
        # Create backup directory
        os.makedirs(backup_path, exist_ok=True)
        
        # Stop LXC container
        subprocess.run(["lxc-stop", "-n", "pidns"], check=True)
        
        # Backup LXC container
        subprocess.run([
            "lxc-copy", "-n", "pidns", "-B", f"{backup_path}/pidns-backup"
        ], check=True)
        
        # Start LXC container
        subprocess.run(["lxc-start", "-n", "pidns", "-d"], check=True)
        
        return True
    except subprocess.CalledProcessError:
        return False

def restore_lxc_data(backup_path: str) -> bool:
    """Restore LXC data"""
    try:
        # Remove existing LXC container if it exists
        if subprocess.run(["lxc-info", "-n", "pidns"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            subprocess.run(["lxc-stop", "-n", "pidns"], check=True)
            subprocess.run(["lxc-destroy", "-n", "pidns"], check=True)
        
        # Restore LXC container from backup
        subprocess.run([
            "lxc-copy", "-n", "pidns-backup", "-R"
        ], check=True)
        
        # Start LXC container
        subprocess.run(["lxc-start", "-n", "pidns", "-d"], check=True)
        
        return True
    except subprocess.CalledProcessError:
        return False

def migrate_docker_to_podman(device_type: str) -> bool:
    """Migrate from Docker to Podman"""
    try:
        # Create temporary backup directory
        with tempfile.TemporaryDirectory() as backup_dir:
            # Backup Docker data
            if not backup_docker_data(backup_dir):
                return False
            
            # Stop Docker containers
            subprocess.run(["docker-compose", "down"], check=True)
            
            # Start Podman containers
            subprocess.run([
                "podman-compose", "-f", "podman-compose.yml", 
                "-f", f"podman-compose.override.{device_type}.yml", 
                "up", "-d"
            ], check=True)
            
            # Restore data to Podman
            if not restore_podman_data(backup_dir):
                return False
            
            return True
    except subprocess.CalledProcessError:
        return False

def migrate_podman_to_docker(device_type: str) -> bool:
    """Migrate from Podman to Docker"""
    try:
        # Create temporary backup directory
        with tempfile.TemporaryDirectory() as backup_dir:
            # Backup Podman data
            if not backup_podman_data(backup_dir):
                return False
            
            # Stop Podman containers
            subprocess.run(["podman-compose", "down"], check=True)
            
            # Start Docker containers
            subprocess.run([
                "docker-compose", "-f", "docker-compose.yml", 
                "-f", f"docker-compose.override.{device_type}.yml", 
                "up", "-d"
            ], check=True)
            
            # Restore data to Docker
            if not restore_docker_data(backup_dir):
                return False
            
            return True
    except subprocess.CalledProcessError:
        return False

def migrate_docker_to_lxc(device_type: str) -> bool:
    """Migrate from Docker to LXC"""
    try:
        # Create temporary backup directory
        with tempfile.TemporaryDirectory() as backup_dir:
            # Backup Docker data
            if not backup_docker_data(backup_dir):
                return False
            
            # Stop Docker containers
            subprocess.run(["docker-compose", "down"], check=True)
            
            # Setup LXC container
            subprocess.run(["./scripts/lxc-setup.sh", device_type], check=True)
            
            # Restore data to LXC
            if not restore_lxc_data(backup_dir):
                return False
            
            return True
    except subprocess.CalledProcessError:
        return False

def migrate_lxc_to_docker(device_type: str) -> bool:
    """Migrate from LXC to Docker"""
    try:
        # Create temporary backup directory
        with tempfile.TemporaryDirectory() as backup_dir:
            # Backup LXC data
            if not backup_lxc_data(backup_dir):
                return False
            
            # Stop LXC container
            subprocess.run(["lxc-stop", "-n", "pidns"], check=True)
            
            # Start Docker containers
            subprocess.run([
                "docker-compose", "-f", "docker-compose.yml", 
                "-f", f"docker-compose.override.{device_type}.yml", 
                "up", "-d"
            ], check=True)
            
            # Restore data to Docker
            if not restore_docker_data(backup_dir):
                return False
            
            return True
    except subprocess.CalledProcessError:
        return False

def migrate_podman_to_lxc(device_type: str) -> bool:
    """Migrate from Podman to LXC"""
    try:
        # Create temporary backup directory
        with tempfile.TemporaryDirectory() as backup_dir:
            # Backup Podman data
            if not backup_podman_data(backup_dir):
                return False
            
            # Stop Podman containers
            subprocess.run(["podman-compose", "down"], check=True)
            
            # Setup LXC container
            subprocess.run(["./scripts/lxc-setup.sh", device_type], check=True)
            
            # Restore data to LXC
            if not restore_lxc_data(backup_dir):
                return False
            
            return True
    except subprocess.CalledProcessError:
        return False

def migrate_lxc_to_podman(device_type: str) -> bool:
    """Migrate from LXC to Podman"""
    try:
        # Create temporary backup directory
        with tempfile.TemporaryDirectory() as backup_dir:
            # Backup LXC data
            if not backup_lxc_data(backup_dir):
                return False
            
            # Stop LXC container
            subprocess.run(["lxc-stop", "-n", "pidns"], check=True)
            
            # Start Podman containers
            subprocess.run([
                "podman-compose", "-f", "podman-compose.yml", 
                "-f", f"podman-compose.override.{device_type}.yml", 
                "up", "-d"
            ], check=True)
            
            # Restore data to Podman
            if not restore_podman_data(backup_dir):
                return False
            
            return True
    except subprocess.CalledProcessError:
        return False

def migrate_container(source_container: str, target_container: str, device_type: str) -> bool:
    """Migrate from one container type to another"""
    if source_container == target_container:
        print("Source and target container types are the same. No migration needed.")
        return True
    
    print(f"Migrating from {source_container} to {target_container}...")
    
    if source_container == "docker" and target_container == "podman":
        return migrate_docker_to_podman(device_type)
    elif source_container == "podman" and target_container == "docker":
        return migrate_podman_to_docker(device_type)
    elif source_container == "docker" and target_container == "lxc":
        return migrate_docker_to_lxc(device_type)
    elif source_container == "lxc" and target_container == "docker":
        return migrate_lxc_to_docker(device_type)
    elif source_container == "podman" and target_container == "lxc":
        return migrate_podman_to_lxc(device_type)
    elif source_container == "lxc" and target_container == "podman":
        return migrate_lxc_to_podman(device_type)
    else:
        print(f"Unsupported migration from {source_container} to {target_container}")
        return False

def main():
    """Main function for testing"""
    if len(sys.argv) != 4:
        print("Usage: python container_migration.py <source_container> <target_container> <device_type>")
        print("Supported container types: docker, podman, lxc")
        print("Supported device types: pi-zero, pi-zero-2w, pi-3, pi-4, pi-5, low-resource-pc, standard-pc")
        sys.exit(1)
    
    source_container = sys.argv[1]
    target_container = sys.argv[2]
    device_type = sys.argv[3]
    
    if migrate_container(source_container, target_container, device_type):
        print(f"Migration from {source_container} to {target_container} completed successfully.")
        sys.exit(0)
    else:
        print(f"Migration from {source_container} to {target_container} failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Migration UI
```python
# scripts/container_migration_ui.py
#!/usr/bin/env python3
"""
Container migration UI for PiDNS
"""

import os
import sys
from typing import Dict, List, Optional

from container_selection import (
    check_container_availability,
    get_device_type,
    get_recommended_container,
    get_available_containers,
    select_container,
    get_system_resources
)

from container_migration import (
    backup_docker_data,
    restore_docker_data,
    backup_podman_data,
    restore_podman_data,
    backup_lxc_data,
    restore_lxc_data,
    migrate_docker_to_podman,
    migrate_podman_to_docker,
    migrate_docker_to_lxc,
    migrate_lxc_to_docker,
    migrate_podman_to_lxc,
    migrate_lxc_to_podman,
    migrate_container
)

def get_current_container() -> Optional[str]:
    """Get the current container type"""
    # Check if Docker is running
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], 
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "pidns" in result.stdout.decode():
            return "docker"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Check if Podman is running
    try:
        result = subprocess.run(["podman", "ps", "--format", "{{.Names}}"], 
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "pidns" in result.stdout.decode():
            return "podman"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Check if LXC is running
    try:
        result = subprocess.run(["lxc-info", "-n", "pidns", "-s"], 
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "RUNNING" in result.stdout.decode():
            return "lxc"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return None

def interactive_container_migration() -> bool:
    """Interactively migrate between container types"""
    # Get device type
    device_type = get_device_type()
    
    # Get current container type
    current_container = get_current_container()
    
    if not current_container:
        print("PiDNS is not currently running in any container.")
        return False
    
    # Get available containers
    available = get_available_containers()
    
    # Remove current container from available options
    available = [c for c in available if c != current_container]
    
    if not available:
        print(f"No other container types are available on this system.")
        return False
    
    print("\nContainer Migration")
    print("==================")
    
    # Display current container information
    print(f"Current container type: {current_container.capitalize()}")
    
    # Display available container types
    print("\nAvailable target container types:")
    for i, container_type in enumerate(available, 1):
        print(f"  {i}. {container_type.capitalize()}")
    
    # Get user selection
    while True:
        try:
            choice = input(f"\nSelect a target container type (1-{len(available)}): ")
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(available):
                target_container = available[choice_num - 1]
                
                # Confirm migration
                confirm = input(f"\nMigrate from {current_container.capitalize()} to {target_container.capitalize()}? (y/n): ")
                if confirm.lower() in ['y', 'yes']:
                    break
            else:
                print(f"Please enter a number between 1 and {len(available)}")
        except ValueError:
            print("Please enter a valid number")
    
    # Perform migration
    print(f"\nMigrating from {current_container.capitalize()} to {target_container.capitalize()}...")
    print("This may take a few minutes...")
    
    if migrate_container(current_container, target_container, device_type):
        print(f"\nMigration from {current_container.capitalize()} to {target_container.capitalize()} completed successfully.")
        return True
    else:
        print(f"\nMigration from {current_container.capitalize()} to {target_container.capitalize()} failed.")
        return False

def main():
    """Main function for testing"""
    if interactive_container_migration():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## 7. Container Management

### Management Commands
```bash
#!/bin/bash
# container-management.sh - Container management commands for PiDNS

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

# Function to get current container type
get_current_container() {
    # Check if Docker is running
    if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^pidns$"; then
        echo "docker"
        return 0
    fi
    
    # Check if Podman is running
    if podman ps --format '{{.Names}}' 2>/dev/null | grep -q "^pidns$"; then
        echo "podman"
        return 0
    fi
    
    # Check if LXC is running
    if lxc-info -n pidns -s 2>/dev/null | grep -q "RUNNING"; then
        echo "lxc"
        return 0
    fi
    
    echo "none"
    return 1
}

# Function to start containers
start_containers() {
    local container_type=$1
    local device_type=$2
    
    print_step "Starting PiDNS containers..."
    
    case $container_type in
        "docker")
            print_status "Starting Docker containers..."
            docker-compose -f docker-compose.yml -f docker-compose.override.$device_type.yml up -d
            ;;
        "podman")
            print_status "Starting Podman containers..."
            podman-compose -f podman-compose.yml -f podman-compose.override.$device_type.yml up -d
            ;;
        "lxc")
            print_status "Starting LXC container..."
            lxc-start -n pidns -d
            ;;
        *)
            print_error "Unknown container type: $container_type"
            return 1
            ;;
    esac
    
    print_status "PiDNS containers started."
    return 0
}

# Function to stop containers
stop_containers() {
    local container_type=$1
    
    print_step "Stopping PiDNS containers..."
    
    case $container_type in
        "docker")
            print_status "Stopping Docker containers..."
            docker-compose down
            ;;
        "podman")
            print_status "Stopping Podman containers..."
            podman-compose down
            ;;
        "lxc")
            print_status "Stopping LXC container..."
            lxc-stop -n pidns
            ;;
        *)
            print_error "Unknown container type: $container_type"
            return 1
            ;;
    esac
    
    print_status "PiDNS containers stopped."
    return 0
}

# Function to restart containers
restart_containers() {
    local container_type=$1
    local device_type=$2
    
    print_step "Restarting PiDNS containers..."
    
    stop_containers $container_type
    sleep 5
    start_containers $container_type $device_type
    
    print_status "PiDNS containers restarted."
    return 0
}

# Function to show container status
show_status() {
    local container_type=$1
    
    print_step "PiDNS Container Status"
    
    case $container_type in
        "docker")
            print_status "Docker containers:"
            docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
            ;;
        "podman")
            print_status "Podman containers:"
            podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
            ;;
        "lxc")
            print_status "LXC containers:"
            lxc-list --format
            ;;
        *)
            print_error "Unknown container type: $container_type"
            return 1
            ;;
    esac
    
    return 0
}

# Function to show container logs
show_logs() {
    local container_type=$1
    local lines=${2:-50}
    
    print_step "PiDNS Container Logs"
    
    case $container_type in
        "docker")
            print_status "Docker container logs:"
            docker logs --tail $lines pidns
            ;;
        "podman")
            print_status "Podman container logs:"
            podman logs --tail $lines pidns
            ;;
        "lxc")
            print_status "LXC container logs:"
            lxc-attach -n pidns -- tail -n $lines /var/log/pidns/app.log
            ;;
        *)
            print_error "Unknown container type: $container_type"
            return 1
            ;;
    esac
    
    return 0
}

# Function to backup containers
backup_containers() {
    local container_type=$1
    local backup_path=${2:-./backup}
    
    print_step "Backing up PiDNS containers..."
    
    # Create backup directory
    mkdir -p $backup_path
    
    case $container_type in
        "docker")
            print_status "Backing up Docker containers..."
            python3 scripts/container_migration.py backup docker $backup_path
            ;;
        "podman")
            print_status "Backing up Podman containers..."
            python3 scripts/container_migration.py backup podman $backup_path
            ;;
        "lxc")
            print_status "Backing up LXC containers..."
            python3 scripts/container_migration.py backup lxc $backup_path
            ;;
        *)
            print_error "Unknown container type: $container_type"
            return 1
            ;;
    esac
    
    print_status "PiDNS containers backed up to $backup_path"
    return 0
}

# Function to restore containers
restore_containers() {
    local container_type=$1
    local backup_path=$2
    
    print_step "Restoring PiDNS containers..."
    
    if [ ! -d "$backup_path" ]; then
        print_error "Backup path does not exist: $backup_path"
        return 1
    fi
    
    case $container_type in
        "docker")
            print_status "Restoring Docker containers..."
            python3 scripts/container_migration.py restore docker $backup_path
            ;;
        "podman")
            print_status "Restoring Podman containers..."
            python3 scripts/container_migration.py restore podman $backup_path
            ;;
        "lxc")
            print_status "Restoring LXC containers..."
            python3 scripts/container_migration.py restore lxc $backup_path
            ;;
        *)
            print_error "Unknown container type: $container_type"
            return 1
            ;;
    esac
    
    print_status "PiDNS containers restored from $backup_path"
    return 0
}

# Function to migrate containers
migrate_containers() {
    local source_container=$1
    local target_container=$2
    local device_type=$3
    
    print_step "Migrating PiDNS containers..."
    
    if [ "$source_container" = "$target_container" ]; then
        print_error "Source and target container types are the same."
        return 1
    fi
    
    python3 scripts/container_migration_ui.py
    
    return $?
}

# Function to show help
show_help() {
    echo "PiDNS Container Management Script"
    echo "================================="
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  start <device_type>           Start PiDNS containers"
    echo "  stop                        Stop PiDNS containers"
    echo "  restart <device_type>        Restart PiDNS containers"
    echo "  status                      Show container status"
    echo "  logs [lines]                 Show container logs"
    echo "  backup [path]               Backup containers"
    echo "  restore <path>              Restore containers"
    echo "  migrate <source> <target> <device_type>  Migrate between container types"
    echo "  help                        Show this help message"
    echo ""
    echo "Container types:"
    echo "  docker                      Docker containers"
    echo "  podman                      Podman containers"
    echo "  lxc                         LXC containers"
    echo ""
    echo "Device types:"
    echo "  pi-zero                     Raspberry Pi Zero W"
    echo "  pi-zero-2w                  Raspberry Pi Zero 2W"
    echo "  pi-3                        Raspberry Pi 3"
    echo "  pi-4                        Raspberry Pi 4"
    echo "  pi-5                        Raspberry Pi 5"
    echo "  low-resource-pc             Low-Resource PC"
    echo "  standard-pc                  Standard PC"
    echo ""
    echo "Examples:"
    echo "  $0 start pi-4"
    echo "  $0 logs 100"
    echo "  $0 backup ./my-backup"
    echo "  $0 restore ./my-backup"
    echo "  $0 migrate docker podman pi-4"
}

# Main function
main() {
    # Check if no arguments provided
    if [ $# -eq 0 ]; then
        show_help
        return 1
    fi
    
    # Get command
    local command=$1
    shift
    
    # Get current container type
    local current_container=$(get_current_container)
    
    # Process command
    case $command in
        "start")
            if [ $# -eq 0 ]; then
                print_error "Device type is required for start command."
                show_help
                return 1
            fi
            local device_type=$1
            start_containers $current_container $device_type
            ;;
        "stop")
            stop_containers $current_container
            ;;
        "restart")
            if [ $# -eq 0 ]; then
                print_error "Device type is required for restart command."
                show_help
                return 1
            fi
            local device_type=$1
            restart_containers $current_container $device_type
            ;;
        "status")
            show_status $current_container
            ;;
        "logs")
            local lines=${1:-50}
            show_logs $current_container $lines
            ;;
        "backup")
            local backup_path=${1:-./backup}
            backup_containers $current_container $backup_path
            ;;
        "restore")
            if [ $# -eq 0 ]; then
                print_error "Backup path is required for restore command."
                show_help
                return 1
            fi
            local backup_path=$1
            restore_containers $current_container $backup_path
            ;;
        "migrate")
            if [ $# -lt 3 ]; then
                print_error "Source container, target container, and device type are required for migrate command."
                show_help
                return 1
            fi
            local source_container=$1
            local target_container=$2
            local device_type=$3
            migrate_containers $source_container $target_container $device_type
            ;;
        "help")
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            return 1
            ;;
    esac
    
    return $?
}

# Run main function
main "$@"
```

## 8. Container Integration with Installation Script

### Installation Script Integration
```bash
#!/bin/bash
# scripts/install.sh - PiDNS installation script with container support

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

# Function to detect device type
detect_device_type() {
    # Check if we're running on a Raspberry Pi
    if [ -f /proc/device-tree/model ]; then
        local model=$(cat /proc/device-tree/model)
        
        if [[ "$model" == *"Raspberry Pi Zero W"* ]]; then
            echo "pi-zero"
        elif [[ "$model" == *"Raspberry Pi Zero 2 W"* ]]; then
            echo "pi-zero-2w"
        elif [[ "$model" == *"Raspberry Pi 3"* ]]; then
            echo "pi-3"
        elif [[ "$model" == *"Raspberry Pi 4"* ]]; then
            echo "pi-4"
        elif [[ "$model" == *"Raspberry Pi 5"* ]]; then
            echo "pi-5"
        else
            # Not a recognized Raspberry Pi model, determine based on resources
            local total_mem=$(free -m | awk '/Mem:/ {print $2}')
            local cpu_cores=$(nproc)
            
            if [ "$total_mem" -le 1024 ] && [ "$cpu_cores" -le 2 ]; then
                echo "low-resource-pc"
            else
                echo "standard-pc"
            fi
        fi
    else
        # Not a Raspberry Pi, determine based on resources
        local total_mem=$(free -m | awk '/Mem:/ {print $2}')
        local cpu_cores=$(nproc)
        
        if [ "$total_mem" -le 1024 ] && [ "$cpu_cores" -le 2 ]; then
            echo "low-resource-pc"
        else
            echo "standard-pc"
        fi
    fi
}

# Function to check container availability
check_container_availability() {
    local container_type=$1
    
    case $container_type in
        "docker")
            if command -v docker &> /dev/null; then
                return 0
            else
                return 1
            fi
            ;;
        "podman")
            if command -v podman &> /dev/null; then
                return 0
            else
                return 1
            fi
            ;;
        "lxc")
            if command -v lxc-create &> /dev/null; then
                return 0
            else
                return 1
            fi
            ;;
        *)
            return 1
            ;;
    esac
}

# Function to get available containers
get_available_containers() {
    local available=()
    
    for container_type in "docker" "podman" "lxc"; do
        if check_container_availability $container_type; then
            available+=($container_type)
        fi
    done
    
    echo "${available[@]}"
}

# Function to get recommended containers for device type
get_recommended_containers() {
    local device_type=$1
    
    case $device_type in
        "pi-zero"|"pi-zero-2w")
            echo "docker lxc"
            ;;
        "pi-3"|"pi-4"|"pi-5"|"low-resource-pc"|"standard-pc")
            echo "docker podman lxc"
            ;;
        *)
            echo "docker podman lxc"
            ;;
    esac
}

# Function to select device type interactively
select_device_type_interactive() {
    print_step "Select Device Type"
    print_status "Please select the type of device you are installing PiDNS on:"
    echo ""
    echo "  1. Raspberry Pi Zero W (512MB RAM, 1-core CPU)"
    echo "  2. Raspberry Pi Zero 2W (512MB RAM, 1-core CPU)"
    echo "  3. Raspberry Pi 3 (1GB RAM, 4-core CPU)"
    echo "  4. Raspberry Pi 4 (2-8GB RAM, 4-core CPU)"
    echo "  5. Raspberry Pi 5 (4-8GB RAM, 4-core CPU)"
    echo "  6. Low-Resource PC (≤1GB RAM, ≤2 cores)"
    echo "  7. Standard PC (>1GB RAM, >2 cores)"
    echo ""
    
    while true; do
        read -p "Enter your choice (1-7): " choice
        
        case $choice in
            1)
                echo "pi-zero"
                return 0
                ;;
            2)
                echo "pi-zero-2w"
                return 0
                ;;
            3)
                echo "pi-3"
                return 0
                ;;
            4)
                echo "pi-4"
                return 0
                ;;
            5)
                echo "pi-5"
                return 0
                ;;
            6)
                echo "low-resource-pc"
                return 0
                ;;
            7)
                echo "standard-pc"
                return 0
                ;;
            *)
                print_error "Invalid choice. Please enter a number between 1 and 7."
                ;;
        esac
    done
}

# Function to select container type interactively
select_container_type_interactive() {
    local device_type=$1
    
    print_step "Select Container Type"
    print_status "Please select the container type to use for PiDNS:"
    echo ""
    
    # Get available containers
    local available=($(get_available_containers))
    
    # Get recommended containers for device type
    local recommended=($(get_recommended_containers $device_type))
    
    # Display available containers
    for i in "${!available[@]}"; do
        local container_type=${available[$i]}
        local marker=""
        
        if [[ " ${recommended[*]} " =~ " ${container_type} " ]]; then
            marker=" (recommended)"
        fi
        
        echo "  $((i+1)). ${container_type^}${marker}"
    done
    
    echo ""
    
    while true; do
        read -p "Enter your choice (1-${#available[@]}): " choice
        
        if [[ $choice =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#available[@]}" ]; then
            echo "${available[$((choice-1))]}"
            return 0
        else
            print_error "Invalid choice. Please enter a number between 1 and ${#available[@]}."
        fi
    done
}

# Function to install PiDNS with Docker
install_with_docker() {
    local device_type=$1
    
    print_step "Installing PiDNS with Docker"
    
    # Check if Docker is available
    if ! check_container_availability "docker"; then
        print_error "Docker is not available on this system."
        return 1
    fi
    
    # Generate Docker configuration
    print_status "Generating Docker configuration..."
    python3 scripts/generate_container_config.py --container docker --device $device_type
    
    # Build Docker image
    print_status "Building Docker image..."
    docker build -t pidns:$device_type .
    
    # Start Docker containers
    print_status "Starting Docker containers..."
    docker-compose -f docker-compose.yml -f docker-compose.override.$device_type.yml up -d
    
    # Enable Docker service
    print_status "Enabling Docker service..."
    cp services/pidns-docker.service /etc/systemd/system/
    sed -i "s/DEVICE_TYPE=.*/DEVICE_TYPE=$device_type/g" /etc/systemd/system/pidns-docker.service
    systemctl daemon-reload
    systemctl enable pidns-docker.service
    
    print_status "PiDNS installed successfully with Docker."
    return 0
}

# Function to install PiDNS with Podman
install_with_podman() {
    local device_type=$1
    
    print_step "Installing PiDNS with Podman"
    
    # Check if Podman is available
    if ! check_container_availability "podman"; then
        print_error "Podman is not available on this system."
        return 1
    fi
    
    # Generate Podman configuration
    print_status "Generating Podman configuration..."
    python3 scripts/generate_container_config.py --container podman --device $device_type
    
    # Build Podman image
    print_status "Building Podman image..."
    podman build -t pidns:$device_type .
    
    # Start Podman containers
    print_status "Starting Podman containers..."
    podman-compose -f podman-compose.yml -f podman-compose.override.$device_type.yml up -d
    
    # Generate Quadlet file
    print_status "Generating Quadlet file..."
    mkdir -p ~/.config/containers/systemd
    cp containers/pidns-$device_type.container ~/.config/containers/systemd/pidns.container
    
    # Enable Podman service
    print_status "Enabling Podman service..."
    cp services/pidns-podman.service /etc/systemd/system/
    sed -i "s/DEVICE_TYPE=.*/DEVICE_TYPE=$device_type/g" /etc/systemd/system/pidns-podman.service
    systemctl daemon-reload
    systemctl enable pidns-podman.service
    
    print_status "PiDNS installed successfully with Podman."
    return 0
}

# Function to install PiDNS with LXC
install_with_lxc() {
    local device_type=$1
    
    print_step "Installing PiDNS with LXC"
    
    # Check if LXC is available
    if ! check_container_availability "lxc"; then
        print_error "LXC is not available on this system."
        return 1
    fi
    
    # Generate LXC configuration
    print_status "Generating LXC configuration..."
    python3 scripts/generate_container_config.py --container lxc --device $device_type
    
    # Setup LXC container
    print_status "Setting up LXC container..."
    ./scripts/lxc-setup.sh $device_type
    
    # Enable LXC service
    print_status "Enabling LXC service..."
    cp services/pidns-lxc.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable pidns-lxc.service
    
    print_status "PiDNS installed successfully with LXC."
    return 0
}

# Function to install PiDNS without containers
install_without_containers() {
    local device_type=$1
    
    print_step "Installing PiDNS without containers"
    
    # Generate configuration
    print_status "Generating configuration..."
    python3 scripts/generate_config.py --device $device_type
    
    # Install dependencies
    print_status "Installing dependencies..."
    apt-get update
    apt-get install -y python3 python3-pip dnsmasq curl wget supervisor
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip3 install -r requirements.txt
    pip3 install -r requirements_adblocker.txt
    
    # Copy configuration files
    print_status "Copying configuration files..."
    cp config/flask_config.$device_type.py config/flask_config.py
    cp config/dnsmasq.$device_type.conf /etc/dnsmasq.conf
    cp services/pidns.$device_type.service /etc/systemd/system/pidns.service
    
    # Enable services
    print_status "Enabling services..."
    systemctl daemon-reload
    systemctl enable pidns.service
    systemctl enable dnsmasq.service
    
    # Start services
    print_status "Starting services..."
    systemctl start pidns.service
    systemctl start dnsmasq.service
    
    print_status "PiDNS installed successfully without containers."
    return 0
}

# Function to parse command line arguments
parse_arguments() {
    local device_type=""
    local container_type=""
    local silent=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --device)
                device_type="$2"
                shift 2
                ;;
            --container)
                container_type="$2"
                shift 2
                ;;
            --silent)
                silent=true
                shift
                ;;
            *)
                print_error "Unknown argument: $1"
                return 1
                ;;
        esac
    done
    
    # If device type is not specified, detect it
    if [ -z "$device_type" ]; then
        device_type=$(detect_device_type)
    fi
    
    # If container type is not specified and not in silent mode, ask for it
    if [ -z "$container_type" ] && [ "$silent" = false ]; then
        container_type=$(select_container_type_interactive $device_type)
    fi
    
    # If container type is not specified and in silent mode, use default
    if [ -z "$container_type" ] && [ "$silent" = true ]; then
        container_type="docker"
    fi
    
    # Validate device type
    case $device_type in
        "pi-zero"|"pi-zero-2w"|"pi-3"|"pi-4"|"pi-5"|"low-resource-pc"|"standard-pc")
            ;;
        *)
            print_error "Invalid device type: $device_type"
            return 1
            ;;
    esac
    
    # Validate container type
    case $container_type in
        "docker"|"podman"|"lxc"|"none")
            ;;
        *)
            print_error "Invalid container type: $container_type"
            return 1
            ;;
    esac
    
    # Return values
    echo "$device_type"
    echo "$container_type"
    echo "$silent"
    
    return 0
}

# Main function
main() {
    print_status "PiDNS Installation Script"
    print_status "========================="
    
    # Parse command line arguments
    local result=$(parse_arguments "$@")
    if [ $? -ne 0 ]; then
        return 1
    fi
    
    local device_type=$(echo "$result" | head -n 1)
    local container_type=$(echo "$result" | head -n 2 | tail -n 1)
    local silent=$(echo "$result" | tail -n 1)
    
    # If not in silent mode, ask for device type
    if [ "$silent" = false ]; then
        device_type=$(select_device_type_interactive)
    fi
    
    # Print installation summary
    print_step "Installation Summary"
    print_status "Device type: $device_type"
    print_status "Container type: $container_type"
    
    # Install PiDNS based on container type
    case $container_type in
        "docker")
            install_with_docker $device_type
            ;;
        "podman")
            install_with_podman $device_type
            ;;
        "lxc")
            install_with_lxc $device_type
            ;;
        "none")
            install_without_containers $device_type
            ;;
    esac
    
    local result=$?
    
    if [ $result -eq 0 ]; then
        print_status "PiDNS installation completed successfully!"
        print_status "You can access the dashboard at http://$(hostname -I | awk '{print $1}'):8080"
        print_status "Default username: admin"
        print_status "Default password: password"
        print_status "Please change the default password after logging in."
    else
        print_error "PiDNS installation failed."
        return 1
    fi
    
    return 0
}

# Run main function
main "$@"
```

## 9. Container Security Considerations

### Docker Security
1. **Non-root User**: Run containers as non-root user
2. **Capability Management**: Limit capabilities to only what's needed
3. **Read-only Filesystem**: Use read-only filesystem where possible
4. **Resource Limits**: Set appropriate memory and CPU limits
5. **Network Isolation**: Use appropriate network settings
6. **Seccomp Profiles**: Use seccomp profiles to restrict system calls
7. **AppArmor Profiles**: Use AppArmor profiles for additional security

### Podman Security
1. **Rootless Containers**: Run containers without root privileges
2. **SELinux Labeling**: Use SELinux labels for file access control
3. **Capability Management**: Limit capabilities to only what's needed
4. **User Namespace Mapping**: Map container user to host user
5. **Network Isolation**: Use appropriate network settings
6. **Seccomp Profiles**: Use seccomp profiles to restrict system calls
7. **No New Privileges**: Prevent containers from gaining new privileges

### LXC Security
1. **Capability Dropping**: Drop unnecessary capabilities
2. **AppArmor Profiles**: Use AppArmor for additional security
3. **Device Restrictions**: Limit access to devices
4. **Resource Limits**: Set appropriate resource limits
5. **Network Isolation**: Use appropriate network settings
6. **Control Groups**: Use cgroups for resource management
7. **Namespace Isolation**: Use namespaces for process isolation

## 10. Container Performance Considerations

### Docker Performance
1. **Multi-stage Build**: Reduce image size
2. **Resource Limits**: Set appropriate limits for each device type
3. **Health Checks**: Monitor container health
4. **Volume Management**: Use appropriate volume types for data persistence
5. **Caching**: Use build cache to speed up builds
6. **Parallel Builds**: Use parallel builds where possible

### Podman Performance
1. **Slim Base Image**: Use minimal base image
2. **Resource Limits**: Set appropriate limits for each device type
3. **Quadlet Integration**: Use systemd for better service management
4. **Volume Management**: Use appropriate volume types for data persistence
5. **Caching**: Use build cache to speed up builds
6. **Parallel Builds**: Use parallel builds where possible

### LXC Performance
1. **Resource Limits**: Set appropriate limits for each device type
2. **Filesystem Mounts**: Use bind mounts for better performance
3. **Network Configuration**: Use appropriate network settings
4. **Autostart Configuration**: Configure container to start automatically
5. **Memory Management**: Use appropriate memory settings
6. **CPU Management**: Use appropriate CPU settings
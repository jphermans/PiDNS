# PiDNS Container-Specific Configuration Files Plan

## 1. Container Configuration Overview

### Configuration Categories
1. **Base Configuration**: Common settings across all container types
2. **Docker Configuration**: Docker-specific settings
3. **Podman Configuration**: Podman-specific settings
4. **LXC Configuration**: LXC-specific settings
5. **Device-Specific Configuration**: Settings tailored to specific device types

### Configuration Goals
1. **Consistency**: Ensure consistent behavior across container types
2. **Optimization**: Optimize for each container type's strengths
3. **Portability**: Allow easy migration between container types
4. **Maintainability**: Keep configurations easy to understand and modify

## 2. Base Container Configuration

### Base Dockerfile
```dockerfile
# Base Dockerfile for PiDNS
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

### Base Containerfile (Podman)
```containerfile
# Base Containerfile for PiDNS
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

### Base LXC Configuration
```conf
# Base LXC configuration for PiDNS

# Container name
lxc.uts.name = pidns

# Architecture
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
lxc.start.order = 100

# Capabilities
lxc.cap.drop = sys_admin sys_module sys_rawio

# Console settings
lxc.tty.max = 4
lxc.pts = 1024

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
```

## 3. Docker-Specific Configuration

### Docker Compose Configuration
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

### Docker Device-Specific Override Files

#### Docker Compose Override for Pi Zero W
```yaml
# docker-compose.override.pi-zero.yml
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
      - ./config/flask_config.pi-zero.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi-zero.conf:/etc/dnsmasq.conf:ro
```

#### Docker Compose Override for Pi 3
```yaml
# docker-compose.override.pi-3.yml
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
      - ./config/flask_config.pi-3.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.pi-3.conf:/etc/dnsmasq.conf:ro
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

#### Docker Compose Override for Low-Resource PC
```yaml
# docker-compose.override.low-resource-pc.yml
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
      - ./config/flask_config.low-resource-pc.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.low-resource-pc.conf:/etc/dnsmasq.conf:ro
```

#### Docker Compose Override for Standard PC
```yaml
# docker-compose.override.standard-pc.yml
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
      - ./config/flask_config.standard-pc.py:/app/config/flask_config.py:ro

  dnsmasq:
    volumes:
      - ./config/dnsmasq.standard-pc.conf:/etc/dnsmasq.conf:ro
```

### Docker Systemd Service
```ini
# /etc/systemd/system/pidns-docker.service
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

## 4. Podman-Specific Configuration

### Podman Compose Configuration
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

### Podman Quadlet Configuration
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
Volume=%h/PiDNS/data:/app/data:z
Volume=%h/PiDNS/config:/app/config:z
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

### Podman Device-Specific Quadlet Files

#### Podman Quadlet for Pi Zero W
```ini
# ~/.config/containers/systemd/pidns-pi-zero.container
[Unit]
Description=PiDNS Container (Pi Zero W)
After=network-online.target

[Container]
Image=localhost/pidns:pi-zero
ContainerName=pidns
Network=host
PublishPort=8080:8080
PublishPort=8081:8081
PublishPort=53:53
PublishPort=67:67/udp
Volume=%h/PiDNS/data:/app/data:z
Volume=%h/PiDNS/config:/app/config:z
Volume=/var/lib/misc:/var/lib/misc:rw,z
Volume=/etc/dnsmasq.conf:/etc/dnsmasq.conf:rw,z
Environment=FLASK_ENV=production
Environment=PIDNS_USERNAME=admin
Environment=PIDNS_PASSWORD=password
Environment=DEVICE_TYPE=pi-zero
UserNS=keep-id

[Service]
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

#### Podman Quadlet for Pi 3
```ini
# ~/.config/containers/systemd/pidns-pi-3.container
[Unit]
Description=PiDNS Container (Pi 3)
After=network-online.target

[Container]
Image=localhost/pidns:pi-3
ContainerName=pidns
Network=host
PublishPort=8080:8080
PublishPort=8081:8081
PublishPort=53:53
PublishPort=67:67/udp
Volume=%h/PiDNS/data:/app/data:z
Volume=%h/PiDNS/config:/app/config:z
Volume=/var/lib/misc:/var/lib/misc:rw,z
Volume=/etc/dnsmasq.conf:/etc/dnsmasq.conf:rw,z
Environment=FLASK_ENV=production
Environment=PIDNS_USERNAME=admin
Environment=PIDNS_PASSWORD=password
Environment=DEVICE_TYPE=pi-3
UserNS=keep-id

[Service]
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

#### Podman Quadlet for Pi 4/5
```ini
# ~/.config/containers/systemd/pidns-pi-4-5.container
[Unit]
Description=PiDNS Container (Pi 4/5)
After=network-online.target

[Container]
Image=localhost/pidns:pi-4
ContainerName=pidns
Network=host
PublishPort=8080:8080
PublishPort=8081:8081
PublishPort=53:53
PublishPort=67:67/udp
Volume=%h/PiDNS/data:/app/data:z
Volume=%h/PiDNS/config:/app/config:z
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

#### Podman Quadlet for Low-Resource PC
```ini
# ~/.config/containers/systemd/pidns-low-resource-pc.container
[Unit]
Description=PiDNS Container (Low-Resource PC)
After=network-online.target

[Container]
Image=localhost/pidns:low-resource-pc
ContainerName=pidns
Network=host
PublishPort=8080:8080
PublishPort=8081:8081
PublishPort=53:53
PublishPort=67:67/udp
Volume=%h/PiDNS/data:/app/data:z
Volume=%h/PiDNS/config:/app/config:z
Volume=/var/lib/misc:/var/lib/misc:rw,z
Volume=/etc/dnsmasq.conf:/etc/dnsmasq.conf:rw,z
Environment=FLASK_ENV=production
Environment=PIDNS_USERNAME=admin
Environment=PIDNS_PASSWORD=password
Environment=DEVICE_TYPE=low-resource-pc
UserNS=keep-id

[Service]
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

#### Podman Quadlet for Standard PC
```ini
# ~/.config/containers/systemd/pidns-standard-pc.container
[Unit]
Description=PiDNS Container (Standard PC)
After=network-online.target

[Container]
Image=localhost/pidns:standard-pc
ContainerName=pidns
Network=host
PublishPort=8080:8080
PublishPort=8081:8081
PublishPort=53:53
PublishPort=67:67/udp
Volume=%h/PiDNS/data:/app/data:z
Volume=%h/PiDNS/config:/app/config:z
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

### Podman Systemd Service
```ini
# /etc/systemd/system/pidns-podman.service
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

## 5. LXC-Specific Configuration

### LXC Device-Specific Configuration Files

#### LXC Configuration for Pi Zero W
```conf
# lxc-pi-zero.conf
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
lxc.cgroup.memory.limit_in_bytes = 512M
lxc.cgroup.memory.swappiness = 10
lxc.cgroup.cpu.shares = 128

# Capabilities
lxc.cap.drop = sys_admin sys_module sys_rawio

# Console settings
lxc.tty.max = 4
lxc.pts = 1024

# AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping
```

#### LXC Configuration for Pi 3
```conf
# lxc-pi-3.conf
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
lxc.cgroup.memory.limit_in_bytes = 1024M
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

#### LXC Configuration for Pi 4/5
```conf
# lxc-pi-4-5.conf
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

#### LXC Configuration for Low-Resource PC
```conf
# lxc-low-resource-pc.conf
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

# Resource limits for Low-Resource PC
lxc.cgroup.memory.limit_in_bytes = 1024M
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

#### LXC Configuration for Standard PC
```conf
# lxc-standard-pc.conf
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

# Resource limits for Standard PC
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

### LXC Setup Script
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
lxc-attach -n pidns -- apt-get install -y python3 python3-pip dnsmasq curl wget supervisor
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

### LXC Systemd Service
```ini
# /etc/systemd/system/pidns-lxc.service
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

## 6. Container Network Configuration

### Docker Network Configuration
```bash
# docker-network.sh - Docker network configuration script

#!/bin/bash

# Create custom network for PiDNS
docker network create --driver bridge pidns-net

# Configure network settings
docker network inspect pidns-net

# Run container with custom network
docker run -d \
    --name pidns \
    --network pidns-net \
    --publish 53:53/udp \
    --publish 67:67/udp \
    --publish 8080:8080 \
    --publish 8081:8081 \
    pidns
```

### Podman Network Configuration
```bash
# podman-network.sh - Podman network configuration script

#!/bin/bash

# Create custom network for PiDNS
podman network create pidns-net

# Configure network settings
podman network inspect pidns-net

# Run container with custom network
podman run -d \
    --name pidns \
    --network pidns-net \
    --publish 53:53/udp \
    --publish 67:67/udp \
    --publish 8080:8080 \
    --publish 8081:8081 \
    pidns
```

### LXC Network Configuration
```bash
# lxc-network.sh - LXC network configuration script

#!/bin/bash

# Create network bridge
sudo brctl addbr lxcbr0
sudo ip addr add 192.168.100.1/24 dev lxcbr0
sudo ip link set lxcbr0 up

# Configure NAT
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i lxcbr0 -j ACCEPT
sudo iptables -A FORWARD -o lxcbr0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Configure LXC container network
cat > /tmp/lxc-net.conf << EOF
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx
EOF
lxc-config -n pidns -s lxc.net.0.type -v veth
lxc-config -n pidns -s lxc.net.0.link -v lxcbr0
```

## 7. Container Storage Configuration

### Docker Volume Configuration
```bash
# docker-volumes.sh - Docker volume configuration script

#!/bin/bash

# Create named volumes
docker volume create pidns-data
docker volume create pidns-logs
docker volume create pidns-config

# Mount volumes in container
docker run -d \
    --name pidns \
    -v pidns-data:/app/data \
    -v pidns-logs:/var/log/pidns \
    -v pidns-config:/app/config \
    pidns
```

### Podman Volume Configuration
```bash
# podman-volumes.sh - Podman volume configuration script

#!/bin/bash

# Create named volumes
podman volume create pidns-data
podman volume create pidns-logs
podman volume create pidns-config

# Mount volumes in container
podman run -d \
    --name pidns \
    -v pidns-data:/app/data \
    -v pidns-logs:/var/log/pidns \
    -v pidns-config:/app/config \
    pidns
```

### LXC Storage Configuration
```bash
# lxc-storage.sh - LXC storage configuration script

#!/bin/bash

# Create LXC storage pool
lxc storage create pidns-pool dir

# Configure container to use storage pool
lxc config device add pidns root disk path=/ pool=pidns-pool
```

## 8. Container Security Configuration

### Docker Security Configuration
```bash
# docker-security.sh - Docker security configuration script

#!/bin/bash

# Run with reduced capabilities
docker run --cap-drop ALL --cap-add NET_ADMIN pidns

# Use non-root user
docker run -u 1000:1000 pidns

# Read-only filesystem where possible
docker run --read-only pidns

# Use seccomp profile
docker run --security-opt seccomp=/path/to/seccomp-profile.json pidns

# Use AppArmor profile
docker run --security-opt apparmor=/path/to/apparmor-profile pidns

# Use no-new-privileges
docker run --security-opt no-new-privileges pidns
```

### Podman Security Configuration
```bash
# podman-security.sh - Podman security configuration script

#!/bin/bash

# Run with rootless user
podman run --userns keep-id pidns

# Use SELinux labeling
podman run -v $(pwd)/data:/app/data:z pidns

# Use seccomp profile
podman run --security-opt seccomp=/path/to/seccomp-profile.json pidns

# Use AppArmor profile
podman run --security-opt apparmor=/path/to/apparmor-profile pidns

# Use no-new-privileges
podman run --security-opt no-new-privileges pidns
```

### LXC Security Configuration
```bash
# lxc-security.sh - LXC security configuration script

#!/bin/bash

# Drop capabilities in container config
lxc.cap.drop = sys_admin sys_module sys_rawio

# Use AppArmor profile
lxc.apparmor.profile = lxc-container-default-with-ping

# Restrict devices
lxc.cgroup.devices.deny = a
lxc.cgroup.devices.allow = c 1:3 rwm
lxc.cgroup.devices.allow = c 1:5 rwm
lxc.cgroup.devices.allow = c 1:7 rwm
lxc.cgroup.devices.allow = c 1:8 rwm
lxc.cgroup.devices.allow = c 1:9 rwm
lxc.cgroup.devices.allow = c 5:0 rwm
lxc.cgroup.devices.allow = c 5:1 rwm
lxc.cgroup.devices.allow = c 5:2 rwm
lxc.cgroup.devices.allow = c 136:* rwm
```

## 9. Container Configuration Management

### Configuration Selection Script
```bash
#!/bin/bash
# select-container-config.sh - Select appropriate container configuration

# Function to select Docker configuration
select_docker_config() {
    local device_type=$1
    
    echo "Using Docker configuration for $device_type"
    
    # Copy device-specific Dockerfile
    cp Dockerfile.base Dockerfile
    sed -i "s/DEVICE_TYPE=.*/DEVICE_TYPE=$device_type/g" Dockerfile
    
    # Copy device-specific docker-compose override
    cp docker-compose.override.$device_type.yml docker-compose.override.yml
    
    # Copy device-specific systemd service
    cp services/pidns-docker.service /etc/systemd/system/
    sed -i "s/DEVICE_TYPE=.*/DEVICE_TYPE=$device_type/g" /etc/systemd/system/pidns-docker.service
    
    # Reload systemd
    systemctl daemon-reload
}

# Function to select Podman configuration
select_podman_config() {
    local device_type=$1
    
    echo "Using Podman configuration for $device_type"
    
    # Copy device-specific Containerfile
    cp Containerfile.base Containerfile
    sed -i "s/DEVICE_TYPE=.*/DEVICE_TYPE=$device_type/g" Containerfile
    
    # Copy device-specific podman-compose override
    cp podman-compose.override.$device_type.yml podman-compose.override.yml
    
    # Copy device-specific Quadlet file
    mkdir -p ~/.config/containers/systemd
    cp containers/pidns-$device_type.container ~/.config/containers/systemd/pidns.container
    
    # Copy device-specific systemd service
    cp services/pidns-podman.service /etc/systemd/system/
    sed -i "s/DEVICE_TYPE=.*/DEVICE_TYPE=$device_type/g" /etc/systemd/system/pidns-podman.service
    
    # Reload systemd
    systemctl --user daemon-reload
    systemctl daemon-reload
}

# Function to select LXC configuration
select_lxc_config() {
    local device_type=$1
    
    echo "Using LXC configuration for $device_type"
    
    # Copy device-specific LXC configuration
    cp lxc/lxc-$device_type.conf /var/lib/lxc/pidns/config
    
    # Copy device-specific systemd service
    cp services/pidns-lxc.service /etc/systemd/system/
    
    # Reload systemd
    systemctl daemon-reload
}

# Function to select container configuration
select_container_config() {
    local container_type=$1
    local device_type=$2
    
    case $container_type in
        "docker")
            select_docker_config $device_type
            ;;
        "podman")
            select_podman_config $device_type
            ;;
        "lxc")
            select_lxc_config $device_type
            ;;
        *)
            echo "Unknown container type: $container_type"
            exit 1
            ;;
    esac
}

# Example usage
select_container_config "docker" "pi-4"
```

### Configuration Validation Script
```bash
#!/bin/bash
# validate-container-config.sh - Validate container configuration

# Function to validate Docker configuration
validate_docker_config() {
    local device_type=$1
    
    echo "Validating Docker configuration for $device_type"
    
    # Check if Dockerfile exists
    if [ ! -f "Dockerfile" ]; then
        echo "Error: Dockerfile not found"
        return 1
    fi
    
    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        echo "Error: docker-compose.yml not found"
        return 1
    fi
    
    # Check if docker-compose override exists
    if [ ! -f "docker-compose.override.yml" ]; then
        echo "Error: docker-compose.override.yml not found"
        return 1
    fi
    
    # Check if systemd service exists
    if [ ! -f "/etc/systemd/system/pidns-docker.service" ]; then
        echo "Error: systemd service not found"
        return 1
    fi
    
    # Test Docker build
    if ! docker build -t pidns:$device_type .; then
        echo "Error: Docker build failed"
        return 1
    fi
    
    # Test docker-compose configuration
    if ! docker-compose config; then
        echo "Error: docker-compose configuration is invalid"
        return 1
    fi
    
    echo "Docker configuration is valid"
    return 0
}

# Function to validate Podman configuration
validate_podman_config() {
    local device_type=$1
    
    echo "Validating Podman configuration for $device_type"
    
    # Check if Containerfile exists
    if [ ! -f "Containerfile" ]; then
        echo "Error: Containerfile not found"
        return 1
    fi
    
    # Check if podman-compose.yml exists
    if [ ! -f "podman-compose.yml" ]; then
        echo "Error: podman-compose.yml not found"
        return 1
    fi
    
    # Check if podman-compose override exists
    if [ ! -f "podman-compose.override.yml" ]; then
        echo "Error: podman-compose.override.yml not found"
        return 1
    fi
    
    # Check if Quadlet file exists
    if [ ! -f "~/.config/containers/systemd/pidns.container" ]; then
        echo "Error: Quadlet file not found"
        return 1
    fi
    
    # Check if systemd service exists
    if [ ! -f "/etc/systemd/system/pidns-podman.service" ]; then
        echo "Error: systemd service not found"
        return 1
    fi
    
    # Test Podman build
    if ! podman build -t pidns:$device_type .; then
        echo "Error: Podman build failed"
        return 1
    fi
    
    # Test podman-compose configuration
    if ! podman-compose config; then
        echo "Error: podman-compose configuration is invalid"
        return 1
    fi
    
    echo "Podman configuration is valid"
    return 0
}

# Function to validate LXC configuration
validate_lxc_config() {
    local device_type=$1
    
    echo "Validating LXC configuration for $device_type"
    
    # Check if LXC configuration exists
    if [ ! -f "/var/lib/lxc/pidns/config" ]; then
        echo "Error: LXC configuration not found"
        return 1
    fi
    
    # Check if systemd service exists
    if [ ! -f "/etc/systemd/system/pidns-lxc.service" ]; then
        echo "Error: systemd service not found"
        return 1
    fi
    
    # Test LXC configuration syntax
    if ! lxc-checkconfig; then
        echo "Error: LXC configuration is invalid"
        return 1
    fi
    
    echo "LXC configuration is valid"
    return 0
}

# Function to validate container configuration
validate_container_config() {
    local container_type=$1
    local device_type=$2
    
    case $container_type in
        "docker")
            validate_docker_config $device_type
            ;;
        "podman")
            validate_podman_config $device_type
            ;;
        "lxc")
            validate_lxc_config $device_type
            ;;
        *)
            echo "Unknown container type: $container_type"
            return 1
            ;;
    esac
}

# Example usage
validate_container_config "docker" "pi-4"
```

## 10. Container Configuration Migration

### Configuration Migration Script
```bash
#!/bin/bash
# migrate-container-config.sh - Migrate container configuration

# Function to migrate Docker configuration
migrate_docker_config() {
    local source_device=$1
    local target_device=$2
    
    echo "Migrating Docker configuration from $source_device to $target_device"
    
    # Update Dockerfile
    sed -i "s/DEVICE_TYPE=$source_device/DEVICE_TYPE=$target_device/g" Dockerfile
    
    # Update docker-compose override
    cp docker-compose.override.$source_device.yml docker-compose.override.$target_device.yml
    sed -i "s/$source_device/$target_device/g" docker-compose.override.$target_device.yml
    
    # Update systemd service
    sed -i "s/DEVICE_TYPE=$source_device/DEVICE_TYPE=$target_device/g" /etc/systemd/system/pidns-docker.service
    
    # Rebuild Docker image
    docker build -t pidns:$target_device .
    
    # Restart Docker container
    docker-compose down
    docker-compose -f docker-compose.yml -f docker-compose.override.$target_device.yml up -d
    
    echo "Docker configuration migrated from $source_device to $target_device"
}

# Function to migrate Podman configuration
migrate_podman_config() {
    local source_device=$1
    local target_device=$2
    
    echo "Migrating Podman configuration from $source_device to $target_device"
    
    # Update Containerfile
    sed -i "s/DEVICE_TYPE=$source_device/DEVICE_TYPE=$target_device/g" Containerfile
    
    # Update podman-compose override
    cp podman-compose.override.$source_device.yml podman-compose.override.$target_device.yml
    sed -i "s/$source_device/$target_device/g" podman-compose.override.$target_device.yml
    
    # Update Quadlet file
    cp ~/.config/containers/systemd/pidns-$source_device.container ~/.config/containers/systemd/pidns-$target_device.container
    sed -i "s/$source_device/$target_device/g" ~/.config/containers/systemd/pidns-$target_device.container
    
    # Update systemd service
    sed -i "s/DEVICE_TYPE=$source_device/DEVICE_TYPE=$target_device/g" /etc/systemd/system/pidns-podman.service
    
    # Rebuild Podman image
    podman build -t pidns:$target_device .
    
    # Restart Podman container
    podman-compose down
    podman-compose -f podman-compose.yml -f podman-compose.override.$target_device.yml up -d
    
    echo "Podman configuration migrated from $source_device to $target_device"
}

# Function to migrate LXC configuration
migrate_lxc_config() {
    local source_device=$1
    local target_device=$2
    
    echo "Migrating LXC configuration from $source_device to $target_device"
    
    # Stop LXC container
    lxc-stop -n pidns
    
    # Update LXC configuration
    cp lxc/lxc-$target_device.conf /var/lib/lxc/pidns/config
    
    # Update systemd service
    sed -i "s/DEVICE_TYPE=$source_device/DEVICE_TYPE=$target_device/g" /etc/systemd/system/pidns-lxc.service
    
    # Start LXC container
    lxc-start -n pidns -d
    
    echo "LXC configuration migrated from $source_device to $target_device"
}

# Function to migrate container configuration
migrate_container_config() {
    local container_type=$1
    local source_device=$2
    local target_device=$3
    
    case $container_type in
        "docker")
            migrate_docker_config $source_device $target_device
            ;;
        "podman")
            migrate_podman_config $source_device $target_device
            ;;
        "lxc")
            migrate_lxc_config $source_device $target_device
            ;;
        *)
            echo "Unknown container type: $container_type"
            exit 1
            ;;
    esac
}

# Example usage
migrate_container_config "docker" "pi-3" "pi-4"
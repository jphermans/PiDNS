# PiDNS Device Detection and Container Support Plan

## 1. Device Detection Logic

### Current Implementation Analysis
The current installation script (`scripts/install.sh`) has basic device detection:
- Detects Raspberry Pi model from `/proc/device-tree/model`
- Gets Pi version from `/proc/cpuinfo`
- Basic configuration differentiation between Pi 4/5 and other models

### Enhanced Device Detection

#### Raspberry Pi Models
```bash
# Enhanced device detection function
detect_device() {
    # Check if running on Raspberry Pi
    if [ -f /proc/device-tree/model ]; then
        PI_MODEL=$(cat /proc/device-tree/model 2>/dev/null || echo "Unknown")
        
        # Extract specific Pi model
        if echo "$PI_MODEL" | grep -q "Raspberry Pi Zero 2 W"; then
            DEVICE_TYPE="pi-zero-2w"
            DEVICE_RAM="512MB"
            DEVICE_CPU="1-core"
        elif echo "$PI_MODEL" | grep -q "Raspberry Pi Zero"; then
            DEVICE_TYPE="pi-zero"
            DEVICE_RAM="512MB"
            DEVICE_CPU="1-core"
        elif echo "$PI_MODEL" | grep -q "Raspberry Pi 3"; then
            DEVICE_TYPE="pi-3"
            DEVICE_RAM="1GB"
            DEVICE_CPU="4-core"
        elif echo "$PI_MODEL" | grep -q "Raspberry Pi 4"; then
            DEVICE_TYPE="pi-4"
            DEVICE_RAM="2GB-8GB"
            DEVICE_CPU="4-core"
        elif echo "$PI_MODEL" | grep -q "Raspberry Pi 5"; then
            DEVICE_TYPE="pi-5"
            DEVICE_RAM="4GB-8GB"
            DEVICE_CPU="4-core"
        else
            DEVICE_TYPE="pi-unknown"
            DEVICE_RAM="unknown"
            DEVICE_CPU="unknown"
        fi
    else
        # Not a Raspberry Pi - check for low-resource PC
        TOTAL_RAM=$(free -m | awk '/Mem:/ {print $2}')
        CPU_CORES=$(nproc)
        
        if [ "$TOTAL_RAM" -le 1024 ] && [ "$CPU_CORES" -le 2 ]; then
            DEVICE_TYPE="low-resource-pc"
            DEVICE_RAM="${TOTAL_RAM}MB"
            DEVICE_CPU="${CPU_CORES}-core"
        else
            DEVICE_TYPE="standard-pc"
            DEVICE_RAM="${TOTAL_RAM}MB"
            DEVICE_CPU="${CPU_CORES}-core"
        fi
    fi
    
    echo "Detected device: $DEVICE_TYPE with $DEVICE_RAM RAM and $DEVICE_CPU CPU"
}
```

#### Device-Specific Configuration Parameters
```bash
# Configuration based on device type
get_device_config() {
    case $DEVICE_TYPE in
        "pi-zero"|"pi-zero-2w")
            CACHE_SIZE=100
            DNS_CACHE=100
            MAX_CONNECTIONS=50
            SWAPINESS=10
            ;;
        "pi-3")
            CACHE_SIZE=200
            DNS_CACHE=200
            MAX_CONNECTIONS=100
            SWAPINESS=10
            ;;
        "pi-4")
            CACHE_SIZE=500
            DNS_CACHE=500
            MAX_CONNECTIONS=200
            SWAPINESS=5
            ;;
        "pi-5")
            CACHE_SIZE=1000
            DNS_CACHE=1000
            MAX_CONNECTIONS=500
            SWAPINESS=5
            ;;
        "low-resource-pc")
            CACHE_SIZE=300
            DNS_CACHE=300
            MAX_CONNECTIONS=150
            SWAPINESS=10
            ;;
        "standard-pc")
            CACHE_SIZE=1000
            DNS_CACHE=1000
            MAX_CONNECTIONS=500
            SWAPNESS=1
            ;;
        *)
            # Default/fallback configuration
            CACHE_SIZE=150
            DNS_CACHE=150
            MAX_CONNECTIONS=100
            SWAPINESS=10
            ;;
    esac
}
```

## 2. Container Support Design

### Container Options
1. **Docker**: Most popular container platform, wide community support
2. **Podman**: Daemonless, rootless containers, better security
3. **LXC**: Lightweight OS-level virtualization, better performance

### Container-Specific Considerations

#### Docker
```bash
# Dockerfile template
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    dnsmasq \
    nginx \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set up application
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements_adblocker.txt .
RUN pip install --no-cache-dir -r requirements_adblocker.txt

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

#### Podman
```bash
# Podman-specific commands
# Similar to Docker but with rootless considerations
podman build -t pidns .
podman run -d --name pidns \
    --network host \
    -v /var/lib/misc:/var/lib/misc:Z \
    -v /etc/dnsmasq.conf:/etc/dnsmasq.conf:Z \
    pidns
```

#### LXC
```bash
# LXC configuration template
lxc-create -n pidns -t download -- -d debian -r bullseye -a armhf
lxc-start -n pidns
lxc-attach -n pidns -- ./scripts/install.sh
```

## 3. Interactive Installation Script Flow

```bash
#!/bin/bash
# Enhanced installation script with device and container selection

# Device selection prompt
echo "Please select your target device:"
echo "1) Raspberry Pi Zero W"
echo "2) Raspberry Pi Zero 2 W"
echo "3) Raspberry Pi 3"
echo "4) Raspberry Pi 4"
echo "5) Raspberry Pi 5"
echo "6) Low-resource PC (≤1GB RAM, ≤2 cores)"
echo "7) Standard PC (>1GB RAM, >2 cores)"
echo "8) Auto-detect"
read -p "Enter your choice (1-8): " device_choice

# Container selection prompt
echo "Do you want to run PiDNS in a container? (y/n)"
read -r container_response

if [ "$container_response" = "y" ]; then
    echo "Please select container type:"
    echo "1) Docker"
    echo "2) Podman"
    echo "3) LXC"
    read -p "Enter your choice (1-3): " container_choice
else
    container_choice="none"
fi

# Apply configurations based on selections
apply_configurations
```

## 4. Configuration Templates

### Device-Specific dnsmasq.conf Templates
- `config/dnsmasq.pi-zero.conf` - Minimal configuration for Pi Zero
- `config/dnsmasq.pi-3.conf` - Balanced configuration for Pi 3
- `config/dnsmasq.pi-4.conf` - Enhanced configuration for Pi 4/5
- `config/dnsmasq.pc.conf` - Standard configuration for PCs

### Container-Specific Service Files
- `services/pidns-docker.service` - Service file for Docker deployment
- `services/pidns-podman.service` - Service file for Podman deployment
- `services/pidns-lxc.service` - Service file for LXC deployment

## 5. Implementation Steps

1. Create device detection script
2. Design container templates
3. Create configuration templates for each device type
4. Modify installation script to include interactive prompts
5. Add container installation options
6. Create device-specific optimization settings
7. Develop container-specific configuration files
8. Update documentation
9. Test the modified installation process

## 6. Testing Strategy

- Test on actual Raspberry Pi models (Zero W, 3, 4)
- Test on low-resource PCs
- Test container deployments (Docker, Podman, LXC)
- Verify performance optimizations are applied correctly
- Ensure all installation paths work as expected
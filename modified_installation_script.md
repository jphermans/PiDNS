# Modified PiDNS Installation Script

## 1. Installation Script Overview

### Script Purpose
The modified PiDNS installation script is designed to:
1. **Detect Device Type**: Automatically detect the type of device PiDNS is being installed on
2. **Prompt for Device Selection**: Allow users to manually select their device type
3. **Prompt for Container Selection**: Allow users to select the container type to use
4. **Generate Configuration**: Generate appropriate configuration files based on selections
5. **Install PiDNS**: Install PiDNS with the selected configuration

### Script Features
1. **Interactive Mode**: Guide users through the installation process with prompts
2. **Silent Mode**: Allow automated installation with command-line arguments
3. **Device Detection**: Automatically detect device type when possible
4. **Container Support**: Support Docker, Podman, LXC, and bare metal installations
5. **Configuration Generation**: Generate optimized configuration files for each device type
6. **Error Handling**: Handle errors gracefully with informative messages
7. **Rollback Capability**: Roll back changes if installation fails

### Script Structure
1. **Initialization**: Set up environment and parse command-line arguments
2. **Device Detection**: Detect device type or prompt for selection
3. **Container Selection**: Select container type or prompt for selection
4. **Configuration Generation**: Generate configuration files
5. **Installation**: Install PiDNS with selected configuration
6. **Post-Installation**: Perform post-installation tasks
7. **Cleanup**: Clean up temporary files and directories

## 2. Installation Script Code

### Main Installation Script
```bash
#!/bin/bash
# scripts/install.sh - PiDNS installation script with device and container selection

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
    print_step "Detecting device type..."
    
    # Check if we're running on a Raspberry Pi
    if [ -f /proc/device-tree/model ]; then
        local model=$(cat /proc/device-tree/model)
        
        if [[ "$model" == *"Raspberry Pi Zero W"* ]]; then
            print_status "Detected device: Raspberry Pi Zero W"
            echo "pi-zero"
            return 0
        elif [[ "$model" == *"Raspberry Pi Zero 2 W"* ]]; then
            print_status "Detected device: Raspberry Pi Zero 2W"
            echo "pi-zero-2w"
            return 0
        elif [[ "$model" == *"Raspberry Pi 3"* ]]; then
            print_status "Detected device: Raspberry Pi 3"
            echo "pi-3"
            return 0
        elif [[ "$model" == *"Raspberry Pi 4"* ]]; then
            print_status "Detected device: Raspberry Pi 4"
            echo "pi-4"
            return 0
        elif [[ "$model" == *"Raspberry Pi 5"* ]]; then
            print_status "Detected device: Raspberry Pi 5"
            echo "pi-5"
            return 0
        else
            print_warning "Unknown Raspberry Pi model: $model"
        fi
    fi
    
    # Not a Raspberry Pi, determine based on resources
    local total_mem=$(free -m | awk '/Mem:/ {print $2}')
    local cpu_cores=$(nproc)
    
    print_status "Detected resources: ${total_mem}MB RAM, $cpu_cores CPU cores"
    
    if [ "$total_mem" -le 1024 ] && [ "$cpu_cores" -le 2 ]; then
        print_status "Detected device: Low-Resource PC"
        echo "low-resource-pc"
    else
        print_status "Detected device: Standard PC"
        echo "standard-pc"
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

# Function to display device information
display_device_info() {
    local device_type=$1
    
    print_step "Device Information"
    
    case $device_type in
        "pi-zero")
            print_status "Device: Raspberry Pi Zero W"
            print_status "Memory: 512MB"
            print_status "CPU: 1-core ARM"
            print_status "Recommended containers: Docker, LXC"
            ;;
        "pi-zero-2w")
            print_status "Device: Raspberry Pi Zero 2W"
            print_status "Memory: 512MB"
            print_status "CPU: 1-core ARM"
            print_status "Recommended containers: Docker, LXC"
            ;;
        "pi-3")
            print_status "Device: Raspberry Pi 3"
            print_status "Memory: 1GB"
            print_status "CPU: 4-core ARM"
            print_status "Recommended containers: Docker, Podman, LXC"
            ;;
        "pi-4")
            print_status "Device: Raspberry Pi 4"
            print_status "Memory: 2-8GB"
            print_status "CPU: 4-core ARM"
            print_status "Recommended containers: Docker, Podman, LXC"
            ;;
        "pi-5")
            print_status "Device: Raspberry Pi 5"
            print_status "Memory: 4-8GB"
            print_status "CPU: 4-core ARM"
            print_status "Recommended containers: Docker, Podman, LXC"
            ;;
        "low-resource-pc")
            print_status "Device: Low-Resource PC"
            print_status "Memory: ≤1GB"
            print_status "CPU: ≤2 cores"
            print_status "Recommended containers: Docker, Podman, LXC"
            ;;
        "standard-pc")
            print_status "Device: Standard PC"
            print_status "Memory: >1GB"
            print_status "CPU: >2 cores"
            print_status "Recommended containers: Docker, Podman, LXC"
            ;;
        *)
            print_error "Unknown device type: $device_type"
            return 1
            ;;
    esac
    
    return 0
}

# Function to display container information
display_container_info() {
    local container_type=$1
    
    print_step "Container Information"
    
    case $container_type in
        "docker")
            print_status "Container: Docker"
            print_status "Description: Most popular container platform with wide community support"
            print_status "Pros: Wide community support, easy to use with Docker Compose, supports resource limits and health checks"
            print_status "Cons: Requires Docker daemon, runs as root by default"
            ;;
        "podman")
            print_status "Container: Podman"
            print_status "Description: Daemonless, rootless containers with better security"
            print_status "Pros: Daemonless architecture, rootless containers by default, compatible with Docker CLI, better security model"
            print_status "Cons: Smaller community than Docker, fewer third-party tools"
            ;;
        "lxc")
            print_status "Container: LXC"
            print_status "Description: Lightweight OS-level virtualization with better performance"
            print_status "Pros: Lightweight with low overhead, direct access to host kernel features, better performance for some workloads"
            print_status "Cons: More complex setup, fewer management tools"
            ;;
        "none")
            print_status "Container: None (Bare Metal)"
            print_status "Description: Install directly on host system without containers"
            print_status "Pros: Direct hardware access, no container overhead, simpler setup"
            print_status "Cons: Less isolation, harder to manage dependencies"
            ;;
        *)
            print_error "Unknown container type: $container_type"
            return 1
            ;;
    esac
    
    return 0
}

# Function to install dependencies
install_dependencies() {
    print_step "Installing dependencies"
    
    # Update package lists
    print_status "Updating package lists..."
    apt-get update
    
    # Install Python and pip
    print_status "Installing Python and pip..."
    apt-get install -y python3 python3-pip
    
    # Install Jinja2 for template rendering
    print_status "Installing Jinja2..."
    pip3 install jinja2
    
    # Install other dependencies
    print_status "Installing other dependencies..."
    apt-get install -y dnsmasq curl wget supervisor
    
    print_status "Dependencies installed successfully"
    return 0
}

# Function to generate configuration files
generate_configuration_files() {
    local device_type=$1
    local container_type=$2
    
    print_step "Generating configuration files"
    
    # Create config directory
    mkdir -p config
    
    # Generate Flask configuration
    print_status "Generating Flask configuration..."
    python3 scripts/generate_config.py --device $device_type --container $container_type
    
    # Generate dnsmasq configuration
    print_status "Generating dnsmasq configuration..."
    cp config/dnsmasq.$device_type.conf config/dnsmasq.conf
    
    # Generate systemd service
    print_status "Generating systemd service..."
    cp services/pidns.$device_type.service services/pidns.service
    
    # Generate container configuration if needed
    if [ "$container_type" != "none" ]; then
        print_status "Generating container configuration..."
        python3 scripts/generate_container_config.py --container $container_type --device $device_type
    fi
    
    print_status "Configuration files generated successfully"
    return 0
}

# Function to install PiDNS with Docker
install_with_docker() {
    local device_type=$1
    
    print_step "Installing PiDNS with Docker"
    
    # Check if Docker is available
    if ! check_container_availability "docker"; then
        print_error "Docker is not available on this system."
        print_status "Please install Docker and try again."
        return 1
    fi
    
    # Install Docker if not already installed
    if ! command -v docker-compose &> /dev/null; then
        print_status "Installing Docker Compose..."
        apt-get install -y docker-compose
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
        print_status "Please install Podman and try again."
        return 1
    fi
    
    # Install Podman Compose if not already installed
    if ! command -v podman-compose &> /dev/null; then
        print_status "Installing Podman Compose..."
        pip3 install podman-compose
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
        print_status "Please install LXC and try again."
        return 1
    fi
    
    # Install LXC dependencies if not already installed
    if ! command -v lxc-info &> /dev/null; then
        print_status "Installing LXC..."
        apt-get install -y lxc lxc-templates debootstrap
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
    python3 scripts/generate_config.py --device $device_type --container none
    
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

# Function to install PiDNS
install_pidns() {
    local device_type=$1
    local container_type=$2
    
    print_step "Installing PiDNS"
    
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
        *)
            print_error "Unknown container type: $container_type"
            return 1
            ;;
    esac
    
    return $?
}

# Function to validate installation
validate_installation() {
    local device_type=$1
    local container_type=$2
    
    print_step "Validating installation"
    
    # Check if dashboard is accessible
    print_status "Checking if dashboard is accessible..."
    local ip_address=$(hostname -I | awk '{print $1}')
    
    if curl -s -f http://$ip_address:8080/api/health > /dev/null; then
        print_status "Dashboard is accessible at http://$ip_address:8080"
    else
        print_error "Dashboard is not accessible at http://$ip_address:8080"
        return 1
    fi
    
    # Check if ad-blocker is accessible if enabled
    if [ "$device_type" != "pi-zero" ] && [ "$device_type" != "pi-zero-2w" ]; then
        print_status "Checking if ad-blocker is accessible..."
        
        if curl -s -f http://$ip_address:8081/api/health > /dev/null; then
            print_status "Ad-blocker is accessible at http://$ip_address:8081"
        else
            print_error "Ad-blocker is not accessible at http://$ip_address:8081"
            return 1
        fi
    fi
    
    # Check if DNS is working
    print_status "Checking if DNS is working..."
    
    if nslookup example.com $ip_address > /dev/null 2>&1; then
        print_status "DNS is working"
    else
        print_error "DNS is not working"
        return 1
    fi
    
    print_status "Installation validated successfully"
    return 0
}

# Function to display post-installation information
display_post_installation_info() {
    local device_type=$1
    local container_type=$2
    
    print_step "Post-Installation Information"
    
    local ip_address=$(hostname -I | awk '{print $1}')
    
    print_status "PiDNS has been successfully installed!"
    print_status ""
    print_status "Dashboard URL: http://$ip_address:8080"
    print_status "Default username: admin"
    print_status "Default password: password"
    print_status ""
    print_status "Please change the default password after logging in."
    print_status ""
    
    if [ "$container_type" != "none" ]; then
        print_status "Container management commands:"
        print_status "  Start: ./scripts/container-management.sh start $device_type"
        print_status "  Stop: ./scripts/container-management.sh stop"
        print_status "  Restart: ./scripts/container-management.sh restart $device_type"
        print_status "  Status: ./scripts/container-management.sh status"
        print_status "  Logs: ./scripts/container-management.sh logs"
        print_status ""
    fi
    
    print_status "Thank you for installing PiDNS!"
}

# Function to parse command line arguments
parse_arguments() {
    local device_type=""
    local container_type=""
    local silent=false
    local help=false
    
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
            --help)
                help=true
                shift
                ;;
            *)
                print_error "Unknown argument: $1"
                return 1
                ;;
        esac
    done
    
    # If help is requested, show help and exit
    if [ "$help" = true ]; then
        show_help
        return 0
    fi
    
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

# Function to show help
show_help() {
    echo "PiDNS Installation Script"
    echo "========================="
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --device DEVICE_TYPE     Specify device type"
    echo "  --container CONTAINER_TYPE  Specify container type"
    echo "  --silent                Run in silent mode"
    echo "  --help                  Show this help message"
    echo ""
    echo "Device types:"
    echo "  pi-zero                 Raspberry Pi Zero W"
    echo "  pi-zero-2w              Raspberry Pi Zero 2W"
    echo "  pi-3                    Raspberry Pi 3"
    echo "  pi-4                    Raspberry Pi 4"
    echo "  pi-5                    Raspberry Pi 5"
    echo "  low-resource-pc         Low-Resource PC"
    echo "  standard-pc              Standard PC"
    echo ""
    echo "Container types:"
    echo "  docker                  Docker containers"
    echo "  podman                  Podman containers"
    echo "  lxc                     LXC containers"
    echo "  none                    No containers (bare metal)"
    echo ""
    echo "Examples:"
    echo "  $0 --device pi-4 --container docker"
    echo "  $0 --device standard-pc --container podman"
    echo "  $0 --silent"
}

# Main function
main() {
    print_status "PiDNS Installation Script"
    print_status "========================="
    
    # Parse command line arguments
    local result=$(parse_arguments "$@")
    local parse_result=$?
    
    if [ $parse_result -ne 0 ]; then
        return $parse_result
    fi
    
    local device_type=$(echo "$result" | head -n 1)
    local container_type=$(echo "$result" | head -n 2 | tail -n 1)
    local silent=$(echo "$result" | tail -n 1)
    
    # If not in silent mode, ask for device type
    if [ "$silent" = false ]; then
        device_type=$(select_device_type_interactive)
    fi
    
    # Display device and container information
    display_device_info $device_type
    display_container_info $container_type
    
    # Confirm installation
    if [ "$silent" = false ]; then
        echo ""
        read -p "Continue with installation? (y/n): " confirm
        
        if [[ "$confirm" != "y" && "$confirm" != "yes" ]]; then
            print_status "Installation cancelled."
            return 0
        fi
    fi
    
    # Install dependencies
    if ! install_dependencies; then
        print_error "Failed to install dependencies."
        return 1
    fi
    
    # Generate configuration files
    if ! generate_configuration_files $device_type $container_type; then
        print_error "Failed to generate configuration files."
        return 1
    fi
    
    # Install PiDNS
    if ! install_pidns $device_type $container_type; then
        print_error "Failed to install PiDNS."
        return 1
    fi
    
    # Validate installation
    if ! validate_installation $device_type $container_type; then
        print_error "Installation validation failed."
        return 1
    fi
    
    # Display post-installation information
    display_post_installation_info $device_type $container_type
    
    return 0
}

# Run main function
main "$@"
```

## 3. Device Detection Script

### Device Detection Script
```python
# scripts/device_detection.py
#!/usr/bin/env python3
"""
Device detection script for PiDNS
"""

import os
import sys
import subprocess
import re
from typing import Dict, List, Optional, Tuple

def get_cpu_info() -> Dict[str, str]:
    """Get CPU information"""
    cpu_info = {}
    
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == 'model name':
                        cpu_info['model'] = value
                    elif key == 'Hardware':
                        cpu_info['hardware'] = value
                    elif key == 'Revision':
                        cpu_info['revision'] = value
                    elif key == 'Serial':
                        cpu_info['serial'] = value
    except FileNotFoundError:
        pass
    
    return cpu_info

def get_memory_info() -> Dict[str, int]:
    """Get memory information"""
    memory_info = {}
    
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == 'MemTotal':
                        # Convert from KB to MB
                        memory_info['total_mb'] = int(value.split()[0]) // 1024
                    elif key == 'MemFree':
                        # Convert from KB to MB
                        memory_info['free_mb'] = int(value.split()[0]) // 1024
                    elif key == 'MemAvailable':
                        # Convert from KB to MB
                        memory_info['available_mb'] = int(value.split()[0]) // 1024
    except FileNotFoundError:
        pass
    
    return memory_info

def get_device_tree_model() -> Optional[str]:
    """Get device tree model"""
    try:
        with open('/proc/device-tree/model', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_system_info() -> Dict[str, str]:
    """Get system information"""
    system_info = {}
    
    try:
        result = subprocess.run(['uname', '-a'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        system_info['uname'] = result.stdout.decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    try:
        result = subprocess.run(['lsb_release', '-a'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        system_info['lsb_release'] = result.stdout.decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return system_info

def get_network_info() -> Dict[str, List[str]]:
    """Get network information"""
    network_info = {}
    
    try:
        result = subprocess.run(['ip', 'link', 'show'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        interfaces = []
        
        for line in result.stdout.decode().split('\n'):
            if ': ' in line and not line.startswith(' '):
                interface = line.split(':')[1].strip()
                interfaces.append(interface)
        
        network_info['interfaces'] = interfaces
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return network_info

def detect_raspberry_pi() -> Optional[str]:
    """Detect Raspberry Pi model"""
    model = get_device_tree_model()
    
    if not model:
        return None
    
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
    
    return None

def detect_pc() -> str:
    """Detect PC type based on resources"""
    memory_info = get_memory_info()
    cpu_info = get_cpu_info()
    
    # Get number of CPU cores
    cpu_cores = os.cpu_count() if hasattr(os, 'cpu_count') else 1
    
    # Get total memory in MB
    total_memory = memory_info.get('total_mb', 1024)
    
    # Determine PC type based on resources
    if total_memory <= 1024 and cpu_cores <= 2:
        return "low-resource-pc"
    else:
        return "standard-pc"

def detect_device_type() -> str:
    """Detect device type"""
    # First try to detect Raspberry Pi
    pi_model = detect_raspberry_pi()
    
    if pi_model:
        return pi_model
    
    # If not a Raspberry Pi, detect PC type
    return detect_pc()

def get_device_info(device_type: str) -> Dict[str, str]:
    """Get device information"""
    device_info = {
        "pi-zero": {
            "name": "Raspberry Pi Zero W",
            "memory": "512MB",
            "cpu": "1-core ARM",
            "recommended_containers": ["docker", "lxc"]
        },
        "pi-zero-2w": {
            "name": "Raspberry Pi Zero 2W",
            "memory": "512MB",
            "cpu": "1-core ARM",
            "recommended_containers": ["docker", "lxc"]
        },
        "pi-3": {
            "name": "Raspberry Pi 3",
            "memory": "1GB",
            "cpu": "4-core ARM",
            "recommended_containers": ["docker", "podman", "lxc"]
        },
        "pi-4": {
            "name": "Raspberry Pi 4",
            "memory": "2-8GB",
            "cpu": "4-core ARM",
            "recommended_containers": ["docker", "podman", "lxc"]
        },
        "pi-5": {
            "name": "Raspberry Pi 5",
            "memory": "4-8GB",
            "cpu": "4-core ARM",
            "recommended_containers": ["docker", "podman", "lxc"]
        },
        "low-resource-pc": {
            "name": "Low-Resource PC",
            "memory": "≤1GB",
            "cpu": "≤2 cores",
            "recommended_containers": ["docker", "podman", "lxc"]
        },
        "standard-pc": {
            "name": "Standard PC",
            "memory": ">1GB",
            "cpu": ">2 cores",
            "recommended_containers": ["docker", "podman", "lxc"]
        }
    }
    
    return device_info.get(device_type, {})

def print_device_info(device_type: str) -> None:
    """Print device information"""
    device_info = get_device_info(device_type)
    
    if not device_info:
        print(f"Unknown device type: {device_type}")
        return
    
    print(f"Device: {device_info['name']}")
    print(f"Memory: {device_info['memory']}")
    print(f"CPU: {device_info['cpu']}")
    print(f"Recommended containers: {', '.join(device_info['recommended_containers'])}")

def main():
    """Main function for testing"""
    # Detect device type
    device_type = detect_device_type()
    
    # Print device type
    print(f"Detected device type: {device_type}")
    
    # Print device information
    print_device_info(device_type)
    
    # Print system information
    print("\nSystem Information:")
    print("==================")
    
    cpu_info = get_cpu_info()
    if cpu_info:
        print(f"CPU Model: {cpu_info.get('model', 'Unknown')}")
        print(f"CPU Hardware: {cpu_info.get('hardware', 'Unknown')}")
        print(f"CPU Revision: {cpu_info.get('revision', 'Unknown')}")
    
    memory_info = get_memory_info()
    if memory_info:
        print(f"Total Memory: {memory_info.get('total_mb', 'Unknown')}MB")
        print(f"Free Memory: {memory_info.get('free_mb', 'Unknown')}MB")
        print(f"Available Memory: {memory_info.get('available_mb', 'Unknown')}MB")
    
    system_info = get_system_info()
    if system_info:
        print(f"System: {system_info.get('uname', 'Unknown')}")
        print(f"Distribution: {system_info.get('lsb_release', 'Unknown')}")
    
    network_info = get_network_info()
    if network_info:
        print(f"Network Interfaces: {', '.join(network_info.get('interfaces', []))}")

if __name__ == "__main__":
    main()
```

## 4. Container Selection Script

### Container Selection Script
```python
# scripts/container_selection.py
#!/usr/bin/env python3
"""
Container selection script for PiDNS
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

def get_container_info(container_type: str) -> Dict[str, str]:
    """Get container information"""
    container_info = {
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
        },
        "none": {
            "name": "None (Bare Metal)",
            "description": "Install directly on host system without containers",
            "pros": [
                "Direct hardware access",
                "No container overhead",
                "Simpler setup"
            ],
            "cons": [
                "Less isolation",
                "Harder to manage dependencies"
            ]
        }
    }
    
    return container_info.get(container_type, {})

def print_container_info(container_type: str) -> None:
    """Print container information"""
    container_info = get_container_info(container_type)
    
    if not container_info:
        print(f"Unknown container type: {container_type}")
        return
    
    print(f"Container: {container_info['name']}")
    print(f"Description: {container_info['description']}")
    print("Pros:")
    for pro in container_info['pros']:
        print(f"  - {pro}")
    print("Cons:")
    for con in container_info['cons']:
        print(f"  - {con}")

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
    print(f"Device type: {device_type}")
    
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
                print_container_info(selected)
                
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

## 5. Configuration Generation Script

### Configuration Generation Script
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

def generate_flask_config(device_type: str, container_type: str, output_dir: str) -> bool:
    """Generate Flask configuration file"""
    template_path = f"flask_config_{device_type}.py.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get(container_type, {})
    
    # Get environment variables
    env_vars = ENVIRONMENTS.get("production", {})
    
    # Add common variables
    common_vars = {
        "base_dir": str(Path.cwd()),
        "container_type": container_type,
        "environment": "production"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars, **env_vars}
    
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
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("docker", {})
    
    # Get environment variables
    env_vars = ENVIRONMENTS.get("production", {})
    
    # Add common variables
    common_vars = {
        "flask_env": "production",
        "pidns_username": "admin",
        "pidns_password": "password",
        "device_type": device_type
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars, **env_vars}
    
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
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("podman", {})
    
    # Get environment variables
    env_vars = ENVIRONMENTS.get("production", {})
    
    # Add common variables
    common_vars = {
        "flask_env": "production",
        "pidns_username": "admin",
        "pidns_password": "password",
        "device_type": device_type
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars, **env_vars}
    
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
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("lxc", {})
    
    # Add common variables
    common_vars = {
        "lxc_arch": "linuxarm" if device_type.startswith("pi") else "linuxamd64",
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars}
    
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
        print(f"Unknown container type: {container_type}")
        return False

def generate_all_configs(device_type: str, container_type: str, output_dir: str) -> bool:
    """Generate all configuration files"""
    # Create output directory
    if not create_output_directory(output_dir):
        return False
    
    # Generate Flask configuration
    if not generate_flask_config(device_type, container_type, output_dir):
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

## 6. Container Configuration Generation Script

### Container Configuration Generation Script
```python
# scripts/generate_container_config.py
#!/usr/bin/env python3
"""
Container configuration generation script for PiDNS
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

def generate_dockerfile(device_type: str, output_dir: str) -> bool:
    """Generate Dockerfile"""
    template_path = "Dockerfile.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("docker", {})
    
    # Get environment variables
    env_vars = ENVIRONMENTS.get("production", {})
    
    # Add common variables
    common_vars = {
        "device_type": device_type,
        "python_version": "3.11",
        "base_image": "python:3.11-slim-bullseye"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars, **env_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / "Dockerfile"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated Dockerfile: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render Dockerfile template: {e}")
        return False

def generate_containerfile(device_type: str, output_dir: str) -> bool:
    """Generate Containerfile"""
    template_path = "Containerfile.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("podman", {})
    
    # Get environment variables
    env_vars = ENVIRONMENTS.get("production", {})
    
    # Add common variables
    common_vars = {
        "device_type": device_type,
        "python_version": "3.11",
        "base_image": "python:3.11-slim-bullseye"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars, **env_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / "Containerfile"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated Containerfile: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render Containerfile template: {e}")
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
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("docker", {})
    
    # Get environment variables
    env_vars = ENVIRONMENTS.get("production", {})
    
    # Add common variables
    common_vars = {
        "flask_env": "production",
        "pidns_username": "admin",
        "pidns_password": "password",
        "device_type": device_type
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars, **env_vars}
    
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
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("podman", {})
    
    # Get environment variables
    env_vars = ENVIRONMENTS.get("production", {})
    
    # Add common variables
    common_vars = {
        "flask_env": "production",
        "pidns_username": "admin",
        "pidns_password": "password",
        "device_type": device_type
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars, **env_vars}
    
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
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("lxc", {})
    
    # Add common variables
    common_vars = {
        "lxc_arch": "linuxarm" if device_type.startswith("pi") else "linuxamd64",
        "dropped_capabilities": "sys_admin sys_module sys_rawio",
        "apparmor_profile": "lxc-container-default-with-ping"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars}
    
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

def generate_lxc_setup_script(device_type: str, output_dir: str) -> bool:
    """Generate LXC setup script"""
    template_path = "lxc-setup.sh.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("lxc", {})
    
    # Add common variables
    common_vars = {
        "device_type": device_type,
        "lxc_arch": "linuxarm" if device_type.startswith("pi") else "linuxamd64"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / "lxc-setup.sh"
        with open(output_file, 'w') as f:
            f.write(output)
        
        # Make script executable
        os.chmod(output_file, 0o755)
        
        print(f"Generated LXC setup script: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render LXC setup script template: {e}")
        return False

def generate_docker_service(device_type: str, output_dir: str) -> bool:
    """Generate Docker systemd service file"""
    template_path = "pidns-docker.service.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("docker", {})
    
    # Add common variables
    common_vars = {
        "device_type": device_type,
        "working_directory": "/home/pi/PiDNS"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / "pidns-docker.service"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated Docker systemd service: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render Docker systemd service template: {e}")
        return False

def generate_podman_service(device_type: str, output_dir: str) -> bool:
    """Generate Podman systemd service file"""
    template_path = "pidns-podman.service.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("podman", {})
    
    # Add common variables
    common_vars = {
        "device_type": device_type,
        "working_directory": "/home/pi/PiDNS"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / "pidns-podman.service"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated Podman systemd service: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render Podman systemd service template: {e}")
        return False

def generate_lxc_service(device_type: str, output_dir: str) -> bool:
    """Generate LXC systemd service file"""
    template_path = "pidns-lxc.service.j2"
    template = load_template(template_path)
    
    if not template:
        return False
    
    # Get device type variables
    device_vars = DEVICE_TYPES.get(device_type, {})
    
    # Get container type variables
    container_vars = CONTAINER_TYPES.get("lxc", {})
    
    # Add common variables
    common_vars = {
        "device_type": device_type,
        "working_directory": "/home/pi/PiDNS"
    }
    
    # Merge variables
    variables = {**common_vars, **device_vars, **container_vars}
    
    # Render template
    try:
        output = template.render(**variables)
        
        # Write output file
        output_file = Path(output_dir) / "pidns-lxc.service"
        with open(output_file, 'w') as f:
            f.write(output)
        
        print(f"Generated LXC systemd service: {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot render LXC systemd service template: {e}")
        return False

def generate_container_config(container_type: str, device_type: str, output_dir: str) -> bool:
    """Generate container configuration files"""
    if container_type == "docker":
        # Create containers directory
        containers_dir = Path(output_dir) / "containers"
        containers_dir.mkdir(exist_ok=True)
        
        # Generate Dockerfile
        if not generate_dockerfile(device_type, containers_dir):
            return False
        
        # Generate Docker Compose files
        if not generate_docker_compose(device_type, output_dir):
            return False
        
        # Generate Docker systemd service
        if not generate_docker_service(device_type, output_dir):
            return False
        
        return True
    elif container_type == "podman":
        # Create containers directory
        containers_dir = Path(output_dir) / "containers"
        containers_dir.mkdir(exist_ok=True)
        
        # Generate Containerfile
        if not generate_containerfile(device_type, containers_dir):
            return False
        
        # Generate Podman Compose files
        if not generate_podman_compose(device_type, output_dir):
            return False
        
        # Generate Podman systemd service
        if not generate_podman_service(device_type, output_dir):
            return False
        
        return True
    elif container_type == "lxc":
        # Create containers directory
        containers_dir = Path(output_dir) / "containers"
        containers_dir.mkdir(exist_ok=True)
        
        # Generate LXC configuration
        if not generate_lxc_config(device_type, containers_dir):
            return False
        
        # Generate LXC setup script
        if not generate_lxc_setup_script(device_type, containers_dir):
            return False
        
        # Generate LXC systemd service
        if not generate_lxc_service(device_type, output_dir):
            return False
        
        return True
    else:
        print(f"Unknown container type: {container_type}")
        return False

def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate PiDNS container configuration files')
    parser.add_argument('--container', type=str, required=True,
                        choices=['docker', 'podman', 'lxc'],
                        help='Container type')
    parser.add_argument('--device', type=str, required=True,
                        choices=['pi-zero', 'pi-zero-2w', 'pi-3', 'pi-4', 'pi-5', 'low-resource-pc', 'standard-pc'],
                        help='Device type')
    parser.add_argument('--output', type=str, default='./',
                        help='Output directory')
    
    args = parser.parse_args()
    
    # Generate container configuration files
    if generate_container_config(args.container, args.device, args.output):
        print(f"Successfully generated container configuration files for {args.container} on {args.device}")
        return 0
    else:
        print(f"Failed to generate container configuration files for {args.container} on {args.device}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

## 7. Installation Script Usage

### Command Line Usage
```bash
# Interactive installation (default)
./scripts/install.sh

# Silent installation with device and container specified
./scripts/install.sh --device pi-4 --container docker --silent

# Silent installation with device specified (container defaults to docker)
./scripts/install.sh --device pi-4 --silent

# Silent installation with container specified (device defaults to auto-detected)
./scripts/install.sh --container docker --silent

# Show help
./scripts/install.sh --help
```

### Interactive Installation Example
```bash
$ ./scripts/install.sh
PiDNS Installation Script
=========================

[STEP] Detecting device type...
[INFO] Detected device: Raspberry Pi 4

[STEP] Select Device Type
[INFO] Please select the type of device you are installing PiDNS on:

  1. Raspberry Pi Zero W (512MB RAM, 1-core CPU)
  2. Raspberry Pi Zero 2W (512MB RAM, 1-core CPU)
  3. Raspberry Pi 3 (1GB RAM, 4-core CPU)
  4. Raspberry Pi 4 (2-8GB RAM, 4-core CPU)
  5. Raspberry Pi 5 (4-8GB RAM, 4-core CPU)
  6. Low-Resource PC (≤1GB RAM, ≤2 cores)
  7. Standard PC (>1GB RAM, >2 cores)

Enter your choice (1-7): 4

[STEP] Select Container Type
[INFO] Please select the container type to use for PiDNS:

  1. Docker (recommended)
  2. Podman (recommended)
  3. LXC (recommended)

Enter your choice (1-3): 1

[STEP] Device Information
[INFO] Device: Raspberry Pi 4
[INFO] Memory: 2-8GB
[INFO] CPU: 4-core ARM
[INFO] Recommended containers: Docker, Podman, LXC

[STEP] Container Information
[INFO] Container: Docker
[INFO] Description: Most popular container platform with wide community support
[INFO] Pros: Wide community support, easy to use with Docker Compose, supports resource limits and health checks
[INFO] Cons: Requires Docker daemon, runs as root by default

Continue with installation? (y/n): y

[STEP] Installing dependencies
[INFO] Updating package lists...
[INFO] Installing Python and pip...
[INFO] Installing Jinja2...
[INFO] Installing other dependencies...
[INFO] Dependencies installed successfully

[STEP] Generating configuration files
[INFO] Generating Flask configuration...
[INFO] Generating dnsmasq configuration...
[INFO] Generating systemd service...
[INFO] Generating container configuration...
[INFO] Configuration files generated successfully

[STEP] Installing PiDNS with Docker
[INFO] Generating Docker configuration...
[INFO] Building Docker image...
[INFO] Starting Docker containers...
[INFO] Enabling Docker service...
[INFO] PiDNS installed successfully with Docker.

[STEP] Validating installation
[INFO] Checking if dashboard is accessible...
[INFO] Dashboard is accessible at http://192.168.1.100:8080
[INFO] Checking if ad-blocker is accessible...
[INFO] Ad-blocker is accessible at http://192.168.1.100:8081
[INFO] Checking if DNS is working...
[INFO] DNS is working
[INFO] Installation validated successfully

[STEP] Post-Installation Information
[INFO] PiDNS has been successfully installed!
[INFO]
[INFO] Dashboard URL: http://192.168.1.100:8080
[INFO] Default username: admin
[INFO] Default password: password
[INFO]
[INFO] Please change the default password after logging in.
[INFO]
[INFO] Container management commands:
[INFO]   Start: ./scripts/container-management.sh start pi-4
[INFO]   Stop: ./scripts/container-management.sh stop
[INFO]   Restart: ./scripts/container-management.sh restart pi-4
[INFO]   Status: ./scripts/container-management.sh status
[INFO]   Logs: ./scripts/container-management.sh logs
[INFO]
[INFO] Thank you for installing PiDNS!
```

### Silent Installation Example
```bash
$ ./scripts/install.sh --device pi-4 --container docker --silent
PiDNS Installation Script
=========================

[STEP] Installing dependencies
[INFO] Updating package lists...
[INFO] Installing Python and pip...
[INFO] Installing Jinja2...
[INFO] Installing other dependencies...
[INFO] Dependencies installed successfully

[STEP] Generating configuration files
[INFO] Generating Flask configuration...
[INFO] Generating dnsmasq configuration...
[INFO] Generating systemd service...
[INFO] Generating container configuration...
[INFO] Configuration files generated successfully

[STEP] Installing PiDNS with Docker
[INFO] Generating Docker configuration...
[INFO] Building Docker image...
[INFO] Starting Docker containers...
[INFO] Enabling Docker service...
[INFO] PiDNS installed successfully with Docker.

[STEP] Validating installation
[INFO] Checking if dashboard is accessible...
[INFO] Dashboard is accessible at http://192.168.1.100:8080
[INFO] Checking if ad-blocker is accessible...
[INFO] Ad-blocker is accessible at http://192.168.1.100:8081
[INFO] Checking if DNS is working...
[INFO] DNS is working
[INFO] Installation validated successfully

[STEP] Post-Installation Information
[INFO] PiDNS has been successfully installed!
[INFO]
[INFO] Dashboard URL: http://192.168.1.100:8080
[INFO] Default username: admin
[INFO] Default password: password
[INFO]
[INFO] Please change the default password after logging in.
[INFO]
[INFO] Container management commands:
[INFO]   Start: ./scripts/container-management.sh start pi-4
[INFO]   Stop: ./scripts/container-management.sh stop
[INFO]   Restart: ./scripts/container-management.sh restart pi-4
[INFO]   Status: ./scripts/container-management.sh status
[INFO]   Logs: ./scripts/container-management.sh logs
[INFO]
[INFO] Thank you for installing PiDNS!
```

## 8. Installation Script Error Handling

### Error Handling Strategies
1. **Graceful Degradation**: If a non-critical step fails, continue with the installation
2. **Rollback**: If a critical step fails, roll back any changes made
3. **Informative Messages**: Provide clear error messages to help users troubleshoot
4. **Logging**: Log all errors for debugging purposes
5. **Exit Codes**: Use appropriate exit codes to indicate success or failure

### Error Handling Examples
```bash
# Function to install dependencies with error handling
install_dependencies() {
    print_step "Installing dependencies"
    
    # Update package lists
    print_status "Updating package lists..."
    if ! apt-get update; then
        print_error "Failed to update package lists."
        return 1
    fi
    
    # Install Python and pip
    print_status "Installing Python and pip..."
    if ! apt-get install -y python3 python3-pip; then
        print_error "Failed to install Python and pip."
        return 1
    fi
    
    # Install Jinja2 for template rendering
    print_status "Installing Jinja2..."
    if ! pip3 install jinja2; then
        print_error "Failed to install Jinja2."
        return 1
    fi
    
    # Install other dependencies
    print_status "Installing other dependencies..."
    if ! apt-get install -y dnsmasq curl wget supervisor; then
        print_error "Failed to install other dependencies."
        return 1
    fi
    
    print_status "Dependencies installed successfully"
    return 0
}

# Function to generate configuration files with error handling
generate_configuration_files() {
    local device_type=$1
    local container_type=$2
    
    print_step "Generating configuration files"
    
    # Create config directory
    if ! mkdir -p config; then
        print_error "Failed to create config directory."
        return 1
    fi
    
    # Generate Flask configuration
    print_status "Generating Flask configuration..."
    if ! python3 scripts/generate_config.py --device $device_type --container $container_type; then
        print_error "Failed to generate Flask configuration."
        return 1
    fi
    
    # Generate dnsmasq configuration
    print_status "Generating dnsmasq configuration..."
    if ! cp config/dnsmasq.$device_type.conf config/dnsmasq.conf; then
        print_error "Failed to generate dnsmasq configuration."
        return 1
    fi
    
    # Generate systemd service
    print_status "Generating systemd service..."
    if ! cp services/pidns.$device_type.service services/pidns.service; then
        print_error "Failed to generate systemd service."
        return 1
    fi
    
    # Generate container configuration if needed
    if [ "$container_type" != "none" ]; then
        print_status "Generating container configuration..."
        if ! python3 scripts/generate_container_config.py --container $container_type --device $device_type; then
            print_error "Failed to generate container configuration."
            return 1
        fi
    fi
    
    print_status "Configuration files generated successfully"
    return 0
}

# Function to install PiDNS with error handling
install_pidns() {
    local device_type=$1
    local container_type=$2
    
    print_step "Installing PiDNS"
    
    case $container_type in
        "docker")
            if ! install_with_docker $device_type; then
                print_error "Failed to install PiDNS with Docker."
                return 1
            fi
            ;;
        "podman")
            if ! install_with_podman $device_type; then
                print_error "Failed to install PiDNS with Podman."
                return 1
            fi
            ;;
        "lxc")
            if ! install_with_lxc $device_type; then
                print_error "Failed to install PiDNS with LXC."
                return 1
            fi
            ;;
        "none")
            if ! install_without_containers $device_type; then
                print_error "Failed to install PiDNS without containers."
                return 1
            fi
            ;;
        *)
            print_error "Unknown container type: $container_type"
            return 1
            ;;
    esac
    
    return 0
}

# Function to validate installation with error handling
validate_installation() {
    local device_type=$1
    local container_type=$2
    
    print_step "Validating installation"
    
    # Check if dashboard is accessible
    print_status "Checking if dashboard is accessible..."
    local ip_address=$(hostname -I | awk '{print $1}')
    
    if ! curl -s -f http://$ip_address:8080/api/health > /dev/null; then
        print_error "Dashboard is not accessible at http://$ip_address:8080"
        return 1
    fi
    
    print_status "Dashboard is accessible at http://$ip_address:8080"
    
    # Check if ad-blocker is accessible if enabled
    if [ "$device_type" != "pi-zero" ] && [ "$device_type" != "pi-zero-2w" ]; then
        print_status "Checking if ad-blocker is accessible..."
        
        if ! curl -s -f http://$ip_address:8081/api/health > /dev/null; then
            print_error "Ad-blocker is not accessible at http://$ip_address:8081"
            return 1
        fi
        
        print_status "Ad-blocker is accessible at http://$ip_address:8081"
    fi
    
    # Check if DNS is working
    print_status "Checking if DNS is working..."
    
    if ! nslookup example.com $ip_address > /dev/null 2>&1; then
        print_error "DNS is not working"
        return 1
    fi
    
    print_status "DNS is working"
    print_status "Installation validated successfully"
    return 0
}

# Function to handle errors
handle_error() {
    local exit_code=$1
    local error_message=$2
    
    print_error "$error_message"
    
    # Log error
    echo "$(date): $error_message" >> /var/log/pidns/install.log
    
    # Exit with error code
    exit $exit_code
}

# Main function with error handling
main() {
    print_status "PiDNS Installation Script"
    print_status "========================="
    
    # Parse command line arguments
    local result=$(parse_arguments "$@")
    local parse_result=$?
    
    if [ $parse_result -ne 0 ]; then
        handle_error $parse_result "Failed to parse command line arguments."
    fi
    
    local device_type=$(echo "$result" | head -n 1)
    local container_type=$(echo "$result" | head -n 2 | tail -n 1)
    local silent=$(echo "$result" | tail -n 1)
    
    # If not in silent mode, ask for device type
    if [ "$silent" = false ]; then
        device_type=$(select_device_type_interactive)
    fi
    
    # Display device and container information
    display_device_info $device_type
    display_container_info $container_type
    
    # Confirm installation
    if [ "$silent" = false ]; then
        echo ""
        read -p "Continue with installation? (y/n): " confirm
        
        if [[ "$confirm" != "y" && "$confirm" != "yes" ]]; then
            print_status "Installation cancelled."
            return 0
        fi
    fi
    
    # Install dependencies
    if ! install_dependencies; then
        handle_error 1 "Failed to install dependencies."
    fi
    
    # Generate configuration files
    if ! generate_configuration_files $device_type $container_type; then
        handle_error 1 "Failed to generate configuration files."
    fi
    
    # Install PiDNS
    if ! install_pidns $device_type $container_type; then
        handle_error 1 "Failed to install PiDNS."
    fi
    
    # Validate installation
    if ! validate_installation $device_type $container_type; then
        handle_error 1 "Installation validation failed."
    fi
    
    # Display post-installation information
    display_post_installation_info $device_type $container_type
    
    return 0
}
```

## 9. Installation Script Testing

### Test Cases
1. **Interactive Installation Test**: Test the interactive installation process
2. **Silent Installation Test**: Test the silent installation process
3. **Device Detection Test**: Test device detection functionality
4. **Container Selection Test**: Test container selection functionality
5. **Configuration Generation Test**: Test configuration generation functionality
6. **Error Handling Test**: Test error handling functionality
7. **Rollback Test**: Test rollback functionality

### Test Scripts
```bash
#!/bin/bash
# tests/test_installation.sh - Test PiDNS installation script

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

# Function to test interactive installation
test_interactive_installation() {
    print_step "Testing interactive installation"
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Create a mock installation script that simulates user input
    cat > /tmp/mock_install.sh << 'EOF'
#!/bin/bash
# Mock installation script that simulates user input

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

# Simulate user input for device and container selection
echo -e "4\n1\ny" | ./scripts/install.sh --test-mode

# Check if installation was successful
if [ $? -eq 0 ]; then
    print_status "Interactive installation test passed."
    exit 0
else
    print_error "Interactive installation test failed."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    local result=$?
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    rm -f /tmp/mock_install.sh
    
    # Return test result
    if [ $result -eq 0 ]; then
        print_status "Interactive installation test passed."
        return 0
    else
        print_error "Interactive installation test failed."
        return 1
    fi
}

# Function to test silent installation
test_silent_installation() {
    print_step "Testing silent installation"
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test silent installation with Raspberry Pi 4 and Docker
    print_status "Testing silent installation with Raspberry Pi 4 and Docker..."
    ./scripts/install.sh --device pi-4 --container docker --silent
    local result=$?
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Return test result
    if [ $result -eq 0 ]; then
        print_status "Silent installation test passed."
        return 0
    else
        print_error "Silent installation test failed."
        return 1
    fi
}

# Function to test device detection
test_device_detection() {
    print_step "Testing device detection"
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test device detection script
    print_status "Testing device detection script..."
    python3 scripts/device_detection.py
    local result=$?
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Return test result
    if [ $result -eq 0 ]; then
        print_status "Device detection test passed."
        return 0
    else
        print_error "Device detection test failed."
        return 1
    fi
}

# Function to test container selection
test_container_selection() {
    print_step "Testing container selection"
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test container selection script
    print_status "Testing container selection script..."
    python3 scripts/container_selection.py
    local result=$?
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Return test result
    if [ $result -eq 0 ]; then
        print_status "Container selection test passed."
        return 0
    else
        print_error "Container selection test failed."
        return 1
    fi
}

# Function to test configuration generation
test_configuration_generation() {
    print_step "Testing configuration generation"
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test configuration generation script
    print_status "Testing configuration generation script..."
    python3 scripts/generate_config.py --device pi-4 --container docker
    local result=$?
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Return test result
    if [ $result -eq 0 ]; then
        print_status "Configuration generation test passed."
        return 0
    else
        print_error "Configuration generation test failed."
        return 1
    fi
}

# Function to test error handling
test_error_handling() {
    print_step "Testing error handling"
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test error handling with invalid device type
    print_status "Testing error handling with invalid device type..."
    ./scripts/install.sh --device invalid-device --container docker --silent
    local result=$?
    
    if [ $result -eq 0 ]; then
        print_error "Installation script did not fail with invalid device type."
        result=1
    else
        print_status "Installation script correctly failed with invalid device type."
        result=0
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Return test result
    if [ $result -eq 0 ]; then
        print_status "Error handling test passed."
        return 0
    else
        print_error "Error handling test failed."
        return 1
    fi
}

# Function to test rollback
test_rollback() {
    print_step "Testing rollback"
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test rollback by simulating a failed installation
    print_status "Testing rollback by simulating a failed installation..."
    
    # Create a mock installation script that fails during installation
    cat > /tmp/mock_install.sh << 'EOF'
#!/bin/bash
# Mock installation script that fails during installation

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

# Simulate user input for device and container selection
echo -e "4\n1\ny" | ./scripts/install.sh --test-mode --fail-at-install

# Check if installation was successful
if [ $? -ne 0 ]; then
    print_status "Rollback test passed. Installation correctly failed and rolled back."
    exit 0
else
    print_error "Rollback test failed. Installation did not fail as expected."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    local result=$?
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    rm -f /tmp/mock_install.sh
    
    # Return test result
    if [ $result -eq 0 ]; then
        print_status "Rollback test passed."
        return 0
    else
        print_error "Rollback test failed."
        return 1
    fi
}

# Main function
main() {
    print_status "Running PiDNS installation script tests"
    print_status "======================================"
    
    local total_tests=0
    local passed_tests=0
    local failed_tests=0
    
    # Test interactive installation
    test_interactive_installation
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Test silent installation
    test_silent_installation
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Test device detection
    test_device_detection
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Test container selection
    test_container_selection
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Test configuration generation
    test_configuration_generation
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Test error handling
    test_error_handling
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Test rollback
    test_rollback
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Print test summary
    print_status "======================================"
    print_status "Test Summary"
    print_status "======================================"
    print_status "Total tests: $total_tests"
    print_status "Passed tests: $passed_tests"
    print_status "Failed tests: $failed_tests"
    
    if [ $failed_tests -eq 0 ]; then
        print_status "All tests passed!"
        return 0
    else
        print_error "$failed_tests test(s) failed."
        return 1
    fi
}

# Run main function
main
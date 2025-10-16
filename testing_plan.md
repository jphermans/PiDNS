# PiDNS Installation Testing Plan

## 1. Testing Overview

### Testing Goals
1. **Functionality**: Ensure all installation options work correctly
2. **Compatibility**: Verify compatibility with all supported devices and containers
3. **Performance**: Confirm performance optimizations are applied correctly
4. **Stability**: Ensure the system remains stable after installation
5. **User Experience**: Validate that the installation process is user-friendly

### Testing Categories
1. **Unit Testing**: Test individual components in isolation
2. **Integration Testing**: Test the entire installation process
3. **Device Testing**: Test on all supported device types
4. **Container Testing**: Test with all container options
5. **Error Handling Testing**: Test error scenarios and recovery
6. **User Acceptance Testing**: Test with real users

## 2. Test Environment Setup

### Test Devices
1. **Raspberry Pi Zero W**: 512MB RAM, 1-core CPU
2. **Raspberry Pi Zero 2W**: 512MB RAM, 1-core CPU
3. **Raspberry Pi 3**: 1GB RAM, 4-core CPU
4. **Raspberry Pi 4**: 4GB RAM, 4-core CPU
5. **Raspberry Pi 5**: 8GB RAM, 4-core CPU
6. **Low-Resource PC**: 1GB RAM, 2-core CPU
7. **Standard PC**: 8GB RAM, 4-core CPU

### Test Operating Systems
1. **Raspberry Pi OS**: Bullseye (32-bit and 64-bit)
2. **Debian**: Bullseye (32-bit and 64-bit)
3. **Ubuntu**: 22.04 LTS (32-bit and 64-bit)

### Test Container Platforms
1. **Docker**: Version 20.10 and later
2. **Podman**: Version 3.0 and later
3. **LXC**: Version 4.0 and later

### Test Network Configurations
1. **Ethernet**: Wired network connection
2. **WiFi**: Wireless network connection
3. **Mixed**: Both Ethernet and WiFi connections

## 3. Test Cases

### Unit Testing

#### Device Detection Test
```bash
#!/bin/bash
# test_device_detection.sh - Test device detection functionality

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

# Function to test device detection
test_device_detection() {
    print_step "Testing device detection..."
    
    local test_passed=true
    
    # Test device detection for Raspberry Pi Zero W
    print_status "Testing device detection for Raspberry Pi Zero W..."
    if ! grep -q "Raspberry Pi Zero W" /proc/device-tree/model 2>/dev/null; then
        # Mock device detection for testing
        echo "Raspberry Pi Zero W" > /tmp/device_model
        DEVICE_TYPE=$(python3 -c "
import sys
sys.path.append('scripts')
from device_detection import detect_device
with open('/tmp/device_model', 'r') as f:
    model = f.read().strip()
print(detect_device(model))
")
        if [ "$DEVICE_TYPE" != "pi-zero" ]; then
            print_error "Incorrect device type detected for Raspberry Pi Zero W: $DEVICE_TYPE (expected: pi-zero)"
            test_passed=false
        else
            print_status "Correct device type detected for Raspberry Pi Zero W: $DEVICE_TYPE"
        fi
    fi
    
    # Test device detection for Raspberry Pi Zero 2W
    print_status "Testing device detection for Raspberry Pi Zero 2W..."
    if ! grep -q "Raspberry Pi Zero 2 W" /proc/device-tree/model 2>/dev/null; then
        # Mock device detection for testing
        echo "Raspberry Pi Zero 2 W" > /tmp/device_model
        DEVICE_TYPE=$(python3 -c "
import sys
sys.path.append('scripts')
from device_detection import detect_device
with open('/tmp/device_model', 'r') as f:
    model = f.read().strip()
print(detect_device(model))
")
        if [ "$DEVICE_TYPE" != "pi-zero-2w" ]; then
            print_error "Incorrect device type detected for Raspberry Pi Zero 2W: $DEVICE_TYPE (expected: pi-zero-2w)"
            test_passed=false
        else
            print_status "Correct device type detected for Raspberry Pi Zero 2W: $DEVICE_TYPE"
        fi
    fi
    
    # Test device detection for Raspberry Pi 3
    print_status "Testing device detection for Raspberry Pi 3..."
    if ! grep -q "Raspberry Pi 3" /proc/device-tree/model 2>/dev/null; then
        # Mock device detection for testing
        echo "Raspberry Pi 3" > /tmp/device_model
        DEVICE_TYPE=$(python3 -c "
import sys
sys.path.append('scripts')
from device_detection import detect_device
with open('/tmp/device_model', 'r') as f:
    model = f.read().strip()
print(detect_device(model))
")
        if [ "$DEVICE_TYPE" != "pi-3" ]; then
            print_error "Incorrect device type detected for Raspberry Pi 3: $DEVICE_TYPE (expected: pi-3)"
            test_passed=false
        else
            print_status "Correct device type detected for Raspberry Pi 3: $DEVICE_TYPE"
        fi
    fi
    
    # Test device detection for Raspberry Pi 4
    print_status "Testing device detection for Raspberry Pi 4..."
    if ! grep -q "Raspberry Pi 4" /proc/device-tree/model 2>/dev/null; then
        # Mock device detection for testing
        echo "Raspberry Pi 4" > /tmp/device_model
        DEVICE_TYPE=$(python3 -c "
import sys
sys.path.append('scripts')
from device_detection import detect_device
with open('/tmp/device_model', 'r') as f:
    model = f.read().strip()
print(detect_device(model))
")
        if [ "$DEVICE_TYPE" != "pi-4" ]; then
            print_error "Incorrect device type detected for Raspberry Pi 4: $DEVICE_TYPE (expected: pi-4)"
            test_passed=false
        else
            print_status "Correct device type detected for Raspberry Pi 4: $DEVICE_TYPE"
        fi
    fi
    
    # Test device detection for Raspberry Pi 5
    print_status "Testing device detection for Raspberry Pi 5..."
    if ! grep -q "Raspberry Pi 5" /proc/device-tree/model 2>/dev/null; then
        # Mock device detection for testing
        echo "Raspberry Pi 5" > /tmp/device_model
        DEVICE_TYPE=$(python3 -c "
import sys
sys.path.append('scripts')
from device_detection import detect_device
with open('/tmp/device_model', 'r') as f:
    model = f.read().strip()
print(detect_device(model))
")
        if [ "$DEVICE_TYPE" != "pi-5" ]; then
            print_error "Incorrect device type detected for Raspberry Pi 5: $DEVICE_TYPE (expected: pi-5)"
            test_passed=false
        else
            print_status "Correct device type detected for Raspberry Pi 5: $DEVICE_TYPE"
        fi
    fi
    
    # Test device detection for Low-Resource PC
    print_status "Testing device detection for Low-Resource PC..."
    # Mock device detection for testing
    echo "Unknown PC" > /tmp/device_model
    TOTAL_MEM=$(free -m | awk '/Mem:/ {print $2}')
    CPU_CORES=$(nproc)
    DEVICE_TYPE=$(python3 -c "
import sys
sys.path.append('scripts')
from device_detection import detect_device
with open('/tmp/device_model', 'r') as f:
    model = f.read().strip()
print(detect_device(model, total_mem=$TOTAL_MEM, cpu_cores=$CPU_CORES))
")
    if [ "$DEVICE_TYPE" != "low-resource-pc" ]; then
        print_error "Incorrect device type detected for Low-Resource PC: $DEVICE_TYPE (expected: low-resource-pc)"
        test_passed=false
    else
        print_status "Correct device type detected for Low-Resource PC: $DEVICE_TYPE"
    fi
    
    # Test device detection for Standard PC
    print_status "Testing device detection for Standard PC..."
    # Mock device detection for testing
    echo "Unknown PC" > /tmp/device_model
    TOTAL_MEM=$(free -m | awk '/Mem:/ {print $2}')
    CPU_CORES=$(nproc)
    DEVICE_TYPE=$(python3 -c "
import sys
sys.path.append('scripts')
from device_detection import detect_device
with open('/tmp/device_model', 'r') as f:
    model = f.read().strip()
print(detect_device(model, total_mem=$TOTAL_MEM, cpu_cores=$CPU_CORES))
")
    if [ "$DEVICE_TYPE" != "standard-pc" ]; then
        print_error "Incorrect device type detected for Standard PC: $DEVICE_TYPE (expected: standard-pc)"
        test_passed=false
    else
        print_status "Correct device type detected for Standard PC: $DEVICE_TYPE"
    fi
    
    # Clean up
    rm -f /tmp/device_model
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Device detection tests passed."
        return 0
    else
        print_error "Device detection tests failed."
        return 1
    fi
}

# Run device detection tests
test_device_detection
```

#### Configuration Generation Test
```bash
#!/bin/bash
# test_configuration_generation.sh - Test configuration generation functionality

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

# Function to test configuration generation
test_configuration_generation() {
    print_step "Testing configuration generation..."
    
    local test_passed=true
    
    # Test configuration generation for Raspberry Pi Zero W
    print_status "Testing configuration generation for Raspberry Pi Zero W..."
    python3 scripts/generate_config.py --device pi-zero --output /tmp
    if [ ! -f "/tmp/flask_config.pi-zero.py" ]; then
        print_error "Flask configuration file not generated for Raspberry Pi Zero W"
        test_passed=false
    else
        print_status "Flask configuration file generated for Raspberry Pi Zero W"
    fi
    
    if [ ! -f "/tmp/dnsmasq.pi-zero.conf" ]; then
        print_error "dnsmasq configuration file not generated for Raspberry Pi Zero W"
        test_passed=false
    else
        print_status "dnsmasq configuration file generated for Raspberry Pi Zero W"
    fi
    
    if [ ! -f "/tmp/pidns.pi-zero.service" ]; then
        print_error "Systemd service file not generated for Raspberry Pi Zero W"
        test_passed=false
    else
        print_status "Systemd service file generated for Raspberry Pi Zero W"
    fi
    
    # Test configuration generation for Raspberry Pi 3
    print_status "Testing configuration generation for Raspberry Pi 3..."
    python3 scripts/generate_config.py --device pi-3 --output /tmp
    if [ ! -f "/tmp/flask_config.pi-3.py" ]; then
        print_error "Flask configuration file not generated for Raspberry Pi 3"
        test_passed=false
    else
        print_status "Flask configuration file generated for Raspberry Pi 3"
    fi
    
    if [ ! -f "/tmp/dnsmasq.pi-3.conf" ]; then
        print_error "dnsmasq configuration file not generated for Raspberry Pi 3"
        test_passed=false
    else
        print_status "dnsmasq configuration file generated for Raspberry Pi 3"
    fi
    
    if [ ! -f "/tmp/pidns.pi-3.service" ]; then
        print_error "Systemd service file not generated for Raspberry Pi 3"
        test_passed=false
    else
        print_status "Systemd service file generated for Raspberry Pi 3"
    fi
    
    # Test configuration generation for Raspberry Pi 4/5
    print_status "Testing configuration generation for Raspberry Pi 4/5..."
    python3 scripts/generate_config.py --device pi-4 --output /tmp
    if [ ! -f "/tmp/flask_config.pi-4-5.py" ]; then
        print_error "Flask configuration file not generated for Raspberry Pi 4/5"
        test_passed=false
    else
        print_status "Flask configuration file generated for Raspberry Pi 4/5"
    fi
    
    if [ ! -f "/tmp/dnsmasq.pi-4-5.conf" ]; then
        print_error "dnsmasq configuration file not generated for Raspberry Pi 4/5"
        test_passed=false
    else
        print_status "dnsmasq configuration file generated for Raspberry Pi 4/5"
    fi
    
    if [ ! -f "/tmp/pidns.pi-4-5.service" ]; then
        print_error "Systemd service file not generated for Raspberry Pi 4/5"
        test_passed=false
    else
        print_status "Systemd service file generated for Raspberry Pi 4/5"
    fi
    
    # Test configuration generation for Low-Resource PC
    print_status "Testing configuration generation for Low-Resource PC..."
    python3 scripts/generate_config.py --device low-resource-pc --output /tmp
    if [ ! -f "/tmp/flask_config.low-resource-pc.py" ]; then
        print_error "Flask configuration file not generated for Low-Resource PC"
        test_passed=false
    else
        print_status "Flask configuration file generated for Low-Resource PC"
    fi
    
    if [ ! -f "/tmp/dnsmasq.low-resource-pc.conf" ]; then
        print_error "dnsmasq configuration file not generated for Low-Resource PC"
        test_passed=false
    else
        print_status "dnsmasq configuration file generated for Low-Resource PC"
    fi
    
    if [ ! -f "/tmp/pidns.low-resource-pc.service" ]; then
        print_error "Systemd service file not generated for Low-Resource PC"
        test_passed=false
    else
        print_status "Systemd service file generated for Low-Resource PC"
    fi
    
    # Test configuration generation for Standard PC
    print_status "Testing configuration generation for Standard PC..."
    python3 scripts/generate_config.py --device standard-pc --output /tmp
    if [ ! -f "/tmp/flask_config.standard-pc.py" ]; then
        print_error "Flask configuration file not generated for Standard PC"
        test_passed=false
    else
        print_status "Flask configuration file generated for Standard PC"
    fi
    
    if [ ! -f "/tmp/dnsmasq.standard-pc.conf" ]; then
        print_error "dnsmasq configuration file not generated for Standard PC"
        test_passed=false
    else
        print_status "dnsmasq configuration file generated for Standard PC"
    fi
    
    if [ ! -f "/tmp/pidns.standard-pc.service" ]; then
        print_error "Systemd service file not generated for Standard PC"
        test_passed=false
    else
        print_status "Systemd service file generated for Standard PC"
    fi
    
    # Test configuration validation
    print_status "Testing configuration validation..."
    python3 scripts/validate_config.py --device pi-zero --config /tmp/flask_config.pi-zero.py
    if [ $? -ne 0 ]; then
        print_error "Flask configuration validation failed for Raspberry Pi Zero W"
        test_passed=false
    else
        print_status "Flask configuration validation passed for Raspberry Pi Zero W"
    fi
    
    python3 scripts/validate_config.py --device pi-zero --config /tmp/dnsmasq.pi-zero.conf
    if [ $? -ne 0 ]; then
        print_error "dnsmasq configuration validation failed for Raspberry Pi Zero W"
        test_passed=false
    else
        print_status "dnsmasq configuration validation passed for Raspberry Pi Zero W"
    fi
    
    python3 scripts/validate_config.py --device pi-zero --config /tmp/pidns.pi-zero.service
    if [ $? -ne 0 ]; then
        print_error "Systemd service validation failed for Raspberry Pi Zero W"
        test_passed=false
    else
        print_status "Systemd service validation passed for Raspberry Pi Zero W"
    fi
    
    # Clean up
    rm -rf /tmp/flask_config.*.py /tmp/dnsmasq.*.conf /tmp/pidns.*.service
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Configuration generation tests passed."
        return 0
    else
        print_error "Configuration generation tests failed."
        return 1
    fi
}

# Run configuration generation tests
test_configuration_generation
```

#### Container Configuration Test
```bash
#!/bin/bash
# test_container_configuration.sh - Test container configuration functionality

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

# Function to test container configuration
test_container_configuration() {
    print_step "Testing container configuration..."
    
    local test_passed=true
    
    # Test Docker configuration generation
    print_status "Testing Docker configuration generation..."
    python3 scripts/generate_container_config.py --container docker --device pi-4 --output /tmp
    if [ ! -f "/tmp/Dockerfile" ]; then
        print_error "Dockerfile not generated for Docker"
        test_passed=false
    else
        print_status "Dockerfile generated for Docker"
    fi
    
    if [ ! -f "/tmp/docker-compose.yml" ]; then
        print_error "docker-compose.yml not generated for Docker"
        test_passed=false
    else
        print_status "docker-compose.yml generated for Docker"
    fi
    
    if [ ! -f "/tmp/docker-compose.override.pi-4.yml" ]; then
        print_error "docker-compose.override.yml not generated for Docker"
        test_passed=false
    else
        print_status "docker-compose.override.yml generated for Docker"
    fi
    
    if [ ! -f "/tmp/pidns-docker.service" ]; then
        print_error "Systemd service file not generated for Docker"
        test_passed=false
    else
        print_status "Systemd service file generated for Docker"
    fi
    
    # Test Podman configuration generation
    print_status "Testing Podman configuration generation..."
    python3 scripts/generate_container_config.py --container podman --device pi-4 --output /tmp
    if [ ! -f "/tmp/Containerfile" ]; then
        print_error "Containerfile not generated for Podman"
        test_passed=false
    else
        print_status "Containerfile generated for Podman"
    fi
    
    if [ ! -f "/tmp/podman-compose.yml" ]; then
        print_error "podman-compose.yml not generated for Podman"
        test_passed=false
    else
        print_status "podman-compose.yml generated for Podman"
    fi
    
    if [ ! -f "/tmp/podman-compose.override.pi-4.yml" ]; then
        print_error "podman-compose.override.yml not generated for Podman"
        test_passed=false
    else
        print_status "podman-compose.override.yml generated for Podman"
    fi
    
    if [ ! -f "/tmp/pidns-podman.service" ]; then
        print_error "Systemd service file not generated for Podman"
        test_passed=false
    else
        print_status "Systemd service file generated for Podman"
    fi
    
    if [ ! -f "/tmp/pidns.container" ]; then
        print_error "Quadlet file not generated for Podman"
        test_passed=false
    else
        print_status "Quadlet file generated for Podman"
    fi
    
    # Test LXC configuration generation
    print_status "Testing LXC configuration generation..."
    python3 scripts/generate_container_config.py --container lxc --device pi-4 --output /tmp
    if [ ! -f "/tmp/lxc-pi-4.conf" ]; then
        print_error "LXC configuration file not generated for LXC"
        test_passed=false
    else
        print_status "LXC configuration file generated for LXC"
    fi
    
    if [ ! -f "/tmp/pidns-lxc.service" ]; then
        print_error "Systemd service file not generated for LXC"
        test_passed=false
    else
        print_status "Systemd service file generated for LXC"
    fi
    
    # Test container configuration validation
    print_status "Testing container configuration validation..."
    python3 scripts/validate_container_config.py --container docker --device pi-4 --config /tmp/Dockerfile
    if [ $? -ne 0 ]; then
        print_error "Docker configuration validation failed"
        test_passed=false
    else
        print_status "Docker configuration validation passed"
    fi
    
    python3 scripts/validate_container_config.py --container docker --device pi-4 --config /tmp/docker-compose.yml
    if [ $? -ne 0 ]; then
        print_error "Docker Compose configuration validation failed"
        test_passed=false
    else
        print_status "Docker Compose configuration validation passed"
    fi
    
    python3 scripts/validate_container_config.py --container podman --device pi-4 --config /tmp/Containerfile
    if [ $? -ne 0 ]; then
        print_error "Podman configuration validation failed"
        test_passed=false
    else
        print_status "Podman configuration validation passed"
    fi
    
    python3 scripts/validate_container_config.py --container podman --device pi-4 --config /tmp/podman-compose.yml
    if [ $? -ne 0 ]; then
        print_error "Podman Compose configuration validation failed"
        test_passed=false
    else
        print_status "Podman Compose configuration validation passed"
    fi
    
    python3 scripts/validate_container_config.py --container lxc --device pi-4 --config /tmp/lxc-pi-4.conf
    if [ $? -ne 0 ]; then
        print_error "LXC configuration validation failed"
        test_passed=false
    else
        print_status "LXC configuration validation passed"
    fi
    
    # Clean up
    rm -rf /tmp/Dockerfile /tmp/Containerfile /tmp/docker-compose*.yml /tmp/podman-compose*.yml /tmp/lxc-*.conf /tmp/pidns*.service /tmp/pidns.container
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Container configuration tests passed."
        return 0
    else
        print_error "Container configuration tests failed."
        return 1
    fi
}

# Run container configuration tests
test_container_configuration
```

### Integration Testing

#### Interactive Installation Test
```bash
#!/bin/bash
# test_interactive_installation.sh - Test interactive installation functionality

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
    print_step "Testing interactive installation..."
    
    local test_passed=true
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test interactive installation with Raspberry Pi Zero W and Docker
    print_status "Testing interactive installation with Raspberry Pi Zero W and Docker..."
    
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

# Simulate user input for device selection
echo "8" | ./scripts/install.sh --test-mode

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
    
    if [ $result -ne 0 ]; then
        print_error "Interactive installation test failed."
        test_passed=false
    else
        print_status "Interactive installation test passed."
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    rm -f /tmp/mock_install.sh
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Interactive installation tests passed."
        return 0
    else
        print_error "Interactive installation tests failed."
        return 1
    fi
}

# Run interactive installation tests
test_interactive_installation
```

#### Silent Installation Test
```bash
#!/bin/bash
# test_silent_installation.sh - Test silent installation functionality

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

# Function to test silent installation
test_silent_installation() {
    print_step "Testing silent installation..."
    
    local test_passed=true
    
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
    
    if [ $result -ne 0 ]; then
        print_error "Silent installation test failed for Raspberry Pi 4 and Docker."
        test_passed=false
    else
        print_status "Silent installation test passed for Raspberry Pi 4 and Docker."
    fi
    
    # Test silent installation with Raspberry Pi 3 and Podman
    print_status "Testing silent installation with Raspberry Pi 3 and Podman..."
    ./scripts/install.sh --device pi-3 --container podman --silent
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Silent installation test failed for Raspberry Pi 3 and Podman."
        test_passed=false
    else
        print_status "Silent installation test passed for Raspberry Pi 3 and Podman."
    fi
    
    # Test silent installation with Low-Resource PC and LXC
    print_status "Testing silent installation with Low-Resource PC and LXC..."
    ./scripts/install.sh --device low-resource-pc --container lxc --silent
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Silent installation test failed for Low-Resource PC and LXC."
        test_passed=false
    else
        print_status "Silent installation test passed for Low-Resource PC and LXC."
    fi
    
    # Test silent installation with Standard PC and bare metal
    print_status "Testing silent installation with Standard PC and bare metal..."
    ./scripts/install.sh --device standard-pc --container none --silent
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Silent installation test failed for Standard PC and bare metal."
        test_passed=false
    else
        print_status "Silent installation test passed for Standard PC and bare metal."
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Silent installation tests passed."
        return 0
    else
        print_error "Silent installation tests failed."
        return 1
    fi
}

# Run silent installation tests
test_silent_installation
```

### Device Testing

#### Raspberry Pi Zero W Test
```bash
#!/bin/bash
# test_raspberry_pi_zero_w.sh - Test installation on Raspberry Pi Zero W

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

# Function to test Raspberry Pi Zero W installation
test_raspberry_pi_zero_w() {
    print_step "Testing Raspberry Pi Zero W installation..."
    
    local test_passed=true
    
    # Check if we're running on a Raspberry Pi Zero W
    if ! grep -q "Raspberry Pi Zero W" /proc/device-tree/model 2>/dev/null; then
        print_warning "Not running on a Raspberry Pi Zero W. Skipping device-specific tests."
        return 0
    fi
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with Docker
    print_status "Testing installation with Docker..."
    ./scripts/install.sh --device pi-zero --container docker --silent
    local result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test failed for Raspberry Pi Zero W with Docker."
        test_passed=false
    else
        print_status "Installation test passed for Raspberry Pi Zero W with Docker."
        
        # Verify that the system is running correctly
        print_status "Verifying system operation..."
        
        # Check if Docker container is running
        if ! docker ps --format '{{.Names}}' | grep -q "^pidns$"; then
            print_error "Docker container is not running."
            test_passed=false
        else
            print_status "Docker container is running."
        fi
        
        # Check if dashboard is accessible
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible."
            test_passed=false
        else
            print_status "Main dashboard is accessible."
        fi
        
        if ! curl -s -f http://localhost:8081/api/health > /dev/null; then
            print_error "Ad-blocker dashboard is not accessible."
            test_passed=false
        else
            print_status "Ad-blocker dashboard is accessible."
        fi
        
        # Check if DNS is working
        if ! nslookup example.com localhost >/dev/null 2>&1; then
            print_error "DNS is not working."
            test_passed=false
        else
            print_status "DNS is working."
        fi
        
        # Check resource usage
        print_status "Checking resource usage..."
        local memory_usage=$(free -m | awk '/Mem:/ {print $3}')
        local cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print $1}')
        
        print_status "Memory usage: ${memory_usage}MB"
        print_status "CPU usage: ${cpu_usage}%"
        
        if [ "$memory_usage" -gt 400 ]; then
            print_warning "Memory usage is high for Raspberry Pi Zero W: ${memory_usage}MB"
        fi
        
        if [ "$cpu_usage" -gt 80 ]; then
            print_warning "CPU usage is high for Raspberry Pi Zero W: ${cpu_usage}%"
        fi
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Raspberry Pi Zero W installation tests passed."
        return 0
    else
        print_error "Raspberry Pi Zero W installation tests failed."
        return 1
    fi
}

# Run Raspberry Pi Zero W tests
test_raspberry_pi_zero_w
```

#### Raspberry Pi 3 Test
```bash
#!/bin/bash
# test_raspberry_pi_3.sh - Test installation on Raspberry Pi 3

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

# Function to test Raspberry Pi 3 installation
test_raspberry_pi_3() {
    print_step "Testing Raspberry Pi 3 installation..."
    
    local test_passed=true
    
    # Check if we're running on a Raspberry Pi 3
    if ! grep -q "Raspberry Pi 3" /proc/device-tree/model 2>/dev/null; then
        print_warning "Not running on a Raspberry Pi 3. Skipping device-specific tests."
        return 0
    fi
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with Podman
    print_status "Testing installation with Podman..."
    ./scripts/install.sh --device pi-3 --container podman --silent
    local result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test failed for Raspberry Pi 3 with Podman."
        test_passed=false
    else
        print_status "Installation test passed for Raspberry Pi 3 with Podman."
        
        # Verify that the system is running correctly
        print_status "Verifying system operation..."
        
        # Check if Podman container is running
        if ! podman ps --format '{{.Names}}' | grep -q "^pidns$"; then
            print_error "Podman container is not running."
            test_passed=false
        else
            print_status "Podman container is running."
        fi
        
        # Check if dashboard is accessible
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible."
            test_passed=false
        else
            print_status "Main dashboard is accessible."
        fi
        
        if ! curl -s -f http://localhost:8081/api/health > /dev/null; then
            print_error "Ad-blocker dashboard is not accessible."
            test_passed=false
        else
            print_status "Ad-blocker dashboard is accessible."
        fi
        
        # Check if DNS is working
        if ! nslookup example.com localhost >/dev/null 2>&1; then
            print_error "DNS is not working."
            test_passed=false
        else
            print_status "DNS is working."
        fi
        
        # Check resource usage
        print_status "Checking resource usage..."
        local memory_usage=$(free -m | awk '/Mem:/ {print $3}')
        local cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print $1}')
        
        print_status "Memory usage: ${memory_usage}MB"
        print_status "CPU usage: ${cpu_usage}%"
        
        if [ "$memory_usage" -gt 700 ]; then
            print_warning "Memory usage is high for Raspberry Pi 3: ${memory_usage}MB"
        fi
        
        if [ "$cpu_usage" -gt 70 ]; then
            print_warning "CPU usage is high for Raspberry Pi 3: ${cpu_usage}%"
        fi
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Raspberry Pi 3 installation tests passed."
        return 0
    else
        print_error "Raspberry Pi 3 installation tests failed."
        return 1
    fi
}

# Run Raspberry Pi 3 tests
test_raspberry_pi_3
```

#### Raspberry Pi 4/5 Test
```bash
#!/bin/bash
# test_raspberry_pi_4_5.sh - Test installation on Raspberry Pi 4/5

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

# Function to test Raspberry Pi 4/5 installation
test_raspberry_pi_4_5() {
    print_step "Testing Raspberry Pi 4/5 installation..."
    
    local test_passed=true
    
    # Check if we're running on a Raspberry Pi 4 or 5
    if ! grep -q "Raspberry Pi 4" /proc/device-tree/model 2>/dev/null && ! grep -q "Raspberry Pi 5" /proc/device-tree/model 2>/dev/null; then
        print_warning "Not running on a Raspberry Pi 4 or 5. Skipping device-specific tests."
        return 0
    fi
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with LXC
    print_status "Testing installation with LXC..."
    ./scripts/install.sh --device pi-4 --container lxc --silent
    local result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test failed for Raspberry Pi 4/5 with LXC."
        test_passed=false
    else
        print_status "Installation test passed for Raspberry Pi 4/5 with LXC."
        
        # Verify that the system is running correctly
        print_status "Verifying system operation..."
        
        # Check if LXC container is running
        if ! lxc-info -n pidns -s | grep -q "RUNNING"; then
            print_error "LXC container is not running."
            test_passed=false
        else
            print_status "LXC container is running."
        fi
        
        # Get container IP
        local container_ip=$(lxc-info -n pidns -iH)
        
        # Check if dashboard is accessible
        if ! curl -s -f http://$container_ip:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible."
            test_passed=false
        else
            print_status "Main dashboard is accessible."
        fi
        
        if ! curl -s -f http://$container_ip:8081/api/health > /dev/null; then
            print_error "Ad-blocker dashboard is not accessible."
            test_passed=false
        else
            print_status "Ad-blocker dashboard is accessible."
        fi
        
        # Check if DNS is working
        if ! nslookup example.com $container_ip >/dev/null 2>&1; then
            print_error "DNS is not working."
            test_passed=false
        else
            print_status "DNS is working."
        fi
        
        # Check resource usage
        print_status "Checking resource usage..."
        local memory_usage=$(free -m | awk '/Mem:/ {print $3}')
        local cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print $1}')
        
        print_status "Memory usage: ${memory_usage}MB"
        print_status "CPU usage: ${cpu_usage}%"
        
        if [ "$memory_usage" -gt 1500 ]; then
            print_warning "Memory usage is high for Raspberry Pi 4/5: ${memory_usage}MB"
        fi
        
        if [ "$cpu_usage" -gt 60 ]; then
            print_warning "CPU usage is high for Raspberry Pi 4/5: ${cpu_usage}%"
        fi
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Raspberry Pi 4/5 installation tests passed."
        return 0
    else
        print_error "Raspberry Pi 4/5 installation tests failed."
        return 1
    fi
}

# Run Raspberry Pi 4/5 tests
test_raspberry_pi_4_5
```

#### Low-Resource PC Test
```bash
#!/bin/bash
# test_low_resource_pc.sh - Test installation on Low-Resource PC

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

# Function to test Low-Resource PC installation
test_low_resource_pc() {
    print_step "Testing Low-Resource PC installation..."
    
    local test_passed=true
    
    # Check if we're running on a Low-Resource PC
    local total_mem=$(free -m | awk '/Mem:/ {print $2}')
    local cpu_cores=$(nproc)
    
    if [ "$total_mem" -gt 1024 ] || [ "$cpu_cores" -gt 2 ]; then
        print_warning "Not running on a Low-Resource PC. Skipping device-specific tests."
        return 0
    fi
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with Docker
    print_status "Testing installation with Docker..."
    ./scripts/install.sh --device low-resource-pc --container docker --silent
    local result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test failed for Low-Resource PC with Docker."
        test_passed=false
    else
        print_status "Installation test passed for Low-Resource PC with Docker."
        
        # Verify that the system is running correctly
        print_status "Verifying system operation..."
        
        # Check if Docker container is running
        if ! docker ps --format '{{.Names}}' | grep -q "^pidns$"; then
            print_error "Docker container is not running."
            test_passed=false
        else
            print_status "Docker container is running."
        fi
        
        # Check if dashboard is accessible
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible."
            test_passed=false
        else
            print_status "Main dashboard is accessible."
        fi
        
        if ! curl -s -f http://localhost:8081/api/health > /dev/null; then
            print_error "Ad-blocker dashboard is not accessible."
            test_passed=false
        else
            print_status "Ad-blocker dashboard is accessible."
        fi
        
        # Check if DNS is working
        if ! nslookup example.com localhost >/dev/null 2>&1; then
            print_error "DNS is not working."
            test_passed=false
        else
            print_status "DNS is working."
        fi
        
        # Check resource usage
        print_status "Checking resource usage..."
        local memory_usage=$(free -m | awk '/Mem:/ {print $3}')
        local cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print $1}')
        
        print_status "Memory usage: ${memory_usage}MB"
        print_status "CPU usage: ${cpu_usage}%"
        
        if [ "$memory_usage" -gt 700 ]; then
            print_warning "Memory usage is high for Low-Resource PC: ${memory_usage}MB"
        fi
        
        if [ "$cpu_usage" -gt 70 ]; then
            print_warning "CPU usage is high for Low-Resource PC: ${cpu_usage}%"
        fi
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Low-Resource PC installation tests passed."
        return 0
    else
        print_error "Low-Resource PC installation tests failed."
        return 1
    fi
}

# Run Low-Resource PC tests
test_low_resource_pc
```

#### Standard PC Test
```bash
#!/bin/bash
# test_standard_pc.sh - Test installation on Standard PC

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

# Function to test Standard PC installation
test_standard_pc() {
    print_step "Testing Standard PC installation..."
    
    local test_passed=true
    
    # Check if we're running on a Standard PC
    local total_mem=$(free -m | awk '/Mem:/ {print $2}')
    local cpu_cores=$(nproc)
    
    if [ "$total_mem" -le 1024 ] || [ "$cpu_cores" -le 2 ]; then
        print_warning "Not running on a Standard PC. Skipping device-specific tests."
        return 0
    fi
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with bare metal
    print_status "Testing installation with bare metal..."
    ./scripts/install.sh --device standard-pc --container none --silent
    local result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test failed for Standard PC with bare metal."
        test_passed=false
    else
        print_status "Installation test passed for Standard PC with bare metal."
        
        # Verify that the system is running correctly
        print_status "Verifying system operation..."
        
        # Check if systemd services are running
        if ! systemctl is-active --quiet pidns.service; then
            print_error "PiDNS service is not running."
            test_passed=false
        else
            print_status "PiDNS service is running."
        fi
        
        if ! systemctl is-active --quiet adblocker.service; then
            print_error "Ad-blocker service is not running."
            test_passed=false
        else
            print_status "Ad-blocker service is running."
        fi
        
        if ! systemctl is-active --quiet dnsmasq; then
            print_error "dnsmasq service is not running."
            test_passed=false
        else
            print_status "dnsmasq service is running."
        fi
        
        # Check if dashboard is accessible
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible."
            test_passed=false
        else
            print_status "Main dashboard is accessible."
        fi
        
        if ! curl -s -f http://localhost:8081/api/health > /dev/null; then
            print_error "Ad-blocker dashboard is not accessible."
            test_passed=false
        else
            print_status "Ad-blocker dashboard is accessible."
        fi
        
        # Check if DNS is working
        if ! nslookup example.com localhost >/dev/null 2>&1; then
            print_error "DNS is not working."
            test_passed=false
        else
            print_status "DNS is working."
        fi
        
        # Check resource usage
        print_status "Checking resource usage..."
        local memory_usage=$(free -m | awk '/Mem:/ {print $3}')
        local cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print $1}')
        
        print_status "Memory usage: ${memory_usage}MB"
        print_status "CPU usage: ${cpu_usage}%"
        
        if [ "$memory_usage" -gt 1500 ]; then
            print_warning "Memory usage is high for Standard PC: ${memory_usage}MB"
        fi
        
        if [ "$cpu_usage" -gt 50 ]; then
            print_warning "CPU usage is high for Standard PC: ${cpu_usage}%"
        fi
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Standard PC installation tests passed."
        return 0
    else
        print_error "Standard PC installation tests failed."
        return 1
    fi
}

# Run Standard PC tests
test_standard_pc
```

### Container Testing

#### Docker Test
```bash
#!/bin/bash
# test_docker.sh - Test Docker installation

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

# Function to test Docker installation
test_docker() {
    print_step "Testing Docker installation..."
    
    local test_passed=true
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Skipping Docker tests."
        return 0
    fi
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with Docker on Raspberry Pi 4
    print_status "Testing installation with Docker on Raspberry Pi 4..."
    ./scripts/install.sh --device pi-4 --container docker --silent
    local result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test failed for Docker on Raspberry Pi 4."
        test_passed=false
    else
        print_status "Installation test passed for Docker on Raspberry Pi 4."
        
        # Verify that the system is running correctly
        print_status "Verifying system operation..."
        
        # Check if Docker container is running
        if ! docker ps --format '{{.Names}}' | grep -q "^pidns$"; then
            print_error "Docker container is not running."
            test_passed=false
        else
            print_status "Docker container is running."
        fi
        
        # Check if dashboard is accessible
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible."
            test_passed=false
        else
            print_status "Main dashboard is accessible."
        fi
        
        if ! curl -s -f http://localhost:8081/api/health > /dev/null; then
            print_error "Ad-blocker dashboard is not accessible."
            test_passed=false
        else
            print_status "Ad-blocker dashboard is accessible."
        fi
        
        # Check if DNS is working
        if ! nslookup example.com localhost >/dev/null 2>&1; then
            print_error "DNS is not working."
            test_passed=false
        else
            print_status "DNS is working."
        fi
        
        # Test Docker management commands
        print_status "Testing Docker management commands..."
        
        # Test container logs
        if ! docker logs pidns >/dev/null 2>&1; then
            print_error "Cannot retrieve Docker container logs."
            test_passed=false
        else
            print_status "Docker container logs retrieved successfully."
        fi
        
        # Test container restart
        if ! docker restart pidns >/dev/null 2>&1; then
            print_error "Cannot restart Docker container."
            test_passed=false
        else
            print_status "Docker container restarted successfully."
        fi
        
        # Wait for container to start
        sleep 10
        
        # Check if dashboard is accessible after restart
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible after restart."
            test_passed=false
        else
            print_status "Main dashboard is accessible after restart."
        fi
        
        # Test container stop and start
        if ! docker stop pidns >/dev/null 2>&1; then
            print_error "Cannot stop Docker container."
            test_passed=false
        else
            print_status "Docker container stopped successfully."
        fi
        
        if ! docker start pidns >/dev/null 2>&1; then
            print_error "Cannot start Docker container."
            test_passed=false
        else
            print_status "Docker container started successfully."
        fi
        
        # Wait for container to start
        sleep 10
        
        # Check if dashboard is accessible after stop and start
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible after stop and start."
            test_passed=false
        else
            print_status "Main dashboard is accessible after stop and start."
        fi
        
        # Test Docker Compose commands
        print_status "Testing Docker Compose commands..."
        
        # Test Docker Compose down
        if ! docker-compose down >/dev/null 2>&1; then
            print_error "Cannot stop services with Docker Compose."
            test_passed=false
        else
            print_status "Services stopped with Docker Compose successfully."
        fi
        
        # Test Docker Compose up
        if ! docker-compose up -d >/dev/null 2>&1; then
            print_error "Cannot start services with Docker Compose."
            test_passed=false
        else
            print_status "Services started with Docker Compose successfully."
        fi
        
        # Wait for services to start
        sleep 10
        
        # Check if dashboard is accessible after Docker Compose up
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible after Docker Compose up."
            test_passed=false
        else
            print_status "Main dashboard is accessible after Docker Compose up."
        fi
        
        # Test Docker volume management
        print_status "Testing Docker volume management..."
        
        # List Docker volumes
        if ! docker volume ls | grep -q "pidns"; then
            print_error "Docker volumes not created."
            test_passed=false
        else
            print_status "Docker volumes created successfully."
        fi
        
        # Test Docker volume backup
        docker run --rm -v pidns-data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz -C /data .
        if [ ! -f "data-backup.tar.gz" ]; then
            print_error "Cannot backup Docker volume."
            test_passed=false
        else
            print_status "Docker volume backed up successfully."
        fi
        
        # Test Docker volume restore
        docker run --rm -v pidns-data:/data -v $(pwd):/backup alpine tar xzf /backup/data-backup.tar.gz -C /data
        if [ $? -ne 0 ]; then
            print_error "Cannot restore Docker volume."
            test_passed=false
        else
            print_status "Docker volume restored successfully."
        fi
        
        # Clean up backup file
        rm -f data-backup.tar.gz
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Docker installation tests passed."
        return 0
    else
        print_error "Docker installation tests failed."
        return 1
    fi
}

# Run Docker tests
test_docker
```

#### Podman Test
```bash
#!/bin/bash
# test_podman.sh - Test Podman installation

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

# Function to test Podman installation
test_podman() {
    print_step "Testing Podman installation..."
    
    local test_passed=true
    
    # Check if Podman is installed
    if ! command -v podman &> /dev/null; then
        print_error "Podman is not installed. Skipping Podman tests."
        return 0
    fi
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with Podman on Raspberry Pi 3
    print_status "Testing installation with Podman on Raspberry Pi 3..."
    ./scripts/install.sh --device pi-3 --container podman --silent
    local result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test failed for Podman on Raspberry Pi 3."
        test_passed=false
    else
        print_status "Installation test passed for Podman on Raspberry Pi 3."
        
        # Verify that the system is running correctly
        print_status "Verifying system operation..."
        
        # Check if Podman container is running
        if ! podman ps --format '{{.Names}}' | grep -q "^pidns$"; then
            print_error "Podman container is not running."
            test_passed=false
        else
            print_status "Podman container is running."
        fi
        
        # Check if dashboard is accessible
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible."
            test_passed=false
        else
            print_status "Main dashboard is accessible."
        fi
        
        if ! curl -s -f http://localhost:8081/api/health > /dev/null; then
            print_error "Ad-blocker dashboard is not accessible."
            test_passed=false
        else
            print_status "Ad-blocker dashboard is accessible."
        fi
        
        # Check if DNS is working
        if ! nslookup example.com localhost >/dev/null 2>&1; then
            print_error "DNS is not working."
            test_passed=false
        else
            print_status "DNS is working."
        fi
        
        # Test Podman management commands
        print_status "Testing Podman management commands..."
        
        # Test container logs
        if ! podman logs pidns >/dev/null 2>&1; then
            print_error "Cannot retrieve Podman container logs."
            test_passed=false
        else
            print_status "Podman container logs retrieved successfully."
        fi
        
        # Test container restart
        if ! podman restart pidns >/dev/null 2>&1; then
            print_error "Cannot restart Podman container."
            test_passed=false
        else
            print_status "Podman container restarted successfully."
        fi
        
        # Wait for container to start
        sleep 10
        
        # Check if dashboard is accessible after restart
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible after restart."
            test_passed=false
        else
            print_status "Main dashboard is accessible after restart."
        fi
        
        # Test container stop and start
        if ! podman stop pidns >/dev/null 2>&1; then
            print_error "Cannot stop Podman container."
            test_passed=false
        else
            print_status "Podman container stopped successfully."
        fi
        
        if ! podman start pidns >/dev/null 2>&1; then
            print_error "Cannot start Podman container."
            test_passed=false
        else
            print_status "Podman container started successfully."
        fi
        
        # Wait for container to start
        sleep 10
        
        # Check if dashboard is accessible after stop and start
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible after stop and start."
            test_passed=false
        else
            print_status "Main dashboard is accessible after stop and start."
        fi
        
        # Test Podman Compose commands
        print_status "Testing Podman Compose commands..."
        
        # Test Podman Compose down
        if ! podman-compose down >/dev/null 2>&1; then
            print_error "Cannot stop services with Podman Compose."
            test_passed=false
        else
            print_status "Services stopped with Podman Compose successfully."
        fi
        
        # Test Podman Compose up
        if ! podman-compose up -d >/dev/null 2>&1; then
            print_error "Cannot start services with Podman Compose."
            test_passed=false
        else
            print_status "Services started with Podman Compose successfully."
        fi
        
        # Wait for services to start
        sleep 10
        
        # Check if dashboard is accessible after Podman Compose up
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible after Podman Compose up."
            test_passed=false
        else
            print_status "Main dashboard is accessible after Podman Compose up."
        fi
        
        # Test Podman volume management
        print_status "Testing Podman volume management..."
        
        # List Podman volumes
        if ! podman volume ls | grep -q "pidns"; then
            print_error "Podman volumes not created."
            test_passed=false
        else
            print_status "Podman volumes created successfully."
        fi
        
        # Test Podman volume backup
        podman run --rm -v pidns-data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz -C /data .
        if [ ! -f "data-backup.tar.gz" ]; then
            print_error "Cannot backup Podman volume."
            test_passed=false
        else
            print_status "Podman volume backed up successfully."
        fi
        
        # Test Podman volume restore
        podman run --rm -v pidns-data:/data -v $(pwd):/backup alpine tar xzf /backup/data-backup.tar.gz -C /data
        if [ $? -ne 0 ]; then
            print_error "Cannot restore Podman volume."
            test_passed=false
        else
            print_status "Podman volume restored successfully."
        fi
        
        # Clean up backup file
        rm -f data-backup.tar.gz
        
        # Test Podman Quadlet
        print_status "Testing Podman Quadlet..."
        
        # Check if Quadlet file exists
        if [ ! -f "$HOME/.config/containers/systemd/pidns.container" ]; then
            print_error "Podman Quadlet file not created."
            test_passed=false
        else
            print_status "Podman Quadlet file created successfully."
        fi
        
        # Test systemd user service
        if ! systemctl --user is-active --quiet pidns; then
            print_error "Podman systemd user service is not running."
            test_passed=false
        else
            print_status "Podman systemd user service is running."
        fi
        
        # Test systemd user service restart
        if ! systemctl --user restart pidns >/dev/null 2>&1; then
            print_error "Cannot restart Podman systemd user service."
            test_passed=false
        else
            print_status "Podman systemd user service restarted successfully."
        fi
        
        # Wait for service to start
        sleep 10
        
        # Check if dashboard is accessible after systemd user service restart
        if ! curl -s -f http://localhost:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible after systemd user service restart."
            test_passed=false
        else
            print_status "Main dashboard is accessible after systemd user service restart."
        fi
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Podman installation tests passed."
        return 0
    else
        print_error "Podman installation tests failed."
        return 1
    fi
}

# Run Podman tests
test_podman
```

#### LXC Test
```bash
#!/bin/bash
# test_lxc.sh - Test LXC installation

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

# Function to test LXC installation
test_lxc() {
    print_step "Testing LXC installation..."
    
    local test_passed=true
    
    # Check if LXC is installed
    if ! command -v lxc-create &> /dev/null; then
        print_error "LXC is not installed. Skipping LXC tests."
        return 0
    fi
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with LXC on Raspberry Pi 4
    print_status "Testing installation with LXC on Raspberry Pi 4..."
    ./scripts/install.sh --device pi-4 --container lxc --silent
    local result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test failed for LXC on Raspberry Pi 4."
        test_passed=false
    else
        print_status "Installation test passed for LXC on Raspberry Pi 4."
        
        # Verify that the system is running correctly
        print_status "Verifying system operation..."
        
        # Check if LXC container is running
        if ! lxc-info -n pidns -s | grep -q "RUNNING"; then
            print_error "LXC container is not running."
            test_passed=false
        else
            print_status "LXC container is running."
        fi
        
        # Get container IP
        local container_ip=$(lxc-info -n pidns -iH)
        
        # Check if dashboard is accessible
        if ! curl -s -f http://$container_ip:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible."
            test_passed=false
        else
            print_status "Main dashboard is accessible."
        fi
        
        if ! curl -s -f http://$container_ip:8081/api/health > /dev/null; then
            print_error "Ad-blocker dashboard is not accessible."
            test_passed=false
        else
            print_status "Ad-blocker dashboard is accessible."
        fi
        
        # Check if DNS is working
        if ! nslookup example.com $container_ip >/dev/null 2>&1; then
            print_error "DNS is not working."
            test_passed=false
        else
            print_status "DNS is working."
        fi
        
        # Test LXC management commands
        print_status "Testing LXC management commands..."
        
        # Test container logs
        if ! lxc-attach -n pidns -- tail -f /var/log/pidns/app.log >/dev/null 2>&1; then
            print_error "Cannot retrieve LXC container logs."
            test_passed=false
        else
            print_status "LXC container logs retrieved successfully."
        fi
        
        # Test container restart
        if ! lxc-stop -n pidns >/dev/null 2>&1; then
            print_error "Cannot stop LXC container."
            test_passed=false
        else
            print_status "LXC container stopped successfully."
        fi
        
        if ! lxc-start -n pidns -d >/dev/null 2>&1; then
            print_error "Cannot start LXC container."
            test_passed=false
        else
            print_status "LXC container started successfully."
        fi
        
        # Wait for container to start
        sleep 10
        
        # Check if dashboard is accessible after restart
        if ! curl -s -f http://$container_ip:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible after restart."
            test_passed=false
        else
            print_status "Main dashboard is accessible after restart."
        fi
        
        # Test LXC container configuration
        print_status "Testing LXC container configuration..."
        
        # Check container configuration
        if ! lxc-config -n pidns -l >/dev/null 2>&1; then
            print_error "Cannot retrieve LXC container configuration."
            test_passed=false
        else
            print_status "LXC container configuration retrieved successfully."
        fi
        
        # Test container resource limits
        local memory_limit=$(lxc-cgroup -n pidns memory.limit_in_bytes)
        local cpu_shares=$(lxc-cgroup -n pidns cpu.shares)
        
        print_status "LXC container memory limit: $memory_limit"
        print_status "LXC container CPU shares: $cpu_shares"
        
        if [ "$memory_limit" != "2147483648" ]; then
            print_warning "LXC container memory limit is not as expected: $memory_limit (expected: 2147483648)"
        fi
        
        if [ "$cpu_shares" != "512" ]; then
            print_warning "LXC container CPU shares are not as expected: $cpu_shares (expected: 512)"
        fi
        
        # Test LXC container network configuration
        print_status "Testing LXC container network configuration..."
        
        # Check container network interfaces
        if ! lxc-attach -n pidns -- ip addr show >/dev/null 2>&1; then
            print_error "Cannot retrieve LXC container network interfaces."
            test_passed=false
        else
            print_status "LXC container network interfaces retrieved successfully."
        fi
        
        # Check container network connectivity
        if ! lxc-attach -n pidns -- ping -c 3 8.8.8.8 >/dev/null 2>&1; then
            print_error "LXC container does not have network connectivity."
            test_passed=false
        else
            print_status "LXC container has network connectivity."
        fi
        
        # Test LXC container file system
        print_status "Testing LXC container file system..."
        
        # Check container file system usage
        if ! lxc-attach -n pidns -- df -h >/dev/null 2>&1; then
            print_error "Cannot retrieve LXC container file system usage."
            test_passed=false
        else
            print_status "LXC container file system usage retrieved successfully."
        fi
        
        # Test container file system mounts
        if ! lxc-attach -n pidns -- mount | grep -q "/var/lib/misc"; then
            print_error "LXC container file system mounts are not as expected."
            test_passed=false
        else
            print_status "LXC container file system mounts are as expected."
        fi
        
        # Test LXC container processes
        print_status "Testing LXC container processes..."
        
        # Check container processes
        if ! lxc-attach -n pidns -- ps aux >/dev/null 2>&1; then
            print_error "Cannot retrieve LXC container processes."
            test_passed=false
        else
            print_status "LXC container processes retrieved successfully."
        fi
        
        # Check if required processes are running
        if ! lxc-attach -n pidns -- pgrep -f "python3 app/app.py" >/dev/null 2>&1; then
            print_error "PiDNS application is not running in LXC container."
            test_passed=false
        else
            print_status "PiDNS application is running in LXC container."
        fi
        
        if ! lxc-attach -n pidns -- pgrep dnsmasq >/dev/null 2>&1; then
            print_error "dnsmasq is not running in LXC container."
            test_passed=false
        else
            print_status "dnsmasq is running in LXC container."
        fi
        
        # Test LXC container security
        print_status "Testing LXC container security..."
        
        # Check container capabilities
        if ! lxc-info -n pidns | grep -q "Capabilities:"; then
            print_error "Cannot retrieve LXC container capabilities."
            test_passed=false
        else
            print_status "LXC container capabilities retrieved successfully."
        fi
        
        # Check container AppArmor profile
        if ! lxc-info -n pidns | grep -q "AppArmor profile:"; then
            print_error "Cannot retrieve LXC container AppArmor profile."
            test_passed=false
        else
            print_status "LXC container AppArmor profile retrieved successfully."
        fi
        
        # Test LXC container backup and restore
        print_status "Testing LXC container backup and restore..."
        
        # Stop container for backup
        if ! lxc-stop -n pidns >/dev/null 2>&1; then
            print_error "Cannot stop LXC container for backup."
            test_passed=false
        else
            print_status "LXC container stopped for backup."
        fi
        
        # Create container backup
        if ! lxc-copy -n pidns -B /tmp/pidns-backup >/dev/null 2>&1; then
            print_error "Cannot create LXC container backup."
            test_passed=false
        else
            print_status "LXC container backup created successfully."
        fi
        
        # Remove container for restore test
        if ! lxc-destroy -n pidns >/dev/null 2>&1; then
            print_error "Cannot remove LXC container for restore test."
            test_passed=false
        else
            print_status "LXC container removed for restore test."
        fi
        
        # Restore container from backup
        if ! lxc-copy -n pidns-backup -R >/dev/null 2>&1; then
            print_error "Cannot restore LXC container from backup."
            test_passed=false
        else
            print_status "LXC container restored from backup successfully."
        fi
        
        # Start restored container
        if ! lxc-start -n pidns -d >/dev/null 2>&1; then
            print_error "Cannot start restored LXC container."
            test_passed=false
        else
            print_status "Restored LXC container started successfully."
        fi
        
        # Wait for container to start
        sleep 10
        
        # Check if dashboard is accessible after restore
        if ! curl -s -f http://$container_ip:8080/api/health > /dev/null; then
            print_error "Main dashboard is not accessible after restore."
            test_passed=false
        else
            print_status "Main dashboard is accessible after restore."
        fi
        
        # Clean up backup
        rm -rf /tmp/pidns-backup
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "LXC installation tests passed."
        return 0
    else
        print_error "LXC installation tests failed."
        return 1
    fi
}

# Run LXC tests
test_lxc
```

### Error Handling Testing

#### Invalid Device Test
```bash
#!/bin/bash
# test_invalid_device.sh - Test handling of invalid device selection

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

# Function to test invalid device selection
test_invalid_device() {
    print_step "Testing handling of invalid device selection..."
    
    local test_passed=true
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test silent installation with invalid device type
    print_status "Testing silent installation with invalid device type..."
    ./scripts/install.sh --device invalid-device --container docker --silent
    local result=$?
    
    if [ $result -eq 0 ]; then
        print_error "Installation script did not fail with invalid device type."
        test_passed=false
    else
        print_status "Installation script correctly failed with invalid device type."
    fi
    
    # Test interactive installation with invalid device selection
    print_status "Testing interactive installation with invalid device selection..."
    
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

# Simulate user input for device selection
echo "9" | ./scripts/install.sh --test-mode

# Check if installation was successful
if [ $? -ne 0 ]; then
    print_status "Interactive installation correctly failed with invalid device selection."
    exit 0
else
    print_error "Interactive installation did not fail with invalid device selection."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Interactive installation test did not handle invalid device selection correctly."
        test_passed=false
    else
        print_status "Interactive installation correctly handled invalid device selection."
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    rm -f /tmp/mock_install.sh
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Invalid device selection tests passed."
        return 0
    else
        print_error "Invalid device selection tests failed."
        return 1
    fi
}

# Run invalid device selection tests
test_invalid_device
```

#### Invalid Container Test
```bash
#!/bin/bash
# test_invalid_container.sh - Test handling of invalid container selection

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

# Function to test invalid container selection
test_invalid_container() {
    print_step "Testing handling of invalid container selection..."
    
    local test_passed=true
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test silent installation with invalid container type
    print_status "Testing silent installation with invalid container type..."
    ./scripts/install.sh --device pi-4 --container invalid-container --silent
    local result=$?
    
    if [ $result -eq 0 ]; then
        print_error "Installation script did not fail with invalid container type."
        test_passed=false
    else
        print_status "Installation script correctly failed with invalid container type."
    fi
    
    # Test interactive installation with invalid container selection
    print_status "Testing interactive installation with invalid container selection..."
    
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
echo -e "1\n5" | ./scripts/install.sh --test-mode

# Check if installation was successful
if [ $? -ne 0 ]; then
    print_status "Interactive installation correctly failed with invalid container selection."
    exit 0
else
    print_error "Interactive installation did not fail with invalid container selection."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Interactive installation test did not handle invalid container selection correctly."
        test_passed=false
    else
        print_status "Interactive installation correctly handled invalid container selection."
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    rm -f /tmp/mock_install.sh
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Invalid container selection tests passed."
        return 0
    else
        print_error "Invalid container selection tests failed."
        return 1
    fi
}

# Run invalid container selection tests
test_invalid_container
```

#### Insufficient Resources Test
```bash
#!/bin/bash
# test_insufficient_resources.sh - Test handling of insufficient resources

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

# Function to test insufficient resources
test_insufficient_resources() {
    print_step "Testing handling of insufficient resources..."
    
    local test_passed=true
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with insufficient disk space
    print_status "Testing installation with insufficient disk space..."
    
    # Create a small filesystem for testing
    dd if=/dev/zero of=/tmp/small_fs.img bs=1M count=100
    mkfs.ext4 /tmp/small_fs.img
    mkdir -p /tmp/small_fs
    mount -o loop /tmp/small_fs.img /tmp/small_fs
    
    # Try to install in the small filesystem
    if (cd /tmp/small_fs && git clone https://github.com/yourusername/PiDNS.git && cd PiDNS && ./scripts/install.sh --device pi-zero --container docker --silent); then
        print_error "Installation script did not fail with insufficient disk space."
        test_passed=false
    else
        print_status "Installation script correctly failed with insufficient disk space."
    fi
    
    # Clean up small filesystem
    umount /tmp/small_fs
    rm -rf /tmp/small_fs /tmp/small_fs.img
    
    # Test installation with insufficient memory
    print_status "Testing installation with insufficient memory..."
    
    # Create a memory-constrained environment
    if ! command -v systemd-run &> /dev/null; then
        print_warning "systemd-run is not available. Skipping memory-constrained test."
    else
        # Try to install with memory constraint
        if systemd-run --scope -p MemoryLimit=128M ./scripts/install.sh --device pi-zero --container docker --silent; then
            print_error "Installation script did not fail with insufficient memory."
            test_passed=false
        else
            print_status "Installation script correctly failed with insufficient memory."
        fi
    fi
    
    # Test installation with insufficient CPU
    print_status "Testing installation with insufficient CPU..."
    
    # Create a CPU-constrained environment
    if ! command -v systemd-run &> /dev/null; then
        print_warning "systemd-run is not available. Skipping CPU-constrained test."
    else
        # Try to install with CPU constraint
        if systemd-run --scope -p CPUQuota=10% ./scripts/install.sh --device pi-zero --container docker --silent; then
            print_error "Installation script did not fail with insufficient CPU."
            test_passed=false
        else
            print_status "Installation script correctly failed with insufficient CPU."
        fi
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Insufficient resources tests passed."
        return 0
    else
        print_error "Insufficient resources tests failed."
        return 1
    fi
}

# Run insufficient resources tests
test_insufficient_resources
```

#### Network Failure Test
```bash
#!/bin/bash
# test_network_failure.sh - Test handling of network failure

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

# Function to test network failure
test_network_failure() {
    print_step "Testing handling of network failure..."
    
    local test_passed=true
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test installation with network failure during download
    print_status "Testing installation with network failure during download..."
    
    # Create a mock installation script that simulates network failure
    cat > /tmp/mock_install.sh << 'EOF'
#!/bin/bash
# Mock installation script that simulates network failure

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

# Block network access
iptables -A OUTPUT -p tcp --dport 443 -j DROP
iptables -A OUTPUT -p tcp --dport 80 -j DROP

# Try to install
./scripts/install.sh --device pi-4 --container docker --silent
result=$?

# Restore network access
iptables -D OUTPUT -p tcp --dport 443 -j DROP
iptables -D OUTPUT -p tcp --dport 80 -j DROP

# Check if installation was successful
if [ $result -ne 0 ]; then
    print_status "Installation correctly failed with network failure."
    exit 0
else
    print_error "Installation did not fail with network failure."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test did not handle network failure correctly."
        test_passed=false
    else
        print_status "Installation correctly handled network failure."
    fi
    
    # Test installation with network failure during package installation
    print_status "Testing installation with network failure during package installation..."
    
    # Create a mock installation script that simulates network failure during package installation
    cat > /tmp/mock_install.sh << 'EOF'
#!/bin/bash
# Mock installation script that simulates network failure during package installation

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

# Create a mock apt-get that fails on package installation
cat > /tmp/mock-apt-get << 'APT_EOF'
#!/bin/bash
if [[ "$*" == *"install"* ]]; then
    echo "E: Failed to fetch https://deb.debian.org/debian/dists/bullseye/InRelease  Temporary failure resolving 'deb.debian.org'"
    exit 100
else
    /usr/bin/apt-get "$@"
fi
APT_EOF

chmod +x /tmp/mock-apt-get

# Add mock apt-get to PATH
export PATH="/tmp:$PATH"

# Try to install
./scripts/install.sh --device pi-4 --container docker --silent
result=$?

# Restore PATH
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin"

# Check if installation was successful
if [ $result -ne 0 ]; then
    print_status "Installation correctly failed with network failure during package installation."
    exit 0
else
    print_error "Installation did not fail with network failure during package installation."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Installation test did not handle network failure during package installation correctly."
        test_passed=false
    else
        print_status "Installation correctly handled network failure during package installation."
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    rm -f /tmp/mock_install.sh /tmp/mock-apt-get
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Network failure tests passed."
        return 0
    else
        print_error "Network failure tests failed."
        return 1
    fi
}

# Run network failure tests
test_network_failure
```

### User Acceptance Testing

#### User Scenario Test
```bash
#!/bin/bash
# test_user_scenario.sh - Test user scenarios

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

# Function to test user scenarios
test_user_scenario() {
    print_step "Testing user scenarios..."
    
    local test_passed=true
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test scenario 1: First-time user with Raspberry Pi 4 and Docker
    print_status "Testing scenario 1: First-time user with Raspberry Pi 4 and Docker..."
    
    # Create a mock installation script that simulates a first-time user
    cat > /tmp/mock_install.sh << 'EOF'
#!/bin/bash
# Mock installation script that simulates a first-time user

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

# Simulate user input for first-time user
echo -e "8\n1\n1\nadmin\npassword\npassword" | ./scripts/install.sh --test-mode

# Check if installation was successful
if [ $? -eq 0 ]; then
    print_status "First-time user scenario test passed."
    exit 0
else
    print_error "First-time user scenario test failed."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "First-time user scenario test failed."
        test_passed=false
    else
        print_status "First-time user scenario test passed."
    fi
    
    # Test scenario 2: Experienced user with Raspberry Pi 3 and Podman
    print_status "Testing scenario 2: Experienced user with Raspberry Pi 3 and Podman..."
    
    # Create a mock installation script that simulates an experienced user
    cat > /tmp/mock_install.sh << 'EOF'
#!/bin/bash
# Mock installation script that simulates an experienced user

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

# Simulate user input for experienced user
echo -e "3\n2\nadmin\nsecurepassword\nsecurepassword" | ./scripts/install.sh --test-mode

# Check if installation was successful
if [ $? -eq 0 ]; then
    print_status "Experienced user scenario test passed."
    exit 0
else
    print_error "Experienced user scenario test failed."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Experienced user scenario test failed."
        test_passed=false
    else
        print_status "Experienced user scenario test passed."
    fi
    
    # Test scenario 3: User with Low-Resource PC and LXC
    print_status "Testing scenario 3: User with Low-Resource PC and LXC..."
    
    # Create a mock installation script that simulates a user with Low-Resource PC
    cat > /tmp/mock_install.sh << 'EOF'
#!/bin/bash
# Mock installation script that simulates a user with Low-Resource PC

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

# Simulate user input for user with Low-Resource PC
echo -e "6\n3\nadmin\nlowresourcepassword\nlowresourcepassword" | ./scripts/install.sh --test-mode

# Check if installation was successful
if [ $? -eq 0 ]; then
    print_status "Low-Resource PC user scenario test passed."
    exit 0
else
    print_error "Low-Resource PC user scenario test failed."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Low-Resource PC user scenario test failed."
        test_passed=false
    else
        print_status "Low-Resource PC user scenario test passed."
    fi
    
    # Test scenario 4: User with Standard PC and bare metal
    print_status "Testing scenario 4: User with Standard PC and bare metal..."
    
    # Create a mock installation script that simulates a user with Standard PC
    cat > /tmp/mock_install.sh << 'EOF'
#!/bin/bash
# Mock installation script that simulates a user with Standard PC

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

# Simulate user input for user with Standard PC
echo -e "7\n4\nadmin\nstandardpassword\nstandardpassword" | ./scripts/install.sh --test-mode

# Check if installation was successful
if [ $? -eq 0 ]; then
    print_status "Standard PC user scenario test passed."
    exit 0
else
    print_error "Standard PC user scenario test failed."
    exit 1
fi
EOF
    
    chmod +x /tmp/mock_install.sh
    
    # Run the mock installation script
    /tmp/mock_install.sh
    result=$?
    
    if [ $result -ne 0 ]; then
        print_error "Standard PC user scenario test failed."
        test_passed=false
    else
        print_status "Standard PC user scenario test passed."
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    rm -f /tmp/mock_install.sh
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "User scenario tests passed."
        return 0
    else
        print_error "User scenario tests failed."
        return 1
    fi
}

# Run user scenario tests
test_user_scenario
```

#### Documentation Usability Test
```bash
#!/bin/bash
# test_documentation_usability.sh - Test documentation usability

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

# Function to test documentation usability
test_documentation_usability() {
    print_step "Testing documentation usability..."
    
    local test_passed=true
    
    # Create a temporary directory for testing
    local test_dir=$(mktemp -d)
    cd "$test_dir"
    
    # Clone the PiDNS repository
    print_status "Cloning PiDNS repository..."
    git clone https://github.com/yourusername/PiDNS.git
    cd PiDNS
    
    # Test README.md usability
    print_status "Testing README.md usability..."
    
    # Check if README.md exists
    if [ ! -f "README.md" ]; then
        print_error "README.md does not exist."
        test_passed=false
    else
        print_status "README.md exists."
    fi
    
    # Check if README.md contains installation instructions
    if ! grep -q "Installation" README.md; then
        print_error "README.md does not contain installation instructions."
        test_passed=false
    else
        print_status "README.md contains installation instructions."
    fi
    
    # Check if README.md contains configuration instructions
    if ! grep -q "Configuration" README.md; then
        print_error "README.md does not contain configuration instructions."
        test_passed=false
    else
        print_status "README.md contains configuration instructions."
    fi
    
    # Check if README.md contains troubleshooting instructions
    if ! grep -q "Troubleshooting" README.md; then
        print_error "README.md does not contain troubleshooting instructions."
        test_passed=false
    else
        print_status "README.md contains troubleshooting instructions."
    fi
    
    # Test INSTALLATION.md usability
    print_status "Testing INSTALLATION.md usability..."
    
    # Check if INSTALLATION.md exists
    if [ ! -f "docs/INSTALLATION.md" ]; then
        print_error "INSTALLATION.md does not exist."
        test_passed=false
    else
        print_status "INSTALLATION.md exists."
    fi
    
    # Check if INSTALLATION.md contains prerequisites
    if ! grep -q "Prerequisites" docs/INSTALLATION.md; then
        print_error "INSTALLATION.md does not contain prerequisites."
        test_passed=false
    else
        print_status "INSTALLATION.md contains prerequisites."
    fi
    
    # Check if INSTALLATION.md contains installation methods
    if ! grep -q "Installation Methods" docs/INSTALLATION.md; then
        print_error "INSTALLATION.md does not contain installation methods."
        test_passed=false
    else
        print_status "INSTALLATION.md contains installation methods."
    fi
    
    # Check if INSTALLATION.md contains device-specific installation
    if ! grep -q "Device-Specific Installation" docs/INSTALLATION.md; then
        print_error "INSTALLATION.md does not contain device-specific installation."
        test_passed=false
    else
        print_status "INSTALLATION.md contains device-specific installation."
    fi
    
    # Check if INSTALLATION.md contains container installation
    if ! grep -q "Container Installation" docs/INSTALLATION.md; then
        print_error "INSTALLATION.md does not contain container installation."
        test_passed=false
    else
        print_status "INSTALLATION.md contains container installation."
    fi
    
    # Check if INSTALLATION.md contains post-installation steps
    if ! grep -q "Post-Installation" docs/INSTALLATION.md; then
        print_error "INSTALLATION.md does not contain post-installation steps."
        test_passed=false
    else
        print_status "INSTALLATION.md contains post-installation steps."
    fi
    
    # Test CONFIGURATION.md usability
    print_status "Testing CONFIGURATION.md usability..."
    
    # Check if CONFIGURATION.md exists
    if [ ! -f "docs/CONFIGURATION.md" ]; then
        print_error "CONFIGURATION.md does not exist."
        test_passed=false
    else
        print_status "CONFIGURATION.md exists."
    fi
    
    # Check if CONFIGURATION.md contains configuration files
    if ! grep -q "Configuration Files" docs/CONFIGURATION.md; then
        print_error "CONFIGURATION.md does not contain configuration files."
        test_passed=false
    else
        print_status "CONFIGURATION.md contains configuration files."
    fi
    
    # Check if CONFIGURATION.md contains device-specific configuration
    if ! grep -q "Device-Specific Configuration" docs/CONFIGURATION.md; then
        print_error "CONFIGURATION.md does not contain device-specific configuration."
        test_passed=false
    else
        print_status "CONFIGURATION.md contains device-specific configuration."
    fi
    
    # Check if CONFIGURATION.md contains container-specific configuration
    if ! grep -q "Container-Specific Configuration" docs/CONFIGURATION.md; then
        print_error "CONFIGURATION.md does not contain container-specific configuration."
        test_passed=false
    else
        print_status "CONFIGURATION.md contains container-specific configuration."
    fi
    
    # Check if CONFIGURATION.md contains DNS configuration
    if ! grep -q "DNS Configuration" docs/CONFIGURATION.md; then
        print_error "CONFIGURATION.md does not contain DNS configuration."
        test_passed=false
    else
        print_status "CONFIGURATION.md contains DNS configuration."
    fi
    
    # Check if CONFIGURATION.md contains DHCP configuration
    if ! grep -q "DHCP Configuration" docs/CONFIGURATION.md; then
        print_error "CONFIGURATION.md does not contain DHCP configuration."
        test_passed=false
    else
        print_status "CONFIGURATION.md contains DHCP configuration."
    fi
    
    # Test TROUBLESHOOTING.md usability
    print_status "Testing TROUBLESHOOTING.md usability..."
    
    # Check if TROUBLESHOOTING.md exists
    if [ ! -f "docs/TROUBLESHOOTING.md" ]; then
        print_error "TROUBLESHOOTING.md does not exist."
        test_passed=false
    else
        print_status "TROUBLESHOOTING.md exists."
    fi
    
    # Check if TROUBLESHOOTING.md contains common issues
    if ! grep -q "Common Issues" docs/TROUBLESHOOTING.md; then
        print_error "TROUBLESHOOTING.md does not contain common issues."
        test_passed=false
    else
        print_status "TROUBLESHOOTING.md contains common issues."
    fi
    
    # Check if TROUBLESHOOTING.md contains installation issues
    if ! grep -q "Installation Issues" docs/TROUBLESHOOTING.md; then
        print_error "TROUBLESHOOTING.md does not contain installation issues."
        test_passed=false
    else
        print_status "TROUBLESHOOTING.md contains installation issues."
    fi
    
    # Check if TROUBLESHOOTING.md contains configuration issues
    if ! grep -q "Configuration Issues" docs/TROUBLESHOOTING.md; then
        print_error "TROUBLESHOOTING.md does not contain configuration issues."
        test_passed=false
    else
        print_status "TROUBLESHOOTING.md contains configuration issues."
    fi
    
    # Check if TROUBLESHOOTING.md contains performance issues
    if ! grep -q "Performance Issues" docs/TROUBLESHOOTING.md; then
        print_error "TROUBLESHOOTING.md does not contain performance issues."
        test_passed=false
    else
        print_status "TROUBLESHOOTING.md contains performance issues."
    fi
    
    # Check if TROUBLESHOOTING.md contains getting help
    if ! grep -q "Getting Help" docs/TROUBLESHOOTING.md; then
        print_error "TROUBLESHOOTING.md does not contain getting help."
        test_passed=false
    else
        print_status "TROUBLESHOOTING.md contains getting help."
    fi
    
    # Test documentation links
    print_status "Testing documentation links..."
    
    # Check if all links in README.md are valid
    if ! python3 scripts/check_links.py README.md; then
        print_error "Some links in README.md are not valid."
        test_passed=false
    else
        print_status "All links in README.md are valid."
    fi
    
    # Check if all links in INSTALLATION.md are valid
    if ! python3 scripts/check_links.py docs/INSTALLATION.md; then
        print_error "Some links in INSTALLATION.md are not valid."
        test_passed=false
    else
        print_status "All links in INSTALLATION.md are valid."
    fi
    
    # Check if all links in CONFIGURATION.md are valid
    if ! python3 scripts/check_links.py docs/CONFIGURATION.md; then
        print_error "Some links in CONFIGURATION.md are not valid."
        test_passed=false
    else
        print_status "All links in CONFIGURATION.md are valid."
    fi
    
    # Check if all links in TROUBLESHOOTING.md are valid
    if ! python3 scripts/check_links.py docs/TROUBLESHOOTING.md; then
        print_error "Some links in TROUBLESHOOTING.md are not valid."
        test_passed=false
    else
        print_status "All links in TROUBLESHOOTING.md are valid."
    fi
    
    # Clean up
    cd /
    rm -rf "$test_dir"
    
    # Print test result
    if [ "$test_passed" = true ]; then
        print_status "Documentation usability tests passed."
        return 0
    else
        print_error "Documentation usability tests failed."
        return 1
    fi
}

# Run documentation usability tests
test_documentation_usability
```

## 4. Test Automation

### Test Automation Script
```bash
#!/bin/bash
# run_all_tests.sh - Run all tests

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

# Function to run a test and check the result
run_test() {
    local test_name=$1
    local test_script=$2
    
    print_step "Running $test_name..."
    
    # Run the test script
    $test_script
    local result=$?
    
    # Check the result
    if [ $result -eq 0 ]; then
        print_status "$test_name passed."
        return 0
    else
        print_error "$test_name failed."
        return 1
    fi
}

# Main function
main() {
    print_status "Running all PiDNS installation tests..."
    print_status "================================"
    
    local total_tests=0
    local passed_tests=0
    local failed_tests=0
    
    # Unit tests
    print_status "Running unit tests..."
    print_status "------------------"
    
    run_test "Device Detection Test" ./tests/test_device_detection.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Configuration Generation Test" ./tests/test_configuration_generation.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Container Configuration Test" ./tests/test_container_configuration.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Integration tests
    print_status "Running integration tests..."
    print_status "---------------------"
    
    run_test "Interactive Installation Test" ./tests/test_interactive_installation.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Silent Installation Test" ./tests/test_silent_installation.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Device tests
    print_status "Running device tests..."
    print_status "----------------"
    
    run_test "Raspberry Pi Zero W Test" ./tests/test_raspberry_pi_zero_w.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Raspberry Pi 3 Test" ./tests/test_raspberry_pi_3.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Raspberry Pi 4/5 Test" ./tests/test_raspberry_pi_4_5.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Low-Resource PC Test" ./tests/test_low_resource_pc.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Standard PC Test" ./tests/test_standard_pc.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Container tests
    print_status "Running container tests..."
    print_status "-------------------"
    
    run_test "Docker Test" ./tests/test_docker.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Podman Test" ./tests/test_podman.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "LXC Test" ./tests/test_lxc.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Error handling tests
    print_status "Running error handling tests..."
    print_status "-------------------------"
    
    run_test "Invalid Device Test" ./tests/test_invalid_device.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Invalid Container Test" ./tests/test_invalid_container.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Insufficient Resources Test" ./tests/test_insufficient_resources.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Network Failure Test" ./tests/test_network_failure.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # User acceptance tests
    print_status "Running user acceptance tests..."
    print_status "--------------------------"
    
    run_test "User Scenario Test" ./tests/test_user_scenario.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    run_test "Documentation Usability Test" ./tests/test_documentation_usability.sh
    if [ $? -eq 0 ]; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Print test summary
    print_status "================================"
    print_status "Test Summary"
    print_status "================================"
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
```

### Test Report Generation
```bash
#!/bin/bash
# generate_test_report.sh - Generate test report

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

# Function to generate test report
generate_test_report() {
    print_step "Generating test report..."
    
    # Create report directory
    local report_dir="test-reports"
    mkdir -p "$report_dir"
    
    # Create report file
    local report_file="$report_dir/test-report-$(date +%Y%m%d-%H%M%S).md"
    
    # Write report header
    cat > "$report_file" << EOF
# PiDNS Installation Test Report

**Date:** $(date)
**Time:** $(date +%H:%M:%S)

## Test Summary

EOF
    
    # Count test results
    local total_tests=$(find tests -name "test_*.sh" | wc -l)
    local passed_tests=$(grep -r "passed" "$report_dir" | wc -l)
    local failed_tests=$(grep -r "failed" "$report_dir" | wc -l)
    
    # Write test summary
    cat >> "$report_file" << EOF
- **Total tests:** $total_tests
- **Passed tests:** $passed_tests
- **Failed tests:** $failed_tests
- **Success rate:** $(echo "scale=2; $passed_tests * 100 / $total_tests" | bc)%

EOF
    
    # Write test results
    cat >> "$report_file" << EOF

## Test Results

EOF
    
    # Add unit test results
    cat >> "$report_file" << EOF
### Unit Tests

EOF
    
    if [ -f "$report_dir/test_device_detection.log" ]; then
        local device_detection_result=$(grep -o "passed\|failed" "$report_dir/test_device_detection.log")
        cat >> "$report_file" << EOF
- **Device Detection Test:** $device_detection_result

EOF
    fi
    
    if [ -f "$report_dir/test_configuration_generation.log" ]; then
        local config_generation_result=$(grep -o "passed\|failed" "$report_dir/test_configuration_generation.log")
        cat >> "$report_file" << EOF
- **Configuration Generation Test:** $config_generation_result

EOF
    fi
    
    if [ -f "$report_dir/test_container_configuration.log" ]; then
        local container_config_result=$(grep -o "passed\|failed" "$report_dir/test_container_configuration.log")
        cat >> "$report_file" << EOF
- **Container Configuration Test:** $container_config_result

EOF
    fi
    
    # Add integration test results
    cat >> "$report_file" << EOF

### Integration Tests

EOF
    
    if [ -f "$report_dir/test_interactive_installation.log" ]; then
        local interactive_install_result=$(grep -o "passed\|failed" "$report_dir/test_interactive_installation.log")
        cat >> "$report_file" << EOF
- **Interactive Installation Test:** $interactive_install_result

EOF
    fi
    
    if [ -f "$report_dir/test_silent_installation.log" ]; then
        local silent_install_result=$(grep -o "passed\|failed" "$report_dir/test_silent_installation.log")
        cat >> "$report_file" << EOF
- **Silent Installation Test:** $silent_install_result

EOF
    fi
    
    # Add device test results
    cat >> "$report_file" << EOF

### Device Tests

EOF
    
    if [ -f "$report_dir/test_raspberry_pi_zero_w.log" ]; then
        local pi_zero_result=$(grep -o "passed\|failed" "$report_dir/test_raspberry_pi_zero_w.log")
        cat >> "$report_file" << EOF
- **Raspberry Pi Zero W Test:** $pi_zero_result

EOF
    fi
    
    if [ -f "$report_dir/test_raspberry_pi_3.log" ]; then
        local pi_3_result=$(grep -o "passed\|failed" "$report_dir/test_raspberry_pi_3.log")
        cat >> "$report_file" << EOF
- **Raspberry Pi 3 Test:** $pi_3_result

EOF
    fi
    
    if [ -f "$report_dir/test_raspberry_pi_4_5.log" ]; then
        local pi_4_5_result=$(grep -o "passed\|failed" "$report_dir/test_raspberry_pi_4_5.log")
        cat >> "$report_file" << EOF
- **Raspberry Pi 4/5 Test:** $pi_4_5_result

EOF
    fi
    
    if [ -f "$report_dir/test_low_resource_pc.log" ]; then
        local low_resource_pc_result=$(grep -o "passed\|failed" "$report_dir/test_low_resource_pc.log")
        cat >> "$report_file" << EOF
- **Low-Resource PC Test:** $low_resource_pc_result

EOF
    fi
    
    if [ -f "$report_dir/test_standard_pc.log" ]; then
        local standard_pc_result=$(grep -o "passed\|failed" "$report_dir/test_standard_pc.log")
        cat >> "$report_file" << EOF
- **Standard PC Test:** $standard_pc_result

EOF
    fi
    
    # Add container test results
    cat >> "$report_file" << EOF

### Container Tests

EOF
    
    if [ -f "$report_dir/test_docker.log" ]; then
        local docker_result=$(grep -o "passed\|failed" "$report_dir/test_docker.log")
        cat >> "$report_file" << EOF
- **Docker Test:** $docker_result

EOF
    fi
    
    if [ -f "$report_dir/test_podman.log" ]; then
        local podman_result=$(grep -o "passed\|failed" "$report_dir/test_podman.log")
        cat >> "$report_file" << EOF
- **Podman Test:** $podman_result

EOF
    fi
    
    if [ -f "$report_dir/test_lxc.log" ]; then
        local lxc_result=$(grep -o "passed\|failed" "$report_dir/test_lxc.log")
        cat >> "$report_file" << EOF
- **LXC Test:** $lxc_result

EOF
    fi
    
    # Add error handling test results
    cat >> "$report_file" << EOF

### Error Handling Tests

EOF
    
    if [ -f "$report_dir/test_invalid_device.log" ]; then
        local invalid_device_result=$(grep -o "passed\|failed" "$report_dir/test_invalid_device.log")
        cat >> "$report_file" << EOF
- **Invalid Device Test:** $invalid_device_result

EOF
    fi
    
    if [ -f "$report_dir/test_invalid_container.log" ]; then
        local invalid_container_result=$(grep -o "passed\|failed" "$report_dir/test_invalid_container.log")
        cat >> "$report_file" << EOF
- **Invalid Container Test:** $invalid_container_result

EOF
    fi
    
    if [ -f "$report_dir/test_insufficient_resources.log" ]; then
        local insufficient_resources_result=$(grep -o "passed\|failed" "$report_dir/test_insufficient_resources.log")
        cat >> "$report_file" << EOF
- **Insufficient Resources Test:** $insufficient_resources_result

EOF
    fi
    
    if [ -f "$report_dir/test_network_failure.log" ]; then
        local network_failure_result=$(grep -o "passed\|failed" "$report_dir/test_network_failure.log")
        cat >> "$report_file" << EOF
- **Network Failure Test:** $network_failure_result

EOF
    fi
    
    # Add user acceptance test results
    cat >> "$report_file" << EOF

### User Acceptance Tests

EOF
    
    if [ -f "$report_dir/test_user_scenario.log" ]; then
        local user_scenario_result=$(grep -o "passed\|failed" "$report_dir/test_user_scenario.log")
        cat >> "$report_file" << EOF
- **User Scenario Test:** $user_scenario_result

EOF
    fi
    
    if [ -f "$report_dir/test_documentation_usability.log" ]; then
        local doc_usability_result=$(grep -o "passed\|failed" "$report_dir/test_documentation_usability.log")
        cat >> "$report_file" << EOF
- **Documentation Usability Test:** $doc_usability_result

EOF
    fi
    
    # Write test details
    cat >> "$report_file" << EOF

## Test Details

EOF
    
    # Add device detection test details
    if [ -f "$report_dir/test_device_detection.log" ]; then
        cat >> "$report_file" << EOF
### Device Detection Test

\`\`\`bash
$(cat "$report_dir/test_device_detection.log")
\`\`\`

EOF
    fi
    
    # Add configuration generation test details
    if [ -f "$report_dir/test_configuration_generation.log" ]; then
        cat >> "$report_file" << EOF
### Configuration Generation Test

\`\`\`bash
$(cat "$report_dir/test_configuration_generation.log")
\`\`\`

EOF
    fi
    
    # Add container configuration test details
    if [ -f "$report_dir/test_container_configuration.log" ]; then
        cat >> "$report_file" << EOF
### Container Configuration Test

\`\`\`bash
$(cat "$report_dir/test_container_configuration.log")
\`\`\`

EOF
    fi
    
    # Add interactive installation test details
    if [ -f "$report_dir/test_interactive_installation.log" ]; then
        cat >> "$report_file" << EOF
### Interactive Installation Test

\`\`\`bash
$(cat "$report_dir/test_interactive_installation.log")
\`\`\`

EOF
    fi
    
    # Add silent installation test details
    if [ -f "$report_dir/test_silent_installation.log" ]; then
        cat >> "$report_file" << EOF
### Silent Installation Test

\`\`\`bash
$(cat "$report_dir/test_silent_installation.log")
\`\`\`

EOF
    fi
    
    # Add Raspberry Pi Zero W test details
    if [ -f "$report_dir/test_raspberry_pi_zero_w.log" ]; then
        cat >> "$report_file" << EOF
### Raspberry Pi Zero W Test

\`\`\`bash
$(cat "$report_dir/test_raspberry_pi_zero_w.log")
\`\`\`

EOF
    fi
    
    # Add Raspberry Pi 3 test details
    if [ -f "$report_dir/test_raspberry_pi_3.log" ]; then
        cat >> "$report_file" << EOF
### Raspberry Pi 3 Test

\`\`\`bash
$(cat "$report_dir/test_raspberry_pi_3.log")
\`\`\`

EOF
    fi
    
    # Add Raspberry Pi 4/5 test details
    if [ -f "$report_dir/test_raspberry_pi_4_5.log" ]; then
        cat >> "$report_file" << EOF
### Raspberry Pi 4/5 Test

\`\`\`bash
$(cat "$report_dir/test_raspberry_pi_4_5.log")
\`\`\`

EOF
    fi
    
    # Add Low-Resource PC test details
    if [ -f "$report_dir/test_low_resource_pc.log" ]; then
        cat >> "$report_file" << EOF
### Low-Resource PC Test

\`\`\`bash
$(cat "$report_dir/test_low_resource_pc.log")
\`\`\`

EOF
    fi
    
    # Add Standard PC test details
    if [ -f "$report_dir/test_standard_pc.log" ]; then
        cat >> "$report_file" << EOF
### Standard PC Test

\`\`\`bash
$(cat "$report_dir/test_standard_pc.log")
\`\`\`

EOF
    fi
    
    # Add Docker test details
    if [ -f "$report_dir/test_docker.log" ]; then
        cat >> "$report_file" << EOF
### Docker Test

\`\`\`bash
$(cat "$report_dir/test_docker.log")
\`\`\`

EOF
    fi
    
    # Add Podman test details
    if [ -f "$report_dir/test_podman.log" ]; then
        cat >> "$report_file" << EOF
### Podman Test

\`\`\`bash
$(cat "$report_dir/test_podman.log")
\`\`\`

EOF
    fi
    
    # Add LXC test details
    if [ -f "$report_dir/test_lxc.log" ]; then
        cat >> "$report_file" << EOF
### LXC Test

\`\`\`bash
$(cat "$report_dir/test_lxc.log")
\`\`\`

EOF
    fi
    
    # Add invalid device test details
    if [ -f "$report_dir/test_invalid_device.log" ]; then
        cat >> "$report_file" << EOF
### Invalid Device Test

\`\`\`bash
$(cat "$report_dir/test_invalid_device.log")
\`\`\`

EOF
    fi
    
    # Add invalid container test details
    if [ -f "$report_dir/test_invalid_container.log" ]; then
        cat >> "$report_file" << EOF
### Invalid Container Test

\`\`\`bash
$(cat "$report_dir/test_invalid_container.log")
\`\`\`

EOF
    fi
    
    # Add insufficient resources test details
    if [ -f "$report_dir/test_insufficient_resources.log" ]; then
        cat >> "$report_file" << EOF
### Insufficient Resources Test

\`\`\`bash
$(cat "$report_dir/test_insufficient_resources.log")
\`\`\`

EOF
    fi
    
    # Add network failure test details
    if [ -f "$report_dir/test_network_failure.log" ]; then
        cat >> "$report_file" << EOF
### Network Failure Test

\`\`\`bash
$(cat "$report_dir/test_network_failure.log")
\`\`\`

EOF
    fi
    
    # Add user scenario test details
    if [ -f "$report_dir/test_user_scenario.log" ]; then
        cat >> "$report_file" << EOF
### User Scenario Test

\`\`\`bash
$(cat "$report_dir/test_user_scenario.log")
\`\`\`

EOF
    fi
    
    # Add documentation usability test details
    if [ -f "$report_dir/test_documentation_usability.log" ]; then
        cat >> "$report_file" << EOF
### Documentation Usability Test

\`\`\`bash
$(cat "$report_dir/test_documentation_usability.log")
\`\`\`

EOF
    fi
    
    # Write report footer
    cat >> "$report_file" << EOF

---

*This report was automatically generated by the PiDNS test suite.*
EOF
    
    print_status "Test report generated: $report_file"
    
    # Convert report to HTML if pandoc is available
    if command -v pandoc &> /dev/null; then
        local html_report_file="${report_file%.md}.html"
        pandoc "$report_file" -o "$html_report_file"
        print_status "Test report converted to HTML: $html_report_file"
    fi
    
    return 0
}

# Generate test report
generate_test_report
```

## 5. Test Execution

### Test Execution Plan
```markdown
# Test Execution Plan

## Test Environment Setup

1. **Hardware Setup**:
   - Set up all test devices (Raspberry Pi Zero W, Pi 3, Pi 4, Pi 5, Low-Resource PC, Standard PC)
   - Install required operating systems (Raspberry Pi OS, Debian, Ubuntu)
   - Configure network connections (Ethernet, WiFi, Mixed)

2. **Software Setup**:
   - Install container platforms (Docker, Podman, LXC)
   - Install test dependencies (Python, Bash, etc.)
   - Clone PiDNS repository

3. **Test Data Setup**:
   - Create test accounts and credentials
   - Prepare test network configurations
   - Set up test databases and files

## Test Execution Schedule

### Week 1: Unit and Integration Tests
- **Day 1-2**: Unit tests (Device Detection, Configuration Generation, Container Configuration)
- **Day 3-4**: Integration tests (Interactive Installation, Silent Installation)
- **Day 5**: Bug fixes and retesting

### Week 2: Device and Container Tests
- **Day 6-7**: Device tests (Raspberry Pi Zero W, Pi 3, Pi 4/5, Low-Resource PC, Standard PC)
- **Day 8-9**: Container tests (Docker, Podman, LXC)
- **Day 10**: Bug fixes and retesting

### Week 3: Error Handling and User Acceptance Tests
- **Day 11-12**: Error handling tests (Invalid Device, Invalid Container, Insufficient Resources, Network Failure)
- **Day 13-14**: User acceptance tests (User Scenario, Documentation Usability)
- **Day 15**: Bug fixes and retesting

### Week 4: Full Regression Testing
- **Day 16-18**: Full regression testing with all test cases
- **Day 19**: Test report generation and review
- **Day 20**: Final bug fixes and preparation for release

## Test Execution Process

### Before Each Test Run
1. **System Preparation**:
   - Reboot test device
   - Clean up any previous test installations
   - Verify network connectivity
   - Check available disk space and memory

2. **Test Environment Setup**:
   - Create temporary test directory
   - Clone latest PiDNS repository
   - Install any required test dependencies

3. **Test Data Preparation**:
   - Create test configuration files
   - Prepare test user accounts
   - Set up test network configurations

### During Each Test Run
1. **Test Execution**:
   - Run test script with appropriate parameters
   - Capture all output and error messages
   - Monitor system resources during test
   - Record test execution time

2. **Result Verification**:
   - Check test script exit code
   - Verify expected system state after test
   - Validate configuration files and settings
   - Test system functionality where applicable

3. **Issue Documentation**:
   - Document any test failures with detailed error messages
   - Capture system logs and diagnostic information
   - Record steps to reproduce any issues
   - Note any deviations from expected behavior

### After Each Test Run
1. **Cleanup**:
   - Remove any temporary files and directories
   - Uninstall PiDNS if installed
   - Reset system configuration changes
   - Free up system resources

2. **Data Collection**:
   - Save test output and logs to test report directory
   - Record test execution time and resource usage
   - Document any issues or anomalies
   - Archive test results for future reference

3. **Reporting**:
   - Update test status in test tracking system
   - Generate test report if all tests in a category are complete
   - Notify team of any critical test failures
   - Schedule retesting for any failed tests

## Test Success Criteria

### Unit Tests
- All device detection functions correctly identify device types
- Configuration generation scripts create valid configuration files
- Container configuration scripts generate valid container configurations
- All unit tests pass with no errors

### Integration Tests
- Interactive installation script correctly handles all user inputs
- Silent installation script correctly processes all command line arguments
- Installation completes successfully for all device and container combinations
- All integration tests pass with no errors

### Device Tests
- Installation completes successfully on all supported device types
- System performance is within expected ranges for each device type
- All device-specific optimizations are correctly applied
- All device tests pass with no errors

### Container Tests
- Installation completes successfully in all supported container types
- Container management commands work correctly (start, stop, restart, etc.)
- Container resource limits are correctly applied
- All container tests pass with no errors

### Error Handling Tests
- Installation script correctly handles all error conditions
- Appropriate error messages are displayed for all error conditions
- System remains stable after all error conditions
- All error handling tests pass with no errors

### User Acceptance Tests
- All user scenarios complete successfully
- Documentation is clear, accurate, and easy to follow
- All user acceptance tests pass with no errors

### Overall Test Success
- All test categories pass with at least 95% success rate
- No critical test failures (installation failures, system crashes, etc.)
- Test report is complete and accurate
- System is ready for release
```

## 6. Test Reporting

### Test Report Template
```markdown
# PiDNS Installation Test Report

## Executive Summary

This report summarizes the results of the PiDNS installation testing conducted from [Start Date] to [End Date]. The testing covered all supported device types, container options, and installation methods to ensure a robust and user-friendly installation experience.

## Test Environment

### Hardware
- **Raspberry Pi Zero W**: 512MB RAM, 1-core CPU
- **Raspberry Pi 3**: 1GB RAM, 4-core CPU
- **Raspberry Pi 4**: 4GB RAM, 4-core CPU
- **Raspberry Pi 5**: 8GB RAM, 4-core CPU
- **Low-Resource PC**: 1GB RAM, 2-core CPU
- **Standard PC**: 8GB RAM, 4-core CPU

### Software
- **Operating Systems**:
  - Raspberry Pi OS Bullseye (32-bit and 64-bit)
  - Debian Bullseye (32-bit and 64-bit)
  - Ubuntu 22.04 LTS (32-bit and 64-bit)
- **Container Platforms**:
  - Docker 20.10+
  - Podman 3.0+
  - LXC 4.0+

### Network Configurations
- Ethernet (wired)
- WiFi (wireless)
- Mixed (both Ethernet and WiFi)

## Test Results Summary

### Overall Results
- **Total Tests**: [Number]
- **Passed Tests**: [Number]
- **Failed Tests**: [Number]
- **Success Rate**: [Percentage]%

### Test Categories

#### Unit Tests
- **Total Tests**: [Number]
- **Passed Tests**: [Number]
- **Failed Tests**: [Number]
- **Success Rate**: [Percentage]%

#### Integration Tests
- **Total Tests**: [Number]
- **Passed Tests**: [Number]
- **Failed Tests**: [Number]
- **Success Rate**: [Percentage]%

#### Device Tests
- **Total Tests**: [Number]
- **Passed Tests**: [Number]
- **Failed Tests**: [Number]
- **Success Rate**: [Percentage]%

#### Container Tests
- **Total Tests**: [Number]
- **Passed Tests**: [Number]
- **Failed Tests**: [Number]
- **Success Rate**: [Percentage]%

#### Error Handling Tests
- **Total Tests**: [Number]
- **Passed Tests**: [Number]
- **Failed Tests**: [Number]
- **Success Rate**: [Percentage]%

#### User Acceptance Tests
- **Total Tests**: [Number]
- **Passed Tests**: [Number]
- **Failed Tests**: [Number]
- **Success Rate**: [Percentage]%

## Detailed Test Results

### Unit Tests

#### Device Detection Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Configuration Generation Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Container Configuration Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

### Integration Tests

#### Interactive Installation Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Silent Installation Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

### Device Tests

#### Raspberry Pi Zero W Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Raspberry Pi 3 Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Raspberry Pi 4/5 Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Low-Resource PC Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Standard PC Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

### Container Tests

#### Docker Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Podman Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### LXC Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

### Error Handling Tests

#### Invalid Device Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Invalid Container Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Insufficient Resources Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Network Failure Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

### User Acceptance Tests

#### User Scenario Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

#### Documentation Usability Test
- **Status**: [Passed/Failed]
- **Execution Time**: [Time]
- **Resource Usage**: [Memory/CPU]
- **Issues**: [Description of any issues]

## Critical Issues

### [Issue 1 Title]
- **Description**: [Detailed description of the issue]
- **Severity**: [Critical/High/Medium/Low]
- **Steps to Reproduce**: [Step-by-step instructions to reproduce the issue]
- **Expected Behavior**: [What should have happened]
- **Actual Behavior**: [What actually happened]
- **Impact**: [How this issue affects users or the system]
- **Proposed Solution**: [Suggested fix or workaround]

### [Issue 2 Title]
- **Description**: [Detailed description of the issue]
- **Severity**: [Critical/High/Medium/Low]
- **Steps to Reproduce**: [Step-by-step instructions to reproduce the issue]
- **Expected Behavior**: [What should have happened]
- **Actual Behavior**: [What actually happened]
- **Impact**: [How this issue affects users or the system]
- **Proposed Solution**: [Suggested fix or workaround]

## Recommendations

### Short-term Recommendations
1. **[Recommendation 1]**: [Description and justification]
2. **[Recommendation 2]**: [Description and justification]
3. **[Recommendation 3]**: [Description and justification]

### Long-term Recommendations
1. **[Recommendation 1]**: [Description and justification]
2. **[Recommendation 2]**: [Description and justification]
3. **[Recommendation 3]**: [Description and justification]

## Conclusion

The PiDNS installation testing has [successfully completed/identified several issues]. The overall success rate of [Percentage]% indicates that the installation process is [robust/needs improvement]. 

[Summary of key findings and overall assessment of the installation process readiness for release.]

## Appendices

### Appendix A: Test Environment Details
- [Detailed information about the test environment, including hardware specifications, software versions, and network configurations]

### Appendix B: Test Scripts and Tools
- [List of test scripts and tools used during testing, with links to repositories or documentation]

### Appendix C: Detailed Test Logs
- [Links to detailed test logs for each test case]

### Appendix D: Performance Metrics
- [Detailed performance metrics for each test case, including execution time, memory usage, and CPU usage]
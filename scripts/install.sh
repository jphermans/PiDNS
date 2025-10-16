#!/bin/bash

# PiDNS Installation Script
# Optimized for Raspberry Pi Zero 2 W

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="/home/pi/PiDNS"
SERVICE_USER="pi"
PYTHON_VENV="$INSTALL_DIR/venv"

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

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "This script should not be run as root. Run as pi user."
    exit 1
fi

# Detect Raspberry Pi model
PI_MODEL=$(cat /proc/device-tree/model 2>/dev/null || echo "Unknown")
PI_VERSION=$(cat /proc/cpuinfo | grep "Revision" | awk '{print $3}' | cut -c1-6)

# Check if running on Raspberry Pi
if ! echo "$PI_MODEL" | grep -q "Raspberry Pi"; then
    print_warning "This script is optimized for Raspberry Pi. Continue anyway? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
fi

print_status "Detected Raspberry Pi model: $PI_MODEL"
print_status "Detected Pi version: $PI_VERSION"

# Set configuration based on Pi model
if echo "$PI_MODEL" | grep -q "Pi 4\|Pi 5"; then
    # Pi 4/5 have more resources
    CACHE_SIZE=300
    DNS_CACHE=300
else
    # Pi Zero/2/3 have limited resources
    CACHE_SIZE=150
    DNS_CACHE=150
fi

print_status "Starting PiDNS installation..."

# Update system packages
print_status "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt-get install -y \
    dnsmasq \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    git \
    curl \
    wget

# Create installation directory if it doesn't exist
if [ ! -d "$INSTALL_DIR" ]; then
    print_status "Creating installation directory..."
    mkdir -p "$INSTALL_DIR"
fi

# Change to installation directory
cd "$INSTALL_DIR"

# Create Python virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv "$PYTHON_VENV"
source "$PYTHON_VENV/bin/activate"

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install ad-blocker dependencies
print_status "Installing ad-blocker dependencies..."
pip install -r requirements_adblocker.txt

# Download MAC vendor database
print_status "Downloading MAC vendor database..."
mkdir -p data
curl -s "https://raw.githubusercontent.com/digitalocean/macvendorlookup/main/data/mac-vendors.json" -o data/mac-vendors.json

# Configure dnsmasq with model-specific settings
print_status "Configuring dnsmasq for $PI_MODEL..."

# Create temporary config with model-specific settings
sed "s/CACHE_SIZE/$CACHE_SIZE/g; s/DNS_CACHE/$DNS_CACHE/g" config/dnsmasq.conf > /tmp/dnsmasq.conf

# Install configuration
sudo cp /tmp/dnsmasq.conf /etc/dnsmasq.conf
sudo systemctl restart dnsmasq
sudo systemctl enable dnsmasq

# Install systemd services
print_status "Installing systemd services..."
sudo cp services/dnsmasq.service /etc/systemd/system/
sudo cp services/pidns.service /etc/systemd/system/
sudo cp services/adblocker.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start PiDNS service
print_status "Enabling and starting PiDNS service..."
sudo systemctl enable pidns.service
sudo systemctl start pidns.service

# Enable and start ad-blocker service
print_status "Enabling and starting ad-blocker service..."
sudo systemctl enable adblocker.service
sudo systemctl start adblocker.service

# Configure firewall (if ufw is available)
if command -v ufw &> /dev/null; then
    print_status "Configuring firewall..."
    sudo ufw allow 8080/tcp
    sudo ufw allow 8081/tcp
    sudo ufw allow 53/udp
    sudo ufw allow 67/udp
fi

# Set up log rotation
print_status "Setting up log rotation..."
sudo tee /etc/logrotate.d/pidns > /dev/null << EOF
/var/log/pidns/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
}
EOF

# Create log directories
sudo mkdir -p /var/log/pidns
sudo chown $SERVICE_USER:$SERVICE_USER /var/log/pidns

sudo mkdir -p /var/log/pidns-adblocker
sudo chown $SERVICE_USER:$SERVICE_USER /var/log/pidns-adblocker

# Create ad-blocker data directories
mkdir -p data/adblocker
mkdir -p data/adblocker/blocklists
mkdir -p logs/adblocker

# Performance optimizations for Pi Zero 2 W
print_status "Applying performance optimizations..."

# Increase socket buffer sizes
echo 'net.core.rmem_max = 16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max = 16777216' | sudo tee -a /etc/sysctl.conf

# Configure swap usage for Pi Zero 2 W
echo 'vm.swappiness = 10' | sudo tee -a /etc/sysctl.conf

# Apply sysctl changes
sudo sysctl -p

# Create startup script
print_status "Creating startup script..."
cat > scripts/start.sh << 'EOF'
#!/bin/bash

# PiDNS startup script

INSTALL_DIR="/home/pi/PiDNS"
PYTHON_VENV="$INSTALL_DIR/venv"

# Change to installation directory
cd "$INSTALL_DIR"

# Activate virtual environment
source "$PYTHON_VENV/bin/activate"

# Start the Flask application
exec python3 app/app.py
EOF

chmod +x scripts/start.sh

# Print installation summary
print_status "Installation completed successfully!"
echo
echo "PiDNS Dashboard Information:"
echo "- Main Dashboard URL: http://$(hostname -I | awk '{print $1}'):8080"
echo "- Ad-Blocker Dashboard URL: http://$(hostname -I | awk '{print $1}'):8081"
echo "- Default username: admin"
echo "- Default password: password"
echo
echo "Ad-Blocker Features:"
echo "- Manage block lists with predefined categories"
echo "- Custom whitelist and blacklist with categories and expiration"
echo "- Real-time statistics and query logging"
echo "- Block ads, tracking, malware, and more"
echo
echo "Important:"
echo "1. Change the default password by setting PIDNS_PASSWORD environment variable"
echo "2. Access the ad-blocker dashboard at http://$(hostname -I | awk '{print $1}'):8081"
echo "3. Configure block lists in the ad-blocker dashboard"
echo "4. Configure your router to use this Pi as DNS server (IP: $(hostname -I | awk '{print $1}'))"
echo "5. Configure your router to use this Pi as DHCP server if needed"
echo
print_warning "Please reboot your system to ensure all services start correctly."
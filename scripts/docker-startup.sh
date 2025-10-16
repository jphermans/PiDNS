#!/bin/bash

# Docker startup script for PiDNS applications
# Provides debugging and ensures proper initialization

set -e

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

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if we're running the main PiDNS app or ad-blocker
APP_TYPE=${1:-pidns}

print_header "Starting $APP_TYPE Application"

# Print environment information
print_status "Environment Information:"
echo "  - Python version: $(python --version)"
echo "  - Working directory: $(pwd)"
echo "  - User: $(whoami)"
echo "  - Hostname: $(hostname)"

# Print relevant environment variables
print_status "Configuration:"
echo "  - PIDNS_USERNAME: ${PIDNS_USERNAME:-not set}"
echo "  - DEBUG: ${DEBUG:-not set}"
echo "  - FLASK_ENV: ${FLASK_ENV:-not set}"
echo "  - SECRET_KEY: ${SECRET_KEY:+set}"

# Check required directories
print_status "Checking directories..."
mkdir -p data logs data/adblocker/blocklists logs/adblocker

# Check for required files
if [ "$APP_TYPE" = "pidns" ]; then
    if [ ! -f "data/mac-vendors.json" ]; then
        print_status "Downloading MAC vendor database..."
        curl -s "https://raw.githubusercontent.com/digitalocean/macvendorlookup/main/data/mac-vendors.json" -o data/mac-vendors.json
    fi
    
    # Check if dnsmasq lease file exists
    if [ ! -f "/var/lib/misc/dnsmasq.leases" ]; then
        print_warning "dnsmasq lease file not found, creating empty one"
        sudo mkdir -p /var/lib/misc
        sudo touch /var/lib/misc/dnsmasq.leases
        sudo chmod 666 /var/lib/misc/dnsmasq.leases
    fi
fi

# Initialize database for ad-blocker
if [ "$APP_TYPE" = "adblocker" ]; then
    print_status "Initializing ad-blocker database..."
    python -c "
from models.database import init_database, db
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/adblocker/adblocker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_database(app)
print('Database initialized successfully')
"
fi

# Health check function
health_check() {
    local app_port=$1
    local health_endpoint=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Performing health check..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "http://localhost:$app_port$health_endpoint" &> /dev/null; then
            print_status "✓ Health check passed on attempt $attempt"
            return 0
        fi
        
        print_status "Health check attempt $attempt/$max_attempts failed, retrying in 2 seconds..."
        sleep 2
        attempt=$((attempt+1))
    done
    
    print_error "✗ Health check failed after $max_attempts attempts"
    return 1
}

# Start the application
print_status "Starting $APP_TYPE application..."

if [ "$APP_TYPE" = "pidns" ]; then
    # Start main PiDNS app in background
    python app/app.py &
    APP_PID=$!
    
    # Wait a moment for startup
    sleep 3
    
    # Perform health check
    if health_check 8080 "/api/health"; then
        print_status "✓ PiDNS application started successfully"
    else
        print_error "✗ PiDNS application failed health check"
        kill $APP_PID 2>/dev/null || true
        exit 1
    fi
    
    # Keep the process running
    wait $APP_PID
    
elif [ "$APP_TYPE" = "adblocker" ]; then
    # Start ad-blocker app in background
    python adblocker/app.py &
    APP_PID=$!
    
    # Wait a moment for startup
    sleep 3
    
    # Perform health check
    if health_check 8081 "/health"; then
        print_status "✓ Ad-blocker application started successfully"
    else
        print_error "✗ Ad-blocker application failed health check"
        kill $APP_PID 2>/dev/null || true
        exit 1
    fi
    
    # Keep the process running
    wait $APP_PID
    
else
    print_error "Unknown application type: $APP_TYPE"
    print_status "Usage: $0 [pidns|adblocker]"
    exit 1
fi
#!/bin/bash

# PiDNS Docker Testing Script
# For testing PiDNS in a Docker environment on MacBook Pro

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="pidns"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

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

# Check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker Desktop for Mac."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose."
        exit 1
    fi

    print_status "Docker environment is ready"
}

# Create environment file if it doesn't exist
setup_environment() {
    if [ ! -f "$ENV_FILE" ]; then
        print_status "Creating environment file..."
        cat > "$ENV_FILE" << EOF
# PiDNS Docker Environment Configuration
PIDNS_USERNAME=admin
PIDNS_PASSWORD=dev-change-me-now!
SECRET_KEY=dev-secret-key
DEBUG=True
EOF
        print_status "Environment file created with default values"
    else
        print_status "Environment file already exists"
    fi
}

# Create necessary directories
setup_directories() {
    print_status "Creating necessary directories..."
    mkdir -p data/adblocker/blocklists
    mkdir -p logs/adblocker
    mkdir -p docker/ssl
    print_status "Directories created"
}

# Build Docker images
build_images() {
    print_header "Building Docker Images"
    docker-compose -f "$COMPOSE_FILE" build --no-cache
    print_status "Docker images built successfully"
}

# Start services
start_services() {
    print_header "Starting PiDNS Services"
    docker-compose -f "$COMPOSE_FILE" up -d
    print_status "Services started"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for dnsmasq
    print_status "Waiting for dnsmasq..."
    sleep 5
    
    # Wait for PiDNS app
    print_status "Waiting for PiDNS application..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:8080/api/health &> /dev/null; then
            print_status "PiDNS application is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "PiDNS application failed to start within timeout"
        return 1
    fi
    
    # Wait for Ad-Blocker
    print_status "Waiting for Ad-Blocker application..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:8081/health &> /dev/null; then
            print_status "Ad-Blocker application is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Ad-Blocker application failed to start within timeout"
        return 1
    fi
}

# Show service status
show_status() {
    print_header "Service Status"
    docker-compose -f "$COMPOSE_FILE" ps
}

# Show access information
show_access_info() {
    print_header "Access Information"
    echo "PiDNS Dashboard Information:"
    echo "- Main Dashboard URL: http://localhost:8080"
    echo "- Ad-Blocker Dashboard URL: http://localhost:8081"
    echo "- Default username: admin"
    echo "- Default password: dev-change-me-now!"
    echo
    echo "DNS Service:"
    echo "- DNS Server: localhost (port 53)"
    echo "- DHCP Server: Enabled (192.168.100.x range)"
    echo
    echo "Management Commands:"
    echo "- View logs: docker-compose -f $COMPOSE_FILE logs -f [service]"
    echo "- Stop services: docker-compose -f $COMPOSE_FILE down"
    echo "- Restart services: docker-compose -f $COMPOSE_FILE restart [service]"
}

# Run tests
run_tests() {
    print_header "Running Basic Tests"
    
    # Test PiDNS health endpoint
    print_status "Testing PiDNS health endpoint..."
    if curl -f http://localhost:8080/api/health &> /dev/null; then
        print_status "✓ PiDNS health check passed"
    else
        print_error "✗ PiDNS health check failed"
        return 1
    fi
    
    # Test Ad-Blocker health endpoint
    print_status "Testing Ad-Blocker health endpoint..."
    if curl -f http://localhost:8081/health &> /dev/null; then
        print_status "✓ Ad-Blocker health check passed"
    else
        print_error "✗ Ad-Blocker health check failed"
        return 1
    fi
    
    # Test DNS resolution
    print_status "Testing DNS resolution..."
    if nslookup google.com localhost &> /dev/null; then
        print_status "✓ DNS resolution test passed"
    else
        print_warning "⚠ DNS resolution test failed (may be expected on macOS)"
    fi
    
    print_status "All tests completed"
}

# Stop services
stop_services() {
    print_header "Stopping PiDNS Services"
    docker-compose -f "$COMPOSE_FILE" down
    print_status "Services stopped"
}

# Clean up
cleanup() {
    print_header "Cleaning Up"
    docker-compose -f "$COMPOSE_FILE" down -v --remove-orphans
    docker system prune -f
    print_status "Cleanup completed"
}

# Show logs
show_logs() {
    local service=$1
    if [ -z "$service" ]; then
        docker-compose -f "$COMPOSE_FILE" logs -f
    else
        docker-compose -f "$COMPOSE_FILE" logs -f "$service"
    fi
}

# Start with nginx
start_with_nginx() {
    print_header "Starting PiDNS Services with Nginx"
    docker-compose -f "$COMPOSE_FILE" --profile with-nginx up -d
    print_status "Services with nginx started"
    
    print_status "Waiting for nginx to be ready..."
    sleep 10
    
    if curl -f http://localhost &> /dev/null; then
        print_status "✓ Nginx is ready"
        echo
        echo "Access Information with Nginx:"
        echo "- Main Dashboard URL: http://localhost"
        echo "- Ad-Blocker URL: http://adblocker.localhost"
        echo "(Add 'adblocker.localhost' to your /etc/hosts file pointing to 127.0.0.1)"
    else
        print_warning "⚠ Nginx may not be ready yet"
    fi
}

# Show usage
show_usage() {
    echo "PiDNS Docker Testing Script"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  start       Build and start all services"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  status      Show service status"
    echo "  logs        Show logs for all services"
    echo "  logs [svc]  Show logs for specific service"
    echo "  test        Run basic tests"
    echo "  nginx       Start services with nginx reverse proxy"
    echo "  cleanup     Stop services and clean up resources"
    echo "  help        Show this help message"
    echo
    echo "Examples:"
    echo "  $0 start    # Build and start all services"
    echo "  $0 logs pidns  # Show logs for PiDNS service"
    echo "  $0 test     # Run basic tests"
}

# Main script logic
main() {
    local command=${1:-help}
    
    case $command in
        start)
            check_docker
            setup_environment
            setup_directories
            build_images
            start_services
            wait_for_services
            show_status
            show_access_info
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            start_services
            wait_for_services
            show_status
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs "$2"
            ;;
        test)
            run_tests
            ;;
        nginx)
            check_docker
            setup_environment
            setup_directories
            build_images
            start_with_nginx
            ;;
        cleanup)
            cleanup
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            print_error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
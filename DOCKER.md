
# PiDNS Docker Testing Guide

This guide provides instructions for testing PiDNS in a Docker environment on MacBook Pro.

## Prerequisites

- Docker Desktop for Mac (latest version)
- Docker Compose
- At least 4GB of available RAM
- 2GB of available disk space

## Quick Start

1. Clone the PiDNS repository:
   ```bash
   git clone <repository-url>
   cd PiDNS
   ```

2. Run the test script:
   ```bash
   ./scripts/docker-test.sh start
   ```

3. Access the dashboards:
   - Main Dashboard: http://localhost:8080
   - Ad-Blocker Dashboard: http://localhost:8081
   - Username: `admin`
   - Password: `dev-change-me-now!`

## Detailed Instructions

### 1. Environment Setup

The Docker testing script automatically creates a `.env` file with default configuration:

```bash
PIDNS_USERNAME=admin
PIDNS_PASSWORD=dev-change-me-now!
SECRET_KEY=dev-secret-key
DEBUG=True
```

You can modify these values before starting the services.

### 2. Directory Structure

The script creates the following directory structure:

```
PiDNS/
├── data/
│   ├── mac-vendors.json
│   └── adblocker/
│       └── blocklists/
├── logs/
│   └── adblocker/
├── docker/
│   ├── nginx.conf
│   └── ssl/
├── Dockerfile
├── Dockerfile.adblocker
├── docker-compose.yml
└── scripts/
    └── docker-test.sh
```

### 3. Services

The Docker environment includes the following services:

#### Dnsmasq (DNS/DHCP Server)
- Container name: `pidns-dnsmasq`
- Ports: `53/udp`, `53/tcp`, `67/udp`
- Configuration: `config/dnsmasq-docker.conf`
- DHCP Range: `192.168.100.100-192.168.100.200`

#### PiDNS Main Application
- Container name: `pidns-app`
- Port: `8080`
- Health check: `/api/health`

#### Ad-Blocker Application
- Container name: `pidns-adblocker`
- Port: `8081`
- Health check: `/health`

#### Nginx Reverse Proxy (Optional)
- Container name: `pidns-nginx`
- Ports: `80`, `443`
- Profile: `with-nginx`

## Script Commands

### Basic Commands

```bash
# Start all services
./scripts/docker-test.sh start

# Stop all services
./scripts/docker-test.sh stop

# Restart all services
./scripts/docker-test.sh restart

# Show service status
./scripts/docker-test.sh status

# Show logs for all services
./scripts/docker-test.sh logs

# Show logs for specific service
./scripts/docker-test.sh logs pidns
./scripts/docker-test.sh logs adblocker
./scripts/docker-test.sh logs dnsmasq
```

### Advanced Commands

```bash
# Run basic tests
./scripts/docker-test.sh test

# Start with nginx reverse proxy
./scripts/docker-test.sh nginx

# Clean up all resources
./scripts/docker-test.sh cleanup

# Show help
./scripts/docker-test.sh help
```

## Testing PiDNS Functionality

### 1. Dashboard Access

After starting the services, you can access:

- **Main Dashboard**: http://localhost:8080
  - Monitor connected devices
  - View network statistics
  - Manage DHCP leases

- **Ad-Blocker Dashboard**: http://localhost:8081
  - Manage block lists
  - Configure whitelist/blacklist
  - View blocking statistics

### 2. DNS Testing

To test the DNS service:

```bash
# Test DNS resolution
nslookup google.com localhost

# Test with specific DNS server
dig @localhost google.com
```

### 3. DHCP Testing

The DHCP service is configured for the `192.168.100.x` network range. To test DHCP functionality, you would need to:

1. Create a separate Docker network for testing
2. Run a client container that requests a DHCP lease
3. Verify the lease assignment

This is more complex and typically not needed for basic testing.

### 4. Ad-Blocker Testing

To test the ad-blocker functionality:

1. Access the Ad-Blocker Dashboard at http://localhost:8081
2. Navigate to the "Block Lists" tab
3. Enable some predefined block lists
4. Wait for the block lists to download
5. Test by trying to access a blocked domain

## Advanced Configuration

### Custom Environment Variables

Create a `.env` file with your custom configuration:

```bash
# Authentication
PIDNS_USERNAME=your_username
PIDNS_PASSWORD=your_secure_password

# Security
SECRET_KEY=your_secret_key_here
DEBUG=False

# Network Configuration
DNSMASQ_LEASE_FILE=/var/lib/misc/dnsmasq.leases
MAC_VENDORS_FILE=/app/data/mac-vendors.json
```

### Using Nginx Reverse Proxy

To use nginx as a reverse proxy:

```bash
./scripts/docker-test.sh nginx
```

Then access:
- Main Dashboard: http://localhost
- Ad-Blocker: http://adblocker.localhost (add to `/etc/hosts`)

### SSL Configuration

To enable SSL with nginx:

1. Generate SSL certificates:
   ```bash
   mkdir -p docker/ssl
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout docker/ssl/key.pem \
     -out docker/ssl/cert.pem
   ```

2. Uncomment the SSL configuration in `docker/nginx.conf`

3. Restart with nginx:
   ```bash
   ./scripts/docker-test.sh nginx
   ```

### Custom dnsmasq Configuration

To customize dnsmasq settings:

1. Edit `config/dnsmasq-docker.conf`
2. Restart the services:
   ```bash
   ./scripts/docker-test.sh restart
   ```

## Troubleshooting

### Port Conflicts

If you encounter port conflicts:

1. Check which ports are in use:
   ```bash
   lsof -i :8080
   lsof -i :8081
   lsof -i :53
   ```

2. Stop the conflicting services or modify the port mappings in `docker-compose.yml`

### Permission Issues

If you encounter permission issues with volume mounts:

1. Ensure the script is executable:
   ```bash
   chmod +x scripts/docker-test.sh
   ```

2. Check Docker Desktop permissions in System Preferences

### Memory Issues

If containers are repeatedly restarting:

1. Check Docker Desktop memory allocation (minimum 4GB recommended)
2. Monitor resource usage:
   ```bash
   docker stats
   ```

### DNS Issues on macOS

DNS testing might not work as expected on macOS due to system DNS resolver:

1. Use `dig` instead of `nslookup` for more reliable testing
2. Consider using a VM for more realistic network testing

## Development Workflow

### Making Changes to the Application

1. Make your code changes
2. Rebuild and restart:
   ```bash
   ./scripts/docker-test.sh restart
   ```

### Viewing Logs in Real-Time

```bash
# Follow all logs
./scripts/docker-test.sh logs

# Follow specific service logs
./scripts/docker-test.sh logs pidns
./scripts/docker-test.sh logs adblocker
```

### Debugging Container Issues

1. Check container status:
   ```bash
   docker ps -a
   ```

2. Inspect a container:
   ```bash
   docker inspect pidns-app
   ```

3. Execute commands in a container:
   ```bash
   docker exec -it pidns-app bash
   ```

## Production Considerations

This Docker setup is intended for testing and development. For production use:

1. Use stronger authentication credentials
2. Enable SSL/TLS encryption
3. Configure proper logging and monitoring
4. Set up regular backups
5. Use environment-specific configurations
6. Implement proper security scanning

## Cleanup

To completely remove all Docker resources:

```bash
./scripts/docker-test.sh cleanup
```

This will:
- Stop and remove all containers
- Remove all volumes
- Remove unused Docker images
- Clean up unused networks

## Support

For issues with:
- Docker Desktop: Refer to Docker documentation
- PiDNS functionality: Check the main PiDNS documentation
- This testing script: Create an issue in the repository
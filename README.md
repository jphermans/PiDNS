# PiDNS - Lightweight DNS and DHCP Server for Raspberry Pi

PiDNS is a lightweight DNS and DHCP server solution designed for various Raspberry Pi models. It includes a web dashboard that allows you to monitor connected devices, view their IP addresses, and see network information in real-time. The ad-blocker feature provides Pi-hole-like functionality to block ads, tracking, malware, and more.

## Features

### Core DNS/DHCP Features
- **DNS Server**: Lightweight DNS forwarding with caching
- **DHCP Server**: Automatic IP address assignment for network devices
- **Web Dashboard**: Real-time monitoring of connected devices
- **Device Information**: IP address, MAC address, hostname, vendor, and connection duration
- **Multi-Pi Support**: Optimized for Pi Zero 2 W, Pi 3/3 B+, and Pi 4/5
- **Screenshot Functionality**: Capture dashboard screenshots directly from the web interface
- **Authentication**: Basic authentication to protect dashboard access
- **Auto-start**: Services start automatically on boot
- **Responsive Design**: Works on desktop and mobile devices

### Ad-Blocker Features (Pi-hole like functionality)
- **Block List Management**: Manage multiple block lists with predefined categories
  - Ads (advertising networks)
  - Tracking (analytics and tracking services)
  - Malware (malicious domains)
  - Phishing (phishing domains)
  - Social Media (optional blocking)
  - Custom block lists
- **Whitelist Management**: Create custom whitelist entries with categories and expiration dates
- **Blacklist Management**: Create custom blacklist entries with categories and expiration dates
- **Real-time Statistics**: View blocked queries, top domains, and client statistics
- **Query Logging**: Monitor DNS queries with detailed logging and visualization
- **Scheduled Updates**: Automatically update block lists on a schedule
- **Responsive Interface**: Mobile-friendly ad-blocker management interface

## System Requirements

### Hardware
- Raspberry Pi Zero 2 W
- MicroSD card (16GB+ recommended)
- Power supply (2.5A+ recommended)
- Network connection (Ethernet or Wi-Fi)

### Software
- Debian OS (Raspberry Pi OS recommended)
- Python 3.7+
- dnsmasq
- Systemd

### Supported Raspberry Pi Models
- **Pi Zero 2 W**: Optimized for limited resources (512MB RAM)
- **Pi 3/3 B+**: Balanced configuration for moderate resources
- **Pi 4/5**: Enhanced configuration for more powerful models

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/PiDNS.git
cd PiDNS
```

### 2. Run the Installation Script

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### 3. Reboot the System

```bash
sudo reboot
```

### 4. Access the Dashboards

Open your web browser and navigate to:

**Main Dashboard:**
```
http://[PI_IP_ADDRESS]:8080
```

**Ad-Blocker Dashboard:**
```
http://[PI_IP_ADDRESS]:8081
```

Default credentials:
- Username: `admin`
- Password: `password`

**Important**: Change the default password immediately after installation!

### 5. Using the Dashboards

#### Main Dashboard
The main dashboard provides:
- **Real-time device monitoring**: See all connected devices with their IP, MAC, hostname, and vendor
- **Network statistics**: View total and active device counts
- **Pi model detection**: Shows which Raspberry Pi model is running the service
- **Screenshot functionality**: Click the "Take Screenshot" button to capture the dashboard
- **Auto-refresh**: Dashboard updates every 30 seconds automatically

#### Ad-Blocker Dashboard
The ad-blocker dashboard provides:
- **Block Lists Management**: Add, update, and manage block lists from various sources
- **Whitelist/Blacklist**: Create custom allow/deny lists with categories and expiration
- **Statistics**: View detailed statistics about blocked queries and top domains
- **Real-time Monitoring**: Monitor DNS queries and blocking activity in real-time

### 6. Configuring the Ad-Blocker

After installation, follow these steps to configure the ad-blocker:

1. **Access the Ad-Blocker Dashboard** at `http://[PI_IP_ADDRESS]:8081`
2. **Add Block Lists**: Navigate to the "Block Lists" tab and add predefined or custom block lists
3. **Configure Whitelist/Blacklist**: Add custom domains to whitelist or blacklist as needed
4. **Monitor Statistics**: Check the "Statistics" tab to monitor blocking activity
5. **Configure Router**: Set your router's DNS server to point to your Pi's IP address

#### Dashboard Screenshots

The dashboard includes a built-in screenshot feature that allows you to:
- Capture the current dashboard view
- Download screenshots as PNG files
- Share network status with others

To take a screenshot:
1. Click the "Take Screenshot" button in the header
2. The screenshot will appear in a modal window
3. Click "Download" to save the screenshot to your device
4. Click "New Screenshot" to capture another view

**Note**: The screenshot feature uses the html2canvas library and may require an internet connection for the first load.

## Configuration

### Changing Dashboard Password

Set the `PIDNS_PASSWORD` environment variable:

```bash
export PIDNS_PASSWORD="your_secure_password"
```

Or edit the configuration file:
```bash
nano config/flask_config.py
```

### Customizing dnsmasq

Edit the dnsmasq configuration:
```bash
sudo nano /etc/dnsmasq.conf
```

After making changes, restart dnsmasq:
```bash
sudo systemctl restart dnsmasq
```

### Network Configuration

The default configuration assumes:
- Pi IP address: 192.168.1.1
- DHCP range: 192.168.1.100-192.168.1.200
- Subnet mask: 255.255.255.0

Adjust these values in `/etc/dnsmasq.conf` to match your network.

## Project Structure

```
PiDNS/
├── config/
│   ├── dnsmasq.conf          # dnsmasq configuration
│   └── flask_config.py       # Flask configuration
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Dashboard styles
│   │   └── js/
│   │       └── dashboard.js  # Dashboard JavaScript
│   ├── templates/
│   │   └── index.html       # Dashboard HTML template
│   └── app.py               # Flask application
├── adblocker/               # Ad-Blocker module
│   ├── app.py               # Ad-Blocker Flask application
│   ├── config/
│   │   └── flask_config.py  # Ad-Blocker Flask configuration
│   ├── models/
│   │   └── database.py      # Database models
│   ├── services/
│   │   ├── auth_service.py  # Authentication service
│   │   ├── blocklist_manager.py # Block list management
│   │   └── query_logger.py  # Query logging service
│   ├── static/
│   │   ├── css/
│   │   │   └── adblocker.css # Ad-Blocker styles
│   │   └── js/
│   │       ├── adblocker.js # Common JavaScript
│   │       ├── blocklists.js # Block lists management
│   │       ├── whitelist.js # Whitelist management
│   │       ├── blacklist.js # Blacklist management
│   │       └── statistics.js # Statistics JavaScript
│   ├── templates/
│   │   ├── base.html        # Base template
│   │   ├── dashboard.html   # Ad-Blocker dashboard
│   │   ├── blocklists.html  # Block lists management
│   │   ├── whitelist.html   # Whitelist management
│   │   ├── blacklist.html   # Blacklist management
│   │   └── statistics.html  # Statistics page
├── scripts/
│   ├── install.sh           # Installation script
│   └── start.sh             # Start services script
├── data/
│   ├── mac-vendors.json     # MAC address vendor database
│   └── adblocker/           # Ad-Blocker data directory
│       └── blocklists/      # Downloaded block lists
├── services/
│   ├── dnsmasq.service      # Systemd service for dnsmasq
│   ├── pidns.service        # Systemd service for Flask app
│   └── adblocker.service    # Systemd service for Ad-Blocker
├── requirements.txt         # Python dependencies
├── requirements_adblocker.txt # Ad-Blocker dependencies
└── README.md                # This file
```

## API Endpoints

### Main Dashboard API
The main dashboard uses the following API endpoints:

- `GET /` - Main dashboard page (requires authentication)
- `GET /api/devices` - Get list of connected devices
- `GET /api/stats` - Get network statistics
- `GET /api/refresh` - Force refresh of lease data

### Ad-Blocker API
The ad-blocker dashboard uses the following API endpoints:

#### Authentication
- `POST /api/auth/login` - Login with username and password
- `POST /api/auth/logout` - Logout and clear token
- `POST /api/auth/verify` - Verify JWT token
- `POST /api/auth/change-password` - Change admin password
- `GET /api/auth/status` - Get authentication status

#### Block Lists
- `GET /api/blocklists` - Get all block lists
- `POST /api/blocklists` - Add new block list
- `PUT /api/blocklists/{id}` - Update block list
- `DELETE /api/blocklists/{id}` - Delete block list
- `POST /api/blocklists/{id}/toggle` - Toggle block list enabled/disabled
- `POST /api/blocklists/{id}/update` - Update block list from source
- `POST /api/blocklists/update-all` - Update all enabled block lists
- `GET /api/blocklists/predefined` - Get predefined block lists
- `POST /api/blocklists/predefined` - Add predefined block list

#### Whitelist
- `GET /api/whitelist` - Get whitelist entries
- `POST /api/whitelist` - Add whitelist entry
- `PUT /api/whitelist/{id}` - Update whitelist entry
- `DELETE /api/whitelist/{id}` - Delete whitelist entry
- `POST /api/whitelist/batch` - Batch add whitelist entries
- `POST /api/whitelist/cleanup` - Remove expired entries
- `GET /api/whitelist/export` - Export whitelist entries

#### Blacklist
- `GET /api/blacklist` - Get blacklist entries
- `POST /api/blacklist` - Add blacklist entry
- `PUT /api/blacklist/{id}` - Update blacklist entry
- `DELETE /api/blacklist/{id}` - Delete blacklist entry
- `POST /api/blacklist/batch` - Batch add blacklist entries
- `POST /api/blacklist/cleanup` - Remove expired entries
- `GET /api/blacklist/export` - Export blacklist entries

#### Statistics
- `GET /api/statistics/overview` - Get overview statistics
- `GET /api/statistics/recent-queries` - Get recent queries
- `GET /api/statistics/top-domains` - Get top queried domains
- `GET /api/statistics/top-clients` - Get top query clients
- `GET /api/statistics/hourly` - Get hourly statistics
- `GET /api/statistics/export` - Export statistics data
- `POST /api/statistics/clear` - Clear statistics data

All API endpoints require authentication (HTTP Basic or JWT token).

## Troubleshooting

### Services Not Starting

Check service status:
```bash
sudo systemctl status dnsmasq
sudo systemctl status pidns
sudo systemctl status adblocker
```

View service logs:
```bash
sudo journalctl -u dnsmasq -f
sudo journalctl -u pidns -f
sudo journalctl -u adblocker -f
```

### Dashboard Not Accessible

1. Check if the service is running:
```bash
sudo systemctl status pidns
sudo systemctl status adblocker
```

2. Check if ports are listening:
```bash
sudo netstat -tlnp | grep 8080
sudo netstat -tlnp | grep 8081
```

3. Check firewall settings:
```bash
sudo ufw status
```

### DHCP Not Working

1. Check dnsmasq configuration:
```bash
sudo dnsmasq --test
```

2. Check dnsmasq logs:
```bash
sudo journalctl -u dnsmasq -f
```

3. Ensure network interface is correct in `/etc/dnsmasq.conf`

### Performance Issues

1. Monitor system resources:
```bash
htop
free -h
df -h
```

2. Check dnsmasq performance:
```bash
sudo systemctl status dnsmasq
```

3. Adjust cache size in dnsmasq configuration if needed

### Ad-Blocker Issues

1. Check if block lists are downloading:
```bash
ls -la data/adblocker/blocklists/
```

2. Check dnsmasq configuration includes block lists:
```bash
grep -n "conf-file" /etc/dnsmasq.conf
```

3. Check query logging:
```bash
tail -f /var/log/pidns-adblocker/query.log
```

4. Check database status:
```bash
sqlite3 data/adblocker/adblocker.db ".tables"
```

## Security Considerations

1. **Change Default Password**: Always change the default dashboard password
2. **Network Access**: Consider restricting dashboard access to local network only
3. **Regular Updates**: Keep your system and packages updated
4. **Firewall**: Configure firewall to restrict unnecessary access
5. **Block List Sources**: Only use reputable block list sources
6. **HTTPS**: Consider using HTTPS for remote dashboard access

## Performance Optimization

The installation script includes several optimizations for the Pi Zero 2 W:

- Increased socket buffer sizes
- Optimized swap usage
- Reduced dnsmasq cache size
- Minimal logging to reduce I/O
- Ad-Blocker service memory limits (128MB)
- CPU quota for ad-blocker service (50%)

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Check the logs for error messages
3. Create an issue on the GitHub repository

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- dnsmasq for providing an excellent lightweight DNS/DHCP server
- Flask for the web framework
- Raspberry Pi Foundation for the amazing hardware
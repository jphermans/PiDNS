# PiDNS - Lightweight DNS and DHCP Server for Raspberry Pi Zero 2 W

PiDNS is a lightweight DNS and DHCP server solution designed specifically for the Raspberry Pi Zero 2 W. It includes a web dashboard that allows you to monitor connected devices, view their IP addresses, and see network information in real-time.

## Features

- **DNS Server**: Lightweight DNS forwarding with caching
- **DHCP Server**: Automatic IP address assignment for network devices
- **Web Dashboard**: Real-time monitoring of connected devices
- **Device Information**: IP address, MAC address, hostname, vendor, and connection duration
- **Resource Optimized**: Designed specifically for Pi Zero 2 W's limited resources
- **Authentication**: Basic authentication to protect dashboard access
- **Auto-start**: Services start automatically on boot

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

### 4. Access the Dashboard

Open your web browser and navigate to:
```
http://[PI_IP_ADDRESS]:8080
```

Default credentials:
- Username: `admin`
- Password: `password`

**Important**: Change the default password immediately after installation!

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
├── scripts/
│   ├── install.sh           # Installation script
│   └── start.sh             # Start services script
├── data/
│   └── mac-vendors.json     # MAC address vendor database
├── services/
│   ├── dnsmasq.service      # Systemd service for dnsmasq
│   └── pidns.service        # Systemd service for Flask app
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## API Endpoints

The dashboard uses the following API endpoints:

- `GET /` - Main dashboard page (requires authentication)
- `GET /api/devices` - Get list of connected devices
- `GET /api/stats` - Get network statistics
- `GET /api/refresh` - Force refresh of lease data

All API endpoints require HTTP Basic Authentication.

## Troubleshooting

### Services Not Starting

Check service status:
```bash
sudo systemctl status dnsmasq
sudo systemctl status pidns
```

View service logs:
```bash
sudo journalctl -u dnsmasq -f
sudo journalctl -u pidns -f
```

### Dashboard Not Accessible

1. Check if the service is running:
```bash
sudo systemctl status pidns
```

2. Check if port 8080 is listening:
```bash
sudo netstat -tlnp | grep 8080
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

## Security Considerations

1. **Change Default Password**: Always change the default dashboard password
2. **Network Access**: Consider restricting dashboard access to local network only
3. **Regular Updates**: Keep your system and packages updated
4. **Firewall**: Configure firewall to restrict unnecessary access

## Performance Optimization

The installation script includes several optimizations for the Pi Zero 2 W:

- Increased socket buffer sizes
- Optimized swap usage
- Reduced dnsmasq cache size
- Minimal logging to reduce I/O

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
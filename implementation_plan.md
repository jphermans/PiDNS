# PiDNS Implementation Plan

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
├── README.md                # Project documentation
└── .gitignore               # Git ignore file
```

## Implementation Details

### 1. Set up project structure and configuration files

- Create directory structure as shown above
- Initialize git repository
- Create .gitignore file
- Set up basic configuration files

### 2. Create dnsmasq configuration for DNS and DHCP services

- Configure dnsmasq as both DNS and DHCP server
- Set up DHCP range and lease time
- Configure DNS forwarding to upstream DNS servers
- Enable local DNS resolution
- Set up lease file location

### 3. Implement Flask backend with API endpoints

- Create Flask application with minimal configuration
- Implement REST API endpoints:
  - `/api/devices` - Get list of connected devices
  - `/api/stats` - Get network statistics
  - `/api/refresh` - Force refresh of lease data
- Add error handling and logging

### 4. Create HTML/CSS/JavaScript frontend dashboard

- Design responsive dashboard layout
- Implement device list with sorting and filtering
- Add visual indicators for device status
- Create clean, lightweight UI optimized for Pi's resources
- Add dark/light theme toggle for better visibility

### 5. Implement lease file parsing functionality

- Parse dnsmasq lease file format
- Extract device information (MAC, IP, hostname, lease time)
- Handle edge cases and malformed entries
- Cache parsed data to reduce file I/O

### 6. Add MAC address vendor lookup functionality

- Download or create MAC vendor database
- Implement efficient lookup mechanism
- Add fallback for unknown vendors
- Update vendor database periodically

### 7. Implement device connection duration calculation

- Calculate connection duration from lease timestamps
- Format duration in human-readable format
- Handle timezone conversions
- Update duration in real-time on dashboard

### 8. Add real-time updates to the dashboard

- Implement periodic polling for new lease data
- Add WebSocket support for instant updates
- Optimize update frequency to balance responsiveness and resource usage
- Add visual indicators for new/disconnected devices

### 9. Create systemd service for auto-start on boot

- Create systemd service files for dnsmasq and Flask app
- Configure service dependencies
- Set up auto-restart on failure
- Add logging configuration

### 10. Add basic authentication for dashboard access

- Implement simple username/password authentication
- Add session management
- Configure secure password storage
- Add logout functionality

### 11. Optimize for Pi Zero 2 W resource constraints

- Minimize memory usage
- Optimize CPU usage
- Reduce disk I/O
- Implement caching strategies
- Monitor resource usage

### 12. Create installation and setup documentation

- Write step-by-step installation guide
- Document configuration options
- Add troubleshooting section
- Include performance optimization tips
- Document API endpoints for potential integrations

## Technology Stack

### Backend
- **dnsmasq**: DNS and DHCP server
- **Python 3**: Programming language
- **Flask**: Web framework
- **Systemd**: Service management

### Frontend
- **HTML5**: Markup language
- **CSS3**: Styling with responsive design
- **Vanilla JavaScript**: No heavy frameworks
- **Chart.js (optional)**: For simple statistics visualization

### Data Storage
- **dnsmasq lease file**: DHCP lease information
- **JSON file**: MAC vendor database
- **In-memory cache**: Parsed lease data

## Security Considerations

- Restrict dashboard access to local network
- Use HTTPS for dashboard (self-signed certificate)
- Implement rate limiting for API endpoints
- Secure configuration of dnsmasq
- Regular security updates

## Performance Considerations

- Minimize memory footprint
- Optimize for single-core CPU
- Reduce disk I/O operations
- Implement efficient data structures
- Use caching where appropriate

## Future Enhancements

- Add DNS query logging and visualization
- Implement DHCP reservation management
- Add network traffic monitoring
- Create mobile app for remote monitoring
- Add integration with home automation systems
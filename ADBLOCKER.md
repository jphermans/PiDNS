# PiDNS Ad-Blocker Documentation

## Overview

The PiDNS Ad-Blocker provides Pi-hole-like functionality to block ads, tracking, malware, and other unwanted content at the DNS level. It includes a comprehensive web interface for managing block lists, custom whitelist/blacklist entries, and viewing detailed statistics.

## Features

### Block List Management
- **Predefined Block Lists**: Choose from a variety of curated block lists organized by category:
  - Ads (advertising networks)
  - Tracking (analytics and tracking services)
  - Malware (malicious domains)
  - Phishing (phishing domains)
  - Social Media (optional blocking)
- **Custom Block Lists**: Add your own block lists from any URL
- **Automatic Updates**: Schedule automatic updates for all block lists
- **Category Management**: Organize block lists by category for easy management

### Whitelist/Blacklist Management
- **Custom Whitelist**: Add domains that should never be blocked
- **Custom Blacklist**: Add specific domains to block
- **Categories**: Organize entries with custom categories
- **Expiration Dates**: Set expiration dates for temporary entries
- **Notes**: Add notes to remember why entries were added
- **Import/Export**: Bulk import/export entries from files

### Statistics and Monitoring
- **Real-time Statistics**: View blocked queries, top domains, and client statistics
- **Query Logging**: Monitor all DNS queries with detailed logging
- **Historical Data**: View statistics for different time periods
- **Visualizations**: Charts and graphs for query trends
- **Export Data**: Export statistics data in various formats

## Installation

The ad-blocker is installed as part of the main PiDNS installation. See the main README.md for installation instructions.

After installation, the ad-blocker dashboard will be available at:
```
http://[PI_IP_ADDRESS]:8081
```

## Configuration

### Initial Setup

1. **Access the Ad-Blocker Dashboard** at `http://[PI_IP_ADDRESS]:8081`
2. **Login** with the default credentials (admin/password)
3. **Add Block Lists**: Navigate to the "Block Lists" tab and add predefined or custom block lists
4. **Configure Whitelist/Blacklist**: Add custom domains to whitelist or blacklist as needed
5. **Monitor Statistics**: Check the "Statistics" tab to monitor blocking activity

### Block List Configuration

1. **Add Predefined Block Lists**:
   - Navigate to "Block Lists" tab
   - Click "Add Predefined Block Lists"
   - Select categories and specific lists to add
   - Click "Add Selected"

2. **Add Custom Block Lists**:
   - Click "Add Block List"
   - Enter a name, URL, and category
   - Click "Save"

3. **Update Block Lists**:
   - Individual lists: Click the update icon next to each list
   - All lists: Click "Update All" button

### Whitelist/Blacklist Configuration

1. **Add Entries**:
   - Navigate to "Whitelist" or "Blacklist" tab
   - Click "Add Domain"
   - Enter domain, category, expiration date, and notes
   - Click "Save"

2. **Bulk Import**:
   - Click "Import" button
   - Upload a file or paste entries
   - Select default category
   - Click "Import"

3. **Export Entries**:
   - Click "Export" button
   - Select format (JSON, CSV, TXT)
   - Save the exported file

## API Reference

The ad-blocker provides a RESTful API for all management functions. All endpoints require authentication.

### Authentication

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```

Response:
```json
{
  "success": true,
  "message": "Login successful",
  "token": "jwt_token_here",
  "user": {
    "username": "admin",
    "role": "admin"
  }
}
```

#### Logout
```http
POST /api/auth/logout
```

#### Verify Token
```http
POST /api/auth/verify
Content-Type: application/json

{
  "token": "jwt_token_here"
}
```

#### Change Password
```http
POST /api/auth/change-password
Content-Type: application/json

{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

### Block Lists

#### Get All Block Lists
```http
GET /api/blocklists
```

#### Add Block List
```http
POST /api/blocklists
Content-Type: application/json

{
  "name": "Example Block List",
  "url": "https://example.com/blocklist.txt",
  "category": "ads",
  "enabled": true
}
```

#### Update Block List
```http
PUT /api/blocklists/{id}
Content-Type: application/json

{
  "name": "Updated Block List",
  "enabled": false
}
```

#### Delete Block List
```http
DELETE /api/blocklists/{id}
```

#### Update Block List from Source
```http
POST /api/blocklists/{id}/update
```

#### Get Predefined Block Lists
```http
GET /api/blocklists/predefined
```

#### Add Predefined Block List
```http
POST /api/blocklists/predefined
Content-Type: application/json

{
  "url": "https://raw.githubusercontent.com/.../blocklist.txt"
}
```

### Whitelist

#### Get Whitelist Entries
```http
GET /api/whitelist
```

#### Add Whitelist Entry
```http
POST /api/whitelist
Content-Type: application/json

{
  "domain": "example.com",
  "category": "essential",
  "expires_at": "2024-12-31T23:59:59Z",
  "notes": "Essential service"
}
```

#### Update Whitelist Entry
```http
PUT /api/whitelist/{id}
Content-Type: application/json

{
  "domain": "updated.example.com",
  "notes": "Updated notes"
}
```

#### Delete Whitelist Entry
```http
DELETE /api/whitelist/{id}
```

#### Batch Add Whitelist Entries
```http
POST /api/whitelist/batch
Content-Type: application/json

{
  "entries": [
    {"domain": "example1.com"},
    {"domain": "example2.com"}
  ],
  "category": "custom"
}
```

### Blacklist

#### Get Blacklist Entries
```http
GET /api/blacklist
```

#### Add Blacklist Entry
```http
POST /api/blacklist
Content-Type: application/json

{
  "domain": "ads.example.com",
  "category": "ads",
  "expires_at": "2024-12-31T23:59:59Z",
  "notes": "Advertising domain"
}
```

#### Update Blacklist Entry
```http
PUT /api/blacklist/{id}
Content-Type: application/json

{
  "domain": "updated.example.com",
  "notes": "Updated notes"
}
```

#### Delete Blacklist Entry
```http
DELETE /api/blacklist/{id}
```

#### Batch Add Blacklist Entries
```http
POST /api/blacklist/batch
Content-Type: application/json

{
  "entries": [
    {"domain": "ads1.example.com"},
    {"domain": "ads2.example.com"}
  ],
  "category": "ads"
}
```

### Statistics

#### Get Overview Statistics
```http
GET /api/statistics/overview?days=7
```

#### Get Recent Queries
```http
GET /api/statistics/recent-queries?limit=50&offset=0&blocked_only=false
```

#### Get Top Domains
```http
GET /api/statistics/top-domains?limit=20&blocked_only=false&days=7
```

#### Get Top Clients
```http
GET /api/statistics/top-clients?limit=20&days=7
```

#### Get Hourly Statistics
```http
GET /api/statistics/hourly?hours=24
```

#### Export Statistics
```http
GET /api/statistics/export?format=json&days=30
```

#### Clear Statistics
```http
POST /api/statistics/clear?days=90
```

## Troubleshooting

### Block Lists Not Updating

1. Check network connectivity:
```bash
ping google.com
```

2. Check block list directory:
```bash
ls -la data/adblocker/blocklists/
```

3. Check ad-blocker service status:
```bash
sudo systemctl status adblocker
```

4. Check ad-blocker logs:
```bash
sudo journalctl -u adblocker -f
```

### Domains Not Being Blocked

1. Check if block lists are loaded in dnsmasq:
```bash
grep -n "conf-file" /etc/dnsmasq.conf
```

2. Check if domain is in block list:
```bash
grep "example.com" data/adblocker/blocklists/*.txt
```

3. Check if domain is in whitelist:
```bash
sqlite3 data/adblocker/adblocker.db "SELECT * FROM whitelist WHERE domain='example.com';"
```

4. Restart dnsmasq:
```bash
sudo systemctl restart dnsmasq
```

### Statistics Not Showing

1. Check if query logging is enabled:
```bash
grep "log-queries" /etc/dnsmasq.conf
```

2. Check query log file:
```bash
tail -f /var/log/pidns-adblocker/query.log
```

3. Check database:
```bash
sqlite3 data/adblocker/adblocker.db "SELECT COUNT(*) FROM query_stats;"
```

### Performance Issues

1. Check system resources:
```bash
free -h
df -h
```

2. Check ad-blocker service memory usage:
```bash
systemctl status adblocker
```

3. Reduce number of block lists if memory is limited
4. Adjust query log retention in configuration

## Advanced Configuration

### Custom Block List Sources

You can add custom block list sources by editing the predefined block lists configuration:

```python
# In adblocker/config/predefined_blocklists.py
PREDEFINED_BLOCKLISTS = {
    "custom_category": [
        {
            "name": "Custom Block List",
            "url": "https://example.com/custom-blocklist.txt",
            "description": "Custom block list for specific needs"
        }
    ]
}
```

### Scheduled Updates

Block list updates are scheduled using APScheduler. You can modify the schedule in the ad-blocker configuration:

```python
# In adblocker/config/flask_config.py
BLOCKLIST_UPDATE_SCHEDULE = {
    "hour": "3",  # 3 AM
    "minute": "0"  # At the top of the hour
}
```

### Database Maintenance

The ad-blocker automatically cleans up old query statistics based on the retention period. You can adjust this in the configuration:

```python
# In adblocker/config/flask_config.py
QUERY_LOG_RETENTION_DAYS = 90  # Keep 90 days of query logs
```

To manually clean up old data:

```bash
sqlite3 data/adblocker/adblocker.db "DELETE FROM query_stats WHERE timestamp < datetime('now', '-90 days');"
```

## Security Considerations

1. **Change Default Password**: Always change the default admin password
2. **Network Access**: Consider restricting dashboard access to local network only
3. **Block List Sources**: Only use reputable block list sources
4. **HTTPS**: Consider using HTTPS for remote dashboard access
5. **Regular Updates**: Keep block lists updated regularly

## Integration with Other Services

### Router Configuration

To use the ad-blocker for your entire network, configure your router's DNS settings:

1. Access your router's administration interface
2. Find the DNS settings
3. Set the primary DNS server to your Pi's IP address
4. Set the secondary DNS server to a public DNS (e.g., 8.8.8.8)
5. Save and apply the settings

### DHCP Configuration

If you're using the Pi as your DHCP server, the DNS settings are automatically configured. If you're using another DHCP server, make sure it's configured to use the Pi as the DNS server.

### Home Assistant Integration

You can integrate the ad-blocker with Home Assistant using the REST API:

```yaml
# configuration.yaml
sensor:
  - platform: rest
    resource: http://[PI_IP_ADDRESS]:8081/api/statistics/overview
    name: "PiDNS Ad-Blocker Statistics"
    headers:
      Authorization: "Bearer YOUR_JWT_TOKEN"
    value_template: "{{ value_json.blocked_queries }}"
    json_attributes:
      - total_queries
      - block_percentage
      - unique_domains
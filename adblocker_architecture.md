# PiDNS Ad-Blocker Architecture

## Overview

This document outlines the architecture for implementing a Pi-hole-like ad-blocking solution for PiDNS. The ad-blocker will be implemented as a separate web interface accessible on a different port or path, with comprehensive block list management and whitelist/blacklist functionality.

## System Architecture

### Components

1. **DNS Sinkhole (dnsmasq)**
   - Core DNS resolution with ad-blocking capabilities
   - Configuration to redirect blocked domains to a sinkhole IP
   - Integration with block lists and custom whitelist/blacklist

2. **Ad-Blocker Management Interface (Flask App)**
   - Separate Flask application for ad-blocker management
   - Runs on a different port (e.g., 8081) or path
   - Provides web interface for managing all ad-blocking features

3. **Database (SQLite)**
   - Stores block list configurations
   - Manages whitelist/blacklist entries with categories, expiration dates, and notes
   - Tracks statistics for blocked queries

4. **Block List Manager**
   - Handles downloading and updating of predefined block lists
   - Manages custom block list URLs
   - Processes and merges block lists into dnsmasq format

5. **Query Logger**
   - Logs DNS queries for statistics and visualization
   - Provides insights into blocked domains and query patterns

## Data Flow

```
┌─────────────┐    DNS Query    ┌──────────────┐    Resolved    ┌─────────────┐
│   Client    │ ──────────────> │  dnsmasq with │ ────────────> │   External  │
│   Device    │                │  Ad-Blocking │               │   DNS       │
└─────────────┘                │   Module     │               └─────────────┘
       ^                       └──────────────┘                      ^
       │                              |                               |
       │                       Blocked Query                       │
       │                              v                               │
       │                       ┌──────────────┐                      │
       │                       │ Query Logger │                      │
       │                       └──────────────┘                      │
       │                              |                               │
       │                              v                               │
       │                       ┌──────────────┐                      │
       └─────────────────────── │ Statistics   │ ──────────────────────┘
                               │   Database   │
                               └──────────────┘
                                      ^
                                      │
                               ┌──────────────┐
                               │ Management   │
                               │   Interface  │
                               └──────────────┘
```

## Detailed Component Design

### 1. DNS Sinkhole (dnsmasq)

The existing dnsmasq configuration will be extended with:

- **Block list integration**: Include block lists via `conf-file` directive
- **Whitelist/Blacklist**: Custom configuration for specific domain handling
- **Query logging**: Log queries to a file for processing
- **Sinkhole IP**: Redirect blocked domains to a local IP (e.g., 0.0.0.0)

Configuration additions:
```
# Ad-blocking configuration
conf-file=/etc/dnsmasq.d/adblock.conf
addn-hosts=/etc/dnsmasq.d/whitelist.conf
addn-hosts=/etc/dnsmasq.d/blacklist.conf
log-queries=extra
server=/blocked/0.0.0.0
```

### 2. Ad-Blocker Management Interface

A separate Flask application with the following structure:

```
adblocker/
├── app.py                 # Main Flask application
├── config/
│   └── flask_config.py    # Flask configuration
├── models/
│   └── database.py         # Database models
├── api/
│   ├── blocklists.py      # Block list API endpoints
│   ├── whitelist.py       # Whitelist API endpoints
│   ├── blacklist.py       # Blacklist API endpoints
│   └── statistics.py      # Statistics API endpoints
├── services/
│   ├── blocklist_manager.py # Block list management
│   ├── dnsmasq_manager.py  # dnsmasq configuration management
│   └── stats_processor.py  # Statistics processing
├── templates/
│   ├── base.html          # Base template
│   ├── dashboard.html     # Main dashboard
│   ├── blocklists.html    # Block list management
│   ├── whitelist.html     # Whitelist management
│   ├── blacklist.html     # Blacklist management
│   └── statistics.html    # Statistics and logs
├── static/
│   ├── css/
│   │   └── style.css      # Styles
│   └── js/
│       ├── dashboard.js   # Dashboard JavaScript
│       ├── blocklists.js  # Block list management JS
│       ├── whitelist.js   # Whitelist management JS
│       ├── blacklist.js   # Blacklist management JS
│       └── statistics.js  # Statistics visualization JS
└── utils/
    ├── database.py        # Database utilities
    └── helpers.py         # Helper functions
```

### 3. Database Schema (SQLite)

#### Block Lists Table
```sql
CREATE TABLE block_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT,
    category TEXT NOT NULL,
    enabled BOOLEAN DEFAULT 1,
    last_updated TIMESTAMP,
    entry_count INTEGER DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Whitelist Table
```sql
CREATE TABLE whitelist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL UNIQUE,
    category TEXT DEFAULT 'custom',
    expires_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Blacklist Table
```sql
CREATE TABLE blacklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL UNIQUE,
    category TEXT DEFAULT 'custom',
    expires_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Query Statistics Table
```sql
CREATE TABLE query_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    domain TEXT NOT NULL,
    client_ip TEXT,
    query_type TEXT,
    blocked BOOLEAN DEFAULT 0,
    block_list_id INTEGER,
    FOREIGN KEY (block_list_id) REFERENCES block_lists(id)
);
```

#### Summary Statistics Table
```sql
CREATE TABLE summary_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    total_queries INTEGER DEFAULT 0,
    blocked_queries INTEGER DEFAULT 0,
    unique_clients INTEGER DEFAULT 0,
    top_blocked_domains TEXT,  # JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);
```

### 4. Block List Manager

The Block List Manager will handle:

- **Predefined Block Lists**: Curated list of popular ad-blocking sources
- **Custom URL Support**: Allow users to add their own block list URLs
- **Download and Update**: Scheduled and manual updates of block lists
- **Processing**: Convert various block list formats to dnsmasq format
- **Merging**: Combine multiple block lists efficiently

Predefined categories:
- Ads (advertisements)
- Trackers (tracking and analytics)
- Malware (malicious domains)
- Phishing (phishing domains)
- Social Media (optional blocking)
- Adult Content (optional blocking)

### 5. Query Logger

The Query Logger will:

- **Parse dnsmasq logs**: Extract query information from log files
- **Store in database**: Save query data for statistics and visualization
- **Process in real-time**: Handle logs as they are generated
- **Aggregate data**: Generate summary statistics for performance

### 6. Management Interface Features

#### Dashboard
- Overview of ad-blocking status
- Statistics summary (queries blocked, percentage, etc.)
- Recent blocked domains
- System status indicators

#### Block List Management
- Enable/disable predefined block lists by category
- Add, edit, remove custom block list URLs
- View block list details (entry count, last updated)
- Manual update trigger for block lists

#### Whitelist Management
- Add domains to whitelist with categories
- Set expiration dates for temporary whitelist entries
- Add notes for documentation
- Search and filter whitelist entries
- Import/export whitelist functionality

#### Blacklist Management
- Add domains to blacklist with categories
- Set expiration dates for temporary blacklist entries
- Add notes for documentation
- Search and filter blacklist entries
- Import/export blacklist functionality

#### Statistics and Logs
- Visualize blocked queries over time
- Show top blocked domains
- Display query origin (client IPs)
- Filter by time range, domain, or client
- Export statistics data

## Security Considerations

1. **Authentication**: Basic authentication for the management interface
2. **Authorization**: Separate from the main PiDNS dashboard
3. **Input Validation**: Validate all user inputs, especially domains and URLs
4. **Rate Limiting**: Prevent abuse of the management interface
5. **Secure Configuration**: Ensure dnsmasq configuration is secure

## Performance Considerations

1. **Lightweight Design**: Optimize for Raspberry Pi Zero 2 W constraints
2. **Efficient Processing**: Minimize CPU and memory usage
3. **Database Optimization**: Use appropriate indexes and queries
4. **Caching**: Cache frequently accessed data
5. **Log Rotation**: Implement log rotation to prevent disk space issues

## Integration with Existing PiDNS

The ad-blocker will integrate with the existing PiDNS installation:

1. **Shared dnsmasq**: Extend the existing dnsmasq configuration
2. **Separate Services**: Run as a separate systemd service
3. **Shared Installation**: Update the installation script to include ad-blocker components
4. **Documentation**: Update existing documentation with ad-blocker features

## Implementation Plan

The implementation will follow the todo list created earlier, with each component built and tested incrementally. The focus will be on creating a robust, user-friendly ad-blocking solution that works well on the Raspberry Pi Zero 2 W.
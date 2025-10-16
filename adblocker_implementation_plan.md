# PiDNS Ad-Blocker Implementation Plan

## Overview

This document provides a detailed implementation plan for adding a Pi-hole-like ad-blocking solution to PiDNS. The plan is organized into phases, with specific tasks and deliverables for each phase.

## Implementation Phases

### Phase 1: Foundation and Core Components (8 hours)

#### Task 1.1: Set up project structure for ad-blocker (1 hour)
- Create directory structure for ad-blocker components
- Set up initial configuration files
- Create requirements file for ad-blocker dependencies
- Set up database initialization scripts

**Deliverables:**
- Directory structure: `adblocker/` with all subdirectories
- Initial configuration files
- `requirements_adblocker.txt` with dependencies
- Database initialization script

#### Task 1.2: Design and implement database schema (2 hours)
- Create SQLite database with all required tables
- Implement database models and relationships
- Create database migration scripts
- Set up database connection utilities

**Deliverables:**
- Database schema implementation
- Database models and utilities
- Migration scripts
- Database connection utilities

#### Task 1.3: Implement DNS sinkhole functionality (3 hours)
- Extend dnsmasq configuration for ad-blocking
- Create configuration file generation utilities
- Implement block list processing for dnsmasq format
- Create whitelist/blacklist configuration generation

**Deliverables:**
- Extended dnsmasq configuration
- Configuration file generation utilities
- Block list processing utilities
- Whitelist/blacklist configuration generation

#### Task 1.4: Create basic Flask app structure (2 hours)
- Set up Flask application with proper configuration
- Implement basic routing and error handling
- Add authentication middleware
- Create base templates

**Deliverables:**
- Flask application structure
- Basic routing and error handling
- Authentication middleware
- Base HTML templates

### Phase 2: Backend API and Services (10 hours)

#### Task 2.1: Implement block list management API (3 hours)
- Create API endpoints for block list CRUD operations
- Implement block list download and update functionality
- Add block list category management
- Create block list status monitoring

**Deliverables:**
- Block list API endpoints
- Download and update functionality
- Category management
- Status monitoring

#### Task 2.2: Implement whitelist/blacklist management API (3 hours)
- Create API endpoints for whitelist CRUD operations
- Create API endpoints for blacklist CRUD operations
- Implement category, expiration date, and notes functionality
- Add import/export functionality

**Deliverables:**
- Whitelist API endpoints
- Blacklist API endpoints
- Category, expiration, and notes functionality
- Import/export functionality

#### Task 2.3: Implement statistics tracking API (2 hours)
- Create API endpoints for query statistics
- Implement data aggregation for summary statistics
- Add filtering and pagination support
- Create data export functionality

**Deliverables:**
- Statistics API endpoints
- Data aggregation functionality
- Filtering and pagination
- Data export functionality

#### Task 2.4: Implement query logging service (2 hours)
- Create dnsmasq log parsing utilities
- Implement real-time log processing
- Add database storage for query logs
- Create log rotation and cleanup utilities

**Deliverables:**
- Log parsing utilities
- Real-time log processing
- Database storage implementation
- Log rotation and cleanup utilities

### Phase 3: Frontend Interface (10 hours)

#### Task 3.1: Create dashboard interface (2 hours)
- Design and implement main dashboard layout
- Add statistics overview widgets
- Create system status indicators
- Implement real-time updates

**Deliverables:**
- Dashboard HTML template
- Dashboard CSS styling
- Dashboard JavaScript functionality
- Real-time update implementation

#### Task 3.2: Create block list management interface (3 hours)
- Design and implement block list management UI
- Add category-based filtering and management
- Create custom URL management interface
- Implement block list update controls

**Deliverables:**
- Block list management HTML templates
- Block list management CSS styling
- Block list management JavaScript
- Category and URL management interfaces

#### Task 3.3: Create whitelist/blacklist management interface (3 hours)
- Design and implement whitelist management UI
- Design and implement blacklist management UI
- Add category, expiration, and notes management
- Implement search and filtering functionality

**Deliverables:**
- Whitelist management HTML templates
- Blacklist management HTML templates
- Management CSS styling
- Search and filtering JavaScript

#### Task 3.4: Create statistics and logs interface (2 hours)
- Design and implement statistics visualization
- Create query log viewer with filtering
- Add data export functionality
- Implement responsive design for all interfaces

**Deliverables:**
- Statistics visualization HTML templates
- Query log viewer HTML templates
- Visualization CSS and JavaScript
- Responsive design implementation

### Phase 4: Integration and Deployment (7 hours)

#### Task 4.1: Create systemd service for ad-blocker (2 hours)
- Create systemd service file for ad-blocker Flask app
- Implement service management utilities
- Add service status monitoring
- Create log rotation configuration

**Deliverables:**
- Systemd service file
- Service management utilities
- Status monitoring implementation
- Log rotation configuration

#### Task 4.2: Update installation script (2 hours)
- Extend installation script with ad-blocker components
- Add ad-blocker service setup
- Implement database initialization
- Add configuration file setup

**Deliverables:**
- Updated installation script
- Service setup implementation
- Database initialization
- Configuration file setup

#### Task 4.3: Update documentation (2 hours)
- Update README with ad-blocker features
- Create ad-blocker usage documentation
- Add troubleshooting section
- Update project documentation

**Deliverables:**
- Updated README.md
- Ad-blocker usage documentation
- Troubleshooting guide
- Updated project documentation

#### Task 4.4: Test and optimize performance (1 hour)
- Test ad-blocker functionality on Raspberry Pi Zero 2 W
- Optimize for resource constraints
- Implement performance monitoring
- Create performance optimization guide

**Deliverables:**
- Test results and optimizations
- Performance monitoring implementation
- Optimization guide
- Final implementation review

## Detailed Implementation Tasks

### Task 1.1: Set up project structure for ad-blocker

**Steps:**
1. Create main adblocker directory
2. Create subdirectories: config, models, api, services, templates, static, utils
3. Create initial configuration files
4. Set up requirements file with dependencies
5. Create database initialization script

**Dependencies:**
- Flask
- Flask-SQLAlchemy
- Flask-HTTPAuth
- requests
- schedule
- python-dotenv

### Task 1.2: Design and implement database schema

**Steps:**
1. Create SQLite database with all required tables
2. Implement database models using SQLAlchemy
3. Create relationships between models
4. Add database migration scripts
5. Implement database connection utilities

**Database Tables:**
- block_lists
- whitelist
- blacklist
- query_stats
- summary_stats

### Task 1.3: Implement DNS sinkhole functionality

**Steps:**
1. Extend dnsmasq configuration for ad-blocking
2. Create configuration file generation utilities
3. Implement block list processing for dnsmasq format
4. Create whitelist/blacklist configuration generation
5. Add configuration reload functionality

**dnsmasq Configuration:**
- Add block list configuration files
- Configure sinkhole IP address
- Enable query logging
- Add whitelist/blacklist configuration

### Task 1.4: Create basic Flask app structure

**Steps:**
1. Set up Flask application with proper configuration
2. Implement basic routing and error handling
3. Add authentication middleware
4. Create base HTML templates
5. Set up static file serving

**Flask Configuration:**
- Separate configuration from main PiDNS app
- Different port (8081) for ad-blocker interface
- Authentication settings
- Database connection settings

### Task 2.1: Implement block list management API

**Steps:**
1. Create API endpoints for block list CRUD operations
2. Implement block list download and update functionality
3. Add block list category management
4. Create block list status monitoring
5. Add API documentation

**API Endpoints:**
- GET /api/blocklists - List all block lists
- POST /api/blocklists - Create new block list
- PUT /api/blocklists/<id> - Update block list
- DELETE /api/blocklists/<id> - Delete block list
- POST /api/blocklists/<id>/update - Update block list from URL

### Task 2.2: Implement whitelist/blacklist management API

**Steps:**
1. Create API endpoints for whitelist CRUD operations
2. Create API endpoints for blacklist CRUD operations
3. Implement category, expiration date, and notes functionality
4. Add import/export functionality
5. Add search and filtering capabilities

**API Endpoints:**
- GET /api/whitelist - List whitelist entries
- POST /api/whitelist - Add to whitelist
- PUT /api/whitelist/<id> - Update whitelist entry
- DELETE /api/whitelist/<id> - Remove from whitelist
- Similar endpoints for blacklist

### Task 2.3: Implement statistics tracking API

**Steps:**
1. Create API endpoints for query statistics
2. Implement data aggregation for summary statistics
3. Add filtering and pagination support
4. Create data export functionality
5. Add real-time statistics updates

**API Endpoints:**
- GET /api/stats/summary - Get summary statistics
- GET /api/stats/queries - Get query statistics
- GET /api/stats/domains - Get top blocked domains
- GET /api/stats/clients - Get client statistics
- GET /api/stats/export - Export statistics data

### Task 2.4: Implement query logging service

**Steps:**
1. Create dnsmasq log parsing utilities
2. Implement real-time log processing
3. Add database storage for query logs
4. Create log rotation and cleanup utilities
5. Add performance optimizations for log processing

**Log Processing:**
- Parse dnsmasq query logs
- Extract domain, client IP, query type
- Determine if query was blocked
- Store in database for statistics
- Aggregate data for summary statistics

### Task 3.1: Create dashboard interface

**Steps:**
1. Design and implement main dashboard layout
2. Add statistics overview widgets
3. Create system status indicators
4. Implement real-time updates
5. Add responsive design

**Dashboard Components:**
- Statistics overview (total queries, blocked queries, percentage)
- Recent blocked domains
- System status indicators
- Quick actions (update block lists, refresh stats)
- Performance metrics

### Task 3.2: Create block list management interface

**Steps:**
1. Design and implement block list management UI
2. Add category-based filtering and management
3. Create custom URL management interface
4. Implement block list update controls
5. Add status indicators for each block list

**Interface Components:**
- Block list table with status indicators
- Category filters
- Add custom block list form
- Update controls
- Block list details view

### Task 3.3: Create whitelist/blacklist management interface

**Steps:**
1. Design and implement whitelist management UI
2. Design and implement blacklist management UI
3. Add category, expiration, and notes management
4. Implement search and filtering functionality
5. Add import/export functionality

**Interface Components:**
- Whitelist table with management controls
- Blacklist table with management controls
- Add/edit forms with category, expiration, and notes
- Search and filter controls
- Import/export buttons

### Task 3.4: Create statistics and logs interface

**Steps:**
1. Design and implement statistics visualization
2. Create query log viewer with filtering
3. Add data export functionality
4. Implement responsive design for all interfaces
5. Add interactive charts and graphs

**Interface Components:**
- Statistics charts and graphs
- Query log table with filtering
- Time range selector
- Data export controls
- Interactive visualizations

### Task 4.1: Create systemd service for ad-blocker

**Steps:**
1. Create systemd service file for ad-blocker Flask app
2. Implement service management utilities
3. Add service status monitoring
4. Create log rotation configuration
5. Test service startup and shutdown

**Service Configuration:**
- Service file with proper dependencies
- Start/stop/restart controls
- Status monitoring
- Log configuration
- Automatic startup on boot

### Task 4.2: Update installation script

**Steps:**
1. Extend installation script with ad-blocker components
2. Add ad-blocker service setup
3. Implement database initialization
4. Add configuration file setup
5. Test installation process

**Installation Updates:**
- Install additional dependencies
- Set up ad-blocker directory structure
- Initialize database
- Configure systemd service
- Update firewall rules if needed

### Task 4.3: Update documentation

**Steps:**
1. Update README with ad-blocker features
2. Create ad-blocker usage documentation
3. Add troubleshooting section
4. Update project documentation
5. Review and finalize all documentation

**Documentation Updates:**
- README.md with ad-blocker features
- Usage guide for ad-blocker interface
- Troubleshooting common issues
- API documentation
- Configuration options

### Task 4.4: Test and optimize performance

**Steps:**
1. Test ad-blocker functionality on Raspberry Pi Zero 2 W
2. Optimize for resource constraints
3. Implement performance monitoring
4. Create performance optimization guide
5. Final review and testing

**Testing and Optimization:**
- Functional testing on target hardware
- Performance benchmarking
- Memory usage optimization
- CPU usage optimization
- Final implementation review

## Total Estimated Time: 35 hours

This implementation plan provides a comprehensive roadmap for adding a Pi-hole-like ad-blocking solution to PiDNS. The plan is organized into logical phases with specific tasks and deliverables, ensuring a systematic approach to implementation.
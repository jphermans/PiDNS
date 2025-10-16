# PiDNS Ad-Blocker System Diagrams

## System Architecture Diagram

```mermaid
graph TD
    A[Client Devices] -->|DNS Query| B[dnsmasq with Ad-Blocking]
    B -->|Blocked Query| C[Query Logger]
    B -->|Resolved Query| D[External DNS]
    C --> E[Statistics Database]
    F[Ad-Blocker Management Interface] -->|Configuration| B
    F -->|Management| E
    F -->|Management| G[Block List Manager]
    G -->|Downloads| H[Block List Sources]
    G -->|Updates| B
    I[Systemd Service] -->|Manages| F
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant C as Client Device
    participant D as dnsmasq
    participant L as Query Logger
    participant S as Statistics DB
    participant M as Management Interface
    participant B as Block List Manager

    C->>D: DNS Query for adomain.com
    alt Domain in Block List
        D->>D: Redirect to sinkhole IP
        D->>L: Log blocked query
        L->>S: Store query data
        D->>C: Return sinkhole IP
    else Domain in Whitelist
        D->>D: Allow query
        D->>L: Log allowed query
        L->>S: Store query data
        D->>E: Forward to External DNS
        E->>D: Return IP address
        D->>C: Return IP address
    else Domain not in lists
        D->>L: Log query
        L->>S: Store query data
        D->>E: Forward to External DNS
        E->>D: Return IP address
        D->>C: Return IP address
    end

    M->>S: Request statistics
    S->>M: Return statistics data
    M->>B: Update block lists
    B->>B: Download and process lists
    B->>D: Update configuration
```

## Database Schema Diagram

```mermaid
erDiagram
    block_lists {
        integer id PK
        string name
        string url
        string category
        boolean enabled
        timestamp last_updated
        integer entry_count
        string description
        timestamp created_at
        timestamp updated_at
    }

    whitelist {
        integer id PK
        string domain UK
        string category
        timestamp expires_at
        string notes
        timestamp created_at
        timestamp updated_at
    }

    blacklist {
        integer id PK
        string domain UK
        string category
        timestamp expires_at
        string notes
        timestamp created_at
        timestamp updated_at
    }

    query_stats {
        integer id PK
        timestamp timestamp
        string domain
        string client_ip
        string query_type
        boolean blocked
        integer block_list_id FK
    }

    summary_stats {
        integer id PK
        date date UK
        integer total_queries
        integer blocked_queries
        integer unique_clients
        string top_blocked_domains
        timestamp created_at
    }

    block_lists ||--o{ query_stats : "contains"
    whitelist ||--o{ query_stats : "exceptions"
    blacklist ||--o{ query_stats : "explicit_blocks"
```

## Component Interaction Diagram

```mermaid
graph LR
    A[Ad-Blocker Flask App] --> B[Authentication Module]
    A --> C[API Endpoints]
    A --> D[Web Templates]
    
    C --> E[Block List API]
    C --> F[Whitelist API]
    C --> G[Blacklist API]
    C --> H[Statistics API]
    
    E --> I[Block List Service]
    F --> J[Whitelist Service]
    G --> K[Blacklist Service]
    H --> L[Statistics Service]
    
    I --> M[Database]
    J --> M
    K --> M
    L --> M
    
    I --> N[dnsmasq Config Manager]
    J --> N
    K --> N
    
    N --> O[dnsmasq Configuration Files]
    O --> P[dnsmasq Service]
    
    Q[Query Log Parser] --> R[dnsmasq Log Files]
    Q --> L
```

## User Interface Flow Diagram

```mermaid
graph TD
    A[Login Page] -->|Authenticated| B[Dashboard]
    
    B --> C[Block List Management]
    B --> D[Whitelist Management]
    B --> E[Blacklist Management]
    B --> F[Statistics & Logs]
    
    C --> G[View Block Lists]
    C --> H[Add Custom Block List]
    C --> I[Update Block Lists]
    
    D --> J[View Whitelist]
    D --> K[Add to Whitelist]
    D --> L[Edit Whitelist Entry]
    
    E --> M[View Blacklist]
    E --> N[Add to Blacklist]
    E --> O[Edit Blacklist Entry]
    
    F --> P[View Statistics]
    F --> Q[View Query Logs]
    F --> R[Export Data]
    
    G --> S[Enable/Disable Categories]
    H --> T[Add URL and Category]
    I --> U[Manual Update]
    
    J --> V[Filter by Category]
    K --> W[Add Domain with Expiration]
    L --> X[Edit Category/Notes]
    
    M --> Y[Filter by Category]
    N --> Z[Add Domain with Expiration]
    O --> AA[Edit Category/Notes]
    
    P --> AB[View Charts]
    Q --> AC[Filter by Time/Domain]
    R --> AD[Export to CSV/JSON]
```

## dnsmasq Integration Diagram

```mermaid
graph TD
    A[dnsmasq.conf] -->|include| B[adblock.conf]
    A -->|include| C[whitelist.conf]
    A -->|include| D[blacklist.conf]
    
    E[Block List Manager] -->|generates| B
    F[Whitelist Service] -->|generates| C
    G[Blacklist Service] -->|generates| D
    
    H[dnsmasq Service] -->|reads| A
    H -->|reads| B
    H -->|reads| C
    H -->|reads| D
    
    H -->|logs to| I[Query Log File]
    J[Query Log Parser] -->|reads| I
    J -->|processes| K[Statistics Service]
    
    L[Management Interface] -->|configures| E
    L -->|configures| F
    L -->|configures| G
    
    E -->|downloads| M[Block List Sources]
    F -->|manages| N[Whitelist Database]
    G -->|manages| O[Blacklist Database]
    
    K -->|stores in| P[Statistics Database]
```

## Installation Process Diagram

```mermaid
graph TD
    A[Run install.sh] --> B[Update System Packages]
    B --> C[Install Dependencies]
    C --> D[Create Directory Structure]
    D --> E[Initialize Database]
    E --> F[Configure dnsmasq]
    F --> G[Set Up Systemd Services]
    G --> H[Configure Firewall]
    H --> I[Start Services]
    I --> J[Display Access Information]
    
    K[Ad-Blocker Service] -->|managed by| L[Systemd]
    M[dnsmasq Service] -->|managed by| L
    
    N[Ad-Blocker Flask App] -->|runs as| K
    O[dnsmasq with Ad-Blocking] -->|runs as| M
    
    P[Management Interface] -->|accessed via| Q[Browser]
    Q -->|connects to| N
```

## Performance Optimization Diagram

```mermaid
graph TD
    A[Performance Monitoring] --> B[CPU Usage]
    A --> C[Memory Usage]
    A --> D[Disk I/O]
    A --> E[Network Traffic]
    
    B --> F[Optimize Block List Processing]
    C --> G[Database Query Optimization]
    D --> H[Log Rotation]
    E --> I[Efficient Log Parsing]
    
    F --> J[Incremental Updates]
    G --> K[Database Indexes]
    H --> L[Compress Old Logs]
    I --> M[Batch Processing]
    
    J --> N[Reduce CPU Load]
    K --> O[Faster Queries]
    L --> P[Reduce Disk Usage]
    M --> Q[Reduce Memory Usage]
    
    N --> R[Improved Performance]
    O --> R
    P --> R
    Q --> R
```

These diagrams provide a visual representation of the PiDNS Ad-Blocker system architecture, data flow, database schema, component interactions, user interface flow, dnsmasq integration, installation process, and performance optimization strategies.
# PiDNS Network Configuration

## 1. Network Configuration Overview

### Purpose
This document describes how PiDNS handles network configuration, allowing users to customize their network range, subnet mask, and DNS settings during installation.

### Network Configuration Components
1. **DHCP Range**: The range of IP addresses that PiDNS assigns to devices on the network.
2. **Subnet Mask**: The subnet mask that defines the network's size and structure.
3. **DNS Servers**: The DNS servers that PiDNS uses for resolving domain names.
4. **Gateway**: The default gateway for the network.
5. **Domain Name**: The local domain name for the network.

### Default Network Configuration
By default, PiDNS uses the following network configuration:
- **Network Range**: 192.168.1.0/24
- **DHCP Range**: 192.168.1.100 to 192.168.1.250
- **Subnet Mask**: 255.255.255.0
- **Gateway**: 192.168.1.1
- **DNS Servers**: 8.8.8.8 (Google), 8.8.4.4 (Google), 1.1.1.1 (Cloudflare)
- **Domain Name**: local

## 2. Network Configuration Templates

### Base dnsmasq Configuration Template
```conf
# templates/dnsmasq_base.conf.j2
# Base dnsmasq configuration template for PiDNS
# This template contains common settings for all device types

# Interface configuration
interface={{ interface }}
# Uncomment the line below if using Ethernet instead of WiFi
# interface=eth0

# DHCP server configuration
dhcp-range={{ dhcp_range_start }},{{ dhcp_range_end }},{{ dhcp_netmask }},{{ dhcp_lease_time }}
dhcp-option=option:router,{{ dhcp_router }}
dhcp-option=option:dns-server,{{ dhcp_dns_server }}
dhcp-authoritative

# DNS configuration
domain-needed
bogus-priv
no-resolv
server={{ dns_server_1 }}
server={{ dns_server_2 }}
server={{ dns_server_3 }}

# Lease file location
dhcp-leasefile=/var/lib/misc/dnsmasq.leases

# Logging
{% if enable_logging %}
log-queries
log-dhcp
{% if log_async %}
log-async={{ log_async_queue_size }}
{% endif %}
{% endif %}

# Performance optimizations
cache-size={{ cache_size }}
dns-forward-max={{ dns_forward_max }}
min-port={{ min_port }}
max-port={{ max_port }}

# Security
no-ping
dhcp-name-match=set:hostname-ignore,wpad
dhcp-ignore-names=tag:hostname-ignore

# Local domain
local=/{{ local_domain }}/
domain={{ local_domain }}

# Static leases (examples - customize as needed)
# dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1
# dhcp-host=11:22:33:44:55:66,192.168.1.11,device2

# Time-to-live settings
local-ttl={{ local_ttl }}
neg-ttl={{ neg_ttl }}
max-ttl={{ max_ttl }}
min-cache-ttl={{ min_cache_ttl }}

# Resource optimization settings
max-cache-ttl={{ max_cache_ttl }}
min-cache-ttl={{ min_cache_ttl }}
cache-lim={{ cache_limit }}
```

### Network Configuration Variables
```python
# templates/variables/network_config.py
# Network configuration variables for PiDNS configuration templates

NETWORK_CONFIG = {
    "default": {
        "interface": "wlan0",
        "dhcp_range_start": "192.168.1.100",
        "dhcp_range_end": "192.168.1.250",
        "dhcp_netmask": "255.255.255.0",
        "dhcp_lease_time": "24h",
        "dhcp_router": "192.168.1.1",
        "dhcp_dns_server": "192.168.1.1",
        "dns_server_1": "8.8.8.8",
        "dns_server_2": "8.8.4.4",
        "dns_server_3": "1.1.1.1",
        "enable_logging": True,
        "log_async": True,
        "log_async_queue_size": 50,
        "cache_size": 500,
        "dns_forward_max": 500,
        "min_port": 4096,
        "max_port": 65535,
        "local_ttl": 1,
        "neg_ttl": 900,
        "max_ttl": 86400,
        "min_cache_ttl": 3600,
        "cache_limit": 500,
        "local_domain": "local"
    },
    "common": {
        "interface_options": ["wlan0", "eth0"],
        "common_netmasks": ["255.255.255.0", "255.255.0.0", "255.0.0.0"],
        "common_dns_servers": [
            {"name": "Google", "primary": "8.8.8.8", "secondary": "8.8.4.4"},
            {"name": "Cloudflare", "primary": "1.1.1.1", "secondary": "1.0.0.1"},
            {"name": "OpenDNS", "primary": "208.67.222.222", "secondary": "208.67.220.220"},
            {"name": "Quad9", "primary": "9.9.9.9", "secondary": "149.112.112.112"}
        ],
        "lease_time_options": ["1h", "6h", "12h", "24h", "7d", "30d"],
        "common_domains": ["local", "home", "lan", "internal"]
    }
}
```

## 3. Network Configuration Selection

### Interactive Network Configuration Selection
```python
# scripts/network_config.py
#!/usr/bin/env python3
"""
Network configuration selection script for PiDNS
"""

import os
import sys
import ipaddress
import re
from typing import Dict, List, Optional, Tuple

def validate_ip_address(ip_address: str) -> bool:
    """Validate an IP address"""
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False

def validate_netmask(netmask: str) -> bool:
    """Validate a subnet mask"""
    try:
        # Check if it's a valid netmask (e.g., 255.255.255.0)
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', netmask):
            netmask_ints = [int(part) for part in netmask.split('.')]
            # Check if it's a valid netmask (all 1s followed by all 0s in binary)
            binary_str = ''.join([format(part, '08b') for part in netmask_ints])
            return '01' not in binary_str.strip('0')
        return False
    except (ValueError, AttributeError):
        return False

def validate_network_range(network_range: str) -> bool:
    """Validate a network range in CIDR notation (e.g., 192.168.1.0/24)"""
    try:
        ipaddress.ip_network(network_range, strict=False)
        return True
    except ValueError:
        return False

def get_network_info() -> Dict[str, str]:
    """Get current network information"""
    network_info = {}
    
    try:
        # Get default gateway
        with open('/proc/net/route', 'r') as f:
            for line in f:
                parts = line.strip().split()
                if parts[1] == '00000000' and parts[2] != '00000000':
                    gateway = '.'.join([str(int(parts[2][i:i+2], 16)) for i in range(0, 8, 2)])
                    network_info['gateway'] = gateway
                    break
        
        # Get interface information
        with open('/proc/net/dev', 'r') as f:
            for line in f:
                if ':' in line and not line.startswith(' '):
                    parts = line.strip().split(':')
                    interface = parts[0].strip()
                    if interface in ['eth0', 'wlan0']:
                        network_info['interface'] = interface
                        break
        
        # Get IP address
        if 'interface' in network_info:
            try:
                with open(f'/sys/class/net/{network_info["interface"]}/address', 'r') as f:
                    mac_address = f.read().strip()
                    network_info['mac_address'] = mac_address
            except FileNotFoundError:
                pass
        
        # Get DNS servers
        try:
            with open('/etc/resolv.conf', 'r') as f:
                dns_servers = []
                for line in f:
                    if line.startswith('nameserver '):
                        dns_server = line.split(' ')[1].strip()
                        if validate_ip_address(dns_server):
                            dns_servers.append(dns_server)
                if dns_servers:
                    network_info['dns_servers'] = dns_servers
        except FileNotFoundError:
            pass
        
    except (FileNotFoundError, ValueError, IndexError, AttributeError):
        pass
    
    return network_info

def suggest_network_config() -> Dict[str, str]:
    """Suggest a network configuration based on current network settings"""
    network_info = get_network_info()
    
    # Default configuration
    config = {
        "interface": "wlan0",
        "network_range": "192.168.1.0/24",
        "dhcp_range_start": "192.168.1.100",
        "dhcp_range_end": "192.168.1.250",
        "netmask": "255.255.255.0",
        "gateway": "192.168.1.1",
        "dns_servers": ["8.8.8.8", "8.8.4.4", "1.1.1.1"],
        "domain": "local"
    }
    
    # Update with current network information if available
    if 'gateway' in network_info and validate_ip_address(network_info['gateway']):
        gateway = network_info['gateway']
        config['gateway'] = gateway
        
        # Suggest network range based on gateway
        gateway_parts = gateway.split('.')
        gateway_parts[-1] = '0'
        network_range = '.'.join(gateway_parts) + '/24'
        config['network_range'] = network_range
        
        # Suggest DHCP range based on gateway
        gateway_parts[-1] = '100'
        config['dhcp_range_start'] = '.'.join(gateway_parts)
        
        gateway_parts[-1] = '250'
        config['dhcp_range_end'] = '.'.join(gateway_parts)
    
    if 'interface' in network_info:
        config['interface'] = network_info['interface']
    
    if 'dns_servers' in network_info and len(network_info['dns_servers']) >= 2:
        config['dns_servers'] = network_info['dns_servers'][:3]  # Use up to 3 DNS servers
    
    return config

def interactive_network_config() -> Dict[str, str]:
    """Interactively configure network settings"""
    print("Network Configuration")
    print("===================")
    
    # Get suggested configuration
    suggested_config = suggest_network_config()
    
    # Interface selection
    print("\nNetwork Interface:")
    print("1. wlan0 (WiFi)")
    print("2. eth0 (Ethernet)")
    
    while True:
        interface_choice = input(f"Select network interface [1-2, default: {'1' if suggested_config['interface'] == 'wlan0' else '2'}]: ") or "
        
        if not interface_choice:
            interface = suggested_config['interface']
            break
        elif interface_choice == '1':
            interface = 'wlan0'
            break
        elif interface_choice == '2':
            interface = 'eth0'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    # Network range configuration
    print("\nNetwork Range (CIDR notation, e.g., 192.168.1.0/24):")
    while True:
        network_range = input(f"Enter network range [default: {suggested_config['network_range']}]: ") or suggested_config['network_range']
        
        if validate_network_range(network_range):
            break
        else:
            print("Invalid network range. Please enter a valid network range in CIDR notation (e.g., 192.168.1.0/24).")
    
    # Extract network address and prefix length
    network = ipaddress.ip_network(network_range, strict=False)
    network_address = str(network.network_address)
    prefix_length = network.prefixlen
    
    # Calculate netmask
    netmask = str(network.netmask)
    
    # Calculate gateway (typically network address + 1)
    gateway_address = ipaddress.ip_address(network_address) + 1
    gateway = str(gateway_address)
    
    # DHCP range configuration
    print("\nDHCP Range:")
    print(f"Network: {network_address}/{prefix_length}")
    print(f"Netmask: {netmask}")
    print(f"Gateway: {gateway}")
    
    # Calculate DHCP range
    # Start at network address + 100
    dhcp_start = ipaddress.ip_address(network_address) + 100
    # End at network address + 250 (or broadcast address - 1, whichever is smaller)
    dhcp_end = min(ipaddress.ip_address(network_address) + 250, network.broadcast_address - 1)
    
    while True:
        dhcp_range_start = input(f"Enter DHCP range start [default: {dhcp_start}]: ") or str(dhcp_start)
        dhcp_range_end = input(f"Enter DHCP range end [default: {dhcp_end}]: ") or str(dhcp_end)
        
        if (validate_ip_address(dhcp_range_start) and 
            validate_ip_address(dhcp_range_end) and
            ipaddress.ip_address(dhcp_range_start) >= network.network_address and
            ipaddress.ip_address(dhcp_range_end) <= network.broadcast_address and
            ipaddress.ip_address(dhcp_range_start) < ipaddress.ip_address(dhcp_range_end)):
            break
        else:
            print("Invalid DHCP range. Please enter valid IP addresses within the network range.")
    
    # DNS servers configuration
    print("\nDNS Servers:")
    print("1. Google (8.8.8.8, 8.8.4.4)")
    print("2. Cloudflare (1.1.1.1, 1.0.0.1)")
    print("3. OpenDNS (208.67.222.222, 208.67.220.220)")
    print("4. Quad9 (9.9.9.9, 149.112.112.112)")
    print("5. Custom")
    
    dns_servers = []
    
    while len(dns_servers) < 3:
        if len(dns_servers) == 0:
            dns_choice = input("Select primary DNS server [1-5, default: 1]: ") or "1"
        elif len(dns_servers) == 1:
            dns_choice = input("Select secondary DNS server [1-5, default: 2]: ") or "2"
        else:
            dns_choice = input("Select tertiary DNS server [1-5, default: 3]: ") or "3"
        
        if dns_choice == '1':
            dns_servers.extend(['8.8.8.8', '8.8.4.4'])
        elif dns_choice == '2':
            dns_servers.extend(['1.1.1.1', '1.0.0.1'])
        elif dns_choice == '3':
            dns_servers.extend(['208.67.222.222', '208.67.220.220'])
        elif dns_choice == '4':
            dns_servers.extend(['9.9.9.9', '149.112.112.112'])
        elif dns_choice == '5':
            while len(dns_servers) < 3:
                dns_server = input(f"Enter {'primary' if len(dns_servers) == 0 else 'secondary' if len(dns_servers) == 1 else 'tertiary'} DNS server: ")
                
                if validate_ip_address(dns_server):
                    dns_servers.append(dns_server)
                else:
                    print("Invalid IP address. Please enter a valid IP address.")
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    
    # Domain name configuration
    print("\nDomain Name:")
    print("1. local")
    print("2. home")
    print("3. lan")
    print("4. internal")
    print("5. Custom")
    
    while True:
        domain_choice = input("Select domain name [1-5, default: 1]: ") or "1"
        
        if domain_choice == '1':
            domain = 'local'
            break
        elif domain_choice == '2':
            domain = 'home'
            break
        elif domain_choice == '3':
            domain = 'lan'
            break
        elif domain_choice == '4':
            domain = 'internal'
            break
        elif domain_choice == '5':
            domain = input("Enter custom domain name: ")
            if domain and re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$', domain):
                break
            else:
                print("Invalid domain name. Please enter a valid domain name.")
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    
    # Return configuration
    return {
        "interface": interface,
        "network_range": network_range,
        "dhcp_range_start": dhcp_range_start,
        "dhcp_range_end": dhcp_range_end,
        "netmask": netmask,
        "gateway": gateway,
        "dns_servers": dns_servers,
        "domain": domain
    }

def main():
    """Main function for testing"""
    # Get network configuration
    config = interactive_network_config()
    
    # Print configuration
    print("\nNetwork Configuration Summary:")
    print("=============================")
    print(f"Interface: {config['interface']}")
    print(f"Network Range: {config['network_range']}")
    print(f"Subnet Mask: {config['netmask']}")
    print(f"Gateway: {config['gateway']}")
    print(f"DHCP Range: {config['dhcp_range_start']} to {config['dhcp_range_end']}")
    print(f"DNS Servers: {', '.join(config['dns_servers'])}")
    print(f"Domain Name: {config['domain']}")

if __name__ == "__main__":
    main()
```

### Network Configuration Integration with Installation Script
```bash
# scripts/install.sh (excerpt)
# Function to get network configuration
get_network_config() {
    print_step "Configuring Network Settings"
    
    # Run network configuration script
    local config_output=$(python3 scripts/network_config.py)
    
    # Parse configuration output
    local interface=$(echo "$config_output" | grep "Interface:" | awk '{print $2}')
    local network_range=$(echo "$config_output" | grep "Network Range:" | awk '{print $3}')
    local dhcp_range_start=$(echo "$config_output" | grep "DHCP Range:" | awk '{print $3}')
    local dhcp_range_end=$(echo "$config_output" | grep "DHCP Range:" | awk '{print $5}')
    local netmask=$(echo "$config_output" | grep "Subnet Mask:" | awk '{print $3}')
    local gateway=$(echo "$config_output" | grep "Gateway:" | awk '{print $2}')
    local dns_servers=$(echo "$config_output" | grep "DNS Servers:" | cut -d: -f2 | sed 's/^ *//')
    local domain=$(echo "$config_output" | grep "Domain Name:" | awk '{print $3}')
    
    # Store configuration in variables
    NETWORK_INTERFACE=$interface
    NETWORK_RANGE=$network_range
    DHCP_RANGE_START=$dhcp_range_start
    DHCP_RANGE_END=$dhcp_range_end
    NETMASK=$netmask
    GATEWAY=$gateway
    DNS_SERVERS=$dns_servers
    DOMAIN=$domain
    
    # Print configuration
    print_status "Network Configuration:"
    print_status "  Interface: $NETWORK_INTERFACE"
    print_status "  Network Range: $NETWORK_RANGE"
    print_status "  Subnet Mask: $NETMASK"
    print_status "  Gateway: $GATEWAY"
    print_status "  DHCP Range: $DHCP_RANGE_START to $DHCP_RANGE_END"
    print_status "  DNS Servers: $DNS_SERVERS"
    print_status "  Domain Name: $DOMAIN"
}

# Function to generate dnsmasq configuration with network settings
generate_dnsmasq_config_with_network() {
    local device_type=$1
    local output_dir=$2
    
    print_step "Generating dnsmasq configuration with network settings"
    
    # Create config directory
    mkdir -p config
    
    # Generate dnsmasq configuration
    python3 -c "
import sys
sys.path.append('templates/variables')
from network_config import NETWORK_CONFIG
from device_types import DEVICE_TYPES
from jinja2 import Environment, FileSystemLoader

# Get device type variables
device_vars = DEVICE_TYPES.get('$device_type', {})

# Get network configuration
network_config = {
    'interface': '$NETWORK_INTERFACE',
    'dhcp_range_start': '$DHCP_RANGE_START',
    'dhcp_range_end': '$DHCP_RANGE_END',
    'dhcp_netmask': '$NETMASK',
    'dhcp_lease_time': '24h',
    'dhcp_router': '$GATEWAY',
    'dhcp_dns_server': '$GATEWAY',
    'dns_server_1': '$(echo $DNS_SERVERS | awk '{print $1}')',
    'dns_server_2': '$(echo $DNS_SERVERS | awk '{print $2}')',
    'dns_server_3': '$(echo $DNS_SERVERS | awk '{print $3}')',
    'enable_logging': True,
    'log_async': True,
    'log_async_queue_size': 50,
    'cache_size': device_vars.get('cache_size', 500),
    'dns_forward_max': device_vars.get('dns_forward_max', 500),
    'min_port': 4096,
    'max_port': 65535,
    'local_ttl': 1,
    'neg_ttl': 900,
    'max_ttl': 86400,
    'min_cache_ttl': 3600,
    'cache_limit': device_vars.get('cache_limit', 500),
    'local_domain': '$DOMAIN'
}

# Load template
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('dnsmasq_base.conf.j2')

# Render template
output = template.render(**network_config)

# Write output file
with open('$output_dir/dnsmasq.$device_type.conf', 'w') as f:
    f.write(output)

print('Generated dnsmasq configuration: $output_dir/dnsmasq.$device_type.conf')
"
    
    print_status "dnsmasq configuration generated successfully"
}

# Modified installation script excerpt
main() {
    print_status "PiDNS Installation Script"
    print_status "========================="
    
    # Parse command line arguments
    local result=$(parse_arguments "$@")
    local parse_result=$?
    
    if [ $parse_result -ne 0 ]; then
        return $parse_result
    fi
    
    local device_type=$(echo "$result" | head -n 1)
    local container_type=$(echo "$result" | head -n 2 | tail -n 1)
    local silent=$(echo "$result" | tail -n 1)
    
    # If not in silent mode, ask for device type
    if [ "$silent" = false ]; then
        device_type=$(select_device_type_interactive)
    fi
    
    # Get network configuration
    if [ "$silent" = false ]; then
        get_network_config
    else
        # Use default network configuration in silent mode
        NETWORK_INTERFACE="wlan0"
        NETWORK_RANGE="192.168.1.0/24"
        DHCP_RANGE_START="192.168.1.100"
        DHCP_RANGE_END="192.168.1.250"
        NETMASK="255.255.255.0"
        GATEWAY="192.168.1.1"
        DNS_SERVERS="8.8.8.8 8.8.4.4 1.1.1.1"
        DOMAIN="local"
    fi
    
    # Display device and container information
    display_device_info $device_type
    display_container_info $container_type
    
    # Confirm installation
    if [ "$silent" = false ]; then
        echo ""
        read -p "Continue with installation? (y/n): " confirm
        
        if [[ "$confirm" != "y" && "$confirm" != "yes" ]]; then
            print_status "Installation cancelled."
            return 0
        fi
    fi
    
    # Install dependencies
    if ! install_dependencies; then
        print_error "Failed to install dependencies."
        return 1
    fi
    
    # Generate configuration files
    if ! generate_configuration_files $device_type $container_type; then
        print_error "Failed to generate configuration files."
        return 1
    fi
    
    # Generate dnsmasq configuration with network settings
    if ! generate_dnsmasq_config_with_network $device_type config; then
        print_error "Failed to generate dnsmasq configuration."
        return 1
    fi
    
    # Install PiDNS
    if ! install_pidns $device_type $container_type; then
        print_error "Failed to install PiDNS."
        return 1
    fi
    
    # Validate installation
    if ! validate_installation $device_type $container_type; then
        print_error "Installation validation failed."
        return 1
    fi
    
    # Display post-installation information
    display_post_installation_info $device_type $container_type
    
    return 0
}
```

## 4. Network Configuration Examples

### Example 1: Home Network
```
Network Configuration Summary:
=============================
Interface: wlan0
Network Range: 192.168.1.0/24
Subnet Mask: 255.255.255.0
Gateway: 192.168.1.1
DHCP Range: 192.168.1.100 to 192.168.1.250
DNS Servers: 8.8.8.8, 8.8.4.4, 1.1.1.1
Domain Name: local
```

### Example 2: Office Network
```
Network Configuration Summary:
=============================
Interface: eth0
Network Range: 10.0.0.0/24
Subnet Mask: 255.255.255.0
Gateway: 10.0.0.1
DHCP Range: 10.0.0.100 to 10.0.0.200
DNS Servers: 8.8.8.8, 8.8.4.4, 1.1.1.1
Domain Name: office
```

### Example 3: School Network
```
Network Configuration Summary:
=============================
Interface: eth0
Network Range: 172.16.0.0/16
Subnet Mask: 255.255.0.0
Gateway: 172.16.0.1
DHCP Range: 172.16.1.1 to 172.16.10.254
DNS Servers: 208.67.222.222, 208.67.220.220, 9.9.9.9
Domain Name: school
```

## 5. Network Configuration Validation

### Validation Script
```python
# scripts/validate_network_config.py
#!/usr/bin/env python3
"""
Network configuration validation script for PiDNS
"""

import os
import sys
import ipaddress
import re
import subprocess
from typing import Dict, List, Optional, Tuple

def validate_network_config(config: Dict[str, str]) -> Tuple[bool, List[str]]:
    """Validate a network configuration"""
    errors = []
    
    # Validate interface
    if config.get('interface') not in ['wlan0', 'eth0']:
        errors.append("Invalid network interface. Must be 'wlan0' or 'eth0'.")
    
    # Validate network range
    try:
        network = ipaddress.ip_network(config.get('network_range', ''), strict=False)
        network_address = str(network.network_address)
        prefix_length = network.prefixlen
        netmask = str(network.netmask)
        broadcast_address = str(network.broadcast_address)
    except ValueError:
        errors.append("Invalid network range. Must be in CIDR notation (e.g., 192.168.1.0/24).")
        return False, errors
    
    # Validate DHCP range
    try:
        dhcp_start = ipaddress.ip_address(config.get('dhcp_range_start', ''))
        dhcp_end = ipaddress.ip_address(config.get('dhcp_range_end', ''))
        
        if dhcp_start < network.network_address or dhcp_end > network.broadcast_address:
            errors.append("DHCP range must be within the network range.")
        
        if dhcp_start >= dhcp_end:
            errors.append("DHCP range start must be less than DHCP range end.")
    except ValueError:
        errors.append("Invalid DHCP range. Must be valid IP addresses.")
    
    # Validate gateway
    try:
        gateway = ipaddress.ip_address(config.get('gateway', ''))
        
        if gateway < network.network_address or gateway > network.broadcast_address:
            errors.append("Gateway must be within the network range.")
    except ValueError:
        errors.append("Invalid gateway. Must be a valid IP address.")
    
    # Validate DNS servers
    dns_servers = config.get('dns_servers', [])
    if len(dns_servers) < 1:
        errors.append("At least one DNS server must be specified.")
    
    for dns_server in dns_servers:
        try:
            ipaddress.ip_address(dns_server)
        except ValueError:
            errors.append(f"Invalid DNS server: {dns_server}. Must be a valid IP address.")
    
    # Validate domain name
    domain = config.get('domain', '')
    if not domain or not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$', domain):
        errors.append("Invalid domain name. Must be a valid domain name.")
    
    # Return validation result
    if errors:
        return False, errors
    else:
        return True, []

def test_network_connectivity(config: Dict[str, str]) -> Tuple[bool, List[str]]:
    """Test network connectivity"""
    errors = []
    
    # Test gateway connectivity
    gateway = config.get('gateway', '')
    if gateway:
        try:
            result = subprocess.run(['ping', '-c', '1', gateway], 
                              capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"Cannot ping gateway: {gateway}")
        except FileNotFoundError:
            errors.append("ping command not found.")
    
    # Test DNS server connectivity
    dns_servers = config.get('dns_servers', [])
    for dns_server in dns_servers[:2]:  # Test first two DNS servers
        try:
            result = subprocess.run(['nslookup', 'example.com', dns_server], 
                              capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"Cannot resolve DNS using server: {dns_server}")
        except FileNotFoundError:
            errors.append("nslookup command not found.")
    
    # Return test result
    if errors:
        return False, errors
    else:
        return True, []

def test_dnsmasq_config(config: Dict[str, str]) -> Tuple[bool, List[str]]:
    """Test dnsmasq configuration"""
    errors = []
    
    # Generate dnsmasq configuration file
    config_file = '/tmp/dnsmasq.conf'
    
    try:
        with open(config_file, 'w') as f:
            f.write(f"# Test dnsmasq configuration\n")
            f.write(f"interface={config.get('interface', 'wlan0')}\n")
            f.write(f"dhcp-range={config.get('dhcp_range_start', '192.168.1.100')},{config.get('dhcp_range_end', '192.168.1.250')},{config.get('netmask', '255.255.255.0')},24h\n")
            f.write(f"dhcp-option=option:router,{config.get('gateway', '192.168.1.1')}\n")
            f.write(f"dhcp-option=option:dns-server,{config.get('gateway', '192.168.1.1')}\n")
            f.write(f"domain-needed\n")
            f.write(f"bogus-priv\n")
            f.write(f"no-resolv\n")
            
            dns_servers = config.get('dns_servers', [])
            for i, dns_server in enumerate(dns_servers[:3]):
                f.write(f"server={dns_server}\n")
            
            f.write(f"local=/{config.get('domain', 'local')}/\n")
            f.write(f"domain={config.get('domain', 'local')}\n")
        
        # Test dnsmasq configuration
        result = subprocess.run(['dnsmasq', '--test', '-C', config_file], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            errors.append(f"dnsmasq configuration test failed: {result.stderr}")
    except FileNotFoundError:
        errors.append("dnsmasq command not found.")
    except Exception as e:
        errors.append(f"Error testing dnsmasq configuration: {str(e)}")
    finally:
        # Clean up
        try:
            os.remove(config_file)
        except FileNotFoundError:
            pass
    
    # Return test result
    if errors:
        return False, errors
    else:
        return True, []

def main():
    """Main function for testing"""
    # Example network configuration
    config = {
        "interface": "wlan0",
        "network_range": "192.168.1.0/24",
        "dhcp_range_start": "192.168.1.100",
        "dhcp_range_end": "192.168.1.250",
        "netmask": "255.255.255.0",
        "gateway": "192.168.1.1",
        "dns_servers": ["8.8.8.8", "8.8.4.4", "1.1.1.1"],
        "domain": "local"
    }
    
    # Validate network configuration
    print("Validating network configuration...")
    is_valid, errors = validate_network_config(config)
    
    if is_valid:
        print("Network configuration is valid.")
    else:
        print("Network configuration is invalid:")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    # Test network connectivity
    print("\nTesting network connectivity...")
    is_connected, errors = test_network_connectivity(config)
    
    if is_connected:
        print("Network connectivity test passed.")
    else:
        print("Network connectivity test failed:")
        for error in errors:
            print(f"  - {error}")
    
    # Test dnsmasq configuration
    print("\nTesting dnsmasq configuration...")
    is_config_valid, errors = test_dnsmasq_config(config)
    
    if is_config_valid:
        print("dnsmasq configuration test passed.")
    else:
        print("dnsmasq configuration test failed:")
        for error in errors:
            print(f"  - {error}")
    
    # Return result
    if is_valid and is_config_valid:
        print("\nAll tests passed.")
        return 0
    else:
        print("\nSome tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## 6. Network Configuration Migration

### Migration Script
```python
# scripts/migrate_network_config.py
#!/usr/bin/env python3
"""
Network configuration migration script for PiDNS
"""

import os
import sys
import re
from typing import Dict, List, Optional, Tuple

def read_current_config(config_file: str) -> Dict[str, str]:
    """Read current dnsmasq configuration"""
    config = {}
    
    try:
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if line.startswith('#') or not line:
                    continue
                
                # Parse configuration lines
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == 'interface':
                        config['interface'] = value
                    elif key == 'dhcp-range':
                        # Parse DHCP range: start,end,netmask,lease_time
                        parts = value.split(',')
                        if len(parts) >= 2:
                            dhcp_range = parts[0].split(',')
                            if len(dhcp_range) >= 2:
                                config['dhcp_range_start'] = dhcp_range[0]
                                config['dhcp_range_end'] = dhcp_range[1]
                    elif key == 'dhcp-option' and value.startswith('option:router,'):
                        config['gateway'] = value.split(',')[1]
                    elif key == 'dhcp-option' and value.startswith('option:dns-server,'):
                        config['dns_server'] = value.split(',')[1]
                    elif key == 'server':
                        if 'dns_servers' not in config:
                            config['dns_servers'] = []
                        config['dns_servers'].append(value)
                    elif key == 'local' and value.startswith('/'):
                        config['domain'] = value.strip('/')
                    elif key == 'domain':
                        config['domain'] = value
    except FileNotFoundError:
        pass
    
    return config

def migrate_config(old_config: Dict[str, str]) -> Dict[str, str]:
    """Migrate old configuration to new format"""
    new_config = {}
    
    # Copy interface
    if 'interface' in old_config:
        new_config['interface'] = old_config['interface']
    else:
        new_config['interface'] = 'wlan0'
    
    # Calculate network range from gateway and DHCP range
    if 'gateway' in old_config and 'dhcp_range_start' in old_config:
        gateway = old_config['gateway']
        dhcp_start = old_config['dhcp_range_start']
        
        # Extract network part from gateway
        gateway_parts = gateway.split('.')
        gateway_parts[-1] = '0'
        network_range = '.'.join(gateway_parts) + '/24'
        
        new_config['network_range'] = network_range
    else:
        new_config['network_range'] = '192.168.1.0/24'
    
    # Copy DHCP range
    if 'dhcp_range_start' in old_config and 'dhcp_range_end' in old_config:
        new_config['dhcp_range_start'] = old_config['dhcp_range_start']
        new_config['dhcp_range_end'] = old_config['dhcp_range_end']
    else:
        new_config['dhcp_range_start'] = '192.168.1.100'
        new_config['dhcp_range_end'] = '192.168.1.250'
    
    # Calculate netmask from network range
    if 'network_range' in new_config:
        if new_config['network_range'].endswith('/24'):
            new_config['netmask'] = '255.255.255.0'
        elif new_config['network_range'].endswith('/16'):
            new_config['netmask'] = '255.255.0.0'
        elif new_config['network_range'].endswith('/8'):
            new_config['netmask'] = '255.0.0.0'
        else:
            new_config['netmask'] = '255.255.255.0'
    else:
        new_config['netmask'] = '255.255.255.0'
    
    # Copy gateway
    if 'gateway' in old_config:
        new_config['gateway'] = old_config['gateway']
    else:
        new_config['gateway'] = '192.168.1.1'
    
    # Copy DNS servers
    if 'dns_servers' in old_config:
        new_config['dns_servers'] = old_config['dns_servers']
    elif 'dns_server' in old_config:
        new_config['dns_servers'] = [old_config['dns_server'], '8.8.4.4', '1.1.1.1']
    else:
        new_config['dns_servers'] = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
    
    # Copy domain
    if 'domain' in old_config:
        new_config['domain'] = old_config['domain']
    else:
        new_config['domain'] = 'local'
    
    return new_config

def write_new_config(config: Dict[str, str], config_file: str) -> bool:
    """Write new configuration to file"""
    try:
        with open(config_file, 'w') as f:
            f.write("# PiDNS dnsmasq configuration\n")
            f.write("# Generated by migration script\n")
            f.write("\n")
            
            # Interface configuration
            f.write(f"# Interface configuration\n")
            f.write(f"interface={config['interface']}\n")
            f.write("\n")
            
            # DHCP server configuration
            f.write(f"# DHCP server configuration\n")
            f.write(f"dhcp-range={config['dhcp_range_start']},{config['dhcp_range_end']},{config['netmask']},24h\n")
            f.write(f"dhcp-option=option:router,{config['gateway']}\n")
            f.write(f"dhcp-option=option:dns-server,{config['gateway']}\n")
            f.write(f"dhcp-authoritative\n")
            f.write("\n")
            
            # DNS configuration
            f.write(f"# DNS configuration\n")
            f.write(f"domain-needed\n")
            f.write(f"bogus-priv\n")
            f.write(f"no-resolv\n")
            
            for dns_server in config['dns_servers']:
                f.write(f"server={dns_server}\n")
            
            f.write("\n")
            
            # Lease file location
            f.write(f"# Lease file location\n")
            f.write(f"dhcp-leasefile=/var/lib/misc/dnsmasq.leases\n")
            f.write("\n")
            
            # Logging
            f.write(f"# Logging\n")
            f.write(f"log-queries\n")
            f.write(f"log-dhcp\n")
            f.write(f"log-async=50\n")
            f.write("\n")
            
            # Performance optimizations
            f.write(f"# Performance optimizations\n")
            f.write(f"cache-size=500\n")
            f.write(f"dns-forward-max=500\n")
            f.write(f"min-port=4096\n")
            f.write(f"max-port=65535\n")
            f.write("\n")
            
            # Security
            f.write(f"# Security\n")
            f.write(f"no-ping\n")
            f.write(f"dhcp-name-match=set:hostname-ignore,wpad\n")
            f.write(f"dhcp-ignore-names=tag:hostname-ignore\n")
            f.write("\n")
            
            # Local domain
            f.write(f"# Local domain\n")
            f.write(f"local=/{config['domain']}/\n")
            f.write(f"domain={config['domain']}\n")
            f.write("\n")
            
            # Static leases (examples)
            f.write(f"# Static leases (examples - customize as needed)\n")
            f.write(f"# dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.10,device1\n")
            f.write(f"# dhcp-host=11:22:33:44:55:66,192.168.1.11,device2\n")
            f.write("\n")
            
            # Time-to-live settings
            f.write(f"# Time-to-live settings\n")
            f.write(f"local-ttl=1\n")
            f.write(f"neg-ttl=900\n")
            f.write(f"max-ttl=86400\n")
            f.write(f"min-cache-ttl=3600\n")
            f.write("\n")
            
            # Resource optimization settings
            f.write(f"# Resource optimization settings\n")
            f.write(f"max-cache-ttl=86400\n")
            f.write(f"min-cache-ttl=3600\n")
            f.write(f"cache-lim=500\n")
        
        return True
    except Exception as e:
        print(f"Error writing configuration file: {str(e)}")
        return False

def main():
    """Main function for testing"""
    # Read current configuration
    print("Reading current dnsmasq configuration...")
    current_config = read_current_config('/etc/dnsmasq.conf')
    
    if not current_config:
        print("No current dnsmasq configuration found.")
        return 1
    
    print("Current configuration:")
    for key, value in current_config.items():
        print(f"  {key}: {value}")
    
    # Migrate configuration
    print("\nMigrating configuration...")
    new_config = migrate_config(current_config)
    
    print("New configuration:")
    for key, value in new_config.items():
        print(f"  {key}: {value}")
    
    # Write new configuration
    print("\nWriting new configuration...")
    if write_new_config(new_config, '/tmp/dnsmasq.migrated.conf'):
        print("New configuration written to /tmp/dnsmasq.migrated.conf")
        print("Please review the new configuration and then copy it to /etc/dnsmasq.conf")
        return 0
    else:
        print("Failed to write new configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
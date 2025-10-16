#!/usr/bin/env python3
"""
PiDNS Flask Application
A lightweight web dashboard for monitoring DNS and DHCP services on Raspberry Pi Zero 2 W
"""

import os
import json
import time
import hmac
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from functools import wraps
from config.flask_config import get_config

# Initialize Flask app
app = Flask(__name__)
config_class = get_config()
app.config.from_object(config_class)

# Security validation for basic authentication credentials
def validate_basic_auth_config():
    """Ensure basic authentication credentials are defined and sufficiently strong."""
    username = app.config.get('BASIC_AUTH_USERNAME')
    password = app.config.get('BASIC_AUTH_PASSWORD')

    if not username or not password:
        raise RuntimeError(
            "Basic authentication credentials are not configured. "
            "Set the PIDNS_USERNAME and PIDNS_PASSWORD environment variables."
        )

    weak_usernames = {"admin", "root", "user", "pidns"}
    weak_passwords = {
        "password",
        "admin",
        "changeme",
        "pidns",
        "123456",
    }

    if username.lower() in weak_usernames:
        raise RuntimeError("The configured basic authentication username is too common. Choose a unique username.")

    if len(password) < 12 or password.lower() in weak_passwords:
        raise RuntimeError(
            "The configured basic authentication password is too weak. "
            "Use a password with at least 12 characters that is not a common default."
        )

    if password.lower() == "dev-change-me-now!":
        if not app.config.get('DEBUG'):
            raise RuntimeError(
                "The development default password cannot be used when DEBUG is disabled. "
                "Update PIDNS_PASSWORD to a unique, strong value."
            )
        app.logger.warning(
            "The development default password is in use. Update PIDNS_PASSWORD to improve security."
        )


validate_basic_auth_config()


def validate_secret_key():
    """Ensure the Flask secret key is set appropriately for the active environment."""
    secret_key = app.config.get('SECRET_KEY')
    if app.config.get('DEBUG'):
        if not secret_key or secret_key == 'dev-secret-key':
            app.logger.warning(
                "The development SECRET_KEY is in use. Set SECRET_KEY to a unique value before deploying."
            )
        return

    if not secret_key or len(secret_key) < 16:
        raise RuntimeError(
            "SECRET_KEY must be set to a unique value of at least 16 characters when DEBUG is disabled."
        )


validate_secret_key()

# Global variables for caching
lease_cache = {}
cache_timestamp = 0
CACHE_DURATION = 10  # seconds

# Authentication decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def check_auth(username, password):
    """Check if username and password are correct"""
    stored_username = app.config.get('BASIC_AUTH_USERNAME')
    stored_password = app.config.get('BASIC_AUTH_PASSWORD')

    if stored_username is None or stored_password is None:
        return False

    return (
        hmac.compare_digest(username, stored_username)
        and hmac.compare_digest(password, stored_password)
    )

def authenticate():
    """Send authentication response"""
    return jsonify({
        'success': False,
        'error': 'Authentication required',
        'message': 'Please provide valid credentials'
    }), 401, {'WWW-Authenticate': 'Basic realm="PiDNS Dashboard"'}

def parse_dnsmasq_leases():
    """
    Parse dnsmasq lease file and return device information
    Format: timestamp mac_address ip_address hostname client_id
    """
    global lease_cache, cache_timestamp

    # Check if cache is still valid
    current_time = time.time()
    if current_time - cache_timestamp < CACHE_DURATION and lease_cache:
        return lease_cache

    devices = []
    lease_file = Path(app.config['DNSMASQ_LEASE_FILE'])

    if not lease_file.exists():
        app.logger.warning(f"Lease file not found: {lease_file}")
        return devices

    try:
        with open(lease_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) < 4:
                    continue

                try:
                    timestamp = int(parts[0])
                    mac_address = parts[1].upper()
                    ip_address = parts[2]
                    hostname = parts[3] if len(parts) > 3 else ""

                    # Calculate connection duration
                    connection_time = datetime.fromtimestamp(timestamp)
                    duration_seconds = int(current_time - timestamp)
                    duration_str = format_duration(duration_seconds)

                    device = {
                        'mac': mac_address,
                        'ip': ip_address,
                        'hostname': hostname,
                        'connection_time': connection_time.isoformat(),
                        'duration_seconds': duration_seconds,
                        'duration': duration_str,
                        'vendor': get_mac_vendor(mac_address)
                    }
                    devices.append(device)

                except (ValueError, IndexError) as e:
                    app.logger.warning(f"Error parsing lease line: {line} - {e}")
                    continue

    except IOError as e:
        app.logger.error(f"Error reading lease file: {e}")

    # Sort by connection time (most recent first)
    devices.sort(key=lambda x: x['connection_time'], reverse=True)

    # Update cache
    lease_cache = devices
    cache_timestamp = current_time

    return devices

def format_duration(seconds):
    """Format duration in seconds to human-readable string"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m {seconds % 60}s"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{days}d {hours}h"

def get_mac_vendor(mac_address):
    """Get vendor name from MAC address"""
    if not mac_address or len(mac_address) < 8:
        return "Unknown"

    # Extract OUI (first 6 characters, removing colons)
    oui = mac_address.replace(':', '')[:6].upper()

    vendor_file = Path(app.config['MAC_VENDORS_FILE'])
    if not vendor_file.exists():
        return "Unknown"

    try:
        with open(vendor_file, 'r') as f:
            vendors = json.load(f)
            return vendors.get(oui, "Unknown")
    except (IOError, json.JSONDecodeError):
        return "Unknown"

@app.route('/')
@requires_auth
def index():
    """Main dashboard page"""
    # Get Pi model information
    pi_model = get_pi_model()
    return render_template('index.html',
                         title=app.config['DASHBOARD_TITLE'],
                         refresh_interval=app.config['REFRESH_INTERVAL'],
                         pi_model=pi_model)

@app.route('/api/devices')
@requires_auth
def get_devices():
    """API endpoint to get connected devices"""
    try:
        devices = parse_dnsmasq_leases()
        return jsonify({
            'success': True,
            'devices': devices,
            'total_devices': len(devices),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        app.logger.error(f"Error getting devices: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'devices': [],
            'total_devices': 0
        }), 500

@app.route('/api/stats')
@requires_auth
def get_stats():
    """API endpoint to get network statistics"""
    try:
        devices = parse_dnsmasq_leases()

        # Calculate statistics
        total_devices = len(devices)
        active_devices = len([d for d in devices if d['duration_seconds'] < 3600])  # Active in last hour

        # Vendor distribution
        vendor_counts = {}
        for device in devices:
            vendor = device['vendor']
            vendor_counts[vendor] = vendor_counts.get(vendor, 0) + 1

        return jsonify({
            'success': True,
            'stats': {
                'total_devices': total_devices,
                'active_devices': active_devices,
                'vendor_distribution': vendor_counts
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        app.logger.error(f"Error getting stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/refresh')
@requires_auth
def refresh_cache():
    """API endpoint to force refresh of lease data"""
    global lease_cache, cache_timestamp
    lease_cache = {}
    cache_timestamp = 0

    try:
        devices = parse_dnsmasq_leases()
        return jsonify({
            'success': True,
            'message': 'Cache refreshed',
            'total_devices': len(devices)
        })
    except Exception as e:
        app.logger.error(f"Error refreshing cache: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

def get_pi_model():
    """Get Raspberry Pi model information"""
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip()
        return model
    except (IOError, OSError):
        return "Unknown"

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
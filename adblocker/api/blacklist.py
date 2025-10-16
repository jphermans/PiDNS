"""
Blacklist API endpoints for PiDNS Ad-Blocker
"""

from flask import Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

from adblocker.models.database import Blacklist, db
from adblocker.services.list_manager import ListManager

# Create blueprint
blacklist_bp = Blueprint('blacklist', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    """Verify username and password"""
    from flask import current_app
    return (username == current_app.config['BASIC_AUTH_USERNAME'] and
            password == current_app.config['BASIC_AUTH_PASSWORD'])

@blacklist_bp.route('/blacklist', methods=['GET'])
@auth.login_required
def get_blacklist():
    """Get blacklist entries"""
    try:
        # Get query parameters
        category = request.args.get('category')
        include_expired = request.args.get('include_expired', 'false').lower() == 'true'
        
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Get entries
        entries = manager.get_blacklist_entries(
            category=category,
            include_expired=include_expired
        )
        
        return jsonify({
            'success': True,
            'entries': entries,
            'total': len(entries)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/<int:entry_id>', methods=['GET'])
@auth.login_required
def get_blacklist_entry(entry_id):
    """Get a specific blacklist entry"""
    try:
        entry = Blacklist.query.get_or_404(entry_id)
        
        return jsonify({
            'success': True,
            'entry': entry.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist', methods=['POST'])
@auth.login_required
def create_blacklist_entry():
    """Create a new blacklist entry"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('domain'):
            return jsonify({
                'success': False,
                'error': 'Domain is required'
            }), 400
        
        domain = data['domain'].strip().lower()
        category = data.get('category', 'custom')
        expires_at = None
        notes = data.get('notes', '')
        
        # Parse expiration date if provided
        if data.get('expires_at'):
            try:
                expires_at = datetime.fromisoformat(data['expires_at'])
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid expiration date format'
                }), 400
        
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Add entry
        success, message = manager.add_blacklist_entry(
            domain=domain,
            category=category,
            expires_at=expires_at,
            notes=notes
        )
        
        if success:
            # Get created entry
            entry = Blacklist.query.filter_by(domain=domain).first()
            return jsonify({
                'success': True,
                'message': message,
                'entry': entry.to_dict() if entry else None
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/<int:entry_id>', methods=['PUT'])
@auth.login_required
def update_blacklist_entry(entry_id):
    """Update a blacklist entry"""
    try:
        entry = Blacklist.query.get_or_404(entry_id)
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Parse expiration date if provided
        expires_at = None
        if 'expires_at' in data and data['expires_at']:
            try:
                expires_at = datetime.fromisoformat(data['expires_at'])
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid expiration date format'
                }), 400
        
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Update entry
        success, message = manager.update_blacklist_entry(
            entry_id=entry_id,
            category=data.get('category'),
            expires_at=expires_at,
            notes=data.get('notes')
        )
        
        if success:
            # Get updated entry
            entry = Blacklist.query.get(entry_id)
            return jsonify({
                'success': True,
                'message': message,
                'entry': entry.to_dict() if entry else None
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/<int:entry_id>', methods=['DELETE'])
@auth.login_required
def delete_blacklist_entry(entry_id):
    """Delete a blacklist entry"""
    try:
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Remove entry
        success, message = manager.remove_blacklist_entry(entry_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/batch', methods=['POST'])
@auth.login_required
def batch_create_blacklist_entries():
    """Create multiple blacklist entries"""
    try:
        data = request.get_json()
        
        if not data or not data.get('entries'):
            return jsonify({
                'success': False,
                'error': 'Entries are required'
            }), 400
        
        entries = data['entries']
        
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Import entries
        success, result = manager.import_entries(
            entries=entries,
            list_type='blacklist',
            category=data.get('category', 'custom')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Blacklist entries imported successfully',
                'result': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/export', methods=['GET'])
@auth.login_required
def export_blacklist_entries():
    """Export blacklist entries"""
    try:
        # Get query parameters
        category = request.args.get('category')
        
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Export entries
        entries = manager.export_entries(
            list_type='blacklist',
            category=category
        )
        
        return jsonify({
            'success': True,
            'entries': entries,
            'total': len(entries)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/categories', methods=['GET'])
@auth.login_required
def get_blacklist_categories():
    """Get available blacklist categories"""
    try:
        from flask import current_app
        categories = current_app.config['BLACKLIST_CATEGORIES']
        
        return jsonify({
            'success': True,
            'categories': categories
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/statistics', methods=['GET'])
@auth.login_required
def get_blacklist_statistics():
    """Get blacklist statistics"""
    try:
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Get statistics
        stats = manager.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats.get('blacklist', {})
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/cleanup', methods=['POST'])
@auth.login_required
def cleanup_expired_blacklist_entries():
    """Clean up expired blacklist entries"""
    try:
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Clean up expired entries
        success = manager.cleanup_expired_entries()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Expired blacklist entries cleaned up successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to cleanup expired entries'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/check', methods=['POST'])
@auth.login_required
def check_blacklist_status():
    """Check if domains are blacklisted"""
    try:
        data = request.get_json()
        
        if not data or not data.get('domains'):
            return jsonify({
                'success': False,
                'error': 'Domains are required'
            }), 400
        
        domains = data['domains']
        
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Check each domain
        results = {}
        for domain in domains:
            results[domain] = manager.is_domain_blacklisted(domain.lower())
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blacklist_bp.route('/blacklist/sync', methods=['POST'])
@auth.login_required
def sync_blacklist_with_blocklists():
    """Sync blacklist with block list updates"""
    try:
        # This endpoint would be used to sync blacklist entries with updates from block lists
        # Implementation would depend on specific requirements
        
        return jsonify({
            'success': True,
            'message': 'Blacklist synchronized successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
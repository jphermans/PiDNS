"""
Whitelist API endpoints for PiDNS Ad-Blocker
"""

from flask import Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

from adblocker.models.database import Whitelist, db
from adblocker.services.list_manager import ListManager

# Create blueprint
whitelist_bp = Blueprint('whitelist', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    """Verify username and password"""
    from flask import current_app
    return (username == current_app.config['BASIC_AUTH_USERNAME'] and
            password == current_app.config['BASIC_AUTH_PASSWORD'])

@whitelist_bp.route('/whitelist', methods=['GET'])
@auth.login_required
def get_whitelist():
    """Get whitelist entries"""
    try:
        # Get query parameters
        category = request.args.get('category')
        include_expired = request.args.get('include_expired', 'false').lower() == 'true'
        
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Get entries
        entries = manager.get_whitelist_entries(
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

@whitelist_bp.route('/whitelist/<int:entry_id>', methods=['GET'])
@auth.login_required
def get_whitelist_entry(entry_id):
    """Get a specific whitelist entry"""
    try:
        entry = Whitelist.query.get_or_404(entry_id)
        
        return jsonify({
            'success': True,
            'entry': entry.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@whitelist_bp.route('/whitelist', methods=['POST'])
@auth.login_required
def create_whitelist_entry():
    """Create a new whitelist entry"""
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
        success, message = manager.add_whitelist_entry(
            domain=domain,
            category=category,
            expires_at=expires_at,
            notes=notes
        )
        
        if success:
            # Get created entry
            entry = Whitelist.query.filter_by(domain=domain).first()
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

@whitelist_bp.route('/whitelist/<int:entry_id>', methods=['PUT'])
@auth.login_required
def update_whitelist_entry(entry_id):
    """Update a whitelist entry"""
    try:
        entry = Whitelist.query.get_or_404(entry_id)
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
        success, message = manager.update_whitelist_entry(
            entry_id=entry_id,
            category=data.get('category'),
            expires_at=expires_at,
            notes=data.get('notes')
        )
        
        if success:
            # Get updated entry
            entry = Whitelist.query.get(entry_id)
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

@whitelist_bp.route('/whitelist/<int:entry_id>', methods=['DELETE'])
@auth.login_required
def delete_whitelist_entry(entry_id):
    """Delete a whitelist entry"""
    try:
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Remove entry
        success, message = manager.remove_whitelist_entry(entry_id)
        
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

@whitelist_bp.route('/whitelist/batch', methods=['POST'])
@auth.login_required
def batch_create_whitelist_entries():
    """Create multiple whitelist entries"""
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
            list_type='whitelist',
            category=data.get('category', 'custom')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Whitelist entries imported successfully',
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

@whitelist_bp.route('/whitelist/export', methods=['GET'])
@auth.login_required
def export_whitelist_entries():
    """Export whitelist entries"""
    try:
        # Get query parameters
        category = request.args.get('category')
        
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Export entries
        entries = manager.export_entries(
            list_type='whitelist',
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

@whitelist_bp.route('/whitelist/categories', methods=['GET'])
@auth.login_required
def get_whitelist_categories():
    """Get available whitelist categories"""
    try:
        from flask import current_app
        categories = current_app.config['WHITELIST_CATEGORIES']
        
        return jsonify({
            'success': True,
            'categories': categories
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@whitelist_bp.route('/whitelist/statistics', methods=['GET'])
@auth.login_required
def get_whitelist_statistics():
    """Get whitelist statistics"""
    try:
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Get statistics
        stats = manager.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats.get('whitelist', {})
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@whitelist_bp.route('/whitelist/cleanup', methods=['POST'])
@auth.login_required
def cleanup_expired_whitelist_entries():
    """Clean up expired whitelist entries"""
    try:
        # Create list manager
        manager = ListManager(request.current_app.config)
        
        # Clean up expired entries
        success = manager.cleanup_expired_entries()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Expired whitelist entries cleaned up successfully'
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

@whitelist_bp.route('/whitelist/check', methods=['POST'])
@auth.login_required
def check_whitelist_status():
    """Check if domains are whitelisted"""
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
            results[domain] = manager.is_domain_whitelisted(domain.lower())
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
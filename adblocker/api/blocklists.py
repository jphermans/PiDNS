"""
Block list API endpoints for PiDNS Ad-Blocker
"""

from flask import Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth

from adblocker.models.database import BlockList, db
from adblocker.services.blocklist_manager import BlockListManager

# Create blueprint
blocklist_bp = Blueprint('blocklists', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    """Verify username and password"""
    from flask import current_app
    return (username == current_app.config['BASIC_AUTH_USERNAME'] and
            password == current_app.config['BASIC_AUTH_PASSWORD'])

@blocklist_bp.route('/blocklists', methods=['GET'])
@auth.login_required
def get_blocklists():
    """Get all block lists"""
    try:
        # Get query parameters
        category = request.args.get('category')
        enabled = request.args.get('enabled')
        
        # Build query
        query = BlockList.query
        
        if category:
            query = query.filter_by(category=category)
        
        if enabled is not None:
            enabled_bool = enabled.lower() == 'true'
            query = query.filter_by(enabled=enabled_bool)
        
        blocklists = query.all()
        
        return jsonify({
            'success': True,
            'blocklists': [blocklist.to_dict() for blocklist in blocklists],
            'total': len(blocklists)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blocklist_bp.route('/blocklists/<int:blocklist_id>', methods=['GET'])
@auth.login_required
def get_blocklist(blocklist_id):
    """Get a specific block list"""
    try:
        blocklist = BlockList.query.get_or_404(blocklist_id)
        
        # Get additional status information
        manager = BlockListManager(request.current_app.config)
        status = manager.get_blocklist_status(blocklist_id)
        
        return jsonify({
            'success': True,
            'blocklist': blocklist.to_dict(),
            'status': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blocklist_bp.route('/blocklists', methods=['POST'])
@auth.login_required
def create_blocklist():
    """Create a new block list"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name') or not data.get('url'):
            return jsonify({
                'success': False,
                'error': 'Name and URL are required'
            }), 400
        
        name = data['name']
        url = data['url']
        category = data.get('category', 'custom')
        description = data.get('description', '')
        enabled = data.get('enabled', True)
        
        # Create block list manager
        manager = BlockListManager(request.current_app.config)
        
        # Add block list
        success, message = manager.add_custom_blocklist(
            name=name,
            url=url,
            category=category,
            description=description
        )
        
        if success:
            # Get created block list
            blocklist = BlockList.query.filter_by(url=url).first()
            return jsonify({
                'success': True,
                'message': message,
                'blocklist': blocklist.to_dict() if blocklist else None
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

@blocklist_bp.route('/blocklists/<int:blocklist_id>', methods=['PUT'])
@auth.login_required
def update_blocklist(blocklist_id):
    """Update a block list"""
    try:
        blocklist = BlockList.query.get_or_404(blocklist_id)
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Update fields
        if 'name' in data:
            blocklist.name = data['name']
        
        if 'category' in data:
            blocklist.category = data['category']
        
        if 'description' in data:
            blocklist.description = data['description']
        
        if 'enabled' in data:
            blocklist.enabled = data['enabled']
        
        blocklist.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Update configuration
        manager = BlockListManager(request.current_app.config)
        manager.generate_combined_config()
        manager.dnsmasq_manager.reload_dnsmasq()
        
        return jsonify({
            'success': True,
            'message': 'Block list updated successfully',
            'blocklist': blocklist.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blocklist_bp.route('/blocklists/<int:blocklist_id>', methods=['DELETE'])
@auth.login_required
def delete_blocklist(blocklist_id):
    """Delete a block list"""
    try:
        manager = BlockListManager(request.current_app.config)
        success, message = manager.remove_blocklist(blocklist_id)
        
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

@blocklist_bp.route('/blocklists/<int:blocklist_id>/toggle', methods=['POST'])
@auth.login_required
def toggle_blocklist(blocklist_id):
    """Toggle block list enabled status"""
    try:
        manager = BlockListManager(request.current_app.config)
        success, message = manager.toggle_blocklist(blocklist_id)
        
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

@blocklist_bp.route('/blocklists/<int:blocklist_id>/update', methods=['POST'])
@auth.login_required
def update_blocklist_content(blocklist_id):
    """Update block list content from URL"""
    try:
        manager = BlockListManager(request.current_app.config)
        success, message = manager.update_blocklist(blocklist_id)
        
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

@blocklist_bp.route('/blocklists/update-all', methods=['POST'])
@auth.login_required
def update_all_blocklists():
    """Update all enabled block lists"""
    try:
        manager = BlockListManager(request.current_app.config)
        updated_count = manager.update_all_blocklists()
        
        return jsonify({
            'success': True,
            'message': f'Updated {updated_count} block lists',
            'updated_count': updated_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blocklist_bp.route('/blocklists/categories', methods=['GET'])
@auth.login_required
def get_blocklist_categories():
    """Get available block list categories"""
    try:
        from flask import current_app
        categories = current_app.config['BLOCKLIST_CATEGORIES']
        
        return jsonify({
            'success': True,
            'categories': categories
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blocklist_bp.route('/blocklists/statistics', methods=['GET'])
@auth.login_required
def get_blocklist_statistics():
    """Get block list statistics"""
    try:
        manager = BlockListManager(request.current_app.config)
        stats = manager.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blocklist_bp.route('/blocklists/predefined', methods=['GET'])
@auth.login_required
def get_predefined_blocklists():
    """Get predefined block lists"""
    try:
        from flask import current_app
        predefined = current_app.config['PREDEFINED_BLOCKLISTS']
        
        # Check which ones are already in the database
        result = []
        for item in predefined:
            existing = BlockList.query.filter_by(url=item['url']).first()
            
            result.append({
                'name': item['name'],
                'url': item['url'],
                'category': item['category'],
                'enabled': item['enabled'],
                'description': f"Predefined {item['category']} block list",
                'in_database': existing is not None,
                'database_id': existing.id if existing else None,
                'database_enabled': existing.enabled if existing else None,
                'last_updated': existing.last_updated.isoformat() if existing and existing.last_updated else None,
                'entry_count': existing.entry_count if existing else 0
            })
        
        return jsonify({
            'success': True,
            'predefined_blocklists': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@blocklist_bp.route('/blocklists/predefined', methods=['POST'])
@auth.login_required
def add_predefined_blocklist():
    """Add a predefined block list to the database"""
    try:
        data = request.get_json()
        
        if not data or not data.get('url'):
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        url = data['url']
        
        # Find predefined block list
        from flask import current_app
        predefined = current_app.config['PREDEFINED_BLOCKLISTS']
        predefined_item = None
        
        for item in predefined:
            if item['url'] == url:
                predefined_item = item
                break
        
        if not predefined_item:
            return jsonify({
                'success': False,
                'error': 'Predefined block list not found'
            }), 404
        
        # Check if already exists
        existing = BlockList.query.filter_by(url=url).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'Block list already exists'
            }), 400
        
        # Add to database
        blocklist = BlockList(
            name=predefined_item['name'],
            url=predefined_item['url'],
            category=predefined_item['category'],
            enabled=predefined_item['enabled'],
            description=f"Predefined {predefined_item['category']} block list"
        )
        
        db.session.add(blocklist)
        db.session.commit()
        
        # Download content
        manager = BlockListManager(request.current_app.config)
        manager.download_blocklist(blocklist.id)
        manager.generate_combined_config()
        manager.dnsmasq_manager.reload_dnsmasq()
        
        return jsonify({
            'success': True,
            'message': 'Predefined block list added successfully',
            'blocklist': blocklist.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
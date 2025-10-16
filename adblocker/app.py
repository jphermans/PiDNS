#!/usr/bin/env python3
"""
PiDNS Ad-Blocker Flask Application
A web interface for managing DNS ad-blocking on Raspberry Pi
"""

import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from functools import wraps
from flask_httpauth import HTTPBasicAuth

from config.flask_config import get_config
from models.database import init_database, db, clean_expired_entries, clean_old_stats

# Initialize Flask app
app = Flask(__name__)
config_class = get_config()
app.config.from_object(config_class)

# Initialize authentication
auth = HTTPBasicAuth()

# Initialize database
init_database(app)

# Authentication verification
@auth.verify_password
def verify_password(username, password):
    """Verify username and password"""
    return (username == app.config['BASIC_AUTH_USERNAME'] and
            password == app.config['BASIC_AUTH_PASSWORD'])

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.errorhandler(401)
def unauthorized():
    return jsonify({
        'success': False,
        'error': 'Authentication required',
        'message': 'Please provide valid credentials'
    }), 401

# Template context processors
@app.context_processor
def inject_config():
    """Inject configuration variables into templates"""
    return {
        'title': app.config['ADBLOCKER_TITLE'],
        'refresh_interval': app.config['REFRESH_INTERVAL']
    }

# Route handlers
@app.route('/')
@auth.login_required
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/blocklists')
@auth.login_required
def blocklists_page():
    """Block lists management page"""
    return render_template('blocklists.html')

@app.route('/whitelist')
@auth.login_required
def whitelist_page():
    """Whitelist management page"""
    return render_template('whitelist.html')

@app.route('/blacklist')
@auth.login_required
def blacklist_page():
    """Blacklist management page"""
    return render_template('blacklist.html')

@app.route('/statistics')
@auth.login_required
def statistics_page():
    """Statistics and logs page"""
    return render_template('statistics.html')

# API endpoints will be imported from api modules
from api.blocklists import blocklist_bp
from api.whitelist import whitelist_bp
from api.blacklist import blacklist_bp
from api.statistics import stats_bp

# Register blueprints
app.register_blueprint(blocklist_bp, url_prefix='/api')
app.register_blueprint(whitelist_bp, url_prefix='/api')
app.register_blueprint(blacklist_bp, url_prefix='/api')
app.register_blueprint(stats_bp, url_prefix='/api')

# Background tasks
def setup_background_tasks():
    """Setup background tasks for maintenance"""
    from services.blocklist_manager import schedule_blocklist_updates
    from services.stats_processor import schedule_stats_processing
    
    # Schedule block list updates
    schedule_blocklist_updates(app)
    
    # Schedule stats processing
    schedule_stats_processing(app)
    
    # Schedule cleanup tasks
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    
    # Clean expired entries daily
    scheduler.add_job(
        func=clean_expired_entries,
        trigger='cron',
        hour=2,
        minute=0,
        id='clean_expired_entries'
    )
    
    # Clean old stats weekly
    scheduler.add_job(
        func=lambda: clean_old_stats(app.config['STATS_RETENTION_DAYS']),
        trigger='cron',
        day_of_week=0,
        hour=3,
        minute=0,
        id='clean_old_stats'
    )
    
    scheduler.start()

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Setup background tasks
    setup_background_tasks()
    
    # Run Flask application
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
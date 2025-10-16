"""
Authentication service for PiDNS Ad-Blocker
Handles user authentication and authorization
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from flask_httpauth import HTTPBasicAuth
import jwt

# Initialize auth
auth = HTTPBasicAuth()


class AuthService:
    """
    Handles user authentication and authorization
    """
    
    def __init__(self, config):
        self.config = config
        self.jwt_secret = config.get('JWT_SECRET', self._generate_secret())
        self.jwt_expiration = config.get('JWT_EXPIRATION', 24)  # hours
        self.session_timeout = config.get('SESSION_TIMEOUT', 3600)  # seconds
        
        # Default admin user
        self.admin_username = config.get('ADMIN_USERNAME', 'admin')
        self.admin_password = config.get('ADMIN_PASSWORD', 'password')
        
    def _generate_secret(self):
        """Generate a random secret key"""
        return secrets.token_hex(32)
        
    def _hash_password(self, password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def verify_password(self, username, password):
        """Verify username and password"""
        if username == self.admin_username:
            return self._hash_password(password) == self._hash_password(self.admin_password)
        return False
        
    def generate_token(self, username):
        """Generate a JWT token for the user"""
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=self.jwt_expiration),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        
    def verify_token(self, token):
        """Verify a JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload['username']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
            
    def change_password(self, current_password, new_password):
        """Change the admin password"""
        if self.verify_password(self.admin_username, current_password):
            self.admin_password = new_password
            return True
        return False
        
    def is_authenticated(self):
        """Check if the current request is authenticated"""
        # Check for basic auth
        if request.authorization:
            return self.verify_password(
                request.authorization.username,
                request.authorization.password
            )
            
        # Check for JWT token in header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            username = self.verify_token(token)
            if username:
                return True
                
        # Check for JWT token in cookie
        token = request.cookies.get('auth_token')
        if token:
            username = self.verify_token(token)
            if username:
                return True
                
        return False


# Initialize auth service
auth_service = None


def init_auth_service(config):
    """Initialize the authentication service"""
    global auth_service
    auth_service = AuthService(config)
    return auth_service


def get_auth_service():
    """Get the authentication service"""
    return auth_service


# Basic auth verification function
@auth.verify_password
def verify_password(username, password):
    """Verify username and password for basic auth"""
    if auth_service:
        return auth_service.verify_password(username, password)
    return False


# Decorator for requiring authentication
def requires_auth(f):
    """Decorator to require authentication for a route"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not auth_service or not auth_service.is_authenticated():
            response = jsonify({
                'success': False,
                'error': 'Authentication required',
                'message': 'Please provide valid credentials'
            })
            response.status_code = 401
            response.headers['WWW-Authenticate'] = 'Basic realm="PiDNS Ad-Blocker"'
            return response
        return f(*args, **kwargs)
    return decorated


# Decorator for requiring admin privileges
def requires_admin(f):
    """Decorator to require admin privileges for a route"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not auth_service or not auth_service.is_authenticated():
            response = jsonify({
                'success': False,
                'error': 'Authentication required',
                'message': 'Please provide valid credentials'
            })
            response.status_code = 401
            response.headers['WWW-Authenticate'] = 'Basic realm="PiDNS Ad-Blocker"'
            return response
            
        # All authenticated users are admin in this simple implementation
        return f(*args, **kwargs)
    return decorated


# Authentication routes
def setup_auth_routes(app):
    """Set up authentication routes"""
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Login with username and password"""
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Username and password required'
            }), 400
            
        username = data['username']
        password = data['password']
        
        if auth_service.verify_password(username, password):
            token = auth_service.generate_token(username)
            
            response = jsonify({
                'success': True,
                'message': 'Login successful',
                'token': token,
                'user': {
                    'username': username,
                    'role': 'admin'
                }
            })
            
            # Set cookie
            response.set_cookie(
                'auth_token',
                token,
                httponly=True,
                secure=app.config.get('FORCE_HTTPS', False),
                samesite='Lax',
                max_age=auth_service.jwt_expiration * 3600
            )
            
            return response
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
            
    @app.route('/api/auth/logout', methods=['POST'])
    def logout():
        """Logout and clear the token"""
        response = jsonify({
            'success': True,
            'message': 'Logout successful'
        })
        
        # Clear cookie
        response.set_cookie(
            'auth_token',
            '',
            httponly=True,
            secure=app.config.get('FORCE_HTTPS', False),
            samesite='Lax',
            expires=0
        )
        
        return response
        
    @app.route('/api/auth/verify', methods=['POST'])
    def verify_token():
        """Verify a JWT token"""
        data = request.get_json()
        
        if not data or not data.get('token'):
            return jsonify({
                'success': False,
                'error': 'Token required'
            }), 400
            
        token = data['token']
        username = auth_service.verify_token(token)
        
        if username:
            return jsonify({
                'success': True,
                'message': 'Token is valid',
                'user': {
                    'username': username,
                    'role': 'admin'
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
            
    @app.route('/api/auth/change-password', methods=['POST'])
    @requires_auth
    def change_password():
        """Change the admin password"""
        data = request.get_json()
        
        if not data or not data.get('current_password') or not data.get('new_password'):
            return jsonify({
                'success': False,
                'error': 'Current password and new password required'
            }), 400
            
        current_password = data['current_password']
        new_password = data['new_password']
        
        if len(new_password) < 8:
            return jsonify({
                'success': False,
                'error': 'New password must be at least 8 characters long'
            }), 400
            
        if auth_service.change_password(current_password, new_password):
            return jsonify({
                'success': True,
                'message': 'Password changed successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            }), 401
            
    @app.route('/api/auth/status', methods=['GET'])
    def auth_status():
        """Get authentication status"""
        if auth_service and auth_service.is_authenticated():
            return jsonify({
                'success': True,
                'authenticated': True,
                'user': {
                    'username': auth_service.admin_username,
                    'role': 'admin'
                }
            })
        else:
            return jsonify({
                'success': True,
                'authenticated': False
            })
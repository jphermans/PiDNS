"""
Database models for PiDNS Ad-Blocker
"""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class BlockList(db.Model):
    """Block list model"""
    __tablename__ = 'block_lists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500))
    category = db.Column(db.String(50), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.DateTime)
    entry_count = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with query stats
    query_stats = db.relationship('QueryStat', backref='block_list', lazy='dynamic')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'category': self.category,
            'enabled': self.enabled,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'entry_count': self.entry_count,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<BlockList {self.name}>'

class Whitelist(db.Model):
    """Whitelist model"""
    __tablename__ = 'whitelist'
    
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(50), default='custom')
    expires_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'domain': self.domain,
            'category': self.category,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_expired(self):
        """Check if whitelist entry has expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f'<Whitelist {self.domain}>'

class Blacklist(db.Model):
    """Blacklist model"""
    __tablename__ = 'blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(50), default='custom')
    expires_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'domain': self.domain,
            'category': self.category,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_expired(self):
        """Check if blacklist entry has expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f'<Blacklist {self.domain}>'

class QueryStat(db.Model):
    """Query statistics model"""
    __tablename__ = 'query_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    client_ip = db.Column(db.String(45))  # IPv6 compatible
    query_type = db.Column(db.String(10), default='A')
    blocked = db.Column(db.Boolean, default=False)
    block_list_id = db.Column(db.Integer, db.ForeignKey('block_lists.id'))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'domain': self.domain,
            'client_ip': self.client_ip,
            'query_type': self.query_type,
            'blocked': self.blocked,
            'block_list_id': self.block_list_id,
            'block_list_name': self.block_list.name if self.block_list else None
        }
    
    def __repr__(self):
        return f'<QueryStat {self.domain}>'

class SummaryStat(db.Model):
    """Summary statistics model"""
    __tablename__ = 'summary_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    total_queries = db.Column(db.Integer, default=0)
    blocked_queries = db.Column(db.Integer, default=0)
    unique_clients = db.Column(db.Integer, default=0)
    top_blocked_domains = db.Column(db.Text)  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_top_blocked_domains(self):
        """Get top blocked domains as list"""
        if self.top_blocked_domains:
            try:
                return json.loads(self.top_blocked_domains)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_top_blocked_domains(self, domains):
        """Set top blocked domains from list"""
        if domains:
            self.top_blocked_domains = json.dumps(domains)
        else:
            self.top_blocked_domains = None
    
    def get_block_percentage(self):
        """Calculate block percentage"""
        if self.total_queries == 0:
            return 0
        return round((self.blocked_queries / self.total_queries) * 100, 2)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'total_queries': self.total_queries,
            'blocked_queries': self.blocked_queries,
            'unique_clients': self.unique_clients,
            'top_blocked_domains': self.get_top_blocked_domains(),
            'block_percentage': self.get_block_percentage(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<SummaryStat {self.date}>'

def init_database(app):
    """Initialize database with app"""
    db.init_app(app)
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Add predefined block lists if they don't exist
        from adblocker.config.flask_config import get_config
        config = get_config()
        
        for blocklist_data in config.PREDEFINED_BLOCKLISTS:
            existing = BlockList.query.filter_by(url=blocklist_data['url']).first()
            if not existing:
                blocklist = BlockList(
                    name=blocklist_data['name'],
                    url=blocklist_data['url'],
                    category=blocklist_data['category'],
                    enabled=blocklist_data['enabled'],
                    description=f"Predefined {blocklist_data['category']} block list"
                )
                db.session.add(blocklist)
        
        db.session.commit()

def clean_expired_entries():
    """Clean up expired whitelist and blacklist entries"""
    current_time = datetime.utcnow()
    
    # Clean expired whitelist entries
    Whitelist.query.filter(
        Whitelist.expires_at.isnot(None),
        Whitelist.expires_at < current_time
    ).delete()
    
    # Clean expired blacklist entries
    Blacklist.query.filter(
        Blacklist.expires_at.isnot(None),
        Blacklist.expires_at < current_time
    ).delete()
    
    db.session.commit()

def clean_old_stats(days_to_keep=90):
    """Clean up old statistics entries"""
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
    
    # Clean old query stats
    QueryStat.query.filter(QueryStat.timestamp < cutoff_date).delete()
    
    # Clean old summary stats
    cutoff_summary_date = date.today() - timedelta(days=days_to_keep)
    SummaryStat.query.filter(SummaryStat.date < cutoff_summary_date).delete()
    
    db.session.commit()
"""
Statistics API endpoints for PiDNS Ad-Blocker
"""

from flask import Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timedelta, date
from sqlalchemy import func, desc

from adblocker.models.database import QueryStat, SummaryStat, BlockList, db
from adblocker.services.dnsmasq_manager import DnsmasqManager

# Create blueprint
stats_bp = Blueprint('stats', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    """Verify username and password"""
    from flask import current_app
    return (username == current_app.config['BASIC_AUTH_USERNAME'] and
            password == current_app.config['BASIC_AUTH_PASSWORD'])

@stats_bp.route('/statistics/overview', methods=['GET'])
@auth.login_required
def get_overview_statistics():
    """Get overview statistics"""
    try:
        # Get time range
        days = request.args.get('days', 7, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get query statistics
        total_queries = QueryStat.query.filter(
            QueryStat.timestamp >= start_date
        ).count()
        
        blocked_queries = QueryStat.query.filter(
            QueryStat.timestamp >= start_date,
            QueryStat.blocked == True
        ).count()
        
        # Calculate block percentage
        block_percentage = 0
        if total_queries > 0:
            block_percentage = round((blocked_queries / total_queries) * 100, 2)
        
        # Get unique domains
        unique_domains = db.session.query(
            func.count(func.distinct(QueryStat.domain))
        ).filter(
            QueryStat.timestamp >= start_date
        ).scalar()
        
        # Get unique clients
        unique_clients = db.session.query(
            func.count(func.distinct(QueryStat.client_ip))
        ).filter(
            QueryStat.timestamp >= start_date
        ).scalar()
        
        # Get service status
        dnsmasq_manager = DnsmasqManager(request.current_app.config)
        dnsmasq_status = dnsmasq_manager.get_dnsmasq_status()
        
        # Get active block lists count
        active_blocklists = BlockList.query.filter_by(enabled=True).count()
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_queries': total_queries,
                'blocked_queries': blocked_queries,
                'block_percentage': block_percentage,
                'unique_domains': unique_domains,
                'unique_clients': unique_clients,
                'dnsmasq_status': dnsmasq_status,
                'active_blocklists': active_blocklists,
                'period_days': days
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@stats_bp.route('/statistics/summary', methods=['GET'])
@auth.login_required
def get_summary_statistics():
    """Get summary statistics by date"""
    try:
        # Get time range
        days = request.args.get('days', 30, type=int)
        start_date = date.today() - timedelta(days=days)
        
        # Get summary stats
        summary_stats = SummaryStat.query.filter(
            SummaryStat.date >= start_date
        ).order_by(desc(SummaryStat.date)).all()
        
        return jsonify({
            'success': True,
            'summary': [stat.to_dict() for stat in summary_stats]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@stats_bp.route('/statistics/recent-queries', methods=['GET'])
@auth.login_required
def get_recent_queries():
    """Get recent DNS queries"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        blocked_only = request.args.get('blocked_only', 'false').lower() == 'true'
        
        # Build query
        query = QueryStat.query
        
        if blocked_only:
            query = query.filter(QueryStat.blocked == True)
        
        # Get queries
        queries = query.order_by(desc(QueryStat.timestamp)).offset(offset).limit(limit).all()
        
        # Get total count
        total = query.count()
        
        return jsonify({
            'success': True,
            'queries': [query.to_dict() for query in queries],
            'total': total,
            'offset': offset,
            'limit': limit
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@stats_bp.route('/statistics/top-domains', methods=['GET'])
@auth.login_required
def get_top_domains():
    """Get top queried or blocked domains"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 20, type=int)
        blocked_only = request.args.get('blocked_only', 'false').lower() == 'true'
        days = request.args.get('days', 7, type=int)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Build query
        query = db.session.query(
            QueryStat.domain,
            func.count(QueryStat.id).label('count')
        ).filter(
            QueryStat.timestamp >= start_date
        )
        
        if blocked_only:
            query = query.filter(QueryStat.blocked == True)
        
        # Get results
        results = query.group_by(
            QueryStat.domain
        ).order_by(desc('count')).limit(limit).all()
        
        return jsonify({
            'success': True,
            'domains': [
                {
                    'domain': result.domain,
                    'count': result.count
                }
                for result in results
            ],
            'blocked_only': blocked_only,
            'period_days': days
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@stats_bp.route('/statistics/top-clients', methods=['GET'])
@auth.login_required
def get_top_clients():
    """Get top query sources by client IP"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 20, type=int)
        days = request.args.get('days', 7, type=int)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get results
        results = db.session.query(
            QueryStat.client_ip,
            func.count(QueryStat.id).label('count')
        ).filter(
            QueryStat.timestamp >= start_date
        ).group_by(
            QueryStat.client_ip
        ).order_by(desc('count')).limit(limit).all()
        
        return jsonify({
            'success': True,
            'clients': [
                {
                    'client_ip': result.client_ip,
                    'count': result.count
                }
                for result in results
            ],
            'period_days': days
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@stats_bp.route('/statistics/blocklist-performance', methods=['GET'])
@auth.login_required
def get_blocklist_performance():
    """Get block list performance statistics"""
    try:
        # Get query parameters
        days = request.args.get('days', 7, type=int)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get block list performance
        results = db.session.query(
            BlockList.name,
            BlockList.category,
            func.count(QueryStat.id).label('blocked_count')
        ).join(
            QueryStat, BlockList.id == QueryStat.block_list_id
        ).filter(
            QueryStat.timestamp >= start_date,
            QueryStat.blocked == True
        ).group_by(
            BlockList.id
        ).order_by(desc('blocked_count')).all()
        
        return jsonify({
            'success': True,
            'blocklists': [
                {
                    'name': result.name,
                    'category': result.category,
                    'blocked_count': result.blocked_count
                }
                for result in results
            ],
            'period_days': days
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@stats_bp.route('/statistics/hourly', methods=['GET'])
@auth.login_required
def get_hourly_statistics():
    """Get hourly statistics for the last 24 hours"""
    try:
        # Get query parameters
        hours = request.args.get('hours', 24, type=int)
        
        start_date = datetime.utcnow() - timedelta(hours=hours)
        
        # Get hourly statistics
        results = db.session.query(
            func.date_trunc('hour', QueryStat.timestamp).label('hour'),
            func.count(QueryStat.id).label('total_queries'),
            func.sum(func.case([(QueryStat.blocked == True, 1)], else_=0)).label('blocked_queries')
        ).filter(
            QueryStat.timestamp >= start_date
        ).group_by(
            func.date_trunc('hour', QueryStat.timestamp)
        ).order_by('hour').all()
        
        return jsonify({
            'success': True,
            'hourly_stats': [
                {
                    'hour': result.hour.isoformat(),
                    'total_queries': result.total_queries,
                    'blocked_queries': result.blocked_queries or 0,
                    'block_percentage': round((result.blocked_queries or 0) / result.total_queries * 100, 2) if result.total_queries > 0 else 0
                }
                for result in results
            ],
            'period_hours': hours
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@stats_bp.route('/statistics/export', methods=['GET'])
@auth.login_required
def export_statistics():
    """Export statistics data"""
    try:
        # Get query parameters
        format_type = request.args.get('format', 'json')
        days = request.args.get('days', 30, type=int)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get query statistics
        queries = QueryStat.query.filter(
            QueryStat.timestamp >= start_date
        ).order_by(desc(QueryStat.timestamp)).all()
        
        # Convert to list of dictionaries
        data = [query.to_dict() for query in queries]
        
        if format_type == 'csv':
            # Convert to CSV
            import csv
            import io
            
            output = io.StringIO()
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            return jsonify({
                'success': True,
                'data': output.getvalue(),
                'format': 'csv'
            })
        else:
            # Return JSON
            return jsonify({
                'success': True,
                'data': data,
                'format': 'json'
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@stats_bp.route('/statistics/clear', methods=['POST'])
@auth.login_required
def clear_statistics():
    """Clear statistics data"""
    try:
        # Get query parameters
        days = request.args.get('days', None, type=int)
        
        if days:
            # Clear data older than specified days
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Delete query stats
            deleted_queries = QueryStat.query.filter(
                QueryStat.timestamp < cutoff_date
            ).delete()
            
            # Delete summary stats
            cutoff_summary_date = date.today() - timedelta(days=days)
            deleted_summary = SummaryStat.query.filter(
                SummaryStat.date < cutoff_summary_date
            ).delete()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Cleared statistics older than {days} days',
                'deleted_queries': deleted_queries,
                'deleted_summary': deleted_summary
            })
        else:
            # Clear all statistics
            deleted_queries = QueryStat.query.delete()
            deleted_summary = SummaryStat.query.delete()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Cleared all statistics',
                'deleted_queries': deleted_queries,
                'deleted_summary': deleted_summary
            })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@stats_bp.route('/statistics/health', methods=['GET'])
@auth.login_required
def get_statistics_health():
    """Get statistics health information"""
    try:
        # Get database size information
        query_count = QueryStat.query.count()
        summary_count = SummaryStat.query.count()
        
        # Get oldest and newest records
        oldest_query = db.session.query(func.min(QueryStat.timestamp)).scalar()
        newest_query = db.session.query(func.max(QueryStat.timestamp)).scalar()
        
        # Get storage information
        from flask import current_app
        db_path = current_app.config['DATABASE_PATH']
        db_size = db_path.stat().st_size if db_path.exists() else 0
        
        return jsonify({
            'success': True,
            'health': {
                'query_count': query_count,
                'summary_count': summary_count,
                'oldest_query': oldest_query.isoformat() if oldest_query else None,
                'newest_query': newest_query.isoformat() if newest_query else None,
                'database_size_bytes': db_size,
                'database_size_mb': round(db_size / (1024 * 1024), 2)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
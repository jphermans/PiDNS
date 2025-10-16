"""
Query logging service for PiDNS Ad-Blocker
Handles logging and processing of DNS queries
"""

import re
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread, Event
from queue import Queue, Empty

from adblocker.models.database import QueryStat, SummaryStat, db
from adblocker.models.database import BlockList, Whitelist, Blacklist


class QueryLogger:
    """
    Handles logging and processing of DNS queries
    """
    
    def __init__(self, config):
        self.config = config
        self.log_file = Path(config['DNSMASQ_LOG_FILE'])
        self.processed_log_file = Path(config['PROCESSED_LOG_FILE'])
        self.batch_size = config.get('QUERY_LOG_BATCH_SIZE', 100)
        self.flush_interval = config.get('QUERY_LOG_FLUSH_INTERVAL', 60)  # seconds
        
        self.running = False
        self.thread = None
        self.stop_event = Event()
        self.query_queue = Queue()
        self.last_position = 0
        
        # Regular expressions for parsing dnsmasq log entries
        self.query_regex = re.compile(
            r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+).*query\[.*?\] (?P<domain>\S+) from (?P<client_ip>\S+)'
        )
        self.blocked_regex = re.compile(
            r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+).*config (?P<domain>\S+) is (?P<result>\S+)'
        )
        
    def start(self):
        """Start the query logger"""
        if self.running:
            return
            
        self.running = True
        self.stop_event.clear()
        self.thread = Thread(target=self._run, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the query logger"""
        if not self.running:
            return
            
        self.running = False
        self.stop_event.set()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
            
        # Process any remaining queries
        self._process_queue()
        
    def _run(self):
        """Main thread function"""
        # Initialize last position
        self._initialize_position()
        
        # Set up flush timer
        last_flush = time.time()
        
        while self.running and not self.stop_event.is_set():
            try:
                # Check for new log entries
                self._check_log_file()
                
                # Process queued queries
                if time.time() - last_flush >= self.flush_interval:
                    self._process_queue()
                    last_flush = time.time()
                    
                # Sleep briefly
                time.sleep(1)
                
            except Exception as e:
                print(f"Error in query logger: {e}")
                time.sleep(5)
                
    def _initialize_position(self):
        """Initialize the last read position in the log file"""
        if self.processed_log_file.exists():
            try:
                with open(self.processed_log_file, 'r') as f:
                    self.last_position = int(f.read().strip())
            except (ValueError, IOError):
                self.last_position = 0
                
        # If log file doesn't exist or is smaller than last position, reset
        if not self.log_file.exists() or self.log_file.stat().st_size < self.last_position:
            self.last_position = 0
            
    def _check_log_file(self):
        """Check for new log entries and process them"""
        if not self.log_file.exists():
            return
            
        current_size = self.log_file.stat().st_size
        
        if current_size <= self.last_position:
            return
            
        try:
            with open(self.log_file, 'r') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()
                
            # Process new lines
            for line in new_lines:
                self._process_log_line(line.strip())
                
            # Update position file
            with open(self.processed_log_file, 'w') as f:
                f.write(str(self.last_position))
                
        except IOError as e:
            print(f"Error reading log file: {e}")
            
    def _process_log_line(self, line):
        """Process a single log line"""
        # Check if it's a query
        query_match = self.query_regex.search(line)
        if query_match:
            timestamp_str = query_match.group('timestamp')
            domain = query_match.group('domain').lower()
            client_ip = query_match.group('client_ip')
            
            # Convert timestamp
            try:
                # Add current year to timestamp
                current_year = datetime.now().year
                timestamp = datetime.strptime(f"{current_year} {timestamp_str}", "%Y %b %d %H:%M:%S")
            except ValueError:
                timestamp = datetime.now()
                
            # Add to queue for processing
            self.query_queue.put({
                'type': 'query',
                'timestamp': timestamp,
                'domain': domain,
                'client_ip': client_ip
            })
            return
            
        # Check if it's a blocked query
        blocked_match = self.blocked_regex.search(line)
        if blocked_match:
            timestamp_str = blocked_match.group('timestamp')
            domain = blocked_match.group('domain').lower()
            result = blocked_match.group('result')
            
            # Check if it was blocked
            if result in ('0.0.0.0', '::', 'blocked'):
                # Convert timestamp
                try:
                    current_year = datetime.now().year
                    timestamp = datetime.strptime(f"{current_year} {timestamp_str}", "%Y %b %d %H:%M:%S")
                except ValueError:
                    timestamp = datetime.now()
                    
                # Add to queue for processing
                self.query_queue.put({
                    'type': 'blocked',
                    'timestamp': timestamp,
                    'domain': domain,
                    'client_ip': None  # Not available in blocked log entry
                })
                
    def _process_queue(self):
        """Process queued queries and save to database"""
        if self.query_queue.empty():
            return
            
        queries = []
        blocked_domains = {}
        
        # Get all queries from queue
        while not self.query_queue.empty():
            try:
                query = self.query_queue.get_nowait()
                queries.append(query)
                
                # Track blocked domains
                if query['type'] == 'blocked':
                    blocked_domains[query['domain']] = query['timestamp']
                    
            except Empty:
                break
                
        if not queries:
            return
            
        # Process in database session
        from adblocker.app import app
        with app.app_context():
            try:
                # Get block list mapping for blocked domains
                block_list_mapping = {}
                if blocked_domains:
                    block_list_mapping = self._get_block_list_mapping(blocked_domains.keys())
                    
                # Save query stats
                query_stats = []
                for query in queries:
                    blocked = query['type'] == 'blocked'
                    block_list_id = None
                    
                    if blocked and query['domain'] in block_list_mapping:
                        block_list_id = block_list_mapping[query['domain']]
                        
                    stat = QueryStat(
                        timestamp=query['timestamp'],
                        domain=query['domain'],
                        client_ip=query['client_ip'] or 'unknown',
                        blocked=blocked,
                        block_list_id=block_list_id
                    )
                    query_stats.append(stat)
                    
                # Batch insert
                if query_stats:
                    db.session.bulk_save_objects(query_stats)
                    
                # Update summary stats
                self._update_summary_stats()
                
                # Commit transaction
                db.session.commit()
                
                # Clean up old data
                self._cleanup_old_data()
                
            except Exception as e:
                db.session.rollback()
                print(f"Error processing query queue: {e}")
                
    def _get_block_list_mapping(self, domains):
        """Get mapping of domains to block list IDs"""
        if not domains:
            return {}
            
        # Query block lists that contain these domains
        from sqlalchemy import or_
        block_lists = BlockList.query.filter(
            BlockList.enabled == True
        ).all()
        
        mapping = {}
        
        for block_list in block_lists:
            # Check if domain is in this block list
            # This is a simplified check - in a real implementation,
            # you might want to use a more efficient method
            block_list_file = Path(self.config['BLOCKLISTS_DIR']) / f"{block_list.id}.txt"
            
            if block_list_file.exists():
                try:
                    with open(block_list_file, 'r') as f:
                        block_list_domains = set(line.strip().lower() for line in f if line.strip())
                        
                    for domain in domains:
                        if domain in block_list_domains:
                            mapping[domain] = block_list.id
                            
                except IOError:
                    pass
                    
        return mapping
        
    def _update_summary_stats(self):
        """Update daily summary statistics"""
        today = datetime.now().date()
        
        # Check if summary already exists for today
        summary = SummaryStat.query.filter_by(date=today).first()
        
        if not summary:
            # Create new summary
            total_queries = QueryStat.query.filter(
                QueryStat.timestamp >= datetime.combine(today, datetime.min.time())
            ).count()
            
            blocked_queries = QueryStat.query.filter(
                QueryStat.timestamp >= datetime.combine(today, datetime.min.time()),
                QueryStat.blocked == True
            ).count()
            
            summary = SummaryStat(
                date=today,
                total_queries=total_queries,
                blocked_queries=blocked_queries
            )
            db.session.add(summary)
        else:
            # Update existing summary
            summary.total_queries = QueryStat.query.filter(
                QueryStat.timestamp >= datetime.combine(today, datetime.min.time())
            ).count()
            
            summary.blocked_queries = QueryStat.query.filter(
                QueryStat.timestamp >= datetime.combine(today, datetime.min.time()),
                QueryStat.blocked == True
            ).count()
            
    def _cleanup_old_data(self):
        """Clean up old query statistics"""
        retention_days = self.config.get('QUERY_LOG_RETENTION_DAYS', 90)
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Delete old query stats
        QueryStat.query.filter(QueryStat.timestamp < cutoff_date).delete()
        
        # Delete old summary stats
        cutoff_summary_date = cutoff_date.date()
        SummaryStat.query.filter(SummaryStat.date < cutoff_summary_date).delete()
        
    def get_query_statistics(self, days=7):
        """Get query statistics for the specified number of days"""
        start_date = datetime.now() - timedelta(days=days)
        
        total_queries = QueryStat.query.filter(
            QueryStat.timestamp >= start_date
        ).count()
        
        blocked_queries = QueryStat.query.filter(
            QueryStat.timestamp >= start_date,
            QueryStat.blocked == True
        ).count()
        
        unique_domains = db.session.query(
            db.func.count(db.func.distinct(QueryStat.domain))
        ).filter(
            QueryStat.timestamp >= start_date
        ).scalar()
        
        unique_clients = db.session.query(
            db.func.count(db.func.distinct(QueryStat.client_ip))
        ).filter(
            QueryStat.timestamp >= start_date
        ).scalar()
        
        return {
            'total_queries': total_queries,
            'blocked_queries': blocked_queries,
            'block_percentage': round((blocked_queries / total_queries * 100) if total_queries > 0 else 0, 2),
            'unique_domains': unique_domains,
            'unique_clients': unique_clients
        }
        
    def get_recent_queries(self, limit=50, offset=0, blocked_only=False):
        """Get recent queries"""
        query = QueryStat.query
        
        if blocked_only:
            query = query.filter(QueryStat.blocked == True)
            
        queries = query.order_by(QueryStat.timestamp.desc()).offset(offset).limit(limit).all()
        
        return [query.to_dict() for query in queries]
        
    def get_top_domains(self, limit=20, blocked_only=False, days=7):
        """Get top queried domains"""
        start_date = datetime.now() - timedelta(days=days)
        
        query = db.session.query(
            QueryStat.domain,
            db.func.count(QueryStat.id).label('count')
        ).filter(
            QueryStat.timestamp >= start_date
        )
        
        if blocked_only:
            query = query.filter(QueryStat.blocked == True)
            
        results = query.group_by(
            QueryStat.domain
        ).order_by(db.desc('count')).limit(limit).all()
        
        return [
            {
                'domain': result.domain,
                'count': result.count
            }
            for result in results
        ]
        
    def get_top_clients(self, limit=20, days=7):
        """Get top query sources by client IP"""
        start_date = datetime.now() - timedelta(days=days)
        
        results = db.session.query(
            QueryStat.client_ip,
            db.func.count(QueryStat.id).label('count')
        ).filter(
            QueryStat.timestamp >= start_date
        ).group_by(
            QueryStat.client_ip
        ).order_by(db.desc('count')).limit(limit).all()
        
        return [
            {
                'client_ip': result.client_ip,
                'count': result.count
            }
            for result in results
        ]
        
    def get_hourly_stats(self, hours=24):
        """Get hourly statistics"""
        start_date = datetime.now() - timedelta(hours=hours)
        
        results = db.session.query(
            db.func.date_trunc('hour', QueryStat.timestamp).label('hour'),
            db.func.count(QueryStat.id).label('total_queries'),
            db.func.sum(db.case([(QueryStat.blocked == True, 1)], else_=0)).label('blocked_queries')
        ).filter(
            QueryStat.timestamp >= start_date
        ).group_by(
            db.func.date_trunc('hour', QueryStat.timestamp)
        ).order_by('hour').all()
        
        return [
            {
                'hour': result.hour.isoformat(),
                'total_queries': result.total_queries,
                'blocked_queries': result.blocked_queries or 0,
                'block_percentage': round((result.blocked_queries or 0) / result.total_queries * 100, 2) if result.total_queries > 0 else 0
            }
            for result in results
        ]
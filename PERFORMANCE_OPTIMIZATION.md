# PiDNS Ad-Blocker Performance Optimization for Raspberry Pi Zero 2 W

## Overview

The Raspberry Pi Zero 2 W has limited resources (512MB RAM, single-core CPU) compared to more powerful Raspberry Pi models. This guide provides optimization recommendations to ensure smooth operation of the PiDNS Ad-Blocker on this hardware.

## System-level Optimizations

### Memory Management

1. **Swap Configuration**
   ```bash
   # Check current swap usage
   swapon --show
   
   # Configure swap usage (already done in installation)
   sudo sysctl vm.swappiness=10
   ```

2. **Memory Monitoring**
   ```bash
   # Monitor memory usage
   free -h
   
   # Monitor memory usage over time
   watch -n 5 free -h
   ```

3. **Reduce Memory Usage**
   ```bash
   # Disable unnecessary services
   sudo systemctl disable bluetooth
   sudo systemctl disable cups
   
   # Minimize GPU memory split
   sudo raspi-config
   # Navigate to Advanced Options > Memory Split and set to 16
   ```

### CPU Optimization

1. **CPU Governor**
   ```bash
   # Set CPU governor to performance (more power but better responsiveness)
   echo 'performance' | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
   ```

2. **Monitor CPU Usage**
   ```bash
   # Monitor CPU usage
   top
   
   # Monitor CPU temperature
   vcgencmd measure_temp
   ```

### Network Optimization

1. **Network Interface Buffers**
   ```bash
   # Increase network buffer sizes (already done in installation)
   sudo sysctl net.core.rmem_max=16777216
   sudo sysctl net.core.wmem_max=16777216
   ```

2. **Disable Power Saving for Wi-Fi**
   ```bash
   # Disable Wi-Fi power saving
   sudo iwconfig wlan0 power off
   ```

## Ad-Blocker Specific Optimizations

### Database Optimization

1. **SQLite Configuration**
   ```python
   # In adblocker/config/flask_config.py
   DATABASE_CONFIG = {
       'journal_mode': 'WAL',  # Better concurrent access
       'synchronous': 'NORMAL',  # Balance between safety and performance
       'cache_size': 2000,  # 2MB cache
       'page_size': 4096,  # Default page size
   }
   ```

2. **Query Log Retention**
   ```python
   # Reduce retention period for query logs
   QUERY_LOG_RETENTION_DAYS = 30  # Default is 90, reduce for Pi Zero 2 W
   ```

3. **Batch Processing**
   ```python
   # Reduce batch sizes for processing
   QUERY_LOG_BATCH_SIZE = 50  # Default is 100, reduce for Pi Zero 2 W
   ```

### Block List Management

1. **Limit Number of Block Lists**
   - Start with 3-5 essential block lists
   - Add more only if needed
   - Monitor memory usage after adding each list

2. **Block List Update Schedule**
   ```python
   # Reduce update frequency to minimize resource usage
   BLOCKLIST_UPDATE_SCHEDULE = {
       "hour": "4",  # Update at 4 AM
       "minute": "0"
   }
   ```

3. **Block List Size Limits**
   ```python
   # Set maximum size for block lists
   MAX_BLOCKLIST_SIZE = 1000000  # 1MB per list
   ```

### Web Interface Optimization

1. **Flask Configuration**
   ```python
   # In adblocker/config/flask_config.py
   class ProductionConfig:
       # Reduce worker threads
       THREADS_PER_PAGE = 1
       
       # Enable compression
       COMPRESS_RESPONSE = True
       
       # Reduce cache size
       SEND_FILE_MAX_AGE_DEFAULT = 3600
   ```

2. **Static File Optimization**
   ```python
   # Enable static file caching
   SEND_FILE_MAX_AGE_DEFAULT = 86400  # 1 day
   
   # Minimize static files
   USE_COMPRESSED_STATIC = True
   ```

### Service Resource Limits

1. **Ad-Blocker Service Limits**
   ```ini
   # In services/adblocker.service
   # Limit memory usage to 128MB
   MemoryLimit=128M
   
   # Limit CPU usage to 50%
   CPUQuota=50%
   ```

2. **Query Logger Optimization**
   ```python
   # Reduce flush interval
   QUERY_LOG_FLUSH_INTERVAL = 30  # seconds (default is 60)
   
   # Reduce batch size
   QUERY_LOG_BATCH_SIZE = 50  # (default is 100)
   ```

## Monitoring and Maintenance

### Performance Monitoring

1. **System Resource Monitoring**
   ```bash
   # Create a monitoring script
   cat > monitor.sh << 'EOF'
   #!/bin/bash
   echo "=== Memory Usage ==="
   free -h
   echo "=== CPU Usage ==="
   top -bn1 | grep "Cpu(s)"
   echo "=== Disk Usage ==="
   df -h
   echo "=== Temperature ==="
   vcgencmd measure_temp
   echo "=== Service Status ==="
   systemctl is-active dnsmasq pidns adblocker
   EOF
   
   chmod +x monitor.sh
   ./monitor.sh
   ```

2. **Ad-Blocker Performance Monitoring**
   ```bash
   # Check ad-blocker service status
   sudo systemctl status adblocker
   
   # Check query log size
   ls -lh data/adblocker/adblocker.db
   
   # Check block list sizes
   du -sh data/adblocker/blocklists/*
   ```

### Maintenance Tasks

1. **Database Maintenance**
   ```bash
   # Rebuild index and optimize database
   sqlite3 data/adblocker/adblocker.db "VACUUM;"
   sqlite3 data/adblocker/adblocker.db "ANALYZE;"
   ```

2. **Log Rotation**
   ```bash
   # Set up log rotation for query logs
   sudo tee /etc/logrotate.d/pidns-adblocker > /dev/null << EOF
   /var/log/pidns-adblocker/*.log {
       weekly
       rotate 4
       compress
       delaycompress
       missingok
       notifempty
       create 644 pi pi
       postrotate
           systemctl reload adblocker
       endscript
   }
   EOF
   ```

3. **Cleanup Old Data**
   ```bash
   # Clean up old query statistics
   sqlite3 data/adblocker/adblocker.db "DELETE FROM query_stats WHERE timestamp < datetime('now', '-30 days');"
   
   # Clean up old summary statistics
   sqlite3 data/adblocker/adblocker.db "DELETE FROM summary_stats WHERE date < date('now', '-30 days');"
   ```

## Troubleshooting Performance Issues

### High Memory Usage

1. **Identify Memory Hog**
   ```bash
   # Check memory usage by process
   ps aux --sort=-%mem | head -10
   ```

2. **Reduce Block Lists**
   - Disable non-essential block lists
   - Use smaller, more focused block lists
   - Remove duplicate entries

3. **Restart Services**
   ```bash
   # Restart ad-blocker service
   sudo systemctl restart adblocker
   
   # Restart dnsmasq
   sudo systemctl restart dnsmasq
   ```

### High CPU Usage

1. **Identify CPU Hog**
   ```bash
   # Check CPU usage by process
   ps aux --sort=-%cpu | head -10
   ```

2. **Reduce Query Logging**
   - Increase batch processing size
   - Increase flush interval
   - Reduce log retention period

3. **Optimize Block Lists**
   - Remove large block lists
   - Use more targeted block lists
   - Schedule updates during off-peak hours

### Slow Web Interface

1. **Check Database Performance**
   ```bash
   # Check database size
   ls -lh data/adblocker/adblocker.db
   
   # Check query performance
   sqlite3 data/adblocker/adblocker.db "EXPLAIN QUERY PLAN SELECT * FROM query_stats LIMIT 10;"
   ```

2. **Optimize Database**
   ```bash
   # Rebuild database
   cp data/adblocker/adblocker.db data/adblocker/adblocker.db.backup
   sqlite3 data/adblocker/adblocker.db ".dump" | sqlite3 data/adblocker/adblocker_new.db
   mv data/adblocker/adblocker_new.db data/adblocker/adblocker.db
   ```

3. **Reduce Statistics Data**
   - Decrease retention period
   - Clean up old data more frequently
   - Reduce the amount of data displayed in the web interface

## Performance Benchmarks

### Expected Performance on Pi Zero 2 W

- **Memory Usage**: 80-120MB total (including OS)
- **CPU Usage**: 10-30% during normal operation
- **Query Response Time**: <50ms for cached queries
- **Web Interface Load Time**: <2 seconds for statistics page

### Stress Testing

1. **DNS Query Stress Test**
   ```bash
   # Install stress testing tool
   sudo apt-get install dnsperf
   
   # Run stress test
   dnsperf -s localhost -p 53 -d queries.txt -l 60
   ```

2. **Web Interface Stress Test**
   ```bash
   # Install stress testing tool
   pip install locust
   
   # Create a simple test script
   cat > locustfile.py << 'EOF'
   from locust import HttpUser, task, between
   
   class WebsiteUser(HttpUser):
       wait_time = between(1, 3)
       
       @task
       def load_dashboard(self):
           self.client.get("/")
           
       @task
       def load_statistics(self):
           self.client.get("/api/statistics/overview")
   EOF
   
   # Run stress test
   locust -f locustfile.py --host=http://localhost:8081
   ```

## Conclusion

By following these optimization guidelines, the PiDNS Ad-Blocker should run smoothly on a Raspberry Pi Zero 2 W. The key is to balance functionality with resource constraints by:

1. Limiting the number and size of block lists
2. Optimizing database operations
3. Implementing proper resource limits
4. Regular maintenance and monitoring

If you experience performance issues, start by reducing the number of block lists and adjusting the query log retention period. These changes will have the most significant impact on memory usage and overall performance.
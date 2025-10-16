# PiDNS Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIDNS_USERNAME=admin \
    PIDNS_PASSWORD=dev-change-me-now! \
    SECRET_KEY=dev-secret-key \
    DEBUG=True

# Install system dependencies
RUN apt-get update && apt-get install -y \
    dnsmasq \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt requirements_adblocker.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements_adblocker.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs data/adblocker/blocklists

# Download MAC vendor database
RUN curl -s "https://raw.githubusercontent.com/digitalocean/macvendorlookup/main/data/mac-vendors.json" -o data/mac-vendors.json

# Create a non-root user
RUN useradd -m -u 1000 pidns && \
    chown -R pidns:pidns /app

USER pidns

# Expose ports
EXPOSE 8080 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Default command
CMD ["python", "app/app.py"]
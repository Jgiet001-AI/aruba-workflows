# n8n Workflow Deployment Guide

## Production Deployment Checklist

### Pre-Deployment Requirements

#### 1. Environment Setup
- [ ] n8n instance running at `http://192.168.40.100:8006`
- [ ] n8n version compatibility verified (supports node typeVersions used)
- [ ] Database backup completed
- [ ] SSL/TLS certificates configured for production
- [ ] Environment variables properly configured

#### 2. Credential Configuration
- [ ] Aruba Central API credentials configured in n8n credential store
- [ ] Slack API tokens configured for notifications
- [ ] ServiceNow credentials configured (if applicable)
- [ ] All credentials tested and validated
- [ ] Credential rotation schedule established

#### 3. Network Configuration
- [ ] Firewall rules configured for n8n webhooks
- [ ] Network access to Aruba APIs verified
- [ ] DNS resolution for all external services confirmed
- [ ] Load balancer configuration (if applicable)

#### 4. Monitoring and Logging
- [ ] Prometheus metrics collection enabled
- [ ] Log aggregation configured
- [ ] Alert manager configured
- [ ] Dashboard templates imported
- [ ] Backup and recovery procedures documented

### Workflow Import Process

#### Step 1: Import Fixed Workflows
```bash
#!/bin/bash
# Import enhanced workflows to n8n

N8N_URL="http://192.168.40.100:8006"
WORKFLOW_DIR="./exported-workflows"

# Import device health monitoring
curl -X POST "${N8N_URL}/api/v1/workflows/import" \
  -H "Content-Type: application/json" \
  -d @"${WORKFLOW_DIR}/device-health-monitor-FIXED.json"

# Import security event response
curl -X POST "${N8N_URL}/api/v1/workflows/import" \
  -H "Content-Type: application/json" \
  -d @"${WORKFLOW_DIR}/security-event-response-automation-FIXED.json"

# Import workflow templates
curl -X POST "${N8N_URL}/api/v1/workflows/import" \
  -H "Content-Type: application/json" \
  -d @"./workflow-templates/aruba-monitoring-template.json"

curl -X POST "${N8N_URL}/api/v1/workflows/import" \
  -H "Content-Type: application/json" \
  -d @"./workflow-templates/aruba-security-template.json"
```

#### Step 2: Configure Credentials
1. Access n8n UI at `http://192.168.40.100:8006`
2. Navigate to **Settings > Credentials**
3. Create the following credential types:

**Aruba API Credential:**
```json
{
  "name": "arubaApi",
  "type": "httpHeaderAuth",
  "data": {
    "name": "Authorization",
    "value": "Bearer YOUR_ARUBA_API_TOKEN"
  },
  "additionalData": {
    "arubaApiUrl": "https://apigw-prod2.central.arubanetworks.com"
  }
}
```

**Slack API Credential:**
```json
{
  "name": "slackApi",
  "type": "slackApi",
  "data": {
    "accessToken": "xoxb-your-slack-bot-token"
  }
}
```

#### Step 3: Activate Workflows
```bash
#!/bin/bash
# Activate imported workflows

# Get workflow IDs
HEALTH_MONITOR_ID=$(curl -s "${N8N_URL}/api/v1/workflows" | jq -r '.data[] | select(.name=="Device Health Monitor - Enhanced") | .id')
SECURITY_RESPONSE_ID=$(curl -s "${N8N_URL}/api/v1/workflows" | jq -r '.data[] | select(.name=="Security Event Response Automation - Enhanced") | .id')

# Activate workflows
curl -X PATCH "${N8N_URL}/api/v1/workflows/${HEALTH_MONITOR_ID}" \
  -H "Content-Type: application/json" \
  -d '{"active": true}'

curl -X PATCH "${N8N_URL}/api/v1/workflows/${SECURITY_RESPONSE_ID}" \
  -H "Content-Type: application/json" \
  -d '{"active": true}'

echo "Workflows activated successfully"
```

### Post-Deployment Verification

#### 1. Webhook Endpoint Testing
```bash
#!/bin/bash
# Test webhook endpoints

# Test device health monitoring webhook
curl -X POST "http://192.168.40.100:8006/webhook/device-health-check" \
  -H "Content-Type: application/json" \
  -d '{
    "device_filter": "all",
    "cpu_critical": 90,
    "memory_critical": 95,
    "include_interfaces": true
  }'

# Test security event response webhook
curl -X POST "http://192.168.40.100:8006/webhook/security-event-handler" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "TEST-001",
    "threat_type": "malware",
    "severity": "high",
    "device_id": "TEST-DEVICE",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
    "confidence_score": 0.85,
    "source_ip": "192.168.1.100"
  }'
```

#### 2. Monitoring Verification
```bash
#!/bin/bash
# Verify monitoring is working

# Check Prometheus metrics
curl -s "http://192.168.40.100:9090/api/v1/query?query=n8n_workflow_executions_total" | jq '.data.result'

# Check log aggregation
curl -s "http://192.168.40.100:3000/api/search" \
  -H "Authorization: Bearer YOUR_GRAFANA_TOKEN" \
  -d '{"query": "n8n workflow"}'

# Verify alerting
curl -s "http://192.168.40.100:9093/api/v1/alerts" | jq '.data[] | select(.labels.workflow_name)'
```

### Production Configuration Recommendations

#### 1. Performance Tuning
```yaml
# n8n configuration for production
N8N_HOST: 0.0.0.0
N8N_PORT: 5678
N8N_PROTOCOL: https
N8N_SSL_KEY: /etc/ssl/private/n8n.key
N8N_SSL_CERT: /etc/ssl/certs/n8n.crt

# Database configuration
DB_TYPE: postgres
DB_POSTGRESDB_HOST: postgres.internal
DB_POSTGRESDB_PORT: 5432
DB_POSTGRESDB_DATABASE: n8n
DB_POSTGRESDB_USER: n8n_user
DB_POSTGRESDB_PASSWORD: secure_password

# Performance settings
EXECUTIONS_TIMEOUT: 300
EXECUTIONS_TIMEOUT_MAX: 600
N8N_DEFAULT_BINARY_DATA_MODE: filesystem
N8N_BINARY_DATA_TTL: 168 # 7 days
N8N_PAYLOAD_MAX_SIZE: 16 # 16MB

# Security settings
N8N_SECURE_COOKIE: true
N8N_BASIC_AUTH_ACTIVE: true
N8N_BASIC_AUTH_USER: admin
N8N_BASIC_AUTH_PASSWORD: secure_admin_password
```

#### 2. Resource Allocation
```yaml
# Docker Compose resource limits
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
    environment:
      - NODE_OPTIONS=--max-old-space-size=2048
```

#### 3. High Availability Setup
```yaml
# Load balancer configuration (nginx)
upstream n8n_backend {
    server n8n-1:5678;
    server n8n-2:5678;
    server n8n-3:5678;
}

server {
    listen 443 ssl;
    server_name n8n.yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/n8n.crt;
    ssl_certificate_key /etc/ssl/private/n8n.key;
    
    location / {
        proxy_pass http://n8n_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Operational Procedures

#### 1. Backup and Recovery
```bash
#!/bin/bash
# Automated backup script

BACKUP_DIR="/opt/backups/n8n"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
N8N_URL="http://192.168.40.100:8006"

# Create backup directory
mkdir -p "${BACKUP_DIR}/${TIMESTAMP}"

# Export all workflows
curl -s "${N8N_URL}/api/v1/workflows" | jq '.data' > "${BACKUP_DIR}/${TIMESTAMP}/workflows.json"

# Export all credentials (encrypted)
curl -s "${N8N_URL}/api/v1/credentials" | jq '.data' > "${BACKUP_DIR}/${TIMESTAMP}/credentials.json"

# Database backup
pg_dump -h postgres.internal -U n8n_user n8n > "${BACKUP_DIR}/${TIMESTAMP}/database.sql"

# Compress backup
tar -czf "${BACKUP_DIR}/n8n_backup_${TIMESTAMP}.tar.gz" -C "${BACKUP_DIR}" "${TIMESTAMP}"
rm -rf "${BACKUP_DIR}/${TIMESTAMP}"

# Cleanup old backups (keep last 30 days)
find "${BACKUP_DIR}" -name "n8n_backup_*.tar.gz" -mtime +30 -delete

echo "Backup completed: n8n_backup_${TIMESTAMP}.tar.gz"
```

#### 2. Health Monitoring
```bash
#!/bin/bash
# Health check script

N8N_URL="http://192.168.40.100:8006"

# Check n8n API health
health_status=$(curl -s -o /dev/null -w "%{http_code}" "${N8N_URL}/healthz")

if [ "$health_status" != "200" ]; then
    echo "CRITICAL: n8n health check failed (HTTP $health_status)"
    # Send alert to monitoring system
    exit 1
fi

# Check active workflows
active_workflows=$(curl -s "${N8N_URL}/api/v1/workflows" | jq '[.data[] | select(.active == true)] | length')

if [ "$active_workflows" -lt 2 ]; then
    echo "WARNING: Expected active workflows not running ($active_workflows active)"
    exit 1
fi

# Check recent executions
recent_executions=$(curl -s "${N8N_URL}/api/v1/executions?limit=10" | jq '.data | length')

if [ "$recent_executions" -eq 0 ]; then
    echo "WARNING: No recent workflow executions detected"
fi

echo "OK: n8n health check passed ($active_workflows active workflows, $recent_executions recent executions)"
```

#### 3. Log Management
```yaml
# Fluent Bit configuration for log collection
[INPUT]
    Name tail
    Path /var/log/n8n/*.log
    Tag n8n.*
    Parser json

[FILTER]
    Name modify
    Match n8n.*
    Add service n8n
    Add environment production

[OUTPUT]
    Name elasticsearch
    Match n8n.*
    Host elasticsearch.internal
    Port 9200
    Index n8n-logs
    Type _doc
```

### Security Hardening

#### 1. Network Security
```bash
# Firewall rules (iptables)
#!/bin/bash

# Allow n8n web interface (HTTPS only)
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow webhook endpoints
iptables -A INPUT -p tcp --dport 5678 -s 192.168.0.0/16 -j ACCEPT

# Allow monitoring
iptables -A INPUT -p tcp --dport 9090 -s 10.0.0.0/8 -j ACCEPT

# Block all other traffic to n8n
iptables -A INPUT -p tcp --dport 5678 -j DROP
```

#### 2. Application Security
```yaml
# Security headers (nginx)
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'";
```

#### 3. Credential Security
```bash
#!/bin/bash
# Credential rotation script

# Rotate Aruba API credentials
new_token=$(generate_aruba_token.sh)

# Update n8n credential
curl -X PATCH "${N8N_URL}/api/v1/credentials/${ARUBA_CRED_ID}" \
  -H "Content-Type: application/json" \
  -d "{\"data\": {\"accessToken\": \"$new_token\"}}"

# Log rotation
echo "$(date): Rotated Aruba API token" >> /var/log/credential-rotation.log
```

### Troubleshooting Guide

#### Common Issues and Solutions

1. **Workflow Import Failures**
   ```bash
   # Check workflow JSON validity
   jq . workflow.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
   
   # Check node type compatibility
   jq '.nodes[] | .type' workflow.json | sort | uniq
   ```

2. **Credential Configuration Issues**
   ```bash
   # Test credential connectivity
   curl -X GET "${N8N_URL}/api/v1/credentials/test/${CRED_ID}"
   ```

3. **Performance Issues**
   ```bash
   # Check memory usage
   docker stats n8n
   
   # Check database connections
   psql -h postgres.internal -U n8n_user -c "SELECT count(*) FROM pg_stat_activity;"
   ```

4. **Webhook Connectivity Issues**
   ```bash
   # Test webhook endpoint
   curl -v -X POST "http://192.168.40.100:8006/webhook/test-endpoint"
   
   # Check nginx logs
   tail -f /var/log/nginx/access.log | grep webhook
   ```

This deployment guide ensures a secure, reliable, and maintainable production deployment of the enhanced Aruba n8n workflows.
# HPE Aruba n8n Workflows - Webhook Testing Guide

**Generated:** 2025-07-18  
**Base URL:** `http://192.168.40.100:8006/webhook/`  
**Total Endpoints:** 23 webhook triggers across all workflows

## Quick Testing Commands

### 🔍 **Security Event Response Automation**
```bash
curl -X POST http://192.168.40.100:8006/webhook/security-event-response \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "threat_detected",
    "severity": "critical", 
    "device_serial": "TEST001",
    "threat_score": 95,
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.50",
    "description": "Malware communication detected"
  }'
```

### 📊 **Alert Aggregation and Correlation**
```bash
curl -X POST http://192.168.40.100:8006/webhook/alert-aggregation \
  -H "Content-Type: application/json" \
  -d '{
    "source": "aruba_central",
    "alert_type": "device_health",
    "device_id": "AP001",
    "severity": "high",
    "message": "High CPU usage detected"
  }'
```

### 🏥 **Device Health Check (Manual)**
```bash
curl -X POST http://192.168.40.100:8006/webhook/device-health-check \
  -H "Content-Type: application/json" \
  -d '{
    "device_filter": "all",
    "cpu_critical": 90,
    "memory_critical": 95,
    "temperature_critical": 65
  }'
```

### 🌐 **IPAM Management**
```bash
# Create IP Pool
curl -X POST http://192.168.40.100:8006/webhook/ipam-management \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_pool",
    "resource_type": "ip_pool",
    "pool_name": "test-pool-001",
    "network": "192.168.100.0/24",
    "gateway": "192.168.100.1",
    "description": "Test IP pool via webhook"
  }'

# Create DHCP Scope  
curl -X POST http://192.168.40.100:8006/webhook/ipam-management \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_dhcp_scope", 
    "resource_type": "dhcp_scope",
    "scope_name": "test-dhcp-001",
    "start_ip": "192.168.100.50",
    "end_ip": "192.168.100.200",
    "gateway": "192.168.100.1"
  }'
```

### 🔌 **AOS-CX Switch Configuration**
```bash
curl -X POST http://192.168.40.100:8006/webhook/aos-cx-switch-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "health_check",
    "switch_ip": "192.168.1.10", 
    "auth_token": "your-aos-cx-token"
  }'
```

### 🏷️ **AOS-CX VLAN Management**  
```bash
curl -X POST http://192.168.40.100:8006/webhook/aos-cx-vlan-management \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_vlan",
    "switch_ip": "192.168.1.10",
    "vlan_id": 100,
    "vlan_name": "test-vlan-100",
    "description": "Test VLAN created via webhook"
  }'
```

### 🌐 **EdgeConnect SD-WAN Policy**
```bash
curl -X POST http://192.168.40.100:8006/webhook/edgeconnect-policy \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list_network_segment_policies",
    "orchestrator_host": "edgeconnect.company.com",
    "auth_token": "your-edgeconnect-token"
  }'
```

### 📋 **ServiceNow Incident Management**
```bash
curl -X POST http://192.168.40.100:8006/webhook/servicenow-incident \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_incident",
    "short_description": "Network device offline",
    "description": "Switch AP001 is not responding to health checks",
    "priority": "2",
    "category": "network",
    "assignment_group": "network-team"
  }'
```

### 📡 **Wireless Configuration Management**
```bash
curl -X POST http://192.168.40.100:8006/webhook/wireless-config-management \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_ssid",
    "ssid_name": "test-guest-wifi",
    "wlan_group": "default",
    "security_type": "wpa2-psk",
    "passphrase": "TestPassword123"
  }'
```

### 📈 **UXI Test Configuration**
```bash
curl -X POST http://192.168.40.100:8006/webhook/uxi-test-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_test",
    "test_name": "connectivity-test-001",
    "test_type": "connectivity",
    "target": "8.8.8.8",
    "frequency": 300
  }'
```

## Complete Webhook Reference

### Security & Event Management

| Endpoint | Operations | Key Parameters |
|----------|------------|----------------|
| `/security-event-response` | threat_analysis, device_isolation, incident_escalation | event_type, severity, device_serial, threat_score |
| `/alert-aggregation` | alert_processing, correlation | source, alert_type, device_id, severity |
| `/ids-ips-rule-management` | create/update/delete_rule | rule_name, rule_type, action, pattern |
| `/siem-integration-management` | log_forwarding, correlation_rule_management | connection_type, log_source, destination |

### Network Infrastructure

| Endpoint | Operations | Key Parameters |
|----------|------------|----------------|
| `/ipam-management` | create/update/delete pools, dhcp, dns, vlans | operation, resource_type, pool_name, network |
| `/aos-cx-switch-config` | health_check, system_info, interface_config | operation, switch_ip, interface_id |
| `/aos-cx-vlan-management` | create/update/delete/list vlans | operation, switch_ip, vlan_id, vlan_name |
| `/wireless-config-management` | ssid, wlan_group, radio, ap_group mgmt | operation, ssid_name, wlan_group, security_type |
| `/network-service-monitoring` | service_health, port_check, performance_test | operation, target_host, service_type |
| `/network-performance-monitoring` | latency, throughput, packet_loss tests | operation, test_type, target, duration |

### Device & Health Monitoring

| Endpoint | Operations | Key Parameters |
|----------|------------|----------------|
| `/device-health-check` | manual health check, threshold config | device_filter, cpu_critical, memory_critical |
| `/central-device-health-monitoring` | aruba central device monitoring | device_serial, include_interfaces, include_wireless |
| `/central-ap-provisioning` | ap provisioning, deprovisioning, config | operation, ap_serial, group_name, template_name |

### SD-WAN & EdgeConnect

| Endpoint | Operations | Key Parameters |
|----------|------------|----------------|
| `/edgeconnect-policy` | network_segment, tunnel, route policies | operation, orchestrator_host, policy_name |
| `/edgeconnect-alert-handler` | alert processing, policy violations | alert_type, appliance_id, severity |

### UXI & Testing

| Endpoint | Operations | Key Parameters |
|----------|------------|----------------|
| `/uxi-test-config` | create/update/delete tests | operation, test_name, test_type, target |
| `/uxi-sensor-management` | sensor config, monitoring | operation, sensor_id, config_type |

### ServiceNow Integration

| Endpoint | Operations | Key Parameters |
|----------|------------|----------------|
| `/servicenow-incident` | create/update incidents | operation, short_description, priority, category |
| `/servicenow-change-management` | create/approve/schedule changes | operation, change_type, description, risk |
| `/servicenow-service-request` | create/fulfill requests | operation, request_type, description |
| `/servicenow-asset-sync` | asset synchronization | operation, asset_type, sync_direction |

### Central Platform

| Endpoint | Operations | Key Parameters |
|----------|------------|----------------|
| `/central-template-management` | template create/update/deploy | operation, template_name, template_type, target_devices |

## Expected Response Format

All webhooks return standardized JSON responses:

### ✅ Success Response
```json
{
  "request_id": "workflow-1642521234567-abc123",
  "operation": "create_pool", 
  "status": "success",
  "message": "IP pool 'test-pool-001' created successfully",
  "timestamp": "2025-07-18T21:30:00.000Z",
  "data": { "pool_id": "pool_12345" }
}
```

### ❌ Error Response  
```json
{
  "request_id": "workflow-1642521234567-abc123",
  "operation": "create_pool",
  "status": "error", 
  "message": "Invalid CIDR notation for network",
  "timestamp": "2025-07-18T21:30:00.000Z",
  "error": {
    "statusCode": 400,
    "details": "Network must be in CIDR format (e.g., 192.168.1.0/24)"
  }
}
```

## Monitoring & Notifications

### 📱 **Slack Notifications**
All workflows send notifications to configured Slack channels:
- **Critical alerts:** `#critical-alerts`
- **Network operations:** `#network-operations`  
- **Device health:** `#device-health-alerts`
- **Security events:** `#security-alerts`
- **EdgeConnect ops:** `#edgeconnect-automation`
- **ServiceNow updates:** `#servicenow-integration`

### 📊 **Request ID Tracking**
Every webhook request generates a unique `request_id` for tracking:
- Format: `{workflow-type}-{timestamp}-{random}`
- Used for debugging and audit trails
- Included in all notifications and responses

## Testing Recommendations

### 🧪 **Testing Strategy**
1. **Start with GET operations** (list, status, health checks)
2. **Test validation** with invalid payloads 
3. **Verify notifications** in Slack channels
4. **Test error scenarios** (invalid credentials, network issues)
5. **Load testing** with multiple concurrent requests

### 🔍 **Validation Testing**
```bash
# Test missing required fields
curl -X POST http://192.168.40.100:8006/webhook/ipam-management \
  -H "Content-Type: application/json" \
  -d '{"operation": "create_pool"}'  # Missing resource_type

# Test invalid operations  
curl -X POST http://192.168.40.100:8006/webhook/security-event-response \
  -H "Content-Type: application/json" \
  -d '{"event_type": "invalid_event", "severity": "critical"}'
```

### ⚡ **Performance Testing**
```bash
# Concurrent requests test
for i in {1..10}; do
  curl -X POST http://192.168.40.100:8006/webhook/device-health-check \
    -H "Content-Type: application/json" \
    -d '{"device_filter": "all"}' &
done
wait
```

## Security Considerations

### 🔐 **API Authentication**
- All workflows expect API tokens in request payloads
- Tokens should be valid for respective services (Aruba Central, AOS-CX, etc.)
- Consider implementing webhook authentication headers for production

### 🛡️ **Input Validation** 
- All workflows include comprehensive input validation
- Invalid requests return clear error messages
- Potential injection attacks are mitigated through JSON parsing

### 📋 **Audit Trail**
- All operations generate audit logs with request IDs
- Slack notifications provide real-time monitoring
- Failed operations are tracked and reported

## Troubleshooting

### 🚨 **Common Issues**
- **404 Not Found:** Workflow not activated or incorrect endpoint path
- **400 Bad Request:** Missing required fields or invalid format
- **500 Internal Error:** API authentication or connectivity issues
- **Timeout:** Large operations or API rate limiting

### 🔧 **Debugging Steps**
1. Verify webhook URL and method (POST)
2. Check JSON payload format and required fields
3. Monitor Slack channels for error notifications
4. Review request_id in n8n execution logs
5. Validate API credentials and connectivity

---

**Note:** All webhooks are currently **inactive** and require manual activation in the n8n interface before testing. Activate workflows through the n8n UI at `http://192.168.40.100:8006` before running tests.
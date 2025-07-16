# HPE Aruba Configuration Management APIs

This document provides comprehensive information about configuration management APIs available in your Postman workspace collections for n8n workflow automation.

## Collections Overview

Based on your Postman workspace, these collections contain configuration APIs:

| Collection | Focus | Configuration Capabilities |
|------------|-------|---------------------------|
| AP provisioning | Wireless APs | Device provisioning, radio config, policy assignment |
| Aruba Central AOS 10 | Central platform | Device management, templates, bulk operations |
| Device-Onboarding-GLP | Device setup | Automated onboarding, initial configuration |
| Device-Onboarding | Device inventory | Bulk provisioning, device discovery |
| EC Orchestrator | SD-WAN | Policy management, template deployment |
| HPE Aruba Networking | Switch/Network | VLAN, interface, ACL configuration |
| New HPE Aruba Networking | Enhanced APIs | Latest configuration features |

---

## 1. Device Configuration Management

### Aruba Central Configuration APIs
```
Base URL: https://{region}.central.arubanetworks.com/api/v2/

Key Endpoints:
GET    /configuration/devices/{device_id}           # Get device config
PUT    /configuration/devices/{device_id}           # Update device config  
POST   /configuration/devices/{device_id}/commands  # Execute CLI commands
GET    /configuration/devices/{device_id}/backup    # Get config backup
POST   /configuration/devices/{device_id}/restore   # Restore config
```

### AOS-CX Switch Configuration
```
Base URL: https://{switch_ip}/rest/v10.08/

Key Endpoints:
GET    /system                    # System information
GET    /system/config             # Running configuration
PUT    /system/config             # Update configuration
POST   /system/config/checkpoint  # Create config checkpoint
POST   /system/config/restore     # Restore from checkpoint
```

---

## 2. Template Management

### Central Template APIs
```
GET    /configuration/templates                    # List templates
POST   /configuration/templates                    # Create template
GET    /configuration/templates/{template_id}      # Get template details
PUT    /configuration/templates/{template_id}      # Update template
DELETE /configuration/templates/{template_id}      # Delete template
POST   /configuration/templates/{template_id}/apply # Apply to devices
```

### Template Structure Example
```json
{
  "template_id": "wifi-corp-template",
  "name": "Corporate WiFi Template",
  "device_type": "AP",
  "configuration": {
    "ssid": "{{CORP_SSID}}",
    "security": "WPA3-Enterprise",
    "vlan": "{{CORP_VLAN}}",
    "radio_settings": {
      "2.4ghz": {"power": "auto", "channel": "auto"},
      "5ghz": {"power": "auto", "channel": "auto"}
    }
  }
}
```

---

## 3. Policy Configuration

### Security Policies
```
GET    /configuration/policies/security           # List security policies
POST   /configuration/policies/security           # Create security policy
PUT    /configuration/policies/security/{id}      # Update policy
GET    /configuration/policies/firewall           # Firewall rules
POST   /configuration/policies/firewall           # Create firewall rule
```

### QoS Policies (EdgeConnect)
```
GET    /orchestrator/policies/qos                 # List QoS policies
POST   /orchestrator/policies/qos                 # Create QoS policy
PUT    /orchestrator/policies/qos/{id}            # Update QoS policy
GET    /orchestrator/policies/traffic-steering    # Traffic policies
```

---

## 4. VLAN and Interface Configuration

### AOS-CX VLAN Management
```
GET    /system/vlans                # List all VLANs
POST   /system/vlans                # Create VLAN
GET    /system/vlans/{vlan_id}      # Get VLAN details
PUT    /system/vlans/{vlan_id}      # Update VLAN
DELETE /system/vlans/{vlan_id}      # Delete VLAN
```

### Interface Configuration
```
GET    /system/interfaces                    # List all interfaces
GET    /system/interfaces/{interface_id}     # Get interface details
PUT    /system/interfaces/{interface_id}     # Configure interface
POST   /system/interfaces/{interface_id}/shutdown   # Shutdown interface
POST   /system/interfaces/{interface_id}/no-shutdown # Enable interface
```

### VLAN Configuration Example
```json
{
  "vlan_id": 100,
  "name": "CORP_DATA",
  "description": "Corporate Data VLAN",
  "admin_state": "up",
  "ip_address": "192.168.100.1/24",
  "dhcp_helper": ["192.168.1.10"]
}
```

---

## 5. Bulk Configuration Operations

### Bulk Device Configuration
```
POST   /configuration/bulk/apply          # Apply config to multiple devices
GET    /configuration/bulk/status/{job_id} # Check bulk operation status
POST   /configuration/bulk/rollback       # Rollback bulk changes
```

### Bulk Operation Example
```json
{
  "operation": "update_vlan",
  "devices": ["AP001", "AP002", "AP003"],
  "configuration": {
    "vlan_id": 200,
    "ssid": "Guest_Network",
    "security": "WPA2-PSK"
  },
  "rollback_on_failure": true
}
```

---

## 6. Configuration Backup and Restore

### Automated Backup APIs
```
GET    /configuration/backups                    # List all backups
POST   /configuration/backups                    # Create backup
GET    /configuration/backups/{backup_id}       # Download backup
POST   /configuration/backups/{backup_id}/restore # Restore from backup
DELETE /configuration/backups/{backup_id}       # Delete backup
```

### Backup Scheduling
```json
{
  "schedule": "daily",
  "time": "02:00",
  "retention_days": 30,
  "devices": ["all"],
  "backup_type": "running_config"
}
```

---

## 7. Configuration Compliance

### Compliance Checking APIs
```
GET    /configuration/compliance/policies       # List compliance policies
POST   /configuration/compliance/scan           # Run compliance scan
GET    /configuration/compliance/reports        # Get compliance reports
POST   /configuration/compliance/remediate      # Auto-remediate violations
```

### Compliance Policy Example
```json
{
  "policy_name": "Security_Baseline",
  "rules": [
    {
      "rule": "ssh_timeout",
      "expected_value": "600",
      "severity": "high"
    },
    {
      "rule": "snmp_community",
      "expected_value": "!= public",
      "severity": "critical"
    }
  ]
}
```

---

## 8. Access Control and Port Security

### Dynamic Port Configuration
```
GET    /configuration/ports                     # List port configurations
PUT    /configuration/ports/{port_id}           # Configure port settings
POST   /configuration/ports/{port_id}/security  # Set port security
GET    /configuration/access-control            # Access control policies
```

### Port Security Example
```json
{
  "port_id": "1/1/1",
  "access_control": {
    "mac_address_limit": 1,
    "violation_action": "shutdown",
    "aging_time": 1440
  },
  "vlan_assignment": {
    "default_vlan": 100,
    "guest_vlan": 200,
    "auth_fail_vlan": 999
  }
}
```

---

## 9. Device Onboarding Configuration

### Zero Touch Provisioning
```
POST   /onboarding/devices                     # Add device for provisioning
GET    /onboarding/devices/{serial}            # Get provisioning status
PUT    /onboarding/devices/{serial}/config     # Set initial configuration
POST   /onboarding/devices/{serial}/activate   # Activate device
```

### Onboarding Workflow
```json
{
  "serial_number": "ABC123456789",
  "device_type": "AP",
  "site": "Building_A_Floor_1",
  "template": "corp_ap_template",
  "custom_config": {
    "hostname": "AP-BA-F1-001",
    "location": "Conference Room A"
  }
}
```

---

## 10. Configuration Validation

### Pre-deployment Validation
```
POST   /configuration/validate                 # Validate configuration
GET    /configuration/validate/{job_id}        # Get validation results
POST   /configuration/test-deployment          # Test configuration deployment
```

---

## n8n Workflow Integration Patterns

### 1. Configuration Backup Workflow
```javascript
// Schedule: Daily at 2 AM
// Trigger: Schedule Trigger (n8n-nodes-base.scheduleTrigger)
// Process: 
//   1. Get device list from Central
//   2. For each device, create backup
//   3. Store backup with timestamp
//   4. Send summary notification
```

### 2. Compliance Monitoring Workflow
```javascript
// Schedule: Weekly compliance scan
// Trigger: Schedule Trigger
// Process:
//   1. Run compliance scan on all devices
//   2. Generate compliance report
//   3. Identify violations
//   4. Create remediation tickets
//   5. Send executive summary
```

### 3. Bulk Configuration Deployment
```javascript
// Trigger: Webhook or Manual
// Process:
//   1. Validate configuration changes
//   2. Create configuration backup
//   3. Apply changes in batches
//   4. Verify deployment success
//   5. Rollback on failure
//   6. Send deployment report
```

### 4. Zero Touch Provisioning
```javascript
// Trigger: Webhook from device activation
// Process:
//   1. Receive device serial number
//   2. Lookup device in inventory
//   3. Apply appropriate template
//   4. Configure device-specific settings
//   5. Activate device
//   6. Verify connectivity
//   7. Send activation notification
```

---

## Security Considerations

### API Access Control
- Use least privilege principles
- Implement role-based access control
- Regular credential rotation
- Audit all configuration changes

### Change Management
- Always backup before changes
- Implement approval workflows
- Test in staging environment
- Maintain change logs

### Validation and Testing
- Validate configurations before deployment
- Test connectivity after changes
- Monitor for configuration drift
- Implement rollback procedures

---

## Rate Limits and Best Practices

### API Rate Limits
| API | Rate Limit | Best Practice |
|-----|------------|---------------|
| Central | 100 req/min | Batch operations, use webhooks |
| AOS-CX | Device specific | Connection pooling, session reuse |
| EdgeConnect | 10 req/sec | Queue management, async operations |

### Performance Optimization
- Use bulk operations when available
- Implement connection pooling
- Cache frequently accessed data
- Use asynchronous processing for large operations

---

**Last Updated**: January 2025  
**Version**: 1.0
# AOS-CX Configuration Management - Master Usage Guide

## 🎯 Overview
Complete automation suite for HPE Aruba AOS-CX switch configuration management using n8n workflows. This guide provides comprehensive instructions for deploying, configuring, and operating all workflow components.

## 📁 Project Structure
```
aos-cx-config-management/
├── README.md                           # Project overview
├── MASTER_USAGE_GUIDE.md              # This comprehensive guide
├── config/                            # Configuration files
│   ├── parameters.json                # Workflow parameters
│   └── credentials.md                 # Credential setup guide
├── docs/                              # Documentation
│   ├── error-handling-framework.md   # Error handling & rollback
│   └── validation-compliance-framework.md # Validation & compliance
├── tests/                             # Testing framework
│   ├── sample-data.json              # Test data
│   ├── comprehensive-test-suite.md   # Complete test suite
│   ├── vlan-test-scenarios.json      # VLAN testing
│   ├── interface-test-scenarios.json # Interface testing
│   ├── policy-test-scenarios.json    # Policy testing
│   └── backup-restore-test-scenarios.json # Backup testing
├── versions/                          # Version history
├── backups/                          # Configuration backups
└── workflows/                        # n8n workflow files
    ├── aos-cx-vlan-management-workflow.json
    ├── aos-cx-interface-configuration-workflow.json
    ├── aos-cx-policy-deployment-workflow.json
    └── aos-cx-backup-restore-workflow.json
```

## 🚀 Quick Start Guide

### 1. Prerequisites
```bash
# Required infrastructure
✅ n8n instance running at http://192.168.40.100:8006
✅ AOS-CX switches with REST API enabled
✅ Network connectivity to switch management interfaces
✅ Valid credentials (username/password or API tokens)
✅ Slack workspace for notifications (optional)
```

### 2. Import Workflows
1. Access n8n at http://192.168.40.100:8006
2. Navigate to Workflows → Import from file
3. Import each workflow JSON file from the `/workflows/` directory:
   - `aos-cx-vlan-management-workflow.json`
   - `aos-cx-interface-configuration-workflow.json`
   - `aos-cx-policy-deployment-workflow.json`
   - `aos-cx-backup-restore-workflow.json`

### 3. Configure Credentials
```bash
# Step 1: Create AOS-CX API credentials in n8n
Name: AOS-CX-API-Auth
Type: HTTP Basic Auth
Username: admin
Password: [your_switch_password]

# Step 2: Create Slack credentials (optional)
Name: Slack-Notifications
Type: Slack
Token: [your_slack_bot_token]
```

### 4. Test Connectivity
```bash
# Test VLAN workflow
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list",
    "switch_ip": "192.168.1.100"
  }'
```

## 🔧 Workflow Operations

### VLAN Management
**Webhook**: `http://192.168.40.100:8006/webhook/aos-cx-vlan`

#### Create VLAN
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create",
    "switch_ip": "192.168.1.100",
    "vlan_id": 100,
    "vlan_name": "USER_DATA",
    "description": "User data VLAN",
    "admin_state": "up"
  }'
```

#### List All VLANs
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list",
    "switch_ip": "192.168.1.100"
  }'
```

#### Update VLAN
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "update",
    "switch_ip": "192.168.1.100",
    "vlan_id": 100,
    "description": "Updated user data VLAN"
  }'
```

#### Delete VLAN
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "delete",
    "switch_ip": "192.168.1.100",
    "vlan_id": 100
  }'
```

### Interface Configuration
**Webhook**: `http://192.168.40.100:8006/webhook/aos-cx-interface-config`

#### Configure Access Port
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-interface-config" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "configure_access",
    "switch_ip": "192.168.1.100",
    "interface_name": "1/1/1",
    "vlan_tag": 100,
    "description": "Employee workstation",
    "admin_state": "up",
    "port_security_enable": true,
    "max_mac_addresses": 1
  }'
```

#### Configure Trunk Port
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-interface-config" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "configure_trunk",
    "switch_ip": "192.168.1.100",
    "interface_name": "1/1/24",
    "vlan_trunks": [100, 200, 300],
    "native_vlan_tag": 1,
    "description": "Uplink to distribution switch",
    "admin_state": "up"
  }'
```

#### List All Interfaces
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-interface-config" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list",
    "switch_ip": "192.168.1.100"
  }'
```

### Policy Deployment
**Webhook**: `http://192.168.40.100:8006/webhook/aos-cx-policy`

#### Create Security ACL (using template)
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-policy" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_acl",
    "switch_ip": "192.168.1.100",
    "acl_name": "SECURITY_BASIC",
    "template": "security_basic"
  }'
```

#### Create Custom ACL
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-policy" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_acl",
    "switch_ip": "192.168.1.100",
    "acl_name": "CUSTOM_SECURITY",
    "acl_type": "ipv4",
    "rules": [
      {
        "sequence_number": 10,
        "action": "deny",
        "protocol": "tcp",
        "src_ip": "any",
        "dst_port": "22",
        "comment": "Block SSH from external"
      },
      {
        "sequence_number": 20,
        "action": "permit",
        "protocol": "any",
        "comment": "Allow all other traffic"
      }
    ]
  }'
```

#### Apply ACL to Interface
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-policy" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "apply_to_interface",
    "switch_ip": "192.168.1.100",
    "acl_name": "SECURITY_BASIC",
    "interface_name": "1/1/1",
    "direction": "in"
  }'
```

### Backup & Restore
**Webhook**: `http://192.168.40.100:8006/webhook/aos-cx-backup-restore`

#### Create Configuration Backup
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "backup",
    "switch_ip": "192.168.1.100",
    "backup_type": "running",
    "backup_name": "daily_backup_2025_01_16",
    "compression_enabled": true
  }'
```

#### List Available Backups
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list_backups",
    "switch_ip": "192.168.1.100"
  }'
```

#### Restore Configuration
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "restore",
    "switch_ip": "192.168.1.100",
    "restore_file": "daily_backup_2025_01_16.json",
    "compare_configs": true
  }'
```

## 🔍 Monitoring & Troubleshooting

### Workflow Execution Monitoring
```bash
# Check workflow status in n8n
1. Navigate to Executions in n8n interface
2. Filter by workflow name
3. Review execution details and logs
4. Check error messages and retry attempts
```

### Common Issues & Solutions

#### 1. Authentication Failures (401/403)
```bash
# Symptoms: HTTP 401/403 errors
# Solution: Verify credentials
curl -k -u admin:password \
  "https://192.168.1.100/rest/v10.08/system"

# Update credentials in n8n if needed
```

#### 2. Network Connectivity Issues
```bash
# Symptoms: Timeout errors
# Solution: Test connectivity
ping 192.168.1.100
telnet 192.168.1.100 443

# Check switch REST API status
ssh admin@192.168.1.100
show web-ui
```

#### 3. VLAN Already Exists (409 Conflict)
```bash
# Symptoms: HTTP 409 when creating VLANs
# Solution: Check existing VLANs first
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -d '{"operation": "list", "switch_ip": "192.168.1.100"}'
```

#### 4. Interface Configuration Failures
```bash
# Symptoms: Interface config not applied
# Solution: Verify interface exists and format
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-interface-config" \
  -d '{"operation": "list", "switch_ip": "192.168.1.100"}'
```

### Logging and Debugging
```bash
# Enable debug mode in workflows
1. Edit workflow in n8n
2. Add "debug": true to webhook parameters
3. Check detailed logs in execution view

# n8n execution logs location
/Users/jeangiet/.n8n/logs/
```

## 📊 Performance Optimization

### Batch Operations
```bash
# Process multiple VLANs efficiently
for vlan_id in {100..110}; do
  curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
    -d "{
      \"operation\": \"create\",
      \"switch_ip\": \"192.168.1.100\",
      \"vlan_id\": $vlan_id,
      \"vlan_name\": \"BATCH_VLAN_$vlan_id\"
    }" &
done
wait
```

### Parallel Processing
```python
# Python example for concurrent operations
import concurrent.futures
import requests

def create_vlan(vlan_id):
    payload = {
        "operation": "create",
        "switch_ip": "192.168.1.100",
        "vlan_id": vlan_id,
        "vlan_name": f"PARALLEL_VLAN_{vlan_id}"
    }
    return requests.post(
        "http://192.168.40.100:8006/webhook/aos-cx-vlan",
        json=payload
    )

# Process VLANs in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(create_vlan, i) for i in range(100, 110)]
    results = [future.result() for future in futures]
```

## 🔐 Security Best Practices

### Credential Management
```bash
# Use n8n credential store (never hardcode)
✅ Store in n8n credentials
❌ Hardcode in workflows
❌ Include in API calls

# Regular credential rotation
1. Update switch passwords monthly
2. Update n8n credentials accordingly
3. Test workflows after credential updates
```

### Network Security
```bash
# Switch configuration
switch(config)# https-server rest access-mode read-write
switch(config)# https-server vrf mgmt
switch(config)# ip access-list standard API_ACCESS
switch(config-acl-std)# permit host 192.168.40.100
```

### Input Validation
```bash
# All workflows include validation
✅ IP address format validation
✅ VLAN ID range checking (1-4094)
✅ Interface name pattern matching
✅ Parameter type validation
```

## 📈 Advanced Usage

### Automation Scripts
```bash
#!/bin/bash
# Daily maintenance script

# Create backup
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -d '{
    "operation": "backup",
    "switch_ip": "192.168.1.100",
    "backup_name": "daily_'$(date +%Y%m%d)'"
  }'

# Check configuration compliance
# (Custom compliance checking logic here)

# Clean up old backups (>30 days)
# (Cleanup logic here)
```

### Integration Examples
```python
# ServiceNow integration example
def create_change_request(switch_ip, operation, details):
    # Create ServiceNow change request
    change_data = {
        "short_description": f"AOS-CX {operation} on {switch_ip}",
        "description": details,
        "type": "normal",
        "state": "new"
    }
    # Submit to ServiceNow API
    
# Monitoring integration
def update_monitoring_system(switch_ip, config_changes):
    # Update monitoring baselines
    # Adjust alerting thresholds
    # Document configuration changes
```

## 📝 Change Management

### Configuration Change Process
1. **Planning**: Document intended changes
2. **Validation**: Use test switches first
3. **Backup**: Create configuration backup
4. **Implementation**: Execute workflows
5. **Verification**: Confirm changes applied
6. **Documentation**: Update network documentation

### Rollback Procedures
```bash
# Emergency rollback
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -d '{
    "operation": "restore",
    "switch_ip": "192.168.1.100",
    "restore_file": "last_known_good_backup.json"
  }'
```

## 🔄 Maintenance

### Regular Tasks
- [ ] Weekly backup verification
- [ ] Monthly credential rotation
- [ ] Quarterly compliance audit
- [ ] Semi-annual disaster recovery testing

### Health Checks
```bash
# Daily health check script
#!/bin/bash
for switch in 192.168.1.100 192.168.1.101; do
  echo "Checking $switch..."
  curl -s -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
    -d "{\"operation\": \"list\", \"switch_ip\": \"$switch\"}" \
    | jq '.status // "ERROR"'
done
```

## 📞 Support & Resources

### Documentation Links
- [Project README](./README.md)
- [Error Handling Framework](./docs/error-handling-framework.md)
- [Validation & Compliance](./docs/validation-compliance-framework.md)
- [Test Suite](./tests/comprehensive-test-suite.md)

### Troubleshooting Resources
- **n8n Documentation**: https://docs.n8n.io/
- **AOS-CX API Reference**: HPE Aruba documentation
- **Project Issues**: Check workflow execution logs

### Contact Information
- **Project Lead**: Network Automation Team
- **Emergency Contact**: Network Operations Center
- **Documentation Updates**: network-team@company.com

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] n8n instance configured and accessible
- [ ] Switch REST API enabled and tested
- [ ] Credentials configured in n8n
- [ ] Network connectivity verified
- [ ] Test switches identified for validation

### Deployment
- [ ] Import all workflow JSON files
- [ ] Configure workflow parameters
- [ ] Test each workflow individually
- [ ] Run integration test suite
- [ ] Verify error handling and rollback

### Post-Deployment
- [ ] Document production switch inventory
- [ ] Set up monitoring and alerting
- [ ] Train operations team on workflows
- [ ] Establish backup and maintenance schedule
- [ ] Create operational runbooks

This master guide provides everything needed to successfully deploy and operate the AOS-CX configuration management automation suite.
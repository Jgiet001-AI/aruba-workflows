# AOS-CX Interface Configuration Workflow

## Overview

This comprehensive n8n workflow automates interface/port configuration for HPE Aruba AOS-CX switches, providing complete CRUD operations with built-in templates, validation, error handling, and rollback capabilities.

## Features

### ✅ **Complete Interface Operations**
- **List**: Get all interfaces on the switch
- **Read**: Get specific interface configuration  
- **Update**: Modify interface settings
- **Configure Access**: Apply access port template
- **Configure Trunk**: Apply trunk port template

### ✅ **Built-in Port Templates**
- **Access Port**: Single VLAN access configuration
- **Trunk Port**: Multi-VLAN trunk configuration  
- **Server Port**: High-performance server connection template
- **Wireless AP Port**: PoE-enabled access point template

### ✅ **Advanced Features**
- **Input Validation**: Comprehensive parameter validation
- **Error Handling**: Smart error categorization and recovery
- **Configuration Rollback**: Automatic rollback on critical failures
- **Real-time Verification**: Post-configuration validation
- **Slack Notifications**: Success/failure alerts with detailed information

## Workflow Structure

```
Webhook Trigger → Input Validation → Operation Router
    ↓
┌─── List Interfaces ────┐
├─── Read Interface ─────┤
├─── Update Interface ───┤ → Verify → Success Notification
├─── Access Template ────┤     ↓
└─── Trunk Template ─────┘   Error → Rollback → Error Notification
```

## API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/rest/v10.08/system/interfaces` | GET | List all interfaces |
| `/rest/v10.08/system/interfaces/{interface_name}` | GET | Get specific interface |
| `/rest/v10.08/system/interfaces/{interface_name}` | PUT | Update interface configuration |
| `/rest/v10.08/system/interfaces` | POST | Create interface (for LAGs) |

## Input Parameters

### Required Parameters
```json
{
  "operation": "read|update|list|configure_access|configure_trunk",
  "switch_ip": "192.168.1.100",
  "interface_name": "1/1/1"  // Not required for 'list' operation
}
```

### Optional Parameters
```json
{
  "admin_state": "up|down",
  "description": "Interface description",
  "vlan_mode": "access|trunk",
  "vlan_tag": 100,                    // For access mode
  "vlan_trunks": [100, 200, 300],     // For trunk mode
  "native_vlan_tag": 1,               // For trunk mode
  "port_security_enable": true,
  "max_mac_addresses": 1,
  "poe_enable": true,                 // For PoE-capable ports
  "speed": "auto|10|100|1000|10000",
  "duplex": "auto|half|full"
}
```

## Interface Name Formats

| Format | Example | Description |
|--------|---------|-------------|
| Physical Port | `1/1/1` | Slot/Module/Port format |
| LAG Interface | `lag1` | Link Aggregation Group |
| VLAN Interface | `vlan100` | VLAN interface |

## Port Templates

### 1. Access Port Template
```json
{
  "operation": "configure_access",
  "interface_name": "1/1/5",
  "switch_ip": "192.168.1.100",
  "vlan_tag": 100,
  "admin_state": "up",
  "description": "Employee workstation",
  "port_security_enable": true,
  "max_mac_addresses": 1,
  "poe_enable": false
}
```

**Applied Configuration:**
- VLAN mode: Access
- Single VLAN assignment
- Port security (optional)
- Auto speed/duplex
- PoE configuration (optional)

### 2. Trunk Port Template
```json
{
  "operation": "configure_trunk",
  "interface_name": "1/1/24",
  "switch_ip": "192.168.1.100",
  "vlan_trunks": [10, 20, 30, 100],
  "native_vlan_tag": 1,
  "admin_state": "up",
  "description": "Uplink to core switch"
}
```

**Applied Configuration:**
- VLAN mode: Trunk
- Multiple VLAN trunking
- Native VLAN configuration
- Higher MAC address limits
- Auto speed/duplex

### 3. Server Port Template
```json
{
  "operation": "configure_access",
  "interface_name": "1/1/48",
  "switch_ip": "192.168.1.100",
  "vlan_tag": 200,
  "admin_state": "up",
  "description": "Server connection",
  "port_security_enable": false,
  "speed": "1000",
  "duplex": "full"
}
```

**Applied Configuration:**
- High-performance settings
- Dedicated server VLAN
- Port security disabled
- Fixed speed/duplex

### 4. Wireless AP Port Template
```json
{
  "operation": "configure_access",
  "interface_name": "1/1/12",
  "switch_ip": "192.168.1.100",
  "vlan_tag": 150,
  "admin_state": "up",
  "description": "Wireless Access Point",
  "poe_enable": true,
  "port_security_enable": false
}
```

**Applied Configuration:**
- Access port for management VLAN
- PoE enabled for AP power
- Port security disabled for flexibility

## Usage Examples

### Example 1: List All Interfaces
```bash
curl -X POST http://192.168.40.100:8006/webhook/aos-cx-interface-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list",
    "switch_ip": "192.168.1.100"
  }'
```

### Example 2: Configure Access Port
```bash
curl -X POST http://192.168.40.100:8006/webhook/aos-cx-interface-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "configure_access",
    "interface_name": "1/1/5",
    "switch_ip": "192.168.1.100",
    "vlan_tag": 100,
    "description": "Employee workstation port",
    "port_security_enable": true,
    "max_mac_addresses": 1
  }'
```

### Example 3: Configure Trunk Port
```bash
curl -X POST http://192.168.40.100:8006/webhook/aos-cx-interface-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "configure_trunk",
    "interface_name": "1/1/24",
    "switch_ip": "192.168.1.100",
    "vlan_trunks": [10, 20, 30, 100],
    "native_vlan_tag": 1,
    "description": "Uplink to distribution switch"
  }'
```

### Example 4: Read Interface Status
```bash
curl -X POST http://192.168.40.100:8006/webhook/aos-cx-interface-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "read",
    "interface_name": "1/1/5",
    "switch_ip": "192.168.1.100"
  }'
```

## Error Handling

### Error Categories

| Error Type | HTTP Code | Description | Rollback |
|------------|-----------|-------------|----------|
| AUTHENTICATION | 401/403 | Invalid credentials | No |
| NOT_FOUND | 404 | Interface doesn't exist | No |
| VALIDATION | 400 | Invalid parameters | No |
| SERVER_ERROR | 500+ | Switch internal error | Yes |
| TIMEOUT | - | Request timeout | Yes |
| CONNECTIVITY | - | Network issues | Yes |

### Automatic Rollback

When `rollback_required` is true, the workflow automatically:
1. Brings the interface administratively down
2. Sets a rollback description with timestamp
3. Resets to safe default configuration (access mode, VLAN 1)
4. Disables port security to prevent lockouts
5. Sends rollback notification to Slack

## Validation Rules

### Interface Name Validation
- Physical ports: Must match `\d+/\d+/\d+` pattern (e.g., "1/1/1")
- LAG interfaces: Must match `lag\d+` pattern (e.g., "lag1")
- VLAN interfaces: Must match `vlan\d+` pattern (e.g., "vlan100")

### VLAN Validation
- VLAN IDs must be between 1-4094
- Access mode requires single `vlan_tag`
- Trunk mode requires `vlan_trunks` array
- Native VLAN must be valid VLAN ID

### Port Security Validation
- When enabled, `max_mac_addresses` must be 1-1024
- Recommended: 1 for access ports, 10+ for trunk ports

## Notification System

### Success Notifications (Slack: #network-config)
```
✅ AOS-CX Interface Configuration Success
Interface: 1/1/5
Switch: 192.168.1.100
Operation: configure_access
Template: access_port
VLAN Config: access: 100
Admin State: up
Port Security: Enabled
```

### Error Notifications (Slack: #network-alerts)
```
🚨 AOS-CX Interface Configuration Error
Interface: 1/1/5
Switch: 192.168.1.100
Operation: configure_access
Error Type: VALIDATION
Severity: MEDIUM
Rollback Required: NO
Error Message: Invalid VLAN ID 5000. VLANs must be between 1-4094
```

### Rollback Notifications (Slack: #network-alerts)
```
🔄 Interface Configuration Rollback Executed
Interface: 1/1/5
Switch: 192.168.1.100
Original Operation: configure_trunk
Rollback Status: SUCCESS
Rollback Reason: Server timeout during configuration
```

## Monitoring and Verification

### Post-Configuration Verification
After successful configuration, the workflow:
1. Queries the interface to verify applied settings
2. Checks administrative and operational status
3. Confirms VLAN assignments
4. Validates port security settings

### Configuration Tracking
Each operation generates a comprehensive response:
```json
{
  "success": true,
  "workflow_id": "aos-cx-interface-config",
  "timestamp": "2025-01-16T10:30:00Z",
  "operation": "configure_access",
  "interface": "1/1/5",
  "switch_ip": "192.168.1.100",
  "configuration": {
    "template_used": "access_port",
    "admin_state": "up",
    "vlan_mode": "access",
    "vlan_config": 100,
    "port_security": true
  },
  "verification": {
    "verified": true,
    "current_status": "up",
    "operational_status": "up"
  }
}
```

## Security Considerations

### Credential Management
- Uses n8n credential store for switch authentication
- Supports username/password and token-based authentication
- Credentials are never logged or exposed

### Port Security
- Template configurations include port security options
- Access ports default to 1 MAC address
- Trunk ports allow higher MAC address limits
- Rollback disables port security to prevent lockouts

### Access Control
- Webhook requires proper authentication
- Operations are logged with timestamps
- All configuration changes are tracked

## Installation and Setup

### 1. Import Workflow
```bash
# Import the workflow into n8n
cp aos-cx-interface-configuration-workflow.json /path/to/n8n/workflows/
```

### 2. Configure Credentials
Create AOS-CX API credentials in n8n:
```
Credential Type: HTTP Header Auth
Name: arubaAosCxApi
Header: Authorization
Value: Bearer YOUR_TOKEN
```

### 3. Configure Slack Notifications
Set up Slack webhook credentials:
```
Credential Type: Slack API
Name: slack-webhook-config
Token: xoxb-your-slack-bot-token
```

### 4. Test Workflow
```bash
# Test with list operation
curl -X POST http://192.168.40.100:8006/webhook/aos-cx-interface-config \
  -H "Content-Type: application/json" \
  -d '{"operation": "list", "switch_ip": "192.168.1.100"}'
```

## Troubleshooting

### Common Issues

**1. Authentication Failures**
- Verify AOS-CX API credentials
- Check token expiration
- Confirm API access is enabled on switch

**2. Interface Not Found**
- Verify interface name format
- Check if interface exists on switch
- Confirm switch IP address

**3. VLAN Assignment Failures**
- Ensure VLANs exist on switch
- Check VLAN ID ranges (1-4094)
- Verify trunk VLAN configuration

**4. Port Security Issues**
- Check MAC address limits
- Verify port security capabilities
- Review security policy settings

### Debug Mode
Enable detailed logging by setting environment variable:
```bash
N8N_LOG_LEVEL=debug
```

## Integration with Other Workflows

### VLAN Management Integration
This workflow pairs with the AOS-CX VLAN Management workflow:
1. Create VLANs first using VLAN workflow
2. Assign interfaces to VLANs using this workflow
3. Verify end-to-end connectivity

### Monitoring Integration
- Interface status can feed into monitoring workflows
- Port utilization triggers can call this workflow
- Configuration drift detection can trigger corrections

## API Rate Limits

### AOS-CX API Limits
- Default: 100 requests per minute
- Workflow includes retry logic with exponential backoff
- Batch operations recommended for multiple interfaces

### Best Practices
- Use bulk operations when possible
- Implement delays between requests
- Monitor API usage patterns

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-16 | Initial release with full CRUD operations |
| | | Templates for access and trunk ports |
| | | Error handling and rollback capabilities |
| | | Slack notifications and verification |

## Support and Maintenance

### Regular Maintenance
- **Weekly**: Review error logs and notification channels
- **Monthly**: Update credentials and validate API access
- **Quarterly**: Review and update port templates

### Support Contacts
- **Primary**: Network Operations Team
- **Secondary**: Claude Code Development Team
- **Escalation**: HPE Aruba Support

---

*This workflow is part of the HPE Aruba Network Automation project. For additional documentation and workflows, see the [project README](../README.md).*
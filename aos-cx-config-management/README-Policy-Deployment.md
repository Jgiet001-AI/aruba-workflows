# AOS-CX Policy Deployment Workflow

## Overview

The AOS-CX Policy Deployment workflow provides comprehensive network policy management for HPE Aruba AOS-CX switches. It supports Access Control Lists (ACLs) and Quality of Service (QoS) policy creation, modification, deletion, and deployment across network interfaces.

## Features

### Core Operations
- **ACL Management**: Create, update, delete, and list ACLs
- **Interface Policy Application**: Apply ACLs to specific interfaces with directional control
- **QoS Policy Management**: Create and configure QoS policies with class-based traffic control
- **Policy Templates**: Pre-built templates for common security and QoS scenarios
- **Input Validation**: Comprehensive parameter validation and error checking
- **Error Handling**: Smart error categorization with automatic rollback capabilities
- **Notifications**: Real-time alerts via Slack and email for success/failure scenarios

### Supported Policy Types
- **Security ACLs**: IPv4, IPv6, and MAC-based access control
- **Network Segmentation**: VLAN and subnet isolation policies
- **QoS Policies**: Traffic classification, marking, and prioritization
- **Guest Network Policies**: Isolated internet access with private network blocking
- **IoT Device Policies**: Restricted connectivity for IoT devices

## API Endpoints Used

### ACL Management
- `GET /rest/v10.08/system/acls` - List all ACLs
- `GET /rest/v10.08/system/acls/{acl_name}` - Get specific ACL details
- `POST /rest/v10.08/system/acls` - Create new ACL
- `PUT /rest/v10.08/system/acls/{acl_name}` - Update existing ACL
- `DELETE /rest/v10.08/system/acls/{acl_name}` - Delete ACL

### Interface Configuration
- `PUT /rest/v10.08/system/interfaces/{interface_name}` - Apply ACL to interface

### QoS Management
- `GET /rest/v10.08/system/qos` - Get QoS configuration
- `PUT /rest/v10.08/system/qos` - Update QoS configuration

## Input Parameters

### Required Parameters
- `operation`: Policy operation to perform
- `switch_ip`: IP address of the target AOS-CX switch

### Operation Types
- `create_acl`: Create a new ACL
- `update_acl`: Update an existing ACL
- `delete_acl`: Delete an ACL
- `list_acls`: List all configured ACLs
- `apply_to_interface`: Apply ACL to a specific interface
- `create_qos_policy`: Create or update QoS policy
- `get_qos`: Retrieve current QoS configuration

### ACL Parameters
- `acl_name`: Name of the ACL (required for ACL operations)
- `acl_type`: Type of ACL (`ipv4`, `ipv6`, `mac`) - default: `ipv4`
- `rules`: Array of ACL rules with sequence, action, protocol, source, destination
- `interface_name`: Interface to apply policy (e.g., "1/1/1")
- `direction`: Traffic direction (`in`, `out`) - default: `in`

### QoS Parameters
- `qos_policy_name`: Name of the QoS policy
- `qos_rules`: QoS configuration with classes and policies

### Template Support
- `template`: Pre-built policy template name
  - `security_basic`: Basic security ACL
  - `guest_network`: Guest network isolation
  - `iot_security`: IoT device restrictions
  - `qos_voice_priority`: Voice traffic prioritization

## Usage Examples

### 1. Create Basic Security ACL

```json
{
  "operation": "create_acl",
  "switch_ip": "192.168.1.100",
  "acl_name": "SECURITY_BASIC",
  "acl_type": "ipv4",
  "template": "security_basic"
}
```

### 2. Create Custom ACL with Rules

```json
{
  "operation": "create_acl",
  "switch_ip": "192.168.1.100",
  "acl_name": "CUSTOM_SECURITY",
  "acl_type": "ipv4",
  "rules": [
    {
      "sequence": 10,
      "action": "deny",
      "protocol": "tcp",
      "source": "any",
      "destination": "192.168.10.0/24",
      "dst_port": "22",
      "comment": "Block SSH to server subnet"
    },
    {
      "sequence": 20,
      "action": "permit",
      "protocol": "tcp",
      "source": "any",
      "destination": "any",
      "dst_port": "80",
      "comment": "Allow HTTP"
    },
    {
      "sequence": 30,
      "action": "permit",
      "protocol": "tcp",
      "source": "any",
      "destination": "any",
      "dst_port": "443",
      "comment": "Allow HTTPS"
    }
  ]
}
```

### 3. Apply ACL to Interface

```json
{
  "operation": "apply_to_interface",
  "switch_ip": "192.168.1.100",
  "acl_name": "SECURITY_BASIC",
  "acl_type": "ipv4",
  "interface_name": "1/1/1",
  "direction": "in"
}
```

### 4. Create QoS Policy

```json
{
  "operation": "create_qos_policy",
  "switch_ip": "192.168.1.100",
  "qos_policy_name": "VOICE_PRIORITY",
  "template": "qos_voice_priority"
}
```

### 5. List All ACLs

```json
{
  "operation": "list_acls",
  "switch_ip": "192.168.1.100"
}
```

### 6. Delete ACL

```json
{
  "operation": "delete_acl",
  "switch_ip": "192.168.1.100",
  "acl_name": "OLD_POLICY"
}
```

## Policy Templates

### Security Templates

#### Basic Security ACL (`security_basic`)
- Blocks SSH (port 22) from external sources
- Blocks Telnet (port 23)
- Blocks RPC (port 135)
- Allows HTTP (port 80) and HTTPS (port 443)
- Default deny for all other traffic

#### Guest Network Policy (`guest_network`)
- Allows DNS resolution (port 53)
- Allows HTTP/HTTPS for internet access
- Blocks access to private network ranges (192.168.x.x, 10.x.x.x)
- Permits general internet access

#### IoT Security Policy (`iot_security`)
- Allows HTTPS for device updates
- Allows NTP for time synchronization
- Allows DNS resolution
- Blocks SSH and Telnet access
- Default deny for security

### QoS Templates

#### Voice Priority QoS (`qos_voice_priority`)
- **Voice Class**: DSCP 46, Priority 7, 30% bandwidth
- **Video Class**: DSCP 34, Priority 5, 40% bandwidth
- **Data Class**: DSCP 0, Priority 1, 30% bandwidth

## Error Handling

### Validation Errors
The workflow performs comprehensive input validation:
- Required parameter checking
- IP address format validation
- ACL name format validation
- Interface name format validation
- Rule structure validation

### API Error Categories
- **Authentication Failed (401)**: Invalid credentials
- **Authorization Failed (403)**: Insufficient permissions
- **Invalid Request (400)**: Malformed request data
- **Resource Not Found (404)**: ACL or interface doesn't exist
- **Resource Conflict (409)**: ACL already exists or interface conflict
- **Validation Failed (422)**: Invalid parameter values
- **Server Error (500)**: Switch internal error

### Rollback Procedures
For critical failures, the workflow supports automatic rollback:

#### ACL Creation Rollback
- Delete partially created ACL
- Verify no interface assignments remain

#### Interface Application Rollback
- Remove ACL from interface
- Restore previous interface configuration

#### QoS Policy Rollback
- Restore previous QoS configuration
- Verify no traffic disruption

## Troubleshooting

### Common Issues

#### Authentication Problems
1. Verify API credentials are correct
2. Check if authentication token has expired
3. Confirm API access is enabled on the switch

#### Invalid Request Errors
1. Review request parameters and format
2. Check ACL name and rule syntax
3. Verify interface name format (e.g., "1/1/1")

#### Resource Conflicts
1. Check if ACL already exists
2. Verify interface is not already configured
3. Review existing policy conflicts

#### Validation Failures
1. Review input validation errors in workflow output
2. Check ACL rule syntax and parameters
3. Verify DSCP and priority values are within valid ranges

### Debugging Steps
1. Check workflow execution logs in n8n
2. Review switch logs for additional details
3. Verify API version compatibility
4. Test API connectivity manually

## Installation

### Prerequisites
- n8n instance running and accessible
- AOS-CX switch with REST API enabled
- Valid API credentials configured in n8n
- Slack/Email integration configured (optional)

### Setup Steps
1. Import the workflow JSON into n8n
2. Configure AOS-CX API credentials
3. Update Slack/Email notification settings
4. Test with a simple operation (e.g., `list_acls`)

### Credential Configuration
Configure the following credential types in n8n:
- **AOS-CX API**: Username/password or token-based authentication
- **Slack**: Webhook URL or API token
- **Email**: SMTP settings for notifications

## Monitoring and Alerts

### Success Notifications
- Slack message with operation summary
- Email report with detailed execution information
- Next steps and recommendations

### Error Notifications
- Slack alert with error details
- Email report with troubleshooting steps
- Rollback information when applicable

### Validation Error Alerts
- Immediate Slack notification for input validation failures
- Detailed parameter error descriptions
- Corrective action recommendations

## Security Considerations

### Access Control
- Use least-privilege API credentials
- Implement proper authentication and authorization
- Regular credential rotation

### Network Security
- Secure API communication (HTTPS)
- Network isolation for management traffic
- Audit trail for all policy changes

### Policy Security
- Validate all ACL rules before deployment
- Test policies in non-production environment
- Implement change approval process

## Performance Optimization

### API Rate Limiting
- Implements retry logic with exponential backoff
- 3 retry attempts with 2-second intervals
- 30-second timeout for API calls

### Batch Operations
- Single workflow can handle multiple operations
- Efficient rule processing and validation
- Optimized API call patterns

## Version History

- **v1.0.0**: Initial release with full ACL and QoS support
- **v1.0.1**: Added policy templates and enhanced error handling
- **v1.0.2**: Improved validation and rollback procedures

## Support

For issues and questions:
- Check n8n workflow execution logs
- Review AOS-CX switch logs
- Refer to HPE Aruba AOS-CX documentation
- Contact network automation team

## Related Workflows

- [AOS-CX VLAN Management](./README.md)
- [AOS-CX Interface Configuration](./README-Interface-Configuration.md)
- Device Health Monitoring
- Configuration Backup and Restore
# AOS-CX VLAN Management Workflow

## Overview

This n8n workflow provides comprehensive VLAN management capabilities for HPE Aruba AOS-CX switches through the REST API. It supports full CRUD (Create, Read, Update, Delete) operations with robust input validation, error handling, and automated notifications.

## Features

- **Complete VLAN Operations**: Create, Read, Update, Delete, and List VLANs
- **Input Validation**: Comprehensive parameter validation with detailed error messages
- **Error Handling**: Smart error detection with rollback capabilities and recovery guidance
- **Notifications**: Real-time success/failure notifications via Slack
- **Monitoring**: Detailed logging and audit trail for all operations
- **Robust Design**: Retry logic, timeout handling, and graceful error recovery

## Workflow Structure

### File Organization
```
aos-cx-config-management/
├── README.md                           # This documentation
├── aos-cx-vlan-management-workflow.json # Main n8n workflow
├── config/
│   ├── credentials.md                  # Credential setup guide
│   └── parameters.json                 # Configuration parameters
├── tests/
│   ├── sample-data.json               # Basic test data
│   └── vlan-test-scenarios.json       # Comprehensive test scenarios
├── docs/                              # Additional documentation
└── versions/                          # Workflow version history
```

## Quick Start

### 1. Prerequisites

- n8n instance running and accessible
- HPE Aruba AOS-CX switch with REST API enabled
- Network connectivity between n8n and switch
- Valid switch credentials with API access
- Slack workspace for notifications (optional)

### 2. Import Workflow

1. Open n8n interface
2. Click **"Import from file"**
3. Select `aos-cx-vlan-management-workflow.json`
4. Save the imported workflow

### 3. Configure Credentials

Set up the following credentials in n8n:

#### AOS-CX API Credentials
- **Name**: `arubaOsCxApi`
- **Type**: HTTP Basic Auth
- **Username**: Your switch username
- **Password**: Your switch password

#### Slack Notifications (Optional)
- **Name**: `slack`
- **Type**: Slack
- **Webhook URL**: Your Slack webhook URL

### 4. Test the Workflow

Use the manual trigger with this sample data:

```json
{
  \"operation\": \"list\",
  \"switch_ip\": \"192.168.1.100\"
}
```

## Usage Guide

### Input Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `operation` | string | Yes | Operation type | `\"create\"`, `\"read\"`, `\"update\"`, `\"delete\"`, `\"list\"` |
| `switch_ip` | string | Yes | Switch IP address | `\"192.168.1.100\"` |
| `vlan_id` | number | Conditional* | VLAN ID (1-4094) | `100` |
| `vlan_name` | string | Conditional** | VLAN name | `\"GUEST_NETWORK\"` |
| `description` | string | No | VLAN description | `\"Guest network for visitors\"` |
| `admin_state` | string | No | Admin state | `\"up\"` (default) or `\"down\"` |

*Required for: create, read, update, delete operations  
**Required for: create, update operations

### Operation Examples

#### List All VLANs
```json
{
  \"operation\": \"list\",
  \"switch_ip\": \"192.168.1.100\"
}
```

#### Read Specific VLAN
```json
{
  \"operation\": \"read\",
  \"switch_ip\": \"192.168.1.100\",
  \"vlan_id\": 100
}
```

#### Create New VLAN
```json
{
  \"operation\": \"create\",
  \"switch_ip\": \"192.168.1.100\",
  \"vlan_id\": 200,
  \"vlan_name\": \"GUEST_NETWORK\",
  \"description\": \"Guest network VLAN\",
  \"admin_state\": \"up\"
}
```

#### Update VLAN
```json
{
  \"operation\": \"update\",
  \"switch_ip\": \"192.168.1.100\",
  \"vlan_id\": 200,
  \"vlan_name\": \"GUEST_WIFI\",
  \"description\": \"Updated guest network\",
  \"admin_state\": \"up\"
}
```

#### Delete VLAN
```json
{
  \"operation\": \"delete\",
  \"switch_ip\": \"192.168.1.100\",
  \"vlan_id\": 200
}
```

## API Endpoints Used

The workflow uses the following AOS-CX REST API endpoints:

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| List VLANs | GET | `/rest/v10.08/system/vlans` | Get all VLANs |
| Read VLAN | GET | `/rest/v10.08/system/vlans/{vlan_id}` | Get specific VLAN |
| Create VLAN | POST | `/rest/v10.08/system/vlans` | Create new VLAN |
| Update VLAN | PUT | `/rest/v10.08/system/vlans/{vlan_id}` | Update existing VLAN |
| Delete VLAN | DELETE | `/rest/v10.08/system/vlans/{vlan_id}` | Remove VLAN |

## Workflow Nodes

### 1. Manual Trigger
- **Purpose**: Initiates the workflow with input parameters
- **Type**: Manual trigger
- **Configuration**: Default settings

### 2. Input Validation
- **Purpose**: Validates all input parameters
- **Type**: JavaScript function
- **Validation Rules**:
  - Required field validation
  - IP address format validation
  - VLAN ID range validation (1-4094)
  - VLAN name format validation
  - Admin state validation

### 3. Operation Router
- **Purpose**: Routes to appropriate operation based on input
- **Type**: Conditional (IF) nodes
- **Logic**: Branches to List, Read, Create, Update, or Delete operations

### 4. HTTP Request Nodes
- **Purpose**: Execute API calls to AOS-CX switch
- **Type**: HTTP Request
- **Configuration**:
  - Authentication: HTTP Basic Auth
  - Timeout: 30 seconds
  - Retry: 3 attempts with 2-second delay
  - Error handling: Never error mode

### 5. Response Processor
- **Purpose**: Processes API responses and handles errors
- **Type**: JavaScript function
- **Features**:
  - Success/failure detection
  - Error categorization
  - Response formatting

### 6. Notification Nodes
- **Purpose**: Send success/failure notifications
- **Type**: Slack nodes
- **Channels**:
  - `#network-automation`: Success notifications
  - `#network-alerts`: Error notifications

### 7. Error Rollback Handler
- **Purpose**: Handles error recovery and rollback logic
- **Type**: JavaScript function
- **Features**:
  - Error analysis
  - Rollback recommendations
  - Manual intervention guidance

## Error Handling

### Validation Errors
- **IP Address Format**: Invalid IP address format
- **Operation Type**: Unsupported operation
- **VLAN ID Range**: VLAN ID outside 1-4094 range
- **Required Fields**: Missing required parameters
- **Name Format**: Invalid VLAN name characters

### API Errors
- **404 Not Found**: VLAN doesn't exist or switch unreachable
- **401/403 Unauthorized**: Authentication or authorization failure
- **409 Conflict**: VLAN already exists (create operation)
- **400 Bad Request**: Invalid request parameters
- **500+ Server Error**: Switch internal error
- **Network Error**: Connection timeout or unreachable

### Error Recovery
1. **Automatic Retry**: 3 attempts with exponential backoff
2. **Error Categorization**: Classify error type for appropriate response
3. **Rollback Logic**: Automated rollback for failed operations (when applicable)
4. **Notifications**: Immediate alerts with recommended actions
5. **Audit Trail**: Complete logging of all operations and errors

## Monitoring and Notifications

### Success Notifications
- Sent to `#network-automation` Slack channel
- Include operation details and results
- Formatted JSON response data
- Timestamp and switch information

### Error Notifications
- Sent to `#network-alerts` Slack channel
- Include error details and recommended actions
- Rollback status information
- Troubleshooting guidance

### Audit Trail
- Complete logging of all operations
- Input parameters and responses
- Error details and recovery actions
- Execution timestamps

## Security Considerations

### Credential Management
- Use n8n credential store (never hardcode)
- Implement least privilege access
- Regular credential rotation
- Secure API token storage

### Network Security
- HTTPS/TLS encryption for all API calls
- Network segmentation for management traffic
- Firewall rules for API access
- VPN or secure network connectivity

### Access Control
- Role-based access to n8n workflows
- Switch user account with minimal required privileges
- Audit logging for all configuration changes
- Approval workflows for critical operations

## Performance Optimization

### Timeout Settings
- API calls: 30-second timeout
- Retry logic: 3 attempts with 2-second delay
- Connection pooling for multiple operations

### Batch Operations
- For multiple VLANs, use separate workflow executions
- Consider rate limiting for switch protection
- Monitor switch CPU/memory during bulk operations

### Caching
- Cache switch connectivity status
- Store frequently accessed VLAN information
- Implement smart refresh intervals

## Troubleshooting

### Common Issues

#### Connection Problems
```
Error: Network error or switch unreachable
Solutions:
- Verify switch IP address
- Check network connectivity
- Ensure REST API is enabled
- Verify firewall rules
```

#### Authentication Failures
```
Error: Authentication failed - check credentials
Solutions:
- Verify username/password in n8n credentials
- Check user privileges on switch
- Ensure API access is enabled
- Verify account is not locked
```

#### VLAN Conflicts
```
Error: VLAN already exists or configuration conflict
Solutions:
- Use read operation to check existing VLANs
- Use update operation instead of create
- Choose different VLAN ID
- Verify VLAN configuration requirements
```

### Debugging Steps

1. **Check Workflow Execution Log**
   - Review each node's execution details
   - Identify failure point in workflow
   - Check input/output data

2. **Verify Switch Connectivity**
   - Test API access with curl or Postman
   - Check switch logs for authentication attempts
   - Verify REST API service status

3. **Validate Input Parameters**
   - Ensure all required fields are provided
   - Check parameter format and ranges
   - Verify operation type spelling

4. **Test Credentials**
   - Manually test switch login
   - Verify API permissions
   - Check account status

## Maintenance

### Regular Tasks
- **Weekly**: Review error logs and success rates
- **Monthly**: Update credentials if required
- **Quarterly**: Review and update notification channels
- **Annually**: Audit security settings and access controls

### Updates and Versioning
- Test all changes in development environment
- Version all workflow modifications
- Document breaking changes
- Maintain backward compatibility when possible

### Backup and Recovery
- Export workflow configurations regularly
- Backup credential configurations (metadata only)
- Document recovery procedures
- Test restore procedures annually

## Support and Documentation

### Additional Resources
- [HPE Aruba AOS-CX REST API Guide](https://developer.arubanetworks.com/)
- [n8n Documentation](https://docs.n8n.io/)
- [Project Planning Document](../PLANNING.md)
- [Task Tracking](../TASKS.md)

### Getting Help
1. Check the troubleshooting section above
2. Review workflow execution logs
3. Test with provided sample data
4. Contact network administration team
5. Submit issues to project repository

### Contributing
- Follow established coding standards
- Update documentation for changes
- Add test scenarios for new features
- Follow security best practices

---

**Last Updated**: January 16, 2025  
**Version**: 1.0.0  
**Maintainer**: Network Automation Team
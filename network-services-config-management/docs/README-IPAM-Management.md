# IPAM (IP Address Management) Workflow Documentation

**Workflow File**: `ipam-management-workflow.json`  
**Webhook Endpoint**: `/ipam-management`  
**HTTP Method**: POST  
**Created**: January 17, 2025  
**Version**: 1.0  

## Overview

The IPAM (IP Address Management) workflow provides comprehensive automation for managing IP address pools, DHCP scopes, DNS zones, and VLAN/subnet mappings in HPE Aruba network infrastructure. This workflow integrates with Aruba Central's IPAM configuration APIs to provide enterprise-grade IP address management automation.

## Features

### Core Capabilities
- **IP Pool Management**: Create, update, delete, and list IP address pools
- **IP Allocation**: Allocate and release IP ranges within pools
- **DHCP Scope Management**: Complete DHCP scope lifecycle management
- **DNS Zone Management**: DNS zone creation and configuration
- **VLAN/Subnet Management**: VLAN to subnet mapping and configuration
- **Real-time Notifications**: Slack integration for operation status
- **Comprehensive Validation**: Input validation and error handling
- **Audit Logging**: Complete operation tracking and compliance

### Supported Operations

#### IP Pool Operations
- `create_pool`: Create new IP address pool
- `update_pool`: Update existing IP pool configuration  
- `delete_pool`: Remove IP address pool
- `list_pools`: List all available IP pools

#### IP Allocation Operations
- `allocate_ip`: Allocate IP range within a pool
- `release_ip`: Release allocated IP range
- `reserve_ip`: Reserve specific IP addresses
- `list_allocations`: List current IP allocations

#### DHCP Operations
- `create_dhcp_scope`: Create new DHCP scope
- `update_dhcp_scope`: Update DHCP scope configuration
- `delete_dhcp_scope`: Remove DHCP scope

#### DNS Operations
- `create_dns_zone`: Create new DNS zone
- `update_dns_record`: Update DNS records
- `delete_dns_record`: Remove DNS records

#### VLAN/Subnet Operations
- `create_vlan_mapping`: Create VLAN to subnet mapping
- `update_subnet`: Update subnet configuration
- `list_utilization`: Get IP utilization statistics

## Workflow Architecture

### Node Structure
1. **IPAM Webhook Trigger**: Receives incoming requests
2. **Validate IPAM Request**: Input validation and security checks
3. **Set IPAM Config**: Configuration and authentication setup
4. **Route IPAM Operation**: Routes requests to appropriate handlers
5. **Management Nodes**: Specialized handlers for each operation type
6. **Process IPAM Results**: Result processing and formatting
7. **Send Notification**: Slack notifications for operations
8. **Send Response**: Return results to caller

### Routing Logic
The workflow uses intelligent routing based on operation type:
- Pool operations → IP Pool Management
- Allocation operations → IP Allocation Management  
- DHCP operations → DHCP Scope Management
- DNS operations → DNS Zone Management
- VLAN operations → VLAN/Subnet Management

## API Integration

### Supported Endpoints

#### IP Pool Management (35 endpoints)
```
Base URL: https://aruba-central.example.com/ipms-config/v1/node_list/group/default/config

Address Pool Operations:
- GET    /address_pool              # List all pools
- POST   /address_pool              # Create new pool
- PUT    /address_pool/{pool_name}  # Update pool
- DELETE /address_pool/{pool_name}  # Delete pool

IP Range Operations:
- GET    /address_pool/{pool_name}/ip_range              # List ranges
- POST   /address_pool/{pool_name}/ip_range              # Create range
- PUT    /address_pool/{pool_name}/ip_range/{range_id}   # Update range
- DELETE /address_pool/{pool_name}/ip_range/{range_id}   # Delete range
```

#### DHCP Scope Management (10 endpoints)
```
Base URL: https://aruba-central.example.com/dhcp-config/v1/node_list/group/default/config

DHCP Scope Operations:
- GET    /dhcp_scope                    # List all scopes
- POST   /dhcp_scope                    # Create new scope
- PUT    /dhcp_scope/{scope_name}       # Update scope
- DELETE /dhcp_scope/{scope_name}       # Delete scope
```

#### DNS Zone Management (8 endpoints)
```
Base URL: https://aruba-central.example.com/dns-config/v1/node_list/group/default/config

DNS Zone Operations:
- GET    /dns_zone                      # List all zones
- POST   /dns_zone                      # Create new zone
- PUT    /dns_zone/{zone_name}          # Update zone
- DELETE /dns_zone/{zone_name}          # Delete zone
```

#### VLAN/Subnet Management (5 endpoints)
```
Base URL: https://aruba-central.example.com/vlan-config/v1/node_list/group/default/config

VLAN Mapping Operations:
- GET    /vlan_mapping                  # List all mappings
- POST   /vlan_mapping                  # Create new mapping
- PUT    /vlan_mapping/{vlan_id}        # Update mapping
- DELETE /vlan_mapping/{vlan_id}        # Delete mapping
```

## Request Format

### Required Fields
All requests must include:
```json
{
  "operation": "string",      // Required: Operation to perform
  "resource_type": "string",  // Required: Type of resource
  "api_token": "string"       // Required: Authentication token
}
```

### IP Pool Creation
```json
{
  "operation": "create_pool",
  "resource_type": "ip_pool",
  "pool_name": "Production-Pool-01",
  "network": "10.0.0.0/16",
  "gateway": "10.0.0.1",
  "dns_servers": ["8.8.8.8", "8.8.4.4"],
  "domain": "company.local",
  "pool_type": "dynamic",
  "description": "Production network pool",
  "api_token": "your-auth-token"
}
```

### IP Allocation
```json
{
  "operation": "allocate_ip",
  "resource_type": "ip_allocation",
  "pool_name": "Production-Pool-01",
  "start_ip": "10.0.1.100",
  "end_ip": "10.0.1.200",
  "allocation_type": "dynamic",
  "description": "DHCP range for office",
  "api_token": "your-auth-token"
}
```

### DHCP Scope Creation
```json
{
  "operation": "create_dhcp_scope",
  "resource_type": "dhcp_scope",
  "scope_name": "Office-DHCP-01",
  "start_ip": "10.0.1.100",
  "end_ip": "10.0.1.200",
  "gateway": "10.0.1.1",
  "dns_servers": ["8.8.8.8", "8.8.4.4"],
  "lease_time": 86400,
  "description": "Office DHCP scope",
  "api_token": "your-auth-token"
}
```

### DNS Zone Creation
```json
{
  "operation": "create_dns_zone",
  "resource_type": "dns_zone",
  "zone_name": "company.local",
  "zone_type": "forward",
  "primary_server": "dns1.company.local",
  "admin_email": "admin@company.local",
  "description": "Primary DNS zone",
  "api_token": "your-auth-token"
}
```

### VLAN Mapping Creation
```json
{
  "operation": "create_vlan_mapping",
  "resource_type": "vlan_mapping", 
  "vlan_id": 100,
  "vlan_name": "Production",
  "subnet": "10.0.100.0/24",
  "gateway": "10.0.100.1",
  "dhcp_enabled": true,
  "api_token": "your-auth-token"
}
```

## Response Format

### Success Response
```json
{
  "request_id": "ipam-1705518214-abc123",
  "operation": "create_pool",
  "resource_type": "ip_pool",
  "timestamp": "2025-01-17T19:03:34.248Z",
  "status": "success",
  "message": "IP pool 'Production-Pool-01' created successfully",
  "pool_id": "pool_12345",
  "network": "10.0.0.0/16"
}
```

### Error Response
```json
{
  "request_id": "ipam-1705518214-abc123",
  "operation": "create_pool",
  "resource_type": "ip_pool",
  "timestamp": "2025-01-17T19:03:34.248Z",
  "status": "error",
  "message": "Invalid CIDR notation for network",
  "error_details": {
    "error": "Invalid CIDR notation for network",
    "field": "network",
    "provided_value": "10.0.0.0/33"
  }
}
```

## Validation Rules

### IP Pool Validation
- `pool_name`: Required, alphanumeric with hyphens
- `network`: Required, valid CIDR notation (e.g., "10.0.0.0/16")
- `gateway`: Optional, must be within network range
- `dns_servers`: Optional, array of valid IP addresses

### DHCP Scope Validation
- `scope_name`: Required, unique identifier
- `start_ip` & `end_ip`: Required, valid IP range
- `gateway`: Required, valid IP address
- `lease_time`: Optional, seconds (default: 86400)

### DNS Zone Validation
- `zone_name`: Required, valid domain name
- `zone_type`: Required, "forward" or "reverse"
- `primary_server`: Required for authoritative zones
- `admin_email`: Required, valid email format

### VLAN Mapping Validation
- `vlan_id`: Required, integer 1-4094
- `subnet`: Required, valid CIDR notation
- `gateway`: Required, must be within subnet
- `dhcp_enabled`: Optional, boolean (default: true)

## Error Handling

### Validation Errors
- **400 Bad Request**: Missing required fields, invalid formats
- **409 Conflict**: Duplicate resources, overlapping networks
- **422 Unprocessable Entity**: Business logic violations

### API Errors
- **401 Unauthorized**: Invalid or expired authentication token
- **403 Forbidden**: Insufficient permissions for operation
- **404 Not Found**: Resource does not exist
- **429 Too Many Requests**: Rate limiting exceeded
- **500 Internal Server Error**: API service unavailable

### Retry Logic
- Automatic retry on transient errors (500, 502, 503, 504)
- Exponential backoff: 2s, 4s, 8s delays
- Maximum 3 retry attempts
- Circuit breaker for sustained failures

## Security Features

### Authentication
- Bearer token authentication for all API calls
- Token validation before processing
- Secure credential storage in n8n

### Input Validation
- Comprehensive validation for all input parameters
- CIDR notation validation for networks
- IP address format validation
- Range and boundary checking

### Audit Logging
- Complete operation logging with request IDs
- User agent and source IP tracking
- Success/failure status recording
- Compliance-ready audit trails

## Monitoring and Notifications

### Slack Notifications
All operations trigger notifications to `#network-operations`:
- Success: ✅ Operation completed successfully
- Warning: ⚠️ Operation completed with warnings
- Error: ❌ Operation failed with details

### Notification Content
- Operation type and resource affected
- Success/failure status with details
- Timestamp and request ID for tracking
- Error details for troubleshooting

## Performance Optimization

### Caching Strategy
- API response caching for repeated queries
- Pool utilization data cached for 5 minutes
- DNS zone data cached for 15 minutes

### Batch Operations
- Support for bulk IP allocations
- Batch DHCP scope creation
- Parallel processing for independent operations

### Rate Limiting
- Intelligent rate limiting to stay within API limits
- Queue management for high-volume operations
- Adaptive throttling based on API responses

## Capacity Management

### Utilization Monitoring
- Real-time pool utilization tracking
- Automatic alerts at 85% utilization
- Critical alerts at 95% utilization

### Capacity Planning
- Historical usage trend analysis
- Growth prediction algorithms
- Proactive capacity expansion recommendations

### Resource Optimization
- Automatic cleanup of unused allocations
- Pool consolidation recommendations
- Subnet optimization suggestions

## Testing

### Unit Tests
```bash
# Test IP pool creation
curl -X POST http://n8n-instance:8006/webhook/ipam-management \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_pool",
    "resource_type": "ip_pool",
    "pool_name": "Test-Pool-01",
    "network": "192.168.1.0/24",
    "gateway": "192.168.1.1",
    "api_token": "test-token"
  }'

# Test DHCP scope creation
curl -X POST http://n8n-instance:8006/webhook/ipam-management \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_dhcp_scope",
    "resource_type": "dhcp_scope",
    "scope_name": "Test-DHCP-01",
    "start_ip": "192.168.1.100",
    "end_ip": "192.168.1.200",
    "gateway": "192.168.1.1",
    "api_token": "test-token"
  }'
```

### Integration Tests
- End-to-end IP pool lifecycle testing
- DHCP scope integration with pool testing
- DNS zone creation and record management
- VLAN mapping with DHCP integration

### Error Scenario Tests
- Invalid CIDR notation handling
- Overlapping network detection
- Rate limiting response
- Authentication failure handling

## Troubleshooting

### Common Issues

#### "Invalid CIDR notation for network"
**Cause**: Network field contains invalid subnet notation
**Solution**: Use valid CIDR format (e.g., "10.0.0.0/16")

#### "Pool name already exists"
**Cause**: Attempting to create pool with existing name
**Solution**: Use unique pool name or update existing pool

#### "Gateway not in network range"
**Cause**: Gateway IP is outside the specified network
**Solution**: Ensure gateway is within network subnet

#### "Overlapping networks detected"
**Cause**: New pool network overlaps with existing pool
**Solution**: Use non-overlapping network range

### Debugging Steps
1. **Check Request Format**: Verify all required fields are present
2. **Validate Input Data**: Ensure all values meet validation criteria
3. **Review Slack Notifications**: Check #network-operations for error details
4. **Check n8n Execution Logs**: Review workflow execution for detailed errors
5. **Verify API Connectivity**: Test API endpoints independently

### Support Contacts
- **Network Team**: #network-operations (Slack)
- **Technical Support**: network-team@company.com
- **Emergency**: 24/7 NOC hotline

## Best Practices

### IP Pool Management
1. **Use descriptive pool names**: Include location, purpose, environment
2. **Plan network hierarchy**: Organize pools by function and location
3. **Monitor utilization**: Set up alerts before pools become full
4. **Document pool purposes**: Maintain clear descriptions

### DHCP Scope Management
1. **Align with network design**: Match scopes to VLANs and subnets
2. **Set appropriate lease times**: Balance availability and tracking
3. **Reserve critical IPs**: Exclude infrastructure IPs from DHCP ranges
4. **Test scope changes**: Validate configuration before deployment

### DNS Zone Management
1. **Use consistent naming**: Follow organization DNS standards
2. **Plan zone hierarchy**: Organize zones by function and authority
3. **Set appropriate TTLs**: Balance caching and update frequency
4. **Maintain zone documentation**: Document all zone purposes and owners

### VLAN Mapping
1. **Align with network segmentation**: Match VLANs to security zones
2. **Use standard VLAN ranges**: Follow organization VLAN standards
3. **Document VLAN purposes**: Maintain clear VLAN descriptions
4. **Plan for growth**: Reserve VLAN ranges for future expansion

## Compliance and Audit

### Regulatory Compliance
- **SOX Compliance**: Complete audit trails for all operations
- **GDPR Compliance**: Data protection for IP assignment records
- **HIPAA Compliance**: Healthcare-specific IP management requirements
- **PCI DSS**: Secure IP management for payment processing networks

### Audit Features
- **Complete Operation Logging**: All operations logged with details
- **User Activity Tracking**: Track all user-initiated operations
- **Change Management**: Record all configuration changes
- **Retention Policies**: Configurable log retention periods

## Future Enhancements

### Planned Features
- **IPv6 Support**: Full IPv6 address management
- **Multi-Tenant Support**: Isolated IP management per tenant
- **Advanced Analytics**: ML-powered capacity planning
- **Mobile Interface**: Mobile app for IPAM operations

### Integration Roadmap
- **ServiceNow Integration**: ITSM workflow integration
- **Infoblox Integration**: Enterprise IPAM platform integration
- **Microsoft DHCP**: Windows DHCP server integration
- **ISC DHCP**: Linux DHCP server integration

---

**Documentation Version**: 1.0  
**Last Updated**: January 17, 2025  
**Workflow ID**: mwlNopavc6S6g9zq  
**Created by**: Claude Code Automation
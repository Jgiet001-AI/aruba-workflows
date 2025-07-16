# Comprehensive HPE Aruba Networking API Endpoint Mapping for n8n Workflows

## Overview

This document provides a complete mapping of HPE Aruba Networking API endpoints extracted from your Postman collections and additional research. This serves as the foundation for building n8n workflows that automate HPE Aruba network operations.

## Data Sources

### Primary Collection Analysis
- **HPE Aruba Networking Central (Classic Central)**: 2,546 endpoints analyzed
- **Additional Endpoint Files**: Known endpoints from API documentation
- **Collections to be analyzed**: 6 additional collections mentioned:
  - AP provisioning
  - Aruba Central AOS 10  
  - Device-Onboarding-GLP
  - Device-Onboarding
  - EC Orchestrator
  - HPE Aruba Networking
  - New HPE Aruba Networking

## HTTP Method Summary

From the HPE Aruba Central (Classic Central) collection:

| Method | Count | Primary Use Cases |
|--------|-------|-------------------|
| **GET** | 1,334 | Data retrieval, monitoring, status checks |
| **POST** | 542 | Resource creation, command execution, authentication |
| **DELETE** | 346 | Resource removal, cleanup operations |
| **PUT** | 286 | Full resource updates, configuration replacement |
| **PATCH** | 38 | Partial updates, incremental changes |

**Total Endpoints**: 2,546

## API Categories for n8n Workflows

### 1. Authentication & Token Management
- **OAuth Operations**: Token creation, refresh, deletion
- **Session Management**: Login, logout, validation
- **Access Control**: User authentication, authorization

**Key Endpoints**:
```
POST /oauth2/authorize/central/api/login
POST /oauth2/token
POST /oauth2/token (refresh)
DELETE /oauth2/api/tokens
```

### 2. Device Management (High Priority for n8n)
**Categories**: 18+ device management endpoints found

**Core Operations**:
```
GET /monitoring/v2/aps - List access points
GET /monitoring/v1/switches - List switches  
GET /monitoring/v1/gateways - List gateways
GET /platform/device_inventory/v1/devices - Device inventory
POST /platform/device_inventory/v1/devices - Add devices
DELETE /platform/device_inventory/v1/devices - Remove devices
```

**Device Actions**:
```
POST /device_management/v1/action - Execute device commands
POST /firmware/v1/upgrade - Firmware upgrades
GET /firmware/v1/status - Upgrade status
```

### 3. Configuration Management (Critical for Automation)
**Template Operations**:
```
GET /configuration/v1/groups/{group}/templates - List templates
POST /configuration/v1/groups/{group}/templates - Create template
PUT /configuration/v1/groups/{group}/templates - Update template
DELETE /configuration/v1/groups/{group}/templates - Delete template
```

**Group Management**:
```
GET /configuration/v2/groups - List groups
POST /configuration/v2/groups - Create group
PUT /configuration/v2/groups/{group} - Update group
DELETE /configuration/v2/groups/{group} - Delete group
```

**WLAN Configuration**:
```
GET /configuration/v2/wlan/{group}/{wlan_name} - Get WLAN
POST /configuration/v2/wlan/{group} - Create WLAN
PUT /configuration/v2/wlan/{group}/{wlan_name} - Update WLAN
DELETE /configuration/v2/wlan/{group}/{wlan_name} - Delete WLAN
```

### 4. Monitoring & Analytics (Perfect for n8n Scheduling)
**Device Health**:
```
GET /monitoring/v1/devices/statistics - Device stats
GET /aiops/v2/insights/global/list - AI insights
GET /monitoring/v1/clients - Client monitoring
GET /branchhealth/v1/health - Branch health
```

**Network Performance**:
```
GET /aiops/v1/connectivity/global/stage/{stage}/export - Connectivity data
GET /network-health/v1/summary - Network health summary
GET /presence/v1/analytics/metrics - Presence analytics
```

### 5. Alerting & Notifications (Event-Driven Workflows)
**Alert Management**:
```
GET /monitoring/v1/alerts - Active alerts
POST /monitoring/v1/alerts/rules - Create alert rules
PUT /monitoring/v1/alerts/rules/{id} - Update rules
DELETE /monitoring/v1/alerts/rules/{id} - Delete rules
```

**Webhook Integration**:
```
GET /central/v1/webhooks - List webhooks
POST /central/v1/webhooks - Create webhook
PUT /central/v1/webhooks/{webhook_id} - Update webhook
DELETE /central/v1/webhooks/{webhook_id} - Delete webhook
POST /central/v1/webhooks/{webhook_id}/test - Test webhook
```

### 6. User & Access Management
**User Operations**:
```
GET /platform/rbac/v1/users - List users
POST /platform/rbac/v1/users - Create user
PUT /platform/rbac/v1/users/{user_id} - Update user
DELETE /platform/rbac/v1/users/{user_id} - Delete user
```

**Guest Management**:
```
GET /guest/v1/users - List guest users
POST /guest/v1/users - Create guest user
PUT /guest/v1/users/{user_id} - Update guest user
DELETE /guest/v1/users/{user_id} - Delete guest user
```

### 7. Advanced Services
**SD-WAN Configuration**:
```
GET /sdwan-config/v1/node_list/{node_id}/config/ - Get SDWAN config
PUT /sdwan-config/v1/node_list/{node_id}/config/ - Update SDWAN config
GET /sdwan-config/v1/branch-mesh/{label}/config/ - Branch mesh config
```

**Overlay WLAN**:
```
GET /overlay-wlan-config/v2/node_list/{node_type}/{node_id}/config/ - Get overlay config
PUT /overlay-wlan-config/v2/node_list/{node_type}/{node_id}/config/ - Update overlay config
```

**Troubleshooting**:
```
POST /troubleshooting/v1/devices/{device_serial}/command - Run diagnostics
GET /troubleshooting/v1/devices/{device_serial}/logs - Get logs
```

## Base API Paths (70 Unique Paths Identified)

### Core Infrastructure
- `/aiops` - AI-powered operations and insights
- `/monitoring` - Device and network monitoring
- `/configuration` - Device and network configuration
- `/platform` - Platform-level operations
- `/firmware` - Firmware management

### Device-Specific
- `/aps` - Access point operations
- `/switches` - Switch operations  
- `/gateways` - Gateway operations
- `/devices` - Generic device operations

### Service-Specific
- `/guest` - Guest user management
- `/webhooks` - Webhook configuration
- `/presence` - Presence analytics
- `/topology` - Network topology
- `/visualrf` - RF visualization

### Advanced Services
- `/sdwan-config` - SD-WAN configuration
- `/overlay-wlan-config` - Overlay WLAN
- `/cloud-connect` - Cloud connectivity
- `/msp_api` - MSP management

## n8n Workflow Building Recommendations

### 1. Authentication Workflow (Foundation)
**Trigger**: Manual or scheduled
**Flow**: 
1. Check token expiry
2. Refresh if needed
3. Store new token
4. Validate access

**Key Endpoints**:
- `POST /oauth2/token` (refresh)
- Token validation endpoints

### 2. Device Health Monitoring (High Value)
**Trigger**: Scheduled (every 5-15 minutes)
**Flow**:
1. Retrieve device list
2. Check device health
3. Analyze performance metrics  
4. Generate alerts for issues
5. Send notifications

**Key Endpoints**:
- `GET /monitoring/v2/aps`
- `GET /monitoring/v1/switches`
- `GET /aiops/v2/insights/global/list`
- `POST /central/v1/webhooks` (for alerts)

### 3. Configuration Backup & Management
**Trigger**: Scheduled (daily/weekly)
**Flow**:
1. List all device groups
2. Export configurations
3. Store backups
4. Verify integrity
5. Report status

**Key Endpoints**:
- `GET /configuration/v2/groups`
- `GET /configuration/v1/devices/{serial}/config`
- `POST /configuration/v1/backup`

### 4. Firmware Management Automation
**Trigger**: Event-driven or scheduled
**Flow**:
1. Check available firmware
2. Compare with current versions
3. Plan upgrade schedule
4. Execute upgrades
5. Monitor progress
6. Report completion

**Key Endpoints**:
- `GET /firmware/v1/versions`
- `POST /firmware/v1/upgrade`
- `GET /firmware/v1/status`

### 5. Alert Processing & Response
**Trigger**: Webhook from Aruba Central
**Flow**:
1. Receive alert webhook
2. Parse alert data
3. Determine severity
4. Execute response actions
5. Notify stakeholders
6. Log incident

**Key Endpoints**:
- Webhook reception
- `GET /monitoring/v1/alerts`
- `POST /troubleshooting/v1/devices/{serial}/command`

### 6. User Management Automation
**Trigger**: External system integration
**Flow**:
1. Receive user creation request
2. Validate permissions
3. Create user account
4. Assign roles
5. Send credentials
6. Log activity

**Key Endpoints**:
- `POST /platform/rbac/v1/users`
- `POST /guest/v1/users`
- `POST /platform/rbac/v1/apps/{app}/roles`

## Rate Limiting & Best Practices

### API Rate Limits
- **Central API**: ~100 requests/minute/token
- **AOS-CX**: ~50 requests/minute/session  
- **EdgeConnect**: ~200 requests/minute/appliance

### n8n Implementation Tips
1. **Use delays between batch operations**
2. **Implement exponential backoff for 429 errors**
3. **Cache frequently-used data**
4. **Use parallel processing where appropriate**
5. **Monitor API usage in workflows**

## Authentication Patterns

### Bearer Token (Central API)
```javascript
{
  "headers": {
    "Authorization": "Bearer {{access_token}}",
    "Content-Type": "application/json"
  }
}
```

### Basic Authentication (AOS-CX)
```javascript
{
  "headers": {
    "Authorization": "Basic {{base64_credentials}}",
    "Content-Type": "application/json"
  }
}
```

## Error Handling

### Common HTTP Status Codes
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### n8n Error Handling Patterns
```javascript
// Example error handling in n8n Function node
try {
  const response = await $http.request(options);
  return response;
} catch (error) {
  if (error.response?.status === 429) {
    // Rate limited - wait and retry
    await new Promise(r => setTimeout(r, 60000));
    return $http.request(options);
  } else if (error.response?.status === 401) {
    // Token expired - refresh and retry
    const newToken = await refreshToken();
    options.headers.Authorization = `Bearer ${newToken}`;
    return $http.request(options);
  }
  throw error;
}
```

## Next Steps

1. **Access Remaining Collections**: Use Postman API or workspace sharing to extract the other 6 collections
2. **Create Collection-Specific Mappings**: Analyze each collection for unique endpoints
3. **Build Template Workflows**: Create reusable n8n workflow templates for common operations
4. **Test & Validate**: Verify all endpoints work with current API versions
5. **Document Integration Patterns**: Create specific integration guides for each service type

## Files Generated

- `/Users/jeangiet/Documents/Claude/aruba-workflows/aruba_central_complete_endpoint_mapping.json` - Complete JSON mapping
- `/Users/jeangiet/Documents/Claude/aruba-workflows/extract_endpoints.py` - Extraction script
- This comprehensive analysis document

## Conclusion

This analysis provides a solid foundation for building comprehensive n8n workflows for HPE Aruba networking automation. The 2,546+ endpoints identified cover all major operational areas, with clear patterns for authentication, monitoring, configuration management, and alerting.

The high number of GET endpoints (1,334) makes this ideal for monitoring workflows, while the substantial number of POST (542) and PUT (286) endpoints provides comprehensive automation capabilities for configuration and management tasks.

For complete coverage, the remaining 6 collections should be analyzed using similar methods to identify any additional endpoints specific to AP provisioning, AOS-10, device onboarding, and EdgeConnect orchestration.
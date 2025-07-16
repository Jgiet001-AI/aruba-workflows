# Known HPE Aruba API Endpoints for n8n Workflows

Based on common HPE Aruba networking automation patterns, here are the expected API endpoints organized by HTTP method and functionality:

## Authentication APIs

### POST Operations
- `POST /oauth2/token` - Get access token
- `POST /api/v2/auth/refresh` - Refresh access token
- `POST /api/v2/auth/logout` - Logout and invalidate token

## Device Management APIs

### GET Operations (Device Retrieval)
- `GET /api/v2/devices` - List all devices
- `GET /api/v2/devices/{serial}` - Get specific device details
- `GET /api/v2/devices/aps` - List access points only
- `GET /api/v2/devices/switches` - List switches only
- `GET /api/v2/devices/gateways` - List gateways only
- `GET /api/v2/devices/{serial}/status` - Device status and health
- `GET /api/v2/devices/{serial}/stats` - Device performance statistics
- `GET /api/v2/devices/{serial}/clients` - Connected clients
- `GET /api/v2/devices/{serial}/interfaces` - Device interfaces

### POST Operations (Device Creation/Actions)
- `POST /api/v2/devices/provision` - Provision new device
- `POST /api/v2/devices/{serial}/reboot` - Reboot device
- `POST /api/v2/devices/{serial}/commands` - Execute CLI commands
- `POST /api/v2/devices/bulk/provision` - Bulk device provisioning
- `POST /api/v2/devices/{serial}/upgrade` - Initiate firmware upgrade

### PUT Operations (Device Updates)
- `PUT /api/v2/devices/{serial}` - Update device configuration
- `PUT /api/v2/devices/{serial}/group` - Move device to group
- `PUT /api/v2/devices/{serial}/location` - Update device location
- `PUT /api/v2/devices/{serial}/name` - Update device name

### PATCH Operations (Partial Updates)
- `PATCH /api/v2/devices/{serial}/config` - Partial configuration update
- `PATCH /api/v2/devices/{serial}/settings` - Update specific settings

### DELETE Operations (Device Removal)
- `DELETE /api/v2/devices/{serial}` - Remove device from management
- `DELETE /api/v2/devices/{serial}/provision` - Deprovision device

## Configuration Management APIs

### GET Operations (Configuration Retrieval)
- `GET /api/v2/configuration/templates` - List configuration templates
- `GET /api/v2/configuration/templates/{id}` - Get template details
- `GET /api/v2/configuration/groups` - List device groups
- `GET /api/v2/configuration/groups/{id}/devices` - Devices in group
- `GET /api/v2/configuration/devices/{serial}/config` - Device running config
- `GET /api/v2/configuration/devices/{serial}/template` - Applied template

### POST Operations (Configuration Creation)
- `POST /api/v2/configuration/templates` - Create new template
- `POST /api/v2/configuration/groups` - Create device group
- `POST /api/v2/configuration/apply` - Apply configuration to devices
- `POST /api/v2/configuration/backup` - Backup device configurations

### PUT Operations (Configuration Updates)
- `PUT /api/v2/configuration/templates/{id}` - Update template
- `PUT /api/v2/configuration/groups/{id}` - Update group settings
- `PUT /api/v2/configuration/devices/{serial}/config` - Replace device config

### DELETE Operations (Configuration Removal)
- `DELETE /api/v2/configuration/templates/{id}` - Delete template
- `DELETE /api/v2/configuration/groups/{id}` - Delete group

## Monitoring and Analytics APIs

### GET Operations (Monitoring Data)
- `GET /api/v2/monitoring/devices` - Device health overview
- `GET /api/v2/monitoring/devices/{serial}/stats` - Device statistics
- `GET /api/v2/monitoring/devices/{serial}/events` - Device events
- `GET /api/v2/monitoring/network/usage` - Network usage statistics
- `GET /api/v2/monitoring/clients` - Client connectivity stats
- `GET /api/v2/monitoring/applications` - Application usage
- `GET /api/v2/monitoring/alerts` - Active alerts
- `GET /api/v2/monitoring/reports` - Available reports

### POST Operations (Monitoring Configuration)
- `POST /api/v2/monitoring/thresholds` - Set monitoring thresholds
- `POST /api/v2/monitoring/alerts/rules` - Create alert rules

## Network Configuration APIs

### GET Operations (Network Settings)
- `GET /api/v2/network/vlans` - List VLANs
- `GET /api/v2/network/vlans/{id}` - VLAN details
- `GET /api/v2/network/ports` - Port configurations
- `GET /api/v2/network/routing` - Routing configuration
- `GET /api/v2/network/security/policies` - Security policies
- `GET /api/v2/network/qos/profiles` - QoS profiles

### POST Operations (Network Creation)
- `POST /api/v2/network/vlans` - Create VLAN
- `POST /api/v2/network/security/policies` - Create security policy
- `POST /api/v2/network/qos/profiles` - Create QoS profile

### PUT Operations (Network Updates)
- `PUT /api/v2/network/vlans/{id}` - Update VLAN
- `PUT /api/v2/network/ports/{id}` - Update port configuration
- `PUT /api/v2/network/security/policies/{id}` - Update security policy

### DELETE Operations (Network Removal)
- `DELETE /api/v2/network/vlans/{id}` - Delete VLAN
- `DELETE /api/v2/network/security/policies/{id}` - Delete security policy

## User and Access Management APIs

### GET Operations (User Management)
- `GET /api/v2/users` - List users
- `GET /api/v2/users/{id}` - User details
- `GET /api/v2/roles` - Available roles
- `GET /api/v2/permissions` - Available permissions

### POST Operations (User Creation)
- `POST /api/v2/users` - Create user
- `POST /api/v2/roles` - Create custom role

### PUT Operations (User Updates)
- `PUT /api/v2/users/{id}` - Update user
- `PUT /api/v2/users/{id}/password` - Change password
- `PUT /api/v2/users/{id}/roles` - Update user roles

### DELETE Operations (User Removal)
- `DELETE /api/v2/users/{id}` - Delete user

## Alerting and Notification APIs

### GET Operations (Alert Management)
- `GET /api/v2/alerts` - List active alerts
- `GET /api/v2/alerts/{id}` - Alert details
- `GET /api/v2/alerts/rules` - Alert rules
- `GET /api/v2/webhooks` - Configured webhooks

### POST Operations (Alert Configuration)
- `POST /api/v2/alerts/rules` - Create alert rule
- `POST /api/v2/webhooks` - Configure webhook
- `POST /api/v2/alerts/{id}/acknowledge` - Acknowledge alert

### PUT Operations (Alert Updates)
- `PUT /api/v2/alerts/rules/{id}` - Update alert rule
- `PUT /api/v2/webhooks/{id}` - Update webhook

### DELETE Operations (Alert Removal)
- `DELETE /api/v2/alerts/rules/{id}` - Delete alert rule
- `DELETE /api/v2/webhooks/{id}` - Remove webhook

## Firmware Management APIs

### GET Operations (Firmware Information)
- `GET /api/v2/firmware/versions` - Available firmware versions
- `GET /api/v2/firmware/devices/{serial}/version` - Device firmware version
- `GET /api/v2/firmware/upgrade/status` - Upgrade status

### POST Operations (Firmware Operations)
- `POST /api/v2/firmware/upgrade` - Initiate firmware upgrade
- `POST /api/v2/firmware/schedule` - Schedule firmware upgrade

## AP Provisioning Specific APIs

### GET Operations
- `GET /api/v2/provisioning/aps` - List provisionable APs
- `GET /api/v2/provisioning/aps/{serial}/status` - AP provision status

### POST Operations
- `POST /api/v2/provisioning/aps` - Provision AP
- `POST /api/v2/provisioning/aps/bulk` - Bulk AP provisioning

## AOS-CX Switch Specific APIs

### GET Operations
- `GET /rest/v10.08/system` - System information
- `GET /rest/v10.08/system/interfaces` - Interface status
- `GET /rest/v10.08/system/vlans` - VLAN configuration

### POST Operations
- `POST /rest/v10.08/system/vlans` - Create VLAN
- `POST /rest/v10.08/system/interfaces/{id}/admin` - Enable/disable interface

### PUT Operations
- `PUT /rest/v10.08/system/interfaces/{id}` - Update interface configuration
- `PUT /rest/v10.08/system/vlans/{id}` - Update VLAN

## EdgeConnect SD-WAN APIs

### GET Operations
- `GET /gms/api/appliances` - List appliances
- `GET /gms/api/appliances/{id}/stats` - Appliance statistics
- `GET /gms/api/policies/qos` - QoS policies

### POST Operations
- `POST /gms/api/policies/security` - Create security policy
- `POST /gms/api/appliances/{id}/reboot` - Reboot appliance

## Common HTTP Status Codes

### Success Responses
- `200 OK` - Successful GET/PUT/PATCH
- `201 Created` - Successful POST
- `202 Accepted` - Request accepted (async operation)
- `204 No Content` - Successful DELETE

### Client Error Responses
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict
- `422 Unprocessable Entity` - Validation errors
- `429 Too Many Requests` - Rate limit exceeded

### Server Error Responses
- `500 Internal Server Error` - Server error
- `502 Bad Gateway` - Gateway error
- `503 Service Unavailable` - Service temporarily unavailable

## Rate Limiting Information

Most HPE Aruba APIs implement rate limiting:
- Central API: ~100 requests per minute per token
- AOS-CX: ~50 requests per minute per session
- EdgeConnect: ~200 requests per minute per appliance

## Authentication Patterns

### Bearer Token (Central API)
```
Authorization: Bearer <access_token>
```

### Basic Authentication (AOS-CX)
```
Authorization: Basic <base64_encoded_credentials>
```

### Session-based (EdgeConnect)
```
Cookie: session_id=<session_id>
```

This endpoint mapping provides the foundation for building comprehensive n8n workflows that can perform all CRUD operations on HPE Aruba infrastructure.
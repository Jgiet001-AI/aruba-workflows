# Aruba Central Client Policy Management Workflow

## Overview

This comprehensive n8n workflow automates client policy management for Aruba Central, providing end-to-end automation for user management, device onboarding, policy deployment, guest access management, and client troubleshooting.

## Features

### Core Operations
- **User Management**: Create, update, and delete users with role assignments
- **Guest Access Management**: Automated guest user creation and portal management
- **Device Onboarding**: BYOD and corporate device enrollment automation
- **Policy Deployment**: Dynamic policy assignment based on device type and user role
- **Client Troubleshooting**: Automated diagnostic and issue resolution
- **Error Handling**: Comprehensive error handling with automatic rollback capabilities

### Policy Templates
- **Corporate Users**: Full network access, productivity tools, no time restrictions
- **Contractors**: Limited network access, time restrictions (8 AM - 6 PM, Mon-Fri)
- **Guests**: Internet-only access, captive portal, 4-hour sessions
- **BYOD Devices**: Segregated network, policy compliance required
- **IoT Devices**: Restricted access, device-specific policies
- **Executive Users**: VIP treatment, priority bandwidth

### Role Templates
- **Network Administrators**: Full management access
- **IT Helpdesk**: Monitoring and basic configuration
- **Site Managers**: Local site management only
- **Guest Sponsors**: Guest user management
- **Auditors**: Read-only access to logs and reports

## Supported Operations

| Operation | Description | Required Parameters |
|-----------|-------------|-------------------|
| `create_user` | Create new user account | username, user_email, user_role |
| `update_user` | Update existing user | user_id, username, user_email, user_role |
| `delete_user` | Delete user account | user_id |
| `create_role` | Create custom role | role_name, permissions |
| `assign_role` | Assign role to user | user_id, user_role |
| `create_guest` | Create guest user | username, user_email, guest_duration, guest_sponsor |
| `configure_byod` | Configure BYOD settings | device_type, authentication_method, certificate_type |
| `apply_policy` | Apply client policy | client_mac, device_type, policy_name |
| `troubleshoot_client` | Troubleshoot client issues | client_mac |

## Input Parameters

### Required Parameters
- `operation`: Operation to perform (see supported operations above)
- `central_base_url`: Aruba Central API base URL
- `customer_id`: Central customer ID

### User Management Parameters
- `user_id`: User identifier for updates/deletes
- `username`: Username for authentication
- `user_email`: User email address
- `user_role`: Role assignment (corporate, contractor, guest, etc.)

### Device Management Parameters
- `client_mac`: Client device MAC address
- `device_type`: Device type (corporate, byod, guest, iot)
- `authentication_method`: Auth method (802.1x, mac_auth, captive_portal, psk)

### Policy Parameters
- `policy_name`: Policy to apply
- `bandwidth_limit`: Speed limit in Mbps
- `session_timeout`: Session duration in minutes
- `time_restrictions`: Time-based access controls (JSON)
- `vlan_assignment`: VLAN for client isolation

### Guest Management Parameters
- `portal_id`: Guest portal identifier
- `guest_duration`: Guest access duration in hours
- `guest_sponsor`: Sponsor email for guest approval

### BYOD Parameters
- `certificate_type`: Certificate type (user, device, ca)

## Policy Configuration Details

### Corporate Policy
- **Network Access**: Full access to all network resources
- **Bandwidth**: Up to 100 Mbps down, 50 Mbps up
- **Session Timeout**: No timeout
- **VLAN**: 10 (corporate VLAN)
- **Applications**: Productivity tools, business apps, collaboration
- **QoS**: Silver class (Gold/Platinum for managers/executives)

### Contractor Policy
- **Network Access**: Limited to internet and specific internal resources
- **Bandwidth**: Up to 50 Mbps down, 25 Mbps up
- **Session Timeout**: 8 hours
- **VLAN**: 20 (contractor VLAN)
- **Time Restrictions**: 8 AM - 6 PM, Monday - Friday
- **Firewall**: Deny internal network access except approved services

### Guest Policy
- **Network Access**: Internet only
- **Bandwidth**: Up to 20 Mbps down, 10 Mbps up
- **Session Timeout**: 4 hours
- **VLAN**: 100 (guest VLAN)
- **Captive Portal**: Required with terms acceptance
- **Firewall**: Block all internal network access

### BYOD Policy
- **Network Access**: Segregated network with limited internal access
- **Bandwidth**: Up to 50 Mbps down, 25 Mbps up
- **Session Timeout**: 12 hours
- **VLAN**: 30 (BYOD VLAN)
- **Compliance**: Device health checks, encryption required
- **Certificate Auth**: Required for 802.1x

### IoT Policy
- **Network Access**: Restricted to specific servers only
- **Bandwidth**: Up to 10 Mbps down, 5 Mbps up
- **Session Timeout**: No timeout
- **VLAN**: 200 (IoT VLAN)
- **Firewall**: Highly restrictive, specific server access only

## BYOD Configuration Features

### Device Registration
- Self-registration for personal devices
- Admin approval for corporate devices
- Sponsor approval for contractor devices

### Authentication
- Certificate-based authentication for 802.1x
- Multi-factor authentication for corporate devices
- MAC authentication for approved devices

### Device Compliance
- Antivirus check
- OS version validation
- Jailbreak/root detection
- Device encryption verification

### Onboarding Automation
- Automatic profile installation
- WiFi profile deployment
- Certificate installation for 802.1x
- VPN profile for corporate devices

### Device Management
- Container mode for corporate devices
- App wrapping for security
- Data loss prevention
- Remote wipe capability

## Client Troubleshooting Features

### Automated Diagnostics
1. **Client Information Retrieval**: Basic client details and connection status
2. **Authentication Status Check**: Verify authentication success/failure
3. **Client Health Assessment**: Signal strength, throughput, errors
4. **Policy Assignment Verification**: Check applied policies
5. **Audit Trail Analysis**: Review recent client activities

### Issue Detection
- Authentication failures
- Poor signal strength (< -70 dBm)
- Missing policy assignments
- Network connectivity issues
- Certificate validation problems

### Automated Recommendations
- Credential verification for auth failures
- AP relocation for signal issues
- Policy assignment for unassigned clients
- Network troubleshooting for connectivity issues

## Error Handling and Rollback

### Error Categories
- **Authentication Errors**: Invalid credentials, expired tokens
- **Authorization Errors**: Insufficient permissions, wrong customer ID
- **Network Errors**: Connectivity issues, timeouts
- **Rate Limiting**: API quota exceeded
- **Server Errors**: Aruba Central service issues
- **Client Errors**: Invalid parameters, malformed requests

### Automatic Rollback
- **Policy Operations**: Remove applied policies on failure
- **User Creation**: Delete created users on subsequent failures
- **BYOD Configuration**: Reset BYOD settings on configuration errors

### Recovery Recommendations
- Credential validation and regeneration
- Parameter validation and correction
- Network connectivity troubleshooting
- Rate limiting implementation
- Service status verification

## API Endpoints Used

### User and Role Management
- `GET /platform/authz/v1/users` - List users
- `POST /platform/authz/v1/users` - Create user
- `PUT /platform/authz/v1/users/{user_id}` - Update user
- `DELETE /platform/authz/v1/users/{user_id}` - Delete user
- `GET /platform/authz/v1/roles` - List roles
- `POST /platform/authz/v1/roles` - Create role
- `PUT /platform/authz/v1/roles/{role_id}` - Update role

### Client Management
- `GET /monitoring/v1/clients` - Get client information
- `PUT /configuration/v1/clients/{client_mac}/policy` - Apply client policy

### Guest Management
- `POST /guest/v1/portals` - Create guest portal
- `PUT /guest/v1/portals/{portal_id}` - Update guest portal
- `GET /guest/v1/visitors` - List guest users
- `POST /guest/v1/visitors` - Create guest user
- `PUT /guest/v1/visitors/{visitor_id}` - Update guest user
- `DELETE /guest/v1/visitors/{visitor_id}` - Delete guest user

### BYOD Management
- `GET /device/v1/byod` - Get BYOD settings
- `PUT /device/v1/byod` - Update BYOD settings
- `POST /device/v1/certificates` - Upload certificates

### Monitoring and Troubleshooting
- `GET /monitoring/v1/audit_trail` - Get audit logs
- `GET /monitoring/v1/clients/{client_mac}/authentication` - Check auth status
- `GET /monitoring/v1/clients/{client_mac}/health` - Get client health

## Usage Examples

### Example 1: Create Corporate User
```json
{
  "operation": "create_user",
  "username": "john.doe",
  "user_email": "john.doe@company.com",
  "user_role": "employee",
  "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
  "customer_id": "your-customer-id"
}
```

### Example 2: Apply BYOD Policy
```json
{
  "operation": "apply_policy",
  "client_mac": "aa:bb:cc:dd:ee:ff",
  "device_type": "byod",
  "user_role": "employee",
  "policy_name": "employee_byod_policy",
  "bandwidth_limit": "30",
  "session_timeout": "720",
  "vlan_assignment": "30",
  "authentication_method": "802.1x",
  "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
  "customer_id": "your-customer-id"
}
```

### Example 3: Create Guest User
```json
{
  "operation": "create_guest",
  "username": "guest.visitor",
  "user_email": "visitor@example.com",
  "guest_duration": "8",
  "guest_sponsor": "sponsor@company.com",
  "portal_id": "guest-portal-1",
  "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
  "customer_id": "your-customer-id"
}
```

### Example 4: Configure BYOD Settings
```json
{
  "operation": "configure_byod",
  "device_type": "corporate",
  "authentication_method": "802.1x",
  "certificate_type": "user",
  "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
  "customer_id": "your-customer-id"
}
```

### Example 5: Troubleshoot Client
```json
{
  "operation": "troubleshoot_client",
  "client_mac": "aa:bb:cc:dd:ee:ff",
  "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
  "customer_id": "your-customer-id"
}
```

## Installation and Setup

### Prerequisites
1. **n8n Installation**: Ensure n8n is installed and running
2. **Aruba Central Access**: Valid API credentials and customer ID
3. **Network Connectivity**: Access to Aruba Central API endpoints

### Credential Configuration
1. Create new credential in n8n of type "HTTP Header Auth"
2. Set credential name to "arubaApiAuth"
3. Configure the following:
   - Header Name: `Authorization`
   - Header Value: `Bearer YOUR_ACCESS_TOKEN`

### Workflow Import
1. Copy the workflow JSON content
2. Import into n8n through the UI
3. Configure credentials
4. Test with sample data

### Slack Integration (Optional)
1. Create Slack app with webhook permissions
2. Configure Slack node with appropriate channel
3. Update notification preferences

## Monitoring and Maintenance

### Success Metrics
- User creation/update success rate
- Policy application success rate
- Guest onboarding completion rate
- BYOD enrollment success rate
- Troubleshooting resolution rate

### Regular Maintenance
- Monitor API credential expiration
- Review error logs and rollback frequency
- Update policy templates as needed
- Validate BYOD configuration changes
- Test troubleshooting accuracy

### Performance Optimization
- Implement request batching for bulk operations
- Add caching for frequently accessed data
- Optimize API call sequences
- Monitor rate limiting and adjust delays

## Security Considerations

### API Security
- Use secure credential storage in n8n
- Implement proper access controls
- Regular credential rotation
- Monitor API usage and access logs

### Data Protection
- Encrypt sensitive data in transit
- Implement data retention policies
- Secure guest user information
- Protect certificate and key material

### Network Security
- Validate all input parameters
- Implement proper VLAN segmentation
- Monitor for policy violations
- Regular security assessments

## Troubleshooting

### Common Issues
1. **Authentication Failures**: Check credential configuration and token validity
2. **Policy Application Errors**: Verify client MAC address and policy parameters
3. **Guest Creation Failures**: Check portal configuration and sponsor settings
4. **BYOD Configuration Issues**: Validate certificate setup and compliance requirements

### Debug Mode
Enable debug mode in n8n to see detailed execution logs and API responses for troubleshooting.

### Support Contacts
- **Technical Issues**: IT Operations Team
- **Policy Questions**: Network Security Team
- **Guest Access**: Facilities Management
- **BYOD Support**: Device Management Team

## Version History

- **v1.0.0**: Initial release with core client policy management features
- Future versions will include enhanced analytics and reporting capabilities

---

**Workflow File**: `aruba-central-client-policy-management-workflow.json`  
**Created**: 2025-01-16  
**Last Updated**: 2025-01-16  
**Maintainer**: Network Automation Team
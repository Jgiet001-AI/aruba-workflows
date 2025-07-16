# Aruba Central Wireless Configuration Workflow

## Overview

This workflow provides comprehensive wireless configuration automation for HPE Aruba Central, enabling automated management of SSIDs, wireless security policies, radio settings, and access point configuration through API calls.

## Features

### Core Operations
- **SSID Management**: Create, update, delete, and list SSIDs
- **Radio Configuration**: Configure 2.4GHz, 5GHz, and 6GHz radio settings
- **Security Policy Management**: Support for all wireless security types
- **Wireless Templates**: Pre-configured templates for different network types
- **Error Handling**: Comprehensive error categorization with automatic rollback
- **Notifications**: Real-time Slack alerts for success/failure scenarios

### Security Templates
- **Corporate Networks**: WPA3 Enterprise with 802.1X authentication
- **Guest Networks**: Captive portal with session time limits
- **IoT Networks**: WPA2 Personal with device isolation
- **Public Networks**: Open with terms acceptance

### Supported Security Types
- Open (no authentication)
- WPA2 Personal (PSK)
- WPA3 Personal (SAE)
- WPA2 Enterprise (802.1X)
- WPA3 Enterprise (802.1X)

## API Endpoints

### SSID Management
- `GET /configuration/v2/wlan/ssid` - List all SSIDs
- `GET /configuration/v2/wlan/ssid/{ssid_name}` - Get specific SSID
- `POST /configuration/v2/wlan/ssid` - Create new SSID
- `PUT /configuration/v2/wlan/ssid/{ssid_name}` - Update SSID
- `DELETE /configuration/v2/wlan/ssid/{ssid_name}` - Delete SSID

### Radio Configuration
- `GET /configuration/v2/ap_groups/{group_name}/wireless_profile` - Get wireless profile
- `PUT /configuration/v2/ap_groups/{group_name}/wireless_profile` - Update wireless profile

### Access Point Management
- `GET /monitoring/v1/aps` - List access points
- `PUT /configuration/v1/devices/{serial}/configuration` - Configure specific AP

## Input Parameters

### Required Parameters
- `operation`: Operation type (`create_ssid`, `update_ssid`, `delete_ssid`, `list_ssids`, `configure_radio`, `update_security`)
- `central_base_url`: Aruba Central API base URL (e.g., `https://apigw-uswest4.central.arubanetworks.com`)
- `customer_id`: Central customer ID

### SSID Parameters
- `ssid_name`: Internal SSID name
- `essid`: Network name displayed to users
- `security_type`: Security method (`open`, `wpa2_personal`, `wpa3_personal`, `wpa2_enterprise`, `wpa3_enterprise`)
- `passphrase`: WPA passphrase (8-63 characters, required for personal networks)
- `vlan_id`: VLAN assignment (1-4094)
- `broadcast_ssid`: Whether to broadcast SSID (default: true)
- `max_clients`: Maximum clients per AP/radio (1-512, default: 128)

### Radio Parameters
- `ap_group`: AP group name
- `radio_band`: Radio band (`2.4GHz`, `5GHz`, `6GHz`, `dual_band`, `tri_band`)
- `channel_width`: Channel width (`20MHz`, `40MHz`, `80MHz`, `160MHz`)
- `power_level`: Power level (`auto`, `low`, `medium`, `high`, or dBm value -30 to 30)
- `band_steering`: Enable band steering (default: true)
- `fast_transition`: Enable 802.11r fast transition (default: true)

### Network Type Templates (Optional)
- `network_type`: Template type (`corporate`, `guest`, `iot`, `public`)

### Enterprise Security Parameters
- `radius_server`: RADIUS server IP/hostname
- `radius_secret`: RADIUS shared secret

### Guest Network Parameters
- `session_timeout`: Session timeout in seconds (default: 3600)
- `bandwidth_limit`: Bandwidth limit in Kbps (default: 10000)

## Usage Examples

### Create Corporate SSID

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-wireless-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_ssid",
    "ssid_name": "CORP-WIFI",
    "essid": "Corporate WiFi",
    "security_type": "wpa3_enterprise",
    "network_type": "corporate",
    "vlan_id": 100,
    "radius_server": "192.168.1.100",
    "radius_secret": "shared-secret-key",
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "your-customer-id"
  }'
```

### Create Guest Network

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-wireless-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_ssid",
    "ssid_name": "GUEST-WIFI",
    "essid": "Guest Network",
    "security_type": "open",
    "network_type": "guest",
    "vlan_id": 200,
    "session_timeout": 3600,
    "bandwidth_limit": 5000,
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "your-customer-id"
  }'
```

### Create IoT Network

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-wireless-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_ssid",
    "ssid_name": "IOT-DEVICES",
    "essid": "IoT Network",
    "security_type": "wpa2_personal",
    "passphrase": "SecureIoTPassword123",
    "network_type": "iot",
    "vlan_id": 300,
    "max_clients": 64,
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "your-customer-id"
  }'
```

### Configure Radio Settings

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-wireless-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "configure_radio",
    "ap_group": "Building-A-APs",
    "radio_band": "dual_band",
    "channel_width": "80MHz",
    "power_level": "auto",
    "max_clients": 100,
    "band_steering": true,
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "your-customer-id"
  }'
```

### Update SSID Security

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-wireless-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "update_ssid",
    "ssid_name": "CORP-WIFI",
    "essid": "Corporate WiFi",
    "security_type": "wpa3_personal",
    "passphrase": "NewSecurePassword2023",
    "vlan_id": 100,
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "your-customer-id"
  }'
```

### List All SSIDs

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-wireless-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list_ssids",
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "your-customer-id"
  }'
```

### Delete SSID

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-wireless-config \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "delete_ssid",
    "ssid_name": "OLD-GUEST-WIFI",
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "your-customer-id"
  }'
```

## Security Templates Details

### Corporate Network Template
```json
{
  "type": "wpa3_enterprise",
  "auth_method": "eap",
  "encryption": "aes",
  "fast_transition": true,
  "pmf": "required",
  "wpa3_transition": true
}
```

### Guest Network Template
```json
{
  "type": "open",
  "auth_method": "open",
  "captive_portal": true,
  "session_timeout": 3600,
  "bandwidth_limit": 10000
}
```

### IoT Network Template
```json
{
  "type": "wpa2_personal",
  "auth_method": "psk",
  "encryption": "aes",
  "device_isolation": true,
  "max_clients": 64,
  "rate_limit": 5000
}
```

### Public Network Template
```json
{
  "type": "open",
  "auth_method": "open",
  "terms_acceptance": true,
  "bandwidth_limit": 5000,
  "session_timeout": 1800
}
```

## Error Handling

### Error Categories
- **Authentication**: 401/403 errors (invalid credentials)
- **Validation**: 400 errors (invalid parameters)
- **Not Found**: 404 errors (SSID/AP group doesn't exist)
- **Conflict**: 409 errors (SSID already exists)
- **Rate Limit**: 429 errors (too many requests)
- **Server Error**: 500+ errors (Central API issues)
- **Network**: Connection timeout/network issues

### Rollback Scenarios
- Failed SSID creation → Automatic deletion attempt
- Failed SSID update → Restore from backup (if available)
- Failed radio configuration → Restore previous settings

### Retry Logic
- Rate limit errors: Automatic retry with exponential backoff
- Server errors: Up to 3 retries with 2-second delays
- Network timeouts: Up to 3 retries with increasing delays

## Response Format

### Success Response
```json
{
  "result": "success",
  "operation": "create_ssid",
  "ssid_name": "CORP-WIFI",
  "timestamp": "2025-01-16T10:30:00Z"
}
```

### Error Response
```json
{
  "result": "error",
  "operation": "create_ssid",
  "error_category": "validation",
  "rollback_required": false,
  "timestamp": "2025-01-16T10:30:00Z"
}
```

## Notifications

### Slack Notifications
- **Success**: Green checkmark with operation details
- **Failure**: Red X with error details and rollback status
- **Channel**: #network-alerts (configurable)

### Email Notifications
- Critical failures automatically generate email alerts
- Include full error context and remediation steps

## Credential Configuration

### Aruba Central API Credentials
Create credentials in n8n with type "arubaApi":
- **Client ID**: Your Central API client ID
- **Client Secret**: Your Central API client secret
- **Access Token**: OAuth 2.0 access token
- **Refresh Token**: OAuth 2.0 refresh token

### Slack Credentials
Create Slack credentials in n8n:
- **Webhook URL**: Slack incoming webhook URL
- **Channel**: #network-alerts
- **Username**: Aruba Automation

## Monitoring and Logging

### Execution Monitoring
- All workflow executions are logged
- Performance metrics tracked
- Error rates monitored
- Success/failure statistics

### Audit Trail
- Complete API call logging
- Input parameter validation logs
- Configuration change tracking
- Rollback operation logs

## Best Practices

### Security
- Use strong passphrases (12+ characters with mixed case, numbers, symbols)
- Regularly rotate API credentials
- Enable WPA3 for new networks when possible
- Use separate VLANs for different network types

### Performance
- Batch similar operations when possible
- Monitor API rate limits
- Use appropriate channel widths for environment
- Configure power levels based on coverage requirements

### Operational
- Test configurations in non-production environment first
- Maintain backup configurations
- Monitor wireless performance after changes
- Document all custom configurations

## Troubleshooting

### Common Issues

#### Authentication Failures
- Verify API credentials in n8n
- Check token expiration
- Confirm customer ID is correct

#### SSID Creation Failures
- Verify SSID name doesn't already exist
- Check VLAN ID validity
- Ensure passphrase meets requirements

#### Radio Configuration Issues
- Verify AP group name exists
- Check channel width compatibility
- Confirm power level settings

#### Network Connectivity
- Test Central API connectivity
- Verify n8n can reach Central endpoints
- Check firewall rules

### Debug Steps
1. Check workflow execution logs in n8n
2. Verify input parameters against validation rules
3. Test API endpoints manually with same parameters
4. Review Slack notifications for error details
5. Check Central UI for configuration conflicts

## File Structure

```
access-points-config-management/
├── aruba-central-wireless-configuration-workflow.json
├── README-Wireless-Configuration.md
├── config/
│   ├── parameters.json
│   └── credentials.md
├── tests/
│   ├── wireless-test-scenarios.json
│   └── quick-test-examples.json
├── docs/
└── versions/
```

## Version History

- **v1.0.0**: Initial release with comprehensive wireless configuration automation
  - SSID CRUD operations
  - Radio configuration
  - Security template management
  - Error handling and rollback
  - Slack notifications

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review workflow execution logs in n8n
3. Verify API documentation at HPE Aruba Developer Portal
4. Contact network automation team

---

**Last Updated**: January 16, 2025  
**Workflow Version**: 1.0.0  
**Author**: Claude Code Automation
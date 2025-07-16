# Access Points Configuration Management - Master Usage Guide

## 🎯 Overview
Complete automation suite for HPE Aruba wireless access point configuration management using n8n workflows. This guide provides comprehensive instructions for deploying, configuring, and operating all wireless automation components.

## 📁 Project Structure
```
access-points-config-management/
├── README.md                                                    # Project overview
├── MASTER_USAGE_GUIDE.md                                       # This comprehensive guide
├── workflows/                                                  # n8n workflow files
│   ├── aruba-central-wireless-configuration-workflow.json     # Wireless/SSID automation
│   ├── aruba-central-ap-provisioning-workflow.json           # AP provisioning automation
│   ├── aruba-central-location-services-workflow.json         # Location/beacon services
│   └── aruba-central-client-policy-management-workflow.json  # Client/user management
├── config/                                                    # Configuration files
│   ├── parameters.json                                       # Workflow parameters
│   └── credentials.md                                        # Credential setup guide
├── docs/                                                     # Documentation frameworks
│   ├── bulk-ap-configuration-framework.md                   # Bulk operations guide
│   └── wireless-compliance-monitoring-framework.md          # Compliance monitoring
├── tests/                                                    # Testing framework
│   └── comprehensive-ap-test-suite.md                       # Complete test suite
└── versions/                                                 # Version history
```

## 🚀 Quick Start Guide

### 1. Prerequisites
```bash
# Required infrastructure
✅ n8n instance running at http://192.168.40.100:8006
✅ Aruba Central cloud account with API access
✅ Valid Central API credentials (OAuth 2.0 or API key)
✅ Network connectivity to Aruba Central API endpoints
✅ Slack workspace for notifications (optional)
```

### 2. Import Workflows
1. Access n8n at http://192.168.40.100:8006
2. Navigate to Workflows → Import from file
3. Import each workflow JSON file from the `/workflows/` directory:
   - `aruba-central-wireless-configuration-workflow.json`
   - `aruba-central-ap-provisioning-workflow.json`
   - `aruba-central-location-services-workflow.json`
   - `aruba-central-client-policy-management-workflow.json`

### 3. Configure Credentials
```bash
# Step 1: Create Aruba Central API credentials in n8n
Name: Aruba-Central-OAuth2
Type: OAuth 2.0
Client ID: [your_client_id]
Client Secret: [your_client_secret]
Access Token URL: https://central-prod.arubanetworks.com/oauth2/token

# Step 2: Create Slack credentials (optional)
Name: Slack-Wireless-Notifications
Type: Slack
Token: [your_slack_bot_token]
```

### 4. Test Connectivity
```bash
# Test wireless configuration workflow
curl -X POST "http://192.168.40.100:8006/webhook/aruba-wireless-config" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list_ssids",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id"
  }'
```

## 🔧 Workflow Operations

### 1. Wireless Configuration Management
**Webhook**: `http://192.168.40.100:8006/webhook/aruba-wireless-config`

#### Create Corporate SSID
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-wireless-config" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_ssid",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "ssid_name": "CORPORATE_WIFI",
    "essid": "Corporate Network",
    "security_type": "wpa3_enterprise",
    "vlan_id": 10,
    "network_type": "corporate",
    "broadcast_ssid": true,
    "max_clients": 100
  }'
```

#### Configure Radio Settings
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-wireless-config" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "configure_radio",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "ap_group": "Corporate-Indoor",
    "radio_band": "dual_band",
    "channel_width": "80MHz",
    "power_level": "medium",
    "band_steering": true,
    "fast_transition": true
  }'
```

#### Create Guest Network
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-wireless-config" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_ssid",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "ssid_name": "GUEST_WIFI",
    "essid": "Guest Network",
    "security_type": "open",
    "network_type": "guest",
    "vlan_id": 100,
    "max_clients": 50,
    "session_timeout": 480
  }'
```

### 2. AP Provisioning Management
**Webhook**: `http://192.168.40.100:8006/webhook/aruba-ap-provisioning`

#### Provision Office AP
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-ap-provisioning" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "provision_ap",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "ap_serial": "CNF7G123ABC1",
    "ap_model": "AP-515",
    "site_name": "Headquarters",
    "environment_template": "office",
    "auto_naming": true,
    "naming_convention": "SITE-FLOOR-LOCATION"
  }'
```

#### Create AP Group
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-ap-provisioning" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_group",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "group_name": "Corporate-Floor-02",
    "group_template": "location_based",
    "environment_template": "office"
  }'
```

#### Zero-Touch Provisioning
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-ap-provisioning" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "zero_touch_setup",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "ap_mac": "00:11:22:33:44:55",
    "site_name": "Branch-Office",
    "environment_template": "office"
  }'
```

### 3. Location Services Management
**Webhook**: `http://192.168.40.100:8006/webhook/aruba-location-services`

#### Setup RTLS System
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-location-services" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "setup_rtls",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "site_id": "site_001",
    "site_name": "Corporate Headquarters",
    "campus_name": "Main Campus",
    "building_name": "Building A",
    "environment_template": "corporate"
  }'
```

#### Configure iBeacon
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-location-services" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "configure_beacon",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "beacon_type": "ibeacon",
    "beacon_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "beacon_major": 1,
    "beacon_minor": 100,
    "beacon_power": -12,
    "beacon_interval": 1000
  }'
```

#### Create Geofence
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-location-services" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_geofence",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "geofence_name": "Executive-Area",
    "geofence_coordinates": [
      {"x": 0, "y": 0},
      {"x": 50, "y": 0},
      {"x": 50, "y": 30},
      {"x": 0, "y": 30}
    ],
    "geofence_type": "enter"
  }'
```

### 4. Client Policy Management
**Webhook**: `http://192.168.40.100:8006/webhook/aruba-client-policy`

#### Create Corporate User
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-client-policy" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_user",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "username": "john.doe",
    "user_email": "john.doe@company.com",
    "user_role": "corporate",
    "device_type": "corporate"
  }'
```

#### Configure BYOD Settings
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-client-policy" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "configure_byod",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "device_type": "byod",
    "authentication_method": "802.1x",
    "certificate_type": "user"
  }'
```

#### Create Guest User
```bash
curl -X POST "http://192.168.40.100:8006/webhook/aruba-client-policy" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_guest",
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "customer_id": "your_customer_id",
    "username": "visitor.smith",
    "user_email": "visitor@external.com",
    "guest_duration": 480,
    "guest_sponsor": "john.doe@company.com"
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

#### 1. OAuth Authentication Failures
```bash
# Symptoms: HTTP 401/403 errors
# Solution: Refresh OAuth token
curl -X POST "https://central-prod.arubanetworks.com/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"

# Update credentials in n8n if needed
```

#### 2. Rate Limiting Issues
```bash
# Symptoms: HTTP 429 errors
# Solution: Implement request throttling
# Check rate limit headers:
# X-RateLimit-Limit: 300
# X-RateLimit-Remaining: 250
# X-RateLimit-Reset: 1642781400
```

#### 3. SSID Configuration Conflicts
```bash
# Symptoms: HTTP 409 when creating SSIDs
# Solution: Check existing SSIDs first
curl -X POST "http://192.168.40.100:8006/webhook/aruba-wireless-config" \
  -d '{"operation": "list_ssids", "central_base_url": "...", "customer_id": "..."}'
```

#### 4. AP Provisioning Failures
```bash
# Symptoms: AP not found in inventory
# Solution: Verify AP exists in Central
curl -X POST "http://192.168.40.100:8006/webhook/aruba-ap-provisioning" \
  -d '{"operation": "list_devices", "central_base_url": "...", "customer_id": "..."}'
```

## 📊 Bulk Operations

### Bulk SSID Creation
```python
#!/usr/bin/env python3
import requests
import json

# Bulk SSID creation example
base_url = "http://192.168.40.100:8006/webhook/aruba-wireless-config"
central_url = "https://apigw-prod2.central.arubanetworks.com"
customer_id = "your_customer_id"

ssids = [
    {"name": "CORP_SALES", "vlan": 10, "type": "corporate"},
    {"name": "CORP_MARKETING", "vlan": 20, "type": "corporate"},
    {"name": "CORP_IT", "vlan": 30, "type": "corporate"},
    {"name": "GUEST_VISITOR", "vlan": 100, "type": "guest"}
]

for ssid in ssids:
    payload = {
        "operation": "create_ssid",
        "central_base_url": central_url,
        "customer_id": customer_id,
        "ssid_name": ssid["name"],
        "essid": ssid["name"].replace("_", " "),
        "security_type": "wpa3_enterprise" if ssid["type"] == "corporate" else "open",
        "vlan_id": ssid["vlan"],
        "network_type": ssid["type"]
    }
    
    response = requests.post(base_url, json=payload)
    print(f"Created SSID {ssid['name']}: {response.status_code}")
```

### Bulk AP Provisioning
```python
#!/usr/bin/env python3
import requests
import concurrent.futures

def provision_ap(ap_data):
    payload = {
        "operation": "provision_ap",
        "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
        "customer_id": "your_customer_id",
        **ap_data
    }
    
    response = requests.post(
        "http://192.168.40.100:8006/webhook/aruba-ap-provisioning",
        json=payload
    )
    return {"ap_serial": ap_data["ap_serial"], "status": response.status_code}

# List of APs to provision
aps = [
    {"ap_serial": "CNF7G123ABC1", "ap_model": "AP-515", "site_name": "HQ-Floor-01", "environment_template": "office"},
    {"ap_serial": "CNF7G123ABC2", "ap_model": "AP-515", "site_name": "HQ-Floor-02", "environment_template": "office"},
    {"ap_serial": "CNF7G123ABC3", "ap_model": "AP-535", "site_name": "HQ-Conference", "environment_template": "office"}
]

# Process APs in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(provision_ap, aps))

for result in results:
    print(f"AP {result['ap_serial']}: {'Success' if result['status'] == 200 else 'Failed'}")
```

## 🔐 Security Best Practices

### Credential Management
```bash
# Use n8n credential store (never hardcode)
✅ Store in n8n credentials
❌ Hardcode in workflows
❌ Include in API calls

# Regular credential rotation
1. Update Central API credentials monthly
2. Update n8n credentials accordingly
3. Test workflows after credential updates
```

### API Security
```bash
# Central configuration
✅ Use OAuth 2.0 with short-lived tokens
✅ Implement IP allowlists if possible
✅ Enable API access logging in Central
✅ Monitor API usage for anomalies
✅ Use HTTPS only for all communications
```

### Input Validation
```bash
# All workflows include validation
✅ Customer ID format validation
✅ SSID name pattern matching
✅ AP serial number validation
✅ Email address validation for users
✅ Coordinate range checking for locations
```

## 📈 Advanced Usage

### Environment-Specific Templates
```json
{
  "office_template": {
    "radio_power": "medium",
    "channel_width": "80MHz",
    "max_clients": 50,
    "band_steering": true
  },
  "retail_template": {
    "radio_power": "high",
    "channel_width": "40MHz",
    "max_clients": 100,
    "load_balancing": true
  },
  "healthcare_template": {
    "radio_power": "low",
    "channel_width": "20MHz",
    "max_clients": 30,
    "location_services": true
  }
}
```

### Integration Examples
```python
# ServiceNow integration example
def create_change_request(operation, details):
    change_data = {
        "short_description": f"Wireless {operation}",
        "description": details,
        "type": "normal",
        "state": "new"
    }
    # Submit to ServiceNow API
    
# Monitoring integration
def update_monitoring_dashboard(metrics):
    # Update network monitoring system
    # Adjust alerting thresholds
    # Document configuration changes
```

## 🔄 Maintenance

### Regular Tasks
- [ ] Weekly credential validation
- [ ] Monthly compliance audits
- [ ] Quarterly template updates
- [ ] Semi-annual disaster recovery testing

### Health Checks
```bash
# Daily health check script
#!/bin/bash
workflows=("aruba-wireless-config" "aruba-ap-provisioning" "aruba-location-services" "aruba-client-policy")

for workflow in "${workflows[@]}"; do
  echo "Checking $workflow..."
  curl -s -X POST "http://192.168.40.100:8006/webhook/$workflow" \
    -d '{"operation": "health_check"}' \
    | jq '.status // "ERROR"'
done
```

## 📞 Support & Resources

### Documentation Links
- [Project README](./README.md)
- [Bulk Operations Framework](./docs/bulk-ap-configuration-framework.md)
- [Compliance Monitoring](./docs/wireless-compliance-monitoring-framework.md)
- [Comprehensive Test Suite](./tests/comprehensive-ap-test-suite.md)

### API References
- **Aruba Central API**: HPE Developer Portal
- **n8n Documentation**: https://docs.n8n.io/
- **OAuth 2.0 Guide**: Central API authentication documentation

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] n8n instance configured and accessible
- [ ] Aruba Central account with API access
- [ ] API credentials configured in n8n
- [ ] Network connectivity verified
- [ ] Test APs identified for validation

### Deployment
- [ ] Import all 4 workflow JSON files
- [ ] Configure workflow parameters
- [ ] Test each workflow individually
- [ ] Run integration test suite
- [ ] Verify error handling and rollback

### Post-Deployment
- [ ] Document production AP inventory
- [ ] Set up monitoring and alerting
- [ ] Train operations team on workflows
- [ ] Establish maintenance schedule
- [ ] Create operational runbooks

This master guide provides everything needed to successfully deploy and operate the complete Access Points configuration management automation suite with enterprise-grade reliability and comprehensive functionality.
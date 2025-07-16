# Aruba Central AP Provisioning Workflow

## Overview

The **Aruba Central AP Provisioning** workflow provides comprehensive automation for access point provisioning, template deployment, and configuration management in HPE Aruba Central environments. This workflow supports zero-touch provisioning, bulk operations, environment-specific templates, and complete error handling with rollback capabilities.

## Features

### ✅ **Core Operations**
- **AP Provisioning**: Complete access point setup and configuration
- **Template Management**: Create, deploy, and manage configuration templates
- **Group Management**: Create and manage AP groups with policies
- **Zero-Touch Setup**: Automated provisioning for new APs
- **Firmware Management**: Update and verify firmware versions
- **Configuration Compliance**: Validate configurations against standards

### ✅ **Advanced Capabilities**
- **Environment Templates**: Pre-configured settings for different environments
- **Smart Error Handling**: Categorized error responses with rollback
- **Configuration Validation**: Compliance checking against organizational policies
- **Automatic Naming**: Intelligent AP naming based on location and conventions
- **Bulk Operations**: Support for processing multiple APs
- **Real-time Monitoring**: Status tracking and notifications

## Supported Operations

| Operation | Description | Required Parameters |
|-----------|-------------|-------------------|
| `provision_ap` | Provision new access point with configuration | `ap_serial`, `ap_group`, `site_name` |
| `create_template` | Create new AP configuration template | `template_name`, `environment_template` |
| `deploy_template` | Deploy template to AP or group | `template_name`, `ap_group` |
| `create_group` | Create new AP group with settings | `ap_group`, `environment_template` |
| `move_ap` | Move AP to different group | `ap_serial`, `ap_group` |
| `firmware_update` | Update AP firmware version | `ap_serial`, `firmware_version` |
| `zero_touch_setup` | Automated zero-touch AP provisioning | `ap_mac` or `ap_serial`, `site_name` |

## Input Parameters

### **Required Parameters**
```json
{
  "operation": "provision_ap|create_template|deploy_template|create_group|move_ap|firmware_update|zero_touch_setup"
}
```

### **Operation-Specific Parameters**

#### AP Provisioning & Management
```json
{
  "ap_serial": "ABC123456789",
  "ap_mac": "00:11:22:33:44:55",
  "ap_model": "AP-515|AP-535|AP-555|AP-575|AP-615|AP-635|AP-655|AP-675|AP-685"
}
```

#### Location & Site Information
```json
{
  "site_name": "Headquarters",
  "floor_name": "Floor-02",
  "ap_group": "HQ-Office-APs"
}
```

#### Template & Configuration
```json
{
  "template_name": "office-standard-template",
  "environment_template": "office|retail|healthcare|education|warehouse|hospitality",
  "default_config": true
}
```

#### Naming & Automation
```json
{
  "auto_naming": true,
  "naming_convention": "{site}-{floor}-AP-{serial}",
  "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
  "customer_id": "default"
}
```

#### Firmware Management
```json
{
  "firmware_version": "8.10.0.8"
}
```

## Environment Templates

### 🏢 **Office Environment**
**Use Case**: Standard corporate office settings
```json
{
  "description": "Standard corporate office settings",
  "features": ["standard_security", "corporate_ssid", "guest_access"],
  "radio_config": {
    "power_level": "medium",
    "channel_width": "80MHz",
    "band_steering": true
  }
}
```

### 🛍️ **Retail Environment**
**Use Case**: High density retail environment
```json
{
  "description": "High density retail environment",
  "features": ["high_density", "guest_portal", "pos_support"],
  "radio_config": {
    "power_level": "high",
    "channel_width": "40MHz",
    "client_limit": 100
  }
}
```

### 🏥 **Healthcare Environment**
**Use Case**: Secure healthcare with IoT support
```json
{
  "description": "Secure healthcare with IoT support",
  "features": ["enhanced_security", "iot_support", "location_services"],
  "radio_config": {
    "power_level": "medium",
    "location_services": true,
    "iot_radio": true
  }
}
```

### 🎓 **Education Environment**
**Use Case**: Multi-SSID education environment
```json
{
  "description": "Multi-SSID education environment",
  "features": ["multi_ssid", "byod_support", "content_filtering"],
  "radio_config": {
    "power_level": "high",
    "multiple_ssid": true,
    "bandwidth_control": true
  }
}
```

### 📦 **Warehouse Environment**
**Use Case**: Extended range warehouse settings
```json
{
  "description": "Extended range warehouse settings",
  "features": ["extended_range", "rugged_settings", "minimal_ssid"],
  "radio_config": {
    "power_level": "maximum",
    "channel_width": "20MHz",
    "coverage_optimization": true
  }
}
```

### 🏨 **Hospitality Environment**
**Use Case**: Guest portal and captive portal
```json
{
  "description": "Guest portal and captive portal",
  "features": ["guest_portal", "captive_portal", "bandwidth_control"],
  "radio_config": {
    "power_level": "medium",
    "guest_isolation": true,
    "rate_limiting": true
  }
}
```

## AP Group Templates

### **Location-Based Groups**
- **Pattern**: `{building}-{floor}-{area}`
- **Example**: `HQ-02-West`
- **Use Case**: Organize APs by physical location

### **Function-Based Groups**
- **Pattern**: `{function}-{location}`
- **Example**: `Corporate-HQ`
- **Use Case**: Group APs by network function

### **Model-Based Groups**
- **Pattern**: `{model}-{environment}`
- **Example**: `AP515-Indoor`
- **Use Case**: Group similar AP models together

## API Endpoints Used

### **Device Management**
```
GET    /platform/device_inventory/v1/devices
GET    /monitoring/v1/aps
PUT    /device_management/v1/device/{serial}/group
PUT    /configuration/v1/devices/{serial}/configuration
```

### **Group Management**
```
POST   /configuration/v2/ap_groups
PUT    /configuration/v2/ap_groups/{group_name}
GET    /configuration/v2/ap_groups/{group_name}
DELETE /configuration/v2/ap_groups/{group_name}
```

### **Template Management**
```
GET    /configuration/v2/ap_groups/{group_name}/template
PUT    /configuration/v2/ap_groups/{group_name}/template
```

### **Firmware Management**
```
POST   /device_management/v1/device/firmware
GET    /device_management/v1/device/firmware/status
```

## Error Handling

### **Error Categories**
- **`ap_not_found`**: AP serial not found in inventory
- **`template_error`**: Template deployment failures
- **`firmware_error`**: Firmware update issues
- **`group_error`**: AP group creation/assignment problems
- **`config_validation`**: Configuration validation errors
- **`network_error`**: Network connectivity issues
- **`authentication_error`**: API authentication failures
- **`rate_limit`**: API rate limiting
- **`server_error`**: Central API server errors

### **Error Severities**
- **`critical`**: Requires immediate attention
- **`high`**: Significant impact on operations
- **`medium`**: Moderate impact, can be addressed during business hours
- **`low`**: Minor issues, informational

### **Rollback Scenarios**
- ✅ **Template Deployment**: Revert to previous template version
- ✅ **Firmware Updates**: Rollback to previous firmware
- ✅ **Configuration Changes**: Restore previous AP configuration
- ✅ **Partial Operations**: Cleanup incomplete resources

## Compliance Checking

### **Compliance Rules by Environment**

#### Office Environment
- **Required SSIDs**: Corporate, Guest
- **Security Standards**: WPA3, WPA2
- **Max Client Limit**: 50
- **Required Features**: band_steering, fast_roaming

#### Retail Environment
- **Required SSIDs**: Store, POS, Guest
- **Security Standards**: WPA3, WPA2
- **Max Client Limit**: 100
- **Required Features**: high_density, load_balancing

#### Healthcare Environment
- **Required SSIDs**: Clinical, Admin, IoT
- **Security Standards**: WPA3-Enterprise
- **Max Client Limit**: 25
- **Required Features**: enhanced_security, location_services

#### Education Environment
- **Required SSIDs**: Faculty, Student, Guest
- **Security Standards**: WPA3, WPA2-Enterprise
- **Max Client Limit**: 75
- **Required Features**: byod_support, content_filtering

#### Warehouse Environment
- **Required SSIDs**: Operations
- **Security Standards**: WPA3
- **Max Client Limit**: 15
- **Required Features**: extended_range, rugged_mode

#### Hospitality Environment
- **Required SSIDs**: Staff, Guest
- **Security Standards**: WPA3, WPA2
- **Max Client Limit**: 80
- **Required Features**: guest_portal, rate_limiting

### **Compliance Scoring**
- **100%**: Fully compliant with all standards
- **75-99%**: Compliant with minor warnings
- **50-74%**: Partially compliant, action needed
- **<50%**: Non-compliant, immediate action required

## Usage Examples

### **Example 1: Provision Office AP**
```json
{
  "operation": "provision_ap",
  "ap_serial": "ABC123456789",
  "ap_model": "AP-515",
  "site_name": "Headquarters",
  "floor_name": "Floor-02",
  "ap_group": "HQ-Office-APs",
  "environment_template": "office",
  "auto_naming": true,
  "naming_convention": "{site}-{floor}-AP-{serial}",
  "default_config": true
}
```

### **Example 2: Zero-Touch Setup**
```json
{
  "operation": "zero_touch_setup",
  "ap_mac": "00:11:22:33:44:55",
  "site_name": "Branch-Office",
  "floor_name": "Ground",
  "environment_template": "office",
  "auto_naming": true
}
```

### **Example 3: Create Retail Group**
```json
{
  "operation": "create_group",
  "ap_group": "Store-Main-APs",
  "environment_template": "retail",
  "template_name": "retail-high-density"
}
```

### **Example 4: Firmware Update**
```json
{
  "operation": "firmware_update",
  "ap_serial": "ABC123456789",
  "firmware_version": "8.10.0.8"
}
```

### **Example 5: Deploy Healthcare Template**
```json
{
  "operation": "deploy_template",
  "template_name": "healthcare-secure",
  "ap_group": "Hospital-Clinical-APs",
  "environment_template": "healthcare"
}
```

## Quick Start Guide

### **Step 1: Set Up Credentials**
1. Configure Aruba Central API credentials in n8n
2. Ensure proper API permissions (read/write access)
3. Test connectivity to Central API

### **Step 2: Import Workflow**
1. Import `aruba-central-ap-provisioning-workflow.json` into n8n
2. Configure credential references
3. Test with sample data

### **Step 3: Basic AP Provisioning**
```bash
# Execute manual trigger with basic parameters
curl -X POST "http://n8n-instance:5678/webhook/ap-provisioning" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "provision_ap",
    "ap_serial": "YOUR_AP_SERIAL",
    "site_name": "YOUR_SITE",
    "environment_template": "office"
  }'
```

### **Step 4: Monitor Execution**
1. Check n8n execution logs
2. Monitor Slack notifications
3. Verify AP status in Central dashboard

## Monitoring & Notifications

### **Success Notifications**
- **Channel**: `#network-operations`
- **Information**: Operation type, AP details, compliance score
- **Actions**: Next steps and monitoring recommendations

### **Error Notifications**
- **Channel**: `#network-alerts`
- **Information**: Error category, severity, recommendations
- **Actions**: Rollback status and corrective measures

### **Compliance Notifications**
- **Channel**: `#compliance-reports`
- **Information**: Compliance score, violations, recommendations
- **Actions**: Remediation steps and follow-up tasks

## Troubleshooting

### **Common Issues**

#### **AP Not Found**
- ✅ Verify AP serial number format (12 alphanumeric characters)
- ✅ Check if AP is in device inventory
- ✅ Ensure AP is powered on and network connected

#### **Template Deployment Failed**
- ✅ Verify template exists in Central
- ✅ Check template syntax and configuration
- ✅ Ensure template compatibility with AP model

#### **Firmware Update Failed**
- ✅ Check firmware version compatibility
- ✅ Verify firmware file availability
- ✅ Ensure AP has sufficient memory

#### **Group Creation Failed**
- ✅ Verify group name format and length
- ✅ Check if group already exists
- ✅ Ensure proper group permissions

#### **Authentication Issues**
- ✅ Check API credentials
- ✅ Verify token expiration
- ✅ Ensure proper API permissions

### **Debug Mode**
Enable debug logging by adding `debug: true` to workflow parameters for detailed execution information.

## Security Considerations

### **Credential Management**
- Use n8n credential store for API keys
- Implement credential rotation schedule
- Monitor credential usage and access

### **API Security**
- Validate all input parameters
- Implement proper error handling
- Use HTTPS for all API communications
- Log all configuration changes

### **Network Security**
- Ensure secure connectivity to Central
- Implement proper firewall rules
- Monitor for unauthorized access attempts

## Performance Optimization

### **API Rate Limiting**
- Implement exponential backoff for rate limits
- Use batch operations where possible
- Monitor API usage patterns

### **Workflow Efficiency**
- Parallel processing for independent operations
- Caching for frequently accessed data
- Timeout optimization for different operations

### **Resource Management**
- Monitor workflow execution times
- Optimize node configurations
- Implement proper error recovery

## Maintenance

### **Regular Tasks**
- **Daily**: Monitor execution logs and success rates
- **Weekly**: Review error patterns and performance metrics
- **Monthly**: Update firmware versions and templates
- **Quarterly**: Security audit and credential rotation

### **Updates**
- Keep workflow updated with latest API versions
- Test changes in development environment
- Document all modifications and versioning

## Support

### **Documentation**
- Workflow configuration guide
- API reference documentation
- Troubleshooting procedures
- Best practices guide

### **Contact**
- **Team**: Network Automation Team
- **Email**: network-automation@company.com
- **Slack**: #network-automation
- **Documentation**: [Internal Wiki Link]

---

**Last Updated**: January 16, 2025  
**Version**: 1.0.0  
**Workflow File**: `aruba-central-ap-provisioning-workflow.json`
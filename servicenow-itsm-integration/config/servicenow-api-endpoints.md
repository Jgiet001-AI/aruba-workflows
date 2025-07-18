# ServiceNow REST API Endpoints for ITSM Integration

**Created**: January 17, 2025  
**Purpose**: Comprehensive API reference for ServiceNow ITSM integration with HPE Aruba automation  
**Version**: 1.0

## Overview

This document provides a complete reference for ServiceNow REST API endpoints used in HPE Aruba network automation integration. The APIs enable seamless integration between Aruba network infrastructure and ServiceNow ITSM processes.

## Base URL Structure
```
https://{instance-name}.service-now.com/api/now/table/{table-name}
```

## Authentication Methods

### 1. Basic Authentication
```http
Authorization: Basic {base64(username:password)}
```

### 2. OAuth 2.0 Bearer Token
```http
Authorization: Bearer {access_token}
```

### 3. API Key Authentication
```http
X-UserToken: {api_key}
```

## Core API Categories

### 1. INCIDENT MANAGEMENT APIS (12 endpoints)

#### Create Incident
```http
POST /api/now/table/incident
Content-Type: application/json

{
  "short_description": "Aruba AP-515 Access Point Down",
  "description": "Access Point AP-515 at Building A Floor 2 is not responding",
  "category": "Network",
  "subcategory": "Wireless",
  "priority": "2",
  "impact": "2",
  "urgency": "2",
  "caller_id": "network.admin@company.com",
  "assignment_group": "Network Operations",
  "business_service": "Wireless Infrastructure",
  "cmdb_ci": "AP-515-BuildingA-F2",
  "location": "Building A Floor 2",
  "u_aruba_device_type": "Access Point",
  "u_aruba_mac_address": "00:11:22:33:44:55",
  "u_aruba_ip_address": "192.168.1.100"
}
```

#### Get Incident
```http
GET /api/now/table/incident/{sys_id}
```

#### Update Incident
```http
PUT /api/now/table/incident/{sys_id}
Content-Type: application/json

{
  "state": "2",
  "work_notes": "Device rebooted via Aruba Central API",
  "assigned_to": "network.admin@company.com",
  "resolution_code": "Solved (Permanently)"
}
```

#### Query Incidents
```http
GET /api/now/table/incident?sysparm_query=category=Network^subcategory=Wireless^state!=6
```

#### Add Work Notes
```http
POST /api/now/table/sys_journal_field
Content-Type: application/json

{
  "element": "work_notes",
  "element_id": "{incident_sys_id}",
  "table": "incident",
  "value": "Automated diagnostic completed - device operational"
}
```

#### Add Attachments
```http
POST /api/now/attachment/file?table_name=incident&table_sys_id={sys_id}
Content-Type: multipart/form-data

{file: diagnostic_report.txt}
```

#### Assign Incident
```http
PUT /api/now/table/incident/{sys_id}
Content-Type: application/json

{
  "assignment_group": "Network Level 2",
  "assigned_to": "senior.network.admin@company.com",
  "state": "2"
}
```

#### Get Incident Comments
```http
GET /api/now/table/sys_journal_field?sysparm_query=element_id={sys_id}^element=comments
```

#### Close Incident
```http
PUT /api/now/table/incident/{sys_id}
Content-Type: application/json

{
  "state": "6",
  "close_code": "Solved (Permanently)",
  "close_notes": "Issue resolved via automated remediation"
}
```

#### Reopen Incident
```http
PUT /api/now/table/incident/{sys_id}
Content-Type: application/json

{
  "state": "2",
  "work_notes": "Issue recurred - reopening for investigation"
}
```

#### Get Incident History
```http
GET /api/now/table/sys_audit?sysparm_query=tablename=incident^documentkey={sys_id}
```

#### Bulk Incident Operations
```http
POST /api/now/import/{import_set_table}
Content-Type: application/json

{
  "records": [
    {"short_description": "Network Issue 1"},
    {"short_description": "Network Issue 2"}
  ]
}
```

### 2. SERVICE REQUEST APIS (8 endpoints)

#### Get Service Catalog
```http
GET /api/sn_sc/servicecatalog/catalogs
```

#### Get Catalog Items
```http
GET /api/sn_sc/servicecatalog/items
```

#### Submit Service Request
```http
POST /api/sn_sc/servicecatalog/items/{item_sys_id}/order_now
Content-Type: application/json

{
  "sysparm_quantity": "1",
  "variables": {
    "u_network_location": "Building A Floor 2",
    "u_access_point_model": "AP-515",
    "u_vlan_requirement": "VLAN 100",
    "u_ssid_configuration": "Corporate-WiFi"
  }
}
```

#### Get Request Status
```http
GET /api/now/table/sc_request/{sys_id}
```

#### Update Request Item
```http
PUT /api/now/table/sc_req_item/{sys_id}
Content-Type: application/json

{
  "state": "3",
  "work_notes": "Access point provisioned via Aruba Central",
  "u_aruba_device_serial": "AP515-ABC123"
}
```

#### Get Approval Status
```http
GET /api/now/table/sysapproval_approver?sysparm_query=source_table=sc_request^document_id={request_id}
```

#### Process Approval
```http
PUT /api/now/table/sysapproval_approver/{approval_id}
Content-Type: application/json

{
  "state": "approved",
  "comments": "Network capacity assessment completed - approved"
}
```

#### Get Request Item Details
```http
GET /api/now/table/sc_req_item/{sys_id}
```

### 3. CHANGE MANAGEMENT APIS (10 endpoints)

#### Create Change Request
```http
POST /api/now/table/change_request
Content-Type: application/json

{
  "short_description": "Network Switch Firmware Update",
  "description": "Update firmware on core switches for security patch",
  "category": "Network",
  "priority": "2",
  "risk": "Medium", 
  "impact": "Medium",
  "requested_by": "network.admin",
  "assignment_group": "Network Operations",
  "planned_start_date": "2025-01-20 02:00:00",
  "planned_end_date": "2025-01-20 04:00:00",
  "implementation_plan": "Sequential firmware update with rollback capability",
  "test_plan": "Verify connectivity post-update",
  "backout_plan": "Rollback to previous firmware version",
  "business_justification": "Security compliance requirement"
}
```

#### Get Change Request
```http
GET /api/now/table/change_request/{sys_id}
```

#### Update Change Status
```http
PUT /api/now/table/change_request/{sys_id}
Content-Type: application/json

{
  "state": "3",
  "work_notes": "Implementation in progress - 50% complete"
}
```

#### Create Change Task
```http
POST /api/now/table/change_task
Content-Type: application/json

{
  "change_request": "{change_request_sys_id}",
  "short_description": "Update switch SW01 firmware",
  "assigned_to": "network.engineer@company.com",
  "planned_start_date": "2025-01-20 02:00:00",
  "planned_end_date": "2025-01-20 02:30:00"
}
```

#### Get Change Tasks
```http
GET /api/now/table/change_task?sysparm_query=change_request={change_request_sys_id}
```

#### Submit for Approval
```http
PUT /api/now/table/change_request/{sys_id}
Content-Type: application/json

{
  "state": "2",
  "approval": "requested"
}
```

#### Get CAB Schedule
```http
GET /api/now/table/change_request?sysparm_query=cab_required=true^state=2
```

#### Schedule Change
```http
PUT /api/now/table/change_request/{sys_id}
Content-Type: application/json

{
  "state": "4",
  "scheduled_start_date": "2025-01-20 02:00:00",
  "scheduled_end_date": "2025-01-20 04:00:00"
}
```

#### Implement Change
```http
PUT /api/now/table/change_request/{sys_id}
Content-Type: application/json

{
  "state": "3",
  "work_start": "2025-01-20 02:00:00",
  "work_notes": "Implementation started"
}
```

#### Close Change
```http
PUT /api/now/table/change_request/{sys_id}
Content-Type: application/json

{
  "state": "3",
  "close_code": "successful",
  "close_notes": "Change implemented successfully",
  "review_comments": "No issues encountered"
}
```

### 4. ASSET MANAGEMENT APIS (12 endpoints)

#### Get Configuration Items
```http
GET /api/now/table/cmdb_ci
```

#### Create CI
```http
POST /api/now/table/cmdb_ci_computer
Content-Type: application/json

{
  "name": "AP-515-BuildingA-F2",
  "serial_number": "AP515ABC123",
  "model_id": "AP-515",
  "manufacturer": "HPE Aruba",
  "location": "Building A Floor 2",
  "ip_address": "192.168.1.100",
  "mac_address": "00:11:22:33:44:55",
  "operational_status": "Operational",
  "u_device_type": "Access Point",
  "u_management_url": "https://aruba-central.company.com"
}
```

#### Update CI
```http
PUT /api/now/table/cmdb_ci_computer/{sys_id}
Content-Type: application/json

{
  "operational_status": "Non-Operational",
  "comments": "Device offline - investigating connectivity"
}
```

#### Get CI Relationships
```http
GET /api/now/table/cmdb_rel_ci?sysparm_query=parent={ci_sys_id}^ORchild={ci_sys_id}
```

#### Create CI Relationship
```http
POST /api/now/table/cmdb_rel_ci
Content-Type: application/json

{
  "parent": "{switch_ci_sys_id}",
  "child": "{ap_ci_sys_id}",
  "type": "Connected to"
}
```

#### Discovery Integration
```http
POST /api/now/table/discovery_status
Content-Type: application/json

{
  "name": "Aruba Network Discovery",
  "state": "Pending",
  "ip_range": "192.168.1.0/24"
}
```

#### Asset Inventory
```http
GET /api/now/table/alm_asset?sysparm_query=model_category=Network Equipment
```

#### Update Asset Status
```http
PUT /api/now/table/alm_asset/{sys_id}
Content-Type: application/json

{
  "install_status": "In use",
  "substatus": "Operational",
  "location": "Building A Floor 2"
}
```

#### Get Hardware Models
```http
GET /api/now/table/cmdb_model?sysparm_query=manufacturer=HPE Aruba
```

#### Software Inventory
```http
GET /api/now/table/cmdb_software_instance?sysparm_query=installed_on={ci_sys_id}
```

#### License Management
```http
GET /api/now/table/alm_license?sysparm_query=software_model={software_model_sys_id}
```

#### Contract Management
```http
GET /api/now/table/ast_contract?sysparm_query=ci={ci_sys_id}
```

#### Warranty Information
```http
GET /api/now/table/alm_hardware?sysparm_query=ci={ci_sys_id}
```

## HPE Aruba Specific Integration Patterns

### Network Device Incident Automation
```javascript
const createNetworkIncident = async (deviceData) => {
  const incidentPayload = {
    short_description: `${deviceData.type} ${deviceData.name} - ${deviceData.issue}`,
    description: `Device: ${deviceData.name}\nIP: ${deviceData.ip}\nMAC: ${deviceData.mac}\nLocation: ${deviceData.location}\nIssue: ${deviceData.issue}`,
    category: "Network",
    subcategory: deviceData.type === "AP" ? "Wireless" : "Wired",
    priority: deviceData.severity,
    impact: deviceData.impact,
    urgency: deviceData.urgency,
    caller_id: "aruba.automation@company.com",
    assignment_group: "Network Operations",
    cmdb_ci: deviceData.ci_name,
    u_aruba_device_type: deviceData.type,
    u_aruba_serial: deviceData.serial,
    u_aruba_ip_address: deviceData.ip,
    u_aruba_mac_address: deviceData.mac,
    u_aruba_central_url: deviceData.central_url
  };
  
  return await createIncident(incidentPayload);
};
```

### Configuration Change Automation
```javascript
const createConfigChangeRequest = async (changeData) => {
  const changePayload = {
    short_description: `${changeData.operation} - ${changeData.devices.length} devices`,
    description: `Automated configuration change via Aruba Central\nOperation: ${changeData.operation}\nDevices: ${changeData.devices.join(', ')}\nConfiguration: ${changeData.config}`,
    category: "Network",
    priority: "3",
    risk: "Low",
    impact: "Low",
    type: "automated",
    requested_by: "aruba.automation",
    assignment_group: "Network Operations",
    implementation_plan: changeData.implementation_plan,
    test_plan: "Automated verification via Aruba Central API",
    backout_plan: "Automatic rollback via configuration templates",
    u_automation_tool: "Aruba Central",
    u_config_template: changeData.template_name
  };
  
  return await createChangeRequest(changePayload);
};
```

## Error Handling and Rate Limiting

### Error Response Format
```json
{
  "error": {
    "message": "Invalid table",
    "detail": "Table 'invalid_table' does not exist"
  },
  "status": "failure"
}
```

### Rate Limiting
- **Default Limit**: 5000 requests per hour per user
- **Rate Limit Headers**:
  ```
  X-RateLimit-Limit: 5000
  X-RateLimit-Remaining: 4999
  X-RateLimit-Reset: 1642447200
  ```

### Retry Strategy
```javascript
const retryRequest = async (requestFn, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await requestFn();
    } catch (error) {
      if (error.status === 429 && i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000; // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
};
```

## Security Best Practices

### 1. Authentication Security
- Use OAuth 2.0 with appropriate scopes
- Implement token refresh logic
- Store credentials securely
- Use service accounts for automation

### 2. API Security
- Validate all input parameters
- Use HTTPS for all requests
- Implement request signing where available
- Log all API interactions for audit

### 3. Data Protection
- Encrypt sensitive data in transit and at rest
- Implement data retention policies
- Follow data privacy regulations
- Use field-level access controls

## Integration Monitoring

### Health Check Endpoint
```http
GET /api/now/stats
```

### Performance Monitoring
- Track response times
- Monitor error rates
- Set up alerting for failures
- Log performance metrics

This comprehensive API reference enables seamless integration between HPE Aruba network infrastructure and ServiceNow ITSM processes, providing automated incident management, service requests, change control, and asset management capabilities.
# Aruba Central API Testing Flow

## Flow Overview
**Name**: Aruba Central API Health Check and Device Management  
**Purpose**: Automated testing of Aruba Central API authentication, device management, and monitoring  
**Trigger**: Scheduled (every 30 minutes) or Manual execution  

## Flow Structure

### 1. Authentication Block
```
┌─────────────────────┐
│  OAuth 2.0 Login    │
│  (POST /oauth2/token)│
│                     │
│  Variables:         │
│  - client_id        │
│  - client_secret    │
│  - grant_type       │
│                     │
│  Output:            │
│  - access_token     │
│  - token_expiry     │
└─────────────────────┘
```

**Configuration**:
- **URL**: `{{auth_url}}/oauth2/token`
- **Method**: POST
- **Headers**: `Content-Type: application/x-www-form-urlencoded`
- **Body**: 
  ```
  grant_type=client_credentials
  client_id={{client_id}}
  client_secret={{client_secret}}
  scope=all
  ```

**Test Script**:
```javascript
// Test successful authentication
pm.test('Authentication successful', function() {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    pm.expect(response).to.have.property('access_token');
    pm.expect(response.token_type).to.eql('Bearer');
    
    // Store token for next requests
    pm.globals.set('access_token', response.access_token);
    pm.globals.set('token_expiry', Date.now() + (response.expires_in * 1000));
});

// Handle authentication failure
pm.test('Handle auth failure gracefully', function() {
    if (pm.response.code !== 200) {
        pm.globals.set('auth_failed', true);
        pm.globals.set('auth_error', pm.response.json().error_description);
    }
});
```

### 2. Device Management Block
```
┌─────────────────────┐
│  List Devices       │
│  (GET /devices)     │
│                     │
│  Headers:           │
│  - Authorization    │
│                     │
│  Query Params:      │
│  - limit: 100       │
│  - offset: 0        │
│                     │
│  Output:            │
│  - device_count     │
│  - device_list      │
└─────────────────────┘
```

**Configuration**:
- **URL**: `{{base_url}}/platform/device_inventory/v1/devices`
- **Method**: GET
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Query Parameters**:
  - `limit`: 100
  - `offset`: 0

**Test Script**:
```javascript
// Test device listing
pm.test('Device list retrieved successfully', function() {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    pm.expect(response).to.have.property('devices');
    pm.expect(response.devices).to.be.an('array');
    
    // Store device count and first device for next tests
    pm.globals.set('device_count', response.devices.length);
    if (response.devices.length > 0) {
        pm.globals.set('first_device_serial', response.devices[0].serial);
    }
});

// Test performance
pm.test('Response time acceptable', function() {
    pm.expect(pm.response.responseTime).to.be.below(5000);
});
```

### 3. Device Details Block
```
┌─────────────────────┐
│  Get Device Details │
│  (GET /devices/{id})│
│                     │
│  Path Variables:    │
│  - device_serial    │
│                     │
│  Headers:           │
│  - Authorization    │
│                     │
│  Output:            │
│  - device_status    │
│  - device_health    │
└─────────────────────┘
```

**Configuration**:
- **URL**: `{{base_url}}/platform/device_inventory/v1/devices/{{first_device_serial}}`
- **Method**: GET
- **Headers**: `Authorization: Bearer {{access_token}}`

**Test Script**:
```javascript
// Test device details
pm.test('Device details retrieved', function() {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    pm.expect(response).to.have.property('serial');
    pm.expect(response).to.have.property('status');
    pm.expect(response).to.have.property('firmware_version');
    
    // Store device health status
    pm.globals.set('device_status', response.status);
    pm.globals.set('device_health', response.health_status || 'unknown');
});
```

### 4. Monitoring Block
```
┌─────────────────────┐
│  Get Performance    │
│  Stats              │
│  (GET /monitoring/  │
│   statistics)       │
│                     │
│  Query Params:      │
│  - timerange: 3H    │
│  - device_type: ap  │
│                     │
│  Output:            │
│  - performance_data │
│  - alert_count      │
└─────────────────────┘
```

**Configuration**:
- **URL**: `{{base_url}}/monitoring/v1/statistics/device`
- **Method**: GET
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Query Parameters**:
  - `timerange`: 3H
  - `device_type`: ap

**Test Script**:
```javascript
// Test monitoring data
pm.test('Performance statistics retrieved', function() {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    pm.expect(response).to.have.property('statistics');
    
    // Store performance metrics
    pm.globals.set('performance_data', JSON.stringify(response.statistics));
});
```

### 5. Health Check Summary Block
```
┌─────────────────────┐
│  Generate Health    │
│  Report             │
│                     │
│  Inputs:            │
│  - auth_status      │
│  - device_count     │
│  - device_health    │
│  - performance_data │
│                     │
│  Output:            │
│  - health_report    │
│  - alert_needed     │
└─────────────────────┘
```

**Configuration**:
- **Type**: Script Block
- **Script**:
```javascript
// Generate comprehensive health report
const healthReport = {
    timestamp: new Date().toISOString(),
    authentication: {
        status: pm.globals.get('auth_failed') ? 'FAILED' : 'SUCCESS',
        error: pm.globals.get('auth_error') || null
    },
    devices: {
        count: parseInt(pm.globals.get('device_count') || '0'),
        status: pm.globals.get('device_status') || 'unknown',
        health: pm.globals.get('device_health') || 'unknown'
    },
    performance: {
        data_available: pm.globals.get('performance_data') ? true : false,
        last_check: new Date().toISOString()
    },
    overall_health: 'HEALTHY' // Will be calculated based on above
};

// Calculate overall health
if (healthReport.authentication.status === 'FAILED') {
    healthReport.overall_health = 'CRITICAL';
} else if (healthReport.devices.count === 0) {
    healthReport.overall_health = 'WARNING';
} else if (healthReport.devices.health === 'down') {
    healthReport.overall_health = 'CRITICAL';
}

// Store report
pm.globals.set('health_report', JSON.stringify(healthReport));
pm.globals.set('alert_needed', healthReport.overall_health !== 'HEALTHY');

console.log('Health Report:', healthReport);
```

### 6. Notification Block (Conditional)
```
┌─────────────────────┐
│  Send Alert         │
│  (POST /webhook)    │
│                     │
│  Condition:         │
│  - alert_needed     │
│                     │
│  Body:              │
│  - health_report    │
│  - alert_level      │
│                     │
│  Output:            │
│  - notification_sent│
└─────────────────────┘
```

**Configuration**:
- **URL**: `{{slack_webhook_url}}`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Condition**: `{{alert_needed}} === true`
- **Body**:
```json
{
    "text": "Aruba Central API Health Alert",
    "attachments": [
        {
            "color": "{{alert_needed === true ? 'danger' : 'good'}}",
            "fields": [
                {
                    "title": "Overall Health",
                    "value": "{{overall_health}}",
                    "short": true
                },
                {
                    "title": "Device Count",
                    "value": "{{device_count}}",
                    "short": true
                },
                {
                    "title": "Authentication",
                    "value": "{{auth_status}}",
                    "short": true
                },
                {
                    "title": "Timestamp",
                    "value": "{{timestamp}}",
                    "short": true
                }
            ]
        }
    ]
}
```

## Flow Variables

### Environment Variables
```javascript
// Set these in your Postman environment
{
    "base_url": "https://apigw-prod2.central.arubanetworks.com",
    "auth_url": "https://app.central.arubanetworks.com",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "slack_webhook_url": "https://hooks.slack.com/services/your/webhook/url"
}
```

### Global Variables (Set during flow execution)
```javascript
{
    "access_token": "Bearer token for API calls",
    "token_expiry": "Token expiration timestamp",
    "device_count": "Number of devices found",
    "first_device_serial": "Serial of first device for testing",
    "device_status": "Status of test device",
    "device_health": "Health status of test device",
    "performance_data": "JSON string of performance metrics",
    "health_report": "JSON string of complete health report",
    "alert_needed": "Boolean indicating if alert should be sent",
    "auth_failed": "Boolean indicating authentication failure",
    "auth_error": "Error message if authentication failed"
}
```

## Flow Execution Steps

1. **Click "Create Flow"** in Postman Flows interface
2. **Add HTTP Request blocks** for each API call above
3. **Configure each block** with the URLs, methods, headers, and bodies specified
4. **Add Test Script blocks** with the JavaScript code provided
5. **Connect blocks** in sequence: Auth → Device List → Device Details → Monitoring → Health Check → Notification
6. **Set up conditional logic** for the notification block
7. **Configure environment variables** with your actual API credentials
8. **Test the flow** manually first
9. **Set up scheduling** for automated execution every 30 minutes

## Expected Outcomes

### Successful Flow
- ✅ Authentication successful
- ✅ Device list retrieved (>0 devices)
- ✅ Device details accessible
- ✅ Performance data available
- ✅ Health report generated
- ✅ No alerts needed

### Failure Scenarios
- ❌ Authentication fails → Critical alert sent
- ❌ No devices found → Warning alert sent
- ❌ Device health critical → Critical alert sent
- ❌ API timeouts → Warning alert sent

## Integration with n8n Workflows

This flow can trigger n8n workflows via webhooks:
- **Healthy status**: No action needed
- **Warning status**: Trigger monitoring workflow
- **Critical status**: Trigger incident response workflow

## Monitoring and Maintenance

- **Review flow execution logs** daily
- **Update credentials** before expiration
- **Monitor performance metrics** for trends
- **Adjust alert thresholds** based on operational needs
- **Test flow manually** after API changes
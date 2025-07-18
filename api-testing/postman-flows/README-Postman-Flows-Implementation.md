# HPE Aruba API Testing - Postman Flows Implementation Guide

**Version**: 1.0  
**Created**: January 17, 2025  
**Purpose**: Step-by-step guide to implement HPE Aruba API testing flows in Postman  

## Overview

This guide provides detailed instructions for implementing the HPE Aruba API testing flows in Postman Flows. The flows automate API health monitoring, testing, and alerting for all major HPE Aruba products.

## Available Flows

### 1. Aruba Central API Flow
- **File**: `aruba-central-api-flow.md`
- **Purpose**: OAuth authentication, device management, monitoring
- **Frequency**: Every 30 minutes
- **Duration**: ~60 seconds

### 2. AOS-CX Switch API Flow
- **File**: `aos-cx-switch-api-flow.md`
- **Purpose**: Session auth, VLAN management, interface configuration
- **Frequency**: Every 15 minutes
- **Duration**: ~45 seconds

### 3. Comprehensive API Health Flow
- **File**: `comprehensive-api-health-flow.md`
- **Purpose**: Monitor all APIs simultaneously with dashboard
- **Frequency**: Every 5 minutes
- **Duration**: ~2-3 minutes

## Implementation Steps

### Step 1: Access Postman Flows

1. **Open Postman**
2. **Navigate to Flows**
   - Click on "Flows" in the left sidebar
   - Or visit the Flows interface directly
3. **Click "Create New"** or "Create Flow"

### Step 2: Create Your First Flow (Aruba Central)

#### 2.1 Set Up Flow Canvas
1. **Click "Create Flow"**
2. **Enter flow name**: "Aruba Central API Health Check"
3. **Add description**: "Automated testing of Aruba Central API authentication, device management, and monitoring"

#### 2.2 Add HTTP Request Blocks

**Block 1: OAuth Authentication**
1. **Drag "HTTP Request" block** to canvas
2. **Configure request**:
   - **Name**: "OAuth 2.0 Login"
   - **Method**: POST
   - **URL**: `{{auth_url}}/oauth2/token`
   - **Headers**: 
     ```
     Content-Type: application/x-www-form-urlencoded
     Accept: application/json
     ```
   - **Body** (x-www-form-urlencoded):
     ```
     grant_type: client_credentials
     client_id: {{client_id}}
     client_secret: {{client_secret}}
     scope: all
     ```

3. **Add Test Script** (in Tests tab):
   ```javascript
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

**Block 2: Device Management**
1. **Drag "HTTP Request" block** to canvas
2. **Configure request**:
   - **Name**: "List Devices"
   - **Method**: GET
   - **URL**: `{{base_url}}/platform/device_inventory/v1/devices?limit=100&offset=0`
   - **Headers**: 
     ```
     Authorization: Bearer {{access_token}}
     ```

3. **Add Test Script**:
   ```javascript
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

   pm.test('Response time acceptable', function() {
       pm.expect(pm.response.responseTime).to.be.below(5000);
   });
   ```

**Block 3: Monitoring**
1. **Drag "HTTP Request" block** to canvas
2. **Configure request**:
   - **Name**: "Get Performance Stats"
   - **Method**: GET
   - **URL**: `{{base_url}}/monitoring/v1/statistics/device?timerange=3H&device_type=ap`
   - **Headers**: 
     ```
     Authorization: Bearer {{access_token}}
     ```

3. **Add Test Script**:
   ```javascript
   pm.test('Performance statistics retrieved', function() {
       pm.response.to.have.status(200);
       const response = pm.response.json();
       pm.expect(response).to.have.property('statistics');
       
       // Store performance metrics
       pm.globals.set('performance_data', JSON.stringify(response.statistics));
   });
   ```

#### 2.3 Add Script Block for Health Summary
1. **Drag "Script" block** to canvas
2. **Configure script**:
   - **Name**: "Generate Health Report"
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
           first_device: pm.globals.get('first_device_serial') || null
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
   }

   // Store report
   pm.globals.set('health_report', JSON.stringify(healthReport));
   pm.globals.set('alert_needed', healthReport.overall_health !== 'HEALTHY');

   console.log('Health Report:', healthReport);
   ```

#### 2.4 Add Conditional Notification Block
1. **Drag "HTTP Request" block** to canvas
2. **Configure request**:
   - **Name**: "Send Slack Alert"
   - **Method**: POST
   - **URL**: `{{slack_webhook_url}}`
   - **Headers**: 
     ```
     Content-Type: application/json
     ```
   - **Body** (JSON):
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

3. **Add Condition**:
   - **Enable conditional execution**
   - **Condition**: `{{alert_needed}} === true`

#### 2.5 Connect Blocks
1. **Connect blocks in sequence**:
   - OAuth Authentication → Device Management → Monitoring → Health Summary → Notification
2. **Use drag-and-drop** to connect output of one block to input of next

### Step 3: Configure Environment Variables

#### 3.1 Create Environment
1. **Click "Environments"** in left sidebar
2. **Click "Create Environment"**
3. **Name**: "HPE Aruba APIs"

#### 3.2 Add Variables
```javascript
// Aruba Central
base_url: https://apigw-prod2.central.arubanetworks.com
auth_url: https://app.central.arubanetworks.com
client_id: your_client_id
client_secret: your_client_secret

// AOS-CX Switch
aos_cx_base_url: https://switch-ip-address
aos_cx_username: admin
aos_cx_password: your_password

// EdgeConnect
edge_base_url: https://orchestrator.example.com
edge_username: admin
edge_password: your_password

// UXI Sensors
uxi_base_url: https://api.uxi.aruba.com
uxi_bearer_token: your_bearer_token

// Notifications
slack_webhook_url: https://hooks.slack.com/services/your/webhook/url
```

### Step 4: Test Your Flow

#### 4.1 Manual Testing
1. **Set environment** to "HPE Aruba APIs"
2. **Click "Run"** button
3. **Monitor execution** in real-time
4. **Check console logs** for debug information
5. **Verify notifications** are sent correctly

#### 4.2 Debug Issues
1. **Check environment variables** are set correctly
2. **Verify API credentials** are valid
3. **Test individual HTTP requests** in Postman
4. **Check test script syntax** for errors
5. **Monitor response times** and status codes

### Step 5: Set Up Scheduling

#### 5.1 Enable Scheduling
1. **Click "Schedule" button** in flow
2. **Set frequency**: Every 30 minutes
3. **Set time zone**: Your local timezone
4. **Enable notifications**: On failure only

#### 5.2 Monitor Scheduled Runs
1. **Check "Runs" tab** regularly
2. **Review execution logs** for errors
3. **Monitor alert notifications** in Slack
4. **Adjust frequency** based on needs

## Advanced Configuration

### Custom Dashboards

**Create HTML Dashboard**:
```javascript
// In Script Block
const htmlDashboard = `
<!DOCTYPE html>
<html>
<head>
    <title>API Health Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .status-healthy { color: green; }
        .status-warning { color: orange; }
        .status-critical { color: red; }
    </style>
</head>
<body>
    <h1>HPE Aruba API Health Dashboard</h1>
    <div class="status-{{overall_health.toLowerCase()}}">
        <h2>Overall Status: {{overall_health}}</h2>
    </div>
    <div>
        <h3>API Details</h3>
        <p>Device Count: {{device_count}}</p>
        <p>Last Check: {{timestamp}}</p>
    </div>
</body>
</html>
`;

pm.globals.set('dashboard_html', htmlDashboard);
```

### Error Handling

**Comprehensive Error Handling**:
```javascript
// In each HTTP request test script
pm.test('Handle API errors gracefully', function() {
    if (pm.response.code >= 400) {
        const errorInfo = {
            status: pm.response.code,
            message: pm.response.text(),
            timestamp: new Date().toISOString()
        };
        
        pm.globals.set('api_error', JSON.stringify(errorInfo));
        console.error('API Error:', errorInfo);
        
        // Continue flow with error state
        pm.globals.set('error_occurred', true);
    }
});
```

### Performance Monitoring

**Track Response Times**:
```javascript
// In test scripts
pm.test('Performance within limits', function() {
    const responseTime = pm.response.responseTime;
    pm.expect(responseTime).to.be.below(5000);
    
    // Store for trending
    const perfData = JSON.parse(pm.globals.get('performance_history') || '[]');
    perfData.push({
        timestamp: new Date().toISOString(),
        response_time: responseTime,
        endpoint: pm.info.requestName
    });
    
    // Keep only last 10 measurements
    if (perfData.length > 10) {
        perfData.shift();
    }
    
    pm.globals.set('performance_history', JSON.stringify(perfData));
});
```

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify credentials in environment variables
   - Check API key permissions
   - Ensure OAuth scopes are correct

2. **Flow Execution Errors**
   - Check syntax in test scripts
   - Verify variable names match between blocks
   - Ensure proper block connections

3. **Notification Issues**
   - Test webhook URLs manually
   - Check JSON formatting in notification body
   - Verify conditional logic syntax

4. **Performance Issues**
   - Monitor response times
   - Check network connectivity
   - Optimize test scripts

### Debug Steps

1. **Enable Console Logging**:
   ```javascript
   console.log('Current variable:', pm.globals.get('variable_name'));
   console.log('Response data:', pm.response.json());
   ```

2. **Test Individual Requests**:
   - Copy request configuration to regular Postman request
   - Test with same environment variables
   - Check response format

3. **Validate Environment Variables**:
   - Ensure all required variables are set
   - Check for typos in variable names
   - Verify sensitive data is properly masked

## Best Practices

### Flow Design
- Keep flows simple and focused
- Use descriptive names for blocks
- Add comments in test scripts
- Handle errors gracefully

### Security
- Use environment variables for sensitive data
- Implement proper token rotation
- Monitor for credential exposure
- Use HTTPS for all API calls

### Performance
- Set appropriate timeouts
- Monitor response times
- Implement caching where appropriate
- Use conditional logic to skip unnecessary calls

### Monitoring
- Set up alerting for critical failures
- Monitor flow execution frequency
- Track API health trends
- Document known issues

## Integration with n8n

### Triggering n8n Workflows
```javascript
// In notification block
if (pm.globals.get('overall_health') === 'CRITICAL') {
    pm.sendRequest({
        url: 'http://192.168.40.100:8006/webhook/incident-response',
        method: 'POST',
        header: {
            'Content-Type': 'application/json'
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                alert_type: 'api_failure',
                severity: 'critical',
                details: pm.globals.get('health_report')
            })
        }
    });
}
```

This implementation guide provides everything needed to create comprehensive API monitoring flows in Postman. The flows will continuously monitor your HPE Aruba APIs, provide real-time health status, and alert you to any issues before they impact your network operations.
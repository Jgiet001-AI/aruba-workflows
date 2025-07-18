# Comprehensive HPE Aruba API Health Monitoring Flow

## Flow Overview
**Name**: HPE Aruba API Health Dashboard  
**Purpose**: Monitor health of all HPE Aruba APIs simultaneously with comprehensive reporting  
**Trigger**: Scheduled (every 5 minutes) or Manual execution  
**Duration**: ~2-3 minutes for complete execution  

## Flow Structure

### 1. Flow Initialization Block
```
┌─────────────────────┐
│  Initialize Flow    │
│                     │
│  Setup:             │
│  - Start timestamp  │
│  - Health counters  │
│  - Error tracking   │
│                     │
│  Output:            │
│  - flow_start_time  │
│  - health_metrics   │
└─────────────────────┘
```

**Configuration**:
- **Type**: Script Block
- **Script**:
```javascript
// Initialize flow tracking
const flowStartTime = Date.now();
const healthMetrics = {
    start_time: new Date().toISOString(),
    apis_tested: 0,
    apis_healthy: 0,
    apis_warning: 0,
    apis_critical: 0,
    total_response_time: 0,
    results: {}
};

pm.globals.set('flow_start_time', flowStartTime);
pm.globals.set('health_metrics', JSON.stringify(healthMetrics));

console.log('Starting comprehensive API health check...');
```

### 2. Parallel API Health Checks

#### 2a. Aruba Central Health Check
```
┌─────────────────────┐
│  Central API Test   │
│                     │
│  Quick Tests:       │
│  1. OAuth Auth      │
│  2. Device Count    │
│  3. Basic Stats     │
│                     │
│  Output:            │
│  - central_health   │
│  - central_metrics  │
└─────────────────────┘
```

**Auth Configuration**:
- **URL**: `{{central_auth_url}}/oauth2/token`
- **Method**: POST
- **Headers**: `Content-Type: application/x-www-form-urlencoded`
- **Body**: `grant_type=client_credentials&client_id={{central_client_id}}&client_secret={{central_client_secret}}&scope=all`

**Test Script**:
```javascript
const startTime = Date.now();
let centralHealth = {
    api_name: 'Aruba Central',
    auth_status: 'FAILED',
    response_time: 0,
    device_count: 0,
    last_check: new Date().toISOString(),
    errors: []
};

pm.test('Central Auth Success', function() {
    try {
        pm.response.to.have.status(200);
        const response = pm.response.json();
        pm.expect(response).to.have.property('access_token');
        
        centralHealth.auth_status = 'SUCCESS';
        pm.globals.set('central_access_token', response.access_token);
    } catch (error) {
        centralHealth.errors.push('Auth failed: ' + error.message);
    }
});

centralHealth.response_time = Date.now() - startTime;
pm.globals.set('central_health', JSON.stringify(centralHealth));
```

**Device Count Check**:
- **URL**: `{{central_base_url}}/platform/device_inventory/v1/devices?limit=1`
- **Method**: GET
- **Headers**: `Authorization: Bearer {{central_access_token}}`

**Test Script**:
```javascript
const centralHealth = JSON.parse(pm.globals.get('central_health') || '{}');

pm.test('Central Device Check', function() {
    try {
        pm.response.to.have.status(200);
        const response = pm.response.json();
        centralHealth.device_count = response.count || 0;
        centralHealth.overall_status = centralHealth.device_count > 0 ? 'HEALTHY' : 'WARNING';
    } catch (error) {
        centralHealth.errors.push('Device check failed: ' + error.message);
        centralHealth.overall_status = 'CRITICAL';
    }
});

pm.globals.set('central_health', JSON.stringify(centralHealth));
```

#### 2b. AOS-CX Health Check
```
┌─────────────────────┐
│  AOS-CX API Test    │
│                     │
│  Quick Tests:       │
│  1. Login           │
│  2. System Info     │
│  3. VLAN Count      │
│                     │
│  Output:            │
│  - aos_cx_health    │
│  - aos_cx_metrics   │
└─────────────────────┘
```

**Login Configuration**:
- **URL**: `{{aos_cx_base_url}}/rest/v1/login`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**: `{"username": "{{aos_cx_username}}", "password": "{{aos_cx_password}}"}`

**Test Script**:
```javascript
const startTime = Date.now();
let aosCxHealth = {
    api_name: 'AOS-CX Switch',
    auth_status: 'FAILED',
    response_time: 0,
    system_info: null,
    vlan_count: 0,
    last_check: new Date().toISOString(),
    errors: []
};

pm.test('AOS-CX Login Success', function() {
    try {
        pm.response.to.have.status(200);
        const sessionCookie = pm.cookies.get('sessionId');
        pm.expect(sessionCookie).to.not.be.null;
        
        aosCxHealth.auth_status = 'SUCCESS';
        pm.globals.set('aos_cx_session', sessionCookie);
    } catch (error) {
        aosCxHealth.errors.push('Login failed: ' + error.message);
    }
});

aosCxHealth.response_time = Date.now() - startTime;
pm.globals.set('aos_cx_health', JSON.stringify(aosCxHealth));
```

**System Check**:
- **URL**: `{{aos_cx_base_url}}/rest/v10.08/system`
- **Method**: GET
- **Headers**: `Cookie: sessionId={{aos_cx_session}}`

**Test Script**:
```javascript
const aosCxHealth = JSON.parse(pm.globals.get('aos_cx_health') || '{}');

pm.test('AOS-CX System Check', function() {
    try {
        pm.response.to.have.status(200);
        const response = pm.response.json();
        aosCxHealth.system_info = {
            hostname: response.hostname,
            platform: response.platform_name,
            version: response.software_version
        };
        aosCxHealth.overall_status = 'HEALTHY';
    } catch (error) {
        aosCxHealth.errors.push('System check failed: ' + error.message);
        aosCxHealth.overall_status = 'CRITICAL';
    }
});

pm.globals.set('aos_cx_health', JSON.stringify(aosCxHealth));
```

#### 2c. EdgeConnect Health Check
```
┌─────────────────────┐
│  EdgeConnect Test   │
│                     │
│  Quick Tests:       │
│  1. Login           │
│  2. User Info       │
│  3. Policy Count    │
│                     │
│  Output:            │
│  - edge_health      │
│  - edge_metrics     │
└─────────────────────┘
```

**Login Configuration**:
- **URL**: `{{edge_base_url}}/gms/rest/authentication/login`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**: `{"username": "{{edge_username}}", "password": "{{edge_password}}"}`

**Test Script**:
```javascript
const startTime = Date.now();
let edgeHealth = {
    api_name: 'EdgeConnect SD-WAN',
    auth_status: 'FAILED',
    response_time: 0,
    policy_count: 0,
    appliance_count: 0,
    last_check: new Date().toISOString(),
    errors: []
};

pm.test('EdgeConnect Login Success', function() {
    try {
        pm.response.to.have.status(200);
        const response = pm.response.json();
        pm.expect(response).to.have.property('token');
        
        edgeHealth.auth_status = 'SUCCESS';
        pm.globals.set('edge_auth_token', response.token);
    } catch (error) {
        edgeHealth.errors.push('Login failed: ' + error.message);
    }
});

edgeHealth.response_time = Date.now() - startTime;
pm.globals.set('edge_health', JSON.stringify(edgeHealth));
```

#### 2d. UXI Health Check
```
┌─────────────────────┐
│  UXI API Test       │
│                     │
│  Quick Tests:       │
│  1. Token Valid     │
│  2. Sensor Count    │
│  3. Test Count      │
│                     │
│  Output:            │
│  - uxi_health       │
│  - uxi_metrics      │
└─────────────────────┘
```

**Token Validation Configuration**:
- **URL**: `{{uxi_base_url}}/api/v1/auth/validate`
- **Method**: GET
- **Headers**: `Authorization: Bearer {{uxi_bearer_token}}`

**Test Script**:
```javascript
const startTime = Date.now();
let uxiHealth = {
    api_name: 'UXI Sensors',
    auth_status: 'FAILED',
    response_time: 0,
    sensor_count: 0,
    test_count: 0,
    last_check: new Date().toISOString(),
    errors: []
};

pm.test('UXI Token Valid', function() {
    try {
        pm.response.to.have.status(200);
        const response = pm.response.json();
        pm.expect(response.valid).to.be.true;
        
        uxiHealth.auth_status = 'SUCCESS';
        uxiHealth.customer_id = response.user.customer_id;
    } catch (error) {
        uxiHealth.errors.push('Token validation failed: ' + error.message);
    }
});

uxiHealth.response_time = Date.now() - startTime;
pm.globals.set('uxi_health', JSON.stringify(uxiHealth));
```

### 3. Health Aggregation Block
```
┌─────────────────────┐
│  Aggregate Results  │
│                     │
│  Inputs:            │
│  - central_health   │
│  - aos_cx_health    │
│  - edge_health      │
│  - uxi_health       │
│                     │
│  Output:            │
│  - dashboard_report │
│  - overall_status   │
└─────────────────────┘
```

**Configuration**:
- **Type**: Script Block
- **Script**:
```javascript
// Aggregate all health results
const flowEndTime = Date.now();
const flowStartTime = pm.globals.get('flow_start_time');
const totalExecutionTime = flowEndTime - flowStartTime;

// Collect all health data
const centralHealth = JSON.parse(pm.globals.get('central_health') || '{}');
const aosCxHealth = JSON.parse(pm.globals.get('aos_cx_health') || '{}');
const edgeHealth = JSON.parse(pm.globals.get('edge_health') || '{}');
const uxiHealth = JSON.parse(pm.globals.get('uxi_health') || '{}');

// Create comprehensive dashboard report
const dashboardReport = {
    timestamp: new Date().toISOString(),
    execution_time_ms: totalExecutionTime,
    overall_status: 'HEALTHY',
    summary: {
        total_apis: 4,
        healthy_apis: 0,
        warning_apis: 0,
        critical_apis: 0,
        avg_response_time: 0
    },
    apis: {
        aruba_central: centralHealth,
        aos_cx_switch: aosCxHealth,
        edgeconnect_sdwan: edgeHealth,
        uxi_sensors: uxiHealth
    },
    alerts: [],
    recommendations: []
};

// Calculate summary statistics
let totalResponseTime = 0;
let healthyCount = 0;
let warningCount = 0;
let criticalCount = 0;

[centralHealth, aosCxHealth, edgeHealth, uxiHealth].forEach(health => {
    if (health.response_time) {
        totalResponseTime += health.response_time;
    }
    
    switch (health.overall_status) {
        case 'HEALTHY':
            healthyCount++;
            break;
        case 'WARNING':
            warningCount++;
            break;
        case 'CRITICAL':
            criticalCount++;
            break;
    }
    
    // Add alerts for issues
    if (health.errors && health.errors.length > 0) {
        dashboardReport.alerts.push({
            api: health.api_name,
            severity: health.overall_status,
            errors: health.errors
        });
    }
});

// Update summary
dashboardReport.summary.healthy_apis = healthyCount;
dashboardReport.summary.warning_apis = warningCount;
dashboardReport.summary.critical_apis = criticalCount;
dashboardReport.summary.avg_response_time = Math.round(totalResponseTime / 4);

// Determine overall status
if (criticalCount > 0) {
    dashboardReport.overall_status = 'CRITICAL';
} else if (warningCount > 0) {
    dashboardReport.overall_status = 'WARNING';
} else {
    dashboardReport.overall_status = 'HEALTHY';
}

// Add recommendations
if (dashboardReport.summary.avg_response_time > 3000) {
    dashboardReport.recommendations.push('API response times are high - investigate network or server performance');
}

if (criticalCount > 0) {
    dashboardReport.recommendations.push('Critical API issues detected - immediate investigation required');
}

if (warningCount > 0) {
    dashboardReport.recommendations.push('Warning-level issues detected - review API configurations');
}

// Store results
pm.globals.set('dashboard_report', JSON.stringify(dashboardReport));
pm.globals.set('overall_status', dashboardReport.overall_status);
pm.globals.set('alert_needed', dashboardReport.overall_status !== 'HEALTHY');

console.log('=== HPE Aruba API Health Dashboard ===');
console.log('Overall Status:', dashboardReport.overall_status);
console.log('Healthy APIs:', healthyCount + '/4');
console.log('Average Response Time:', dashboardReport.summary.avg_response_time + 'ms');
console.log('Execution Time:', totalExecutionTime + 'ms');

if (dashboardReport.alerts.length > 0) {
    console.log('Alerts:', dashboardReport.alerts);
}
```

### 4. Dashboard Visualization Block
```
┌─────────────────────┐
│  Create Dashboard   │
│  HTML Report        │
│                     │
│  Inputs:            │
│  - dashboard_report │
│                     │
│  Output:            │
│  - html_dashboard   │
│  - dashboard_url    │
└─────────────────────┘
```

**Configuration**:
- **Type**: Script Block
- **Script**:
```javascript
// Generate HTML dashboard
const dashboardReport = JSON.parse(pm.globals.get('dashboard_report') || '{}');

const htmlDashboard = `
<!DOCTYPE html>
<html>
<head>
    <title>HPE Aruba API Health Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .dashboard { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .status-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .status-healthy { border-left: 5px solid #4CAF50; }
        .status-warning { border-left: 5px solid #FF9800; }
        .status-critical { border-left: 5px solid #F44336; }
        .metric { display: flex; justify-content: space-between; margin: 10px 0; }
        .metric-value { font-weight: bold; }
        .alerts { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .alert { padding: 10px; margin: 5px 0; border-radius: 5px; }
        .alert-critical { background: #ffebee; border: 1px solid #f44336; }
        .alert-warning { background: #fff3e0; border: 1px solid #ff9800; }
        .footer { text-align: center; color: #666; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>HPE Aruba API Health Dashboard</h1>
            <p>Last Updated: ${dashboardReport.timestamp}</p>
            <p>Overall Status: <strong>${dashboardReport.overall_status}</strong></p>
            <p>Execution Time: ${dashboardReport.execution_time_ms}ms</p>
        </div>
        
        <div class="status-grid">
            <div class="status-card status-${dashboardReport.apis.aruba_central.overall_status?.toLowerCase()}">
                <h3>Aruba Central</h3>
                <div class="metric">
                    <span>Status:</span>
                    <span class="metric-value">${dashboardReport.apis.aruba_central.overall_status}</span>
                </div>
                <div class="metric">
                    <span>Auth:</span>
                    <span class="metric-value">${dashboardReport.apis.aruba_central.auth_status}</span>
                </div>
                <div class="metric">
                    <span>Devices:</span>
                    <span class="metric-value">${dashboardReport.apis.aruba_central.device_count}</span>
                </div>
                <div class="metric">
                    <span>Response Time:</span>
                    <span class="metric-value">${dashboardReport.apis.aruba_central.response_time}ms</span>
                </div>
            </div>
            
            <div class="status-card status-${dashboardReport.apis.aos_cx_switch.overall_status?.toLowerCase()}">
                <h3>AOS-CX Switch</h3>
                <div class="metric">
                    <span>Status:</span>
                    <span class="metric-value">${dashboardReport.apis.aos_cx_switch.overall_status}</span>
                </div>
                <div class="metric">
                    <span>Auth:</span>
                    <span class="metric-value">${dashboardReport.apis.aos_cx_switch.auth_status}</span>
                </div>
                <div class="metric">
                    <span>Hostname:</span>
                    <span class="metric-value">${dashboardReport.apis.aos_cx_switch.system_info?.hostname || 'N/A'}</span>
                </div>
                <div class="metric">
                    <span>Response Time:</span>
                    <span class="metric-value">${dashboardReport.apis.aos_cx_switch.response_time}ms</span>
                </div>
            </div>
            
            <div class="status-card status-${dashboardReport.apis.edgeconnect_sdwan.overall_status?.toLowerCase()}">
                <h3>EdgeConnect SD-WAN</h3>
                <div class="metric">
                    <span>Status:</span>
                    <span class="metric-value">${dashboardReport.apis.edgeconnect_sdwan.overall_status}</span>
                </div>
                <div class="metric">
                    <span>Auth:</span>
                    <span class="metric-value">${dashboardReport.apis.edgeconnect_sdwan.auth_status}</span>
                </div>
                <div class="metric">
                    <span>Policies:</span>
                    <span class="metric-value">${dashboardReport.apis.edgeconnect_sdwan.policy_count}</span>
                </div>
                <div class="metric">
                    <span>Response Time:</span>
                    <span class="metric-value">${dashboardReport.apis.edgeconnect_sdwan.response_time}ms</span>
                </div>
            </div>
            
            <div class="status-card status-${dashboardReport.apis.uxi_sensors.overall_status?.toLowerCase()}">
                <h3>UXI Sensors</h3>
                <div class="metric">
                    <span>Status:</span>
                    <span class="metric-value">${dashboardReport.apis.uxi_sensors.overall_status}</span>
                </div>
                <div class="metric">
                    <span>Auth:</span>
                    <span class="metric-value">${dashboardReport.apis.uxi_sensors.auth_status}</span>
                </div>
                <div class="metric">
                    <span>Sensors:</span>
                    <span class="metric-value">${dashboardReport.apis.uxi_sensors.sensor_count}</span>
                </div>
                <div class="metric">
                    <span>Response Time:</span>
                    <span class="metric-value">${dashboardReport.apis.uxi_sensors.response_time}ms</span>
                </div>
            </div>
        </div>
        
        ${dashboardReport.alerts.length > 0 ? `
        <div class="alerts">
            <h3>Active Alerts</h3>
            ${dashboardReport.alerts.map(alert => `
                <div class="alert alert-${alert.severity.toLowerCase()}">
                    <strong>${alert.api}</strong>: ${alert.errors.join(', ')}
                </div>
            `).join('')}
        </div>
        ` : ''}
        
        ${dashboardReport.recommendations.length > 0 ? `
        <div class="alerts">
            <h3>Recommendations</h3>
            ${dashboardReport.recommendations.map(rec => `
                <div class="alert alert-warning">
                    ${rec}
                </div>
            `).join('')}
        </div>
        ` : ''}
        
        <div class="footer">
            <p>HPE Aruba API Health Dashboard | Generated by Postman Flows</p>
        </div>
    </div>
</body>
</html>
`;

pm.globals.set('html_dashboard', htmlDashboard);
console.log('HTML Dashboard generated successfully');
```

### 5. Notification Block
```
┌─────────────────────┐
│  Send Notifications │
│                     │
│  Channels:          │
│  - Slack            │
│  - Email            │
│  - Webhook          │
│                     │
│  Condition:         │
│  - Status change    │
│  - Critical alerts  │
└─────────────────────┘
```

**Slack Notification Configuration**:
- **URL**: `{{slack_webhook_url}}`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Condition**: `{{alert_needed}} === true`
- **Body**:
```json
{
    "text": "HPE Aruba API Health Dashboard Alert",
    "attachments": [
        {
            "color": "{{overall_status === 'CRITICAL' ? 'danger' : (overall_status === 'WARNING' ? 'warning' : 'good')}}",
            "title": "API Health Status: {{overall_status}}",
            "fields": [
                {
                    "title": "Healthy APIs",
                    "value": "{{healthy_apis}}/4",
                    "short": true
                },
                {
                    "title": "Response Time",
                    "value": "{{avg_response_time}}ms",
                    "short": true
                },
                {
                    "title": "Aruba Central",
                    "value": "{{central_status}}",
                    "short": true
                },
                {
                    "title": "AOS-CX Switch",
                    "value": "{{aos_cx_status}}",
                    "short": true
                },
                {
                    "title": "EdgeConnect",
                    "value": "{{edge_status}}",
                    "short": true
                },
                {
                    "title": "UXI Sensors",
                    "value": "{{uxi_status}}",
                    "short": true
                }
            ],
            "footer": "HPE Aruba API Monitor",
            "ts": "{{$timestamp}}"
        }
    ]
}
```

## Environment Variables

```javascript
{
    // Aruba Central
    "central_base_url": "https://apigw-prod2.central.arubanetworks.com",
    "central_auth_url": "https://app.central.arubanetworks.com",
    "central_client_id": "your_client_id",
    "central_client_secret": "your_client_secret",
    
    // AOS-CX Switch
    "aos_cx_base_url": "https://switch-ip-address",
    "aos_cx_username": "admin",
    "aos_cx_password": "your_password",
    
    // EdgeConnect
    "edge_base_url": "https://orchestrator.example.com",
    "edge_username": "admin",
    "edge_password": "your_password",
    
    // UXI Sensors
    "uxi_base_url": "https://api.uxi.aruba.com",
    "uxi_bearer_token": "your_bearer_token",
    
    // Notifications
    "slack_webhook_url": "https://hooks.slack.com/services/your/webhook/url",
    "email_webhook_url": "https://your-email-service.com/webhook"
}
```

## Implementation Steps

1. **Create New Flow** in Postman Flows interface
2. **Add Script Block** for flow initialization
3. **Add 4 Parallel HTTP Request blocks** for each API
4. **Add Test Scripts** to each HTTP request block
5. **Add Aggregation Script Block** to combine results
6. **Add Dashboard Generation Block** for HTML report
7. **Add Conditional Notification Block** for alerts
8. **Configure Environment Variables** with actual credentials
9. **Test Flow Execution** manually
10. **Set up Scheduling** for automated execution

## Expected Results

### Healthy State (All APIs Working)
- ✅ All 4 APIs authenticated successfully
- ✅ All health checks passed
- ✅ Response times within acceptable limits
- ✅ No alerts generated
- ✅ Dashboard shows all green status

### Warning State (Some Issues)
- ⚠️ 1-2 APIs showing degraded performance
- ⚠️ High response times but APIs functional
- ⚠️ Some configuration issues detected
- ⚠️ Warning alerts sent to team

### Critical State (Major Issues)
- ❌ 1+ APIs completely failing
- ❌ Authentication failures
- ❌ Service unavailable responses
- ❌ Critical alerts sent immediately

## Monitoring and Alerting

### Alert Thresholds
- **Critical**: Any API authentication failure
- **Warning**: Response time > 3 seconds
- **Info**: All APIs healthy

### Escalation Path
1. **First Alert**: Slack notification to team
2. **Persistent Issues**: Email to operations team
3. **Critical Failures**: Page on-call engineer

## Integration with n8n

The flow can trigger n8n workflows based on health status:
- **Healthy**: Log metrics to database
- **Warning**: Trigger investigation workflow
- **Critical**: Trigger incident response workflow

This comprehensive monitoring flow provides real-time visibility into all HPE Aruba API health and enables proactive issue resolution.
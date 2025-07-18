# AOS-CX Switch API Testing Flow

## Flow Overview
**Name**: AOS-CX Switch Configuration Health Check  
**Purpose**: Automated testing of AOS-CX switch API authentication, VLAN management, and interface configuration  
**Trigger**: Scheduled (every 15 minutes) or Manual execution  

## Flow Structure

### 1. Authentication Block
```
┌─────────────────────┐
│  Switch Login       │
│  (POST /login)      │
│                     │
│  Variables:         │
│  - username         │
│  - password         │
│                     │
│  Output:            │
│  - session_cookie   │
│  - login_status     │
└─────────────────────┘
```

**Configuration**:
- **URL**: `{{base_url}}/rest/v1/login`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**: 
```json
{
    "username": "{{username}}",
    "password": "{{password}}"
}
```

**Test Script**:
```javascript
// Test successful login
pm.test('Switch login successful', function() {
    pm.response.to.have.status(200);
    
    // Extract session cookie
    const sessionCookie = pm.cookies.get('sessionId');
    pm.expect(sessionCookie).to.not.be.null;
    pm.globals.set('session_id', sessionCookie);
    pm.globals.set('login_status', 'SUCCESS');
});

// Handle login failure
pm.test('Handle login failure gracefully', function() {
    if (pm.response.code !== 200) {
        pm.globals.set('login_status', 'FAILED');
        pm.globals.set('login_error', pm.response.text());
    }
});
```

### 2. System Information Block
```
┌─────────────────────┐
│  Get System Info    │
│  (GET /system)      │
│                     │
│  Headers:           │
│  - Cookie           │
│                     │
│  Output:            │
│  - hostname         │
│  - platform_name    │
│  - software_version │
│  - system_health    │
└─────────────────────┘
```

**Configuration**:
- **URL**: `{{base_url}}/rest/v10.08/system`
- **Method**: GET
- **Headers**: `Cookie: sessionId={{session_id}}`

**Test Script**:
```javascript
// Test system information retrieval
pm.test('System information retrieved', function() {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    
    pm.expect(response).to.have.property('hostname');
    pm.expect(response).to.have.property('platform_name');
    pm.expect(response).to.have.property('software_version');
    
    // Store system information
    pm.globals.set('switch_hostname', response.hostname);
    pm.globals.set('platform_name', response.platform_name);
    pm.globals.set('software_version', response.software_version);
    pm.globals.set('system_health', 'HEALTHY');
});

// Test response time
pm.test('System response time acceptable', function() {
    pm.expect(pm.response.responseTime).to.be.below(3000);
});
```

### 3. VLAN Management Test Block
```
┌─────────────────────┐
│  VLAN Operations    │
│  Test               │
│                     │
│  Operations:        │
│  1. List VLANs      │
│  2. Create Test     │
│  3. Verify Creation │
│  4. Delete Test     │
│                     │
│  Output:            │
│  - vlan_test_result │
│  - vlan_count       │
└─────────────────────┘
```

#### 3a. List VLANs Sub-block
**Configuration**:
- **URL**: `{{base_url}}/rest/v10.08/system/vlans`
- **Method**: GET
- **Headers**: `Cookie: sessionId={{session_id}}`

**Test Script**:
```javascript
// Test VLAN listing
pm.test('VLAN list retrieved successfully', function() {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    
    pm.expect(response).to.be.an('object');
    
    // Count VLANs
    const vlanCount = Object.keys(response).length;
    pm.globals.set('vlan_count', vlanCount);
    
    // Verify default VLAN exists
    pm.expect(response).to.have.property('1');
    pm.expect(response['1']).to.have.property('name');
});
```

#### 3b. Create Test VLAN Sub-block
**Configuration**:
- **URL**: `{{base_url}}/rest/v10.08/system/vlans/{{test_vlan_id}}`
- **Method**: POST
- **Headers**: 
  - `Cookie: sessionId={{session_id}}`
  - `Content-Type: application/json`
- **Body**:
```json
{
    "name": "API_Test_VLAN_{{$timestamp}}",
    "description": "Test VLAN for API health check",
    "admin": "up"
}
```

**Pre-request Script**:
```javascript
// Generate random VLAN ID for testing
const testVlanId = Math.floor(Math.random() * 900) + 100;
pm.globals.set('test_vlan_id', testVlanId);
```

**Test Script**:
```javascript
// Test VLAN creation
pm.test('Test VLAN created successfully', function() {
    pm.response.to.have.status(201);
    
    const location = pm.response.headers.get('Location');
    pm.expect(location).to.include('/vlans/' + pm.globals.get('test_vlan_id'));
    
    pm.globals.set('vlan_create_status', 'SUCCESS');
});
```

#### 3c. Verify VLAN Creation Sub-block
**Configuration**:
- **URL**: `{{base_url}}/rest/v10.08/system/vlans/{{test_vlan_id}}`
- **Method**: GET
- **Headers**: `Cookie: sessionId={{session_id}}`

**Test Script**:
```javascript
// Test VLAN verification
pm.test('Created VLAN verified', function() {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    
    pm.expect(response).to.have.property('name');
    pm.expect(response).to.have.property('description');
    pm.expect(response.admin).to.eql('up');
    
    pm.globals.set('vlan_verify_status', 'SUCCESS');
});
```

#### 3d. Delete Test VLAN Sub-block
**Configuration**:
- **URL**: `{{base_url}}/rest/v10.08/system/vlans/{{test_vlan_id}}`
- **Method**: DELETE
- **Headers**: `Cookie: sessionId={{session_id}}`

**Test Script**:
```javascript
// Test VLAN deletion
pm.test('Test VLAN deleted successfully', function() {
    pm.response.to.have.status(204);
    pm.expect(pm.response.text()).to.be.empty;
    
    pm.globals.set('vlan_delete_status', 'SUCCESS');
});
```

### 4. Interface Configuration Test Block
```
┌─────────────────────┐
│  Interface Test     │
│                     │
│  Operations:        │
│  1. List Interfaces │
│  2. Get Interface   │
│  3. Update Config   │
│  4. Verify Update   │
│                     │
│  Output:            │
│  - interface_test   │
│  - interface_count  │
└─────────────────────┘
```

#### 4a. List Interfaces Sub-block
**Configuration**:
- **URL**: `{{base_url}}/rest/v10.08/system/interfaces`
- **Method**: GET
- **Headers**: `Cookie: sessionId={{session_id}}`

**Test Script**:
```javascript
// Test interface listing
pm.test('Interface list retrieved', function() {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    
    pm.expect(response).to.be.an('object');
    
    // Count interfaces and store first interface for testing
    const interfaceCount = Object.keys(response).length;
    pm.globals.set('interface_count', interfaceCount);
    
    if (interfaceCount > 0) {
        const firstInterface = Object.keys(response)[0];
        pm.globals.set('test_interface', firstInterface);
    }
});
```

#### 4b. Update Interface Description Sub-block
**Configuration**:
- **URL**: `{{base_url}}/rest/v10.08/system/interfaces/{{test_interface}}`
- **Method**: PUT
- **Headers**: 
  - `Cookie: sessionId={{session_id}}`
  - `Content-Type: application/json`
- **Body**:
```json
{
    "description": "API Health Check - {{$timestamp}}"
}
```

**Test Script**:
```javascript
// Test interface update
pm.test('Interface description updated', function() {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    
    pm.expect(response.description).to.include('API Health Check');
    pm.globals.set('interface_update_status', 'SUCCESS');
});
```

### 5. Configuration Backup Test Block
```
┌─────────────────────┐
│  Configuration      │
│  Backup Test        │
│                     │
│  Operations:        │
│  1. Get Running     │
│  2. Get Startup     │
│  3. Compare Configs │
│                     │
│  Output:            │
│  - config_status    │
│  - config_size      │
└─────────────────────┘
```

#### 5a. Get Running Configuration Sub-block
**Configuration**:
- **URL**: `{{base_url}}/rest/v10.08/system/config`
- **Method**: GET
- **Headers**: `Cookie: sessionId={{session_id}}`

**Test Script**:
```javascript
// Test running config retrieval
pm.test('Running configuration retrieved', function() {
    pm.response.to.have.status(200);
    const configText = pm.response.text();
    
    pm.expect(configText).to.not.be.empty;
    pm.expect(configText).to.include('hostname');
    
    pm.globals.set('running_config_size', configText.length);
    pm.globals.set('config_backup_status', 'SUCCESS');
});
```

### 6. Health Summary Block
```
┌─────────────────────┐
│  Generate Health    │
│  Summary            │
│                     │
│  Inputs:            │
│  - login_status     │
│  - system_health    │
│  - vlan_test_result │
│  - interface_test   │
│  - config_status    │
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
    switch_info: {
        hostname: pm.globals.get('switch_hostname') || 'unknown',
        platform: pm.globals.get('platform_name') || 'unknown',
        software_version: pm.globals.get('software_version') || 'unknown'
    },
    authentication: {
        status: pm.globals.get('login_status') || 'UNKNOWN',
        error: pm.globals.get('login_error') || null
    },
    system: {
        health: pm.globals.get('system_health') || 'UNKNOWN',
        response_time: 'within_limits'
    },
    vlans: {
        count: parseInt(pm.globals.get('vlan_count') || '0'),
        create_test: pm.globals.get('vlan_create_status') || 'NOT_TESTED',
        verify_test: pm.globals.get('vlan_verify_status') || 'NOT_TESTED',
        delete_test: pm.globals.get('vlan_delete_status') || 'NOT_TESTED'
    },
    interfaces: {
        count: parseInt(pm.globals.get('interface_count') || '0'),
        update_test: pm.globals.get('interface_update_status') || 'NOT_TESTED'
    },
    configuration: {
        backup_status: pm.globals.get('config_backup_status') || 'NOT_TESTED',
        config_size: parseInt(pm.globals.get('running_config_size') || '0')
    },
    overall_health: 'HEALTHY' // Will be calculated
};

// Calculate overall health
let alertNeeded = false;

if (healthReport.authentication.status === 'FAILED') {
    healthReport.overall_health = 'CRITICAL';
    alertNeeded = true;
} else if (healthReport.vlans.create_test === 'FAILED' || 
           healthReport.interfaces.update_test === 'FAILED' ||
           healthReport.configuration.backup_status === 'FAILED') {
    healthReport.overall_health = 'WARNING';
    alertNeeded = true;
} else if (healthReport.vlans.count === 0 || healthReport.interfaces.count === 0) {
    healthReport.overall_health = 'WARNING';
    alertNeeded = true;
}

// Store results
pm.globals.set('health_report', JSON.stringify(healthReport));
pm.globals.set('alert_needed', alertNeeded);

console.log('AOS-CX Health Report:', healthReport);
```

### 7. Logout Block
```
┌─────────────────────┐
│  Logout             │
│  (POST /logout)     │
│                     │
│  Headers:           │
│  - Cookie           │
│                     │
│  Output:            │
│  - logout_status    │
└─────────────────────┘
```

**Configuration**:
- **URL**: `{{base_url}}/rest/v1/logout`
- **Method**: POST
- **Headers**: `Cookie: sessionId={{session_id}}`

**Test Script**:
```javascript
// Test logout
pm.test('Logout successful', function() {
    pm.response.to.have.status(200);
    pm.globals.unset('session_id');
    pm.globals.set('logout_status', 'SUCCESS');
});
```

### 8. Notification Block (Conditional)
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
    "text": "AOS-CX Switch Health Alert",
    "attachments": [
        {
            "color": "{{overall_health === 'CRITICAL' ? 'danger' : 'warning'}}",
            "fields": [
                {
                    "title": "Switch",
                    "value": "{{switch_hostname}}",
                    "short": true
                },
                {
                    "title": "Overall Health",
                    "value": "{{overall_health}}",
                    "short": true
                },
                {
                    "title": "VLAN Count",
                    "value": "{{vlan_count}}",
                    "short": true
                },
                {
                    "title": "Interface Count",
                    "value": "{{interface_count}}",
                    "short": true
                },
                {
                    "title": "Authentication",
                    "value": "{{login_status}}",
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
{
    "base_url": "https://switch-ip-address",
    "username": "admin",
    "password": "your_password",
    "slack_webhook_url": "https://hooks.slack.com/services/your/webhook/url"
}
```

### Global Variables (Set during flow execution)
```javascript
{
    "session_id": "Session cookie for API calls",
    "login_status": "SUCCESS or FAILED",
    "switch_hostname": "Hostname of the switch",
    "platform_name": "Switch platform name",
    "software_version": "Switch software version",
    "vlan_count": "Number of VLANs configured",
    "interface_count": "Number of interfaces",
    "test_vlan_id": "VLAN ID used for testing",
    "test_interface": "Interface name used for testing",
    "health_report": "JSON string of complete health report",
    "alert_needed": "Boolean indicating if alert should be sent"
}
```

## Flow Execution Results

### Success Indicators
- ✅ Login successful
- ✅ System information retrieved
- ✅ VLAN CRUD operations successful
- ✅ Interface configuration successful
- ✅ Configuration backup successful
- ✅ Logout successful

### Failure Scenarios
- ❌ Login fails → Critical alert
- ❌ VLAN operations fail → Warning alert
- ❌ Interface operations fail → Warning alert
- ❌ Configuration backup fails → Warning alert

## Integration with n8n

This flow can trigger n8n workflows:
- **Healthy**: Continue normal operations
- **Warning**: Trigger configuration review workflow
- **Critical**: Trigger incident response workflow

## Scheduling

- **Frequency**: Every 15 minutes
- **Peak hours**: Every 10 minutes (8 AM - 6 PM)
- **Maintenance window**: Skip during planned maintenance
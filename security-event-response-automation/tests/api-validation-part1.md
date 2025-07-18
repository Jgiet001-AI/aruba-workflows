# HPE Aruba Central Security Event API Test Collection

## Overview
Comprehensive test collection for automated threat response capabilities using HPE Aruba Central security APIs.

## Test Results - Part 1: Security Alerts API

### Environment Configuration
```javascript
// Environment Variables
const config = {
    baseURL: "https://central.arubanetworks.com",
    apiVersion: "v2",
    clientId: "{{CLIENT_ID}}",
    clientSecret: "{{CLIENT_SECRET}}",
    accessToken: "{{ACCESS_TOKEN}}",
    refreshToken: "{{REFRESH_TOKEN}}",
    customerId: "{{CUSTOMER_ID}}"
};

// Pre-request Script for Token Management
pm.sendRequest({
    url: config.baseURL + "/oauth2/token",
    method: 'POST',
    header: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: {
        mode: 'urlencoded',
        urlencoded: [
            {key: 'grant_type', value: 'client_credentials'},
            {key: 'client_id', value: config.clientId},
            {key: 'client_secret', value: config.clientSecret}
        ]
    }
}, function (err, res) {
    if (res && res.json().access_token) {
        pm.environment.set("ACCESS_TOKEN", res.json().access_token);
    }
});
```

### Authentication Tests
```javascript
// Test 1: OAuth 2.0 Authentication
pm.test("OAuth 2.0 Token Generation", function () {
    pm.sendRequest({
        url: config.baseURL + "/oauth2/token",
        method: 'POST',
        header: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
            mode: 'urlencoded',
            urlencoded: [
                {key: 'grant_type', value: 'client_credentials'},
                {key: 'client_id', value: config.clientId},
                {key: 'client_secret', value: config.clientSecret}
            ]
        }
    }, function (err, res) {
        pm.test("Token request successful", function () {
            pm.expect(res.code).to.equal(200);
            pm.expect(res.json()).to.have.property('access_token');
            pm.expect(res.json()).to.have.property('token_type', 'Bearer');
            pm.expect(res.json()).to.have.property('expires_in');
        });
        
        pm.environment.set("ACCESS_TOKEN", res.json().access_token);
    });
});

// Test 2: API Token Validation
pm.test("API Token Validation", function () {
    pm.sendRequest({
        url: config.baseURL + "/api/v2/platform/device_inventory",
        method: 'GET',
        header: {
            'Authorization': 'Bearer ' + pm.environment.get("ACCESS_TOKEN")
        }
    }, function (err, res) {
        pm.test("Token validation successful", function () {
            pm.expect(res.code).to.equal(200);
        });
        
        pm.test("Authentication failure handling", function () {
            if (res.code === 401) {
                pm.expect(res.json()).to.have.property('error', 'unauthorized');
            }
        });
    });
});
```

### Security Alerts API Tests
```javascript
// Test 3: GET /api/v2/alerts - Security Alerts Retrieval
pm.test("Security Alerts Retrieval", function () {
    const alertsRequest = {
        url: config.baseURL + "/api/v2/alerts",
        method: 'GET',
        header: {
            'Authorization': 'Bearer ' + pm.environment.get("ACCESS_TOKEN"),
            'Content-Type': 'application/json'
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                "filter": {
                    "severity": ["critical", "high"],
                    "category": ["security", "intrusion"],
                    "time_range": {
                        "start": "2024-01-01T00:00:00Z",
                        "end": "2024-12-31T23:59:59Z"
                    }
                },
                "limit": 100,
                "offset": 0
            })
        }
    };
    
    pm.sendRequest(alertsRequest, function (err, res) {
        pm.test("Security alerts retrieved successfully", function () {
            pm.expect(res.code).to.equal(200);
            pm.expect(res.json()).to.have.property('alerts');
            pm.expect(res.json()).to.have.property('total_count');
        });
        
        pm.test("Alert data structure validation", function () {
            const alerts = res.json().alerts;
            if (alerts && alerts.length > 0) {
                const alert = alerts[0];
                pm.expect(alert).to.have.property('alert_id');
                pm.expect(alert).to.have.property('severity');
                pm.expect(alert).to.have.property('category');
                pm.expect(alert).to.have.property('timestamp');
                pm.expect(alert).to.have.property('device_id');
                pm.expect(alert).to.have.property('description');
                pm.expect(alert).to.have.property('threat_score');
            }
        });
        
        pm.test("Critical threat detection", function () {
            const alerts = res.json().alerts;
            const criticalAlerts = alerts.filter(alert => alert.severity === 'critical');
            
            criticalAlerts.forEach(alert => {
                pm.expect(alert.threat_score).to.be.above(80);
                pm.expect(alert).to.have.property('remediation_steps');
            });
        });
    });
});
```

## Next: Test threat response and device isolation APIs
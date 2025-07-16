# Aruba Central Credentials Configuration

## Required Credentials

### 1. Aruba Central API Authentication
Create an n8n credential for Aruba Central API access

#### Option A: OAuth 2.0 (Recommended)
```json
{
  "name": "Aruba Central OAuth2",
  "type": "oauth2Api",
  "data": {
    "grant_type": "client_credentials",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "access_token_url": "https://central-prod.arubanetworks.com/oauth2/token",
    "scope": "all"
  }
}
```

#### Option B: API Key Authentication
```json
{
  "name": "Aruba Central API Key",
  "type": "httpHeaderAuth",
  "data": {
    "name": "Authorization",
    "value": "Bearer your_access_token"
  }
}
```

### 2. Central API Configuration
Configure these as n8n environment variables or workflow parameters:

```json
{
  "CENTRAL_BASE_URL": "https://apigw-prod2.central.arubanetworks.com",
  "API_VERSION": "v2",
  "CUSTOMER_ID": "your_customer_id",
  "VERIFY_SSL": true,
  "TIMEOUT": 45000
}
```

## Setting Up API Access in Aruba Central

### 1. Create API Client
```bash
# In Aruba Central UI:
1. Navigate to Account Home → API Gateway
2. Click "System Apps & Tokens" 
3. Click "+Add" to create new system app
4. Fill in application details:
   - Name: "n8n Automation"
   - Description: "Network automation workflows"
5. Select required API categories:
   - Configuration (Read/Write)
   - Monitoring (Read)
   - Location Services (Read/Write)
   - Network Operations (Read/Write)
6. Save and note Client ID and Client Secret
```

### 2. Required API Permissions
The API client needs these minimum permissions:
- **Configuration**: Read/Write access to device configurations
- **Templates**: Read/Write access to configuration templates
- **Sites & Labels**: Read/Write access to site management
- **Device Management**: Read/Write access to AP provisioning
- **Clients**: Read access to client information
- **Monitoring**: Read access to device status and statistics
- **Location Services**: Read/Write access to location configuration
- **Alerts & Events**: Read access to system alerts

### 3. OAuth 2.0 Token Generation
```bash
# Test token generation
curl -X POST "https://central-prod.arubanetworks.com/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET"

# Expected response:
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 7200
}
```

## Security Best Practices

### 1. Central Platform Security
```bash
# Recommended Central settings:
- Enable API access logging
- Restrict API access by IP (if possible)
- Use OAuth 2.0 with short-lived tokens
- Enable multi-factor authentication for admin accounts
- Regular audit of API client permissions
```

### 2. Network Security
- Use HTTPS only for all API communications
- Implement IP allowlists for API clients
- Store credentials in n8n credential store only
- Regular credential rotation (90 days recommended)
- Monitor API usage for anomalies

### 3. n8n Security
- Store credentials in n8n credential store (never in workflow)
- Use environment variables for sensitive configuration
- Enable workflow-level credential restrictions
- Implement rate limiting to respect API quotas
- Log API calls for audit trails

## API Endpoint Format

All Aruba Central API calls follow this pattern:
```
https://apigw-prod2.central.arubanetworks.com/{api_version}/{resource}
```

Examples:
- **SSIDs**: `https://apigw-prod2.central.arubanetworks.com/configuration/v2/wlan/ssid`
- **Access Points**: `https://apigw-prod2.central.arubanetworks.com/monitoring/v1/aps`
- **Templates**: `https://apigw-prod2.central.arubanetworks.com/configuration/v2/ap_groups`
- **Clients**: `https://apigw-prod2.central.arubanetworks.com/monitoring/v1/clients`

## Testing Credentials

### Basic Connectivity Test
```bash
# Test API access
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://apigw-prod2.central.arubanetworks.com/platform/device_inventory/v1/devices"

# Expected response: HTTP 200 with device list JSON
```

### Specific API Tests
```bash
# Test SSID access
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://apigw-prod2.central.arubanetworks.com/configuration/v2/wlan/ssid"

# Test AP monitoring access  
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://apigw-prod2.central.arubanetworks.com/monitoring/v1/aps"

# Test template access
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://apigw-prod2.central.arubanetworks.com/configuration/v2/ap_groups"
```

## Troubleshooting

### Common Issues

#### 1. 401 Unauthorized
**Symptoms**: Authentication failures
**Causes**: Invalid credentials, expired tokens
**Solutions**:
- Verify client ID and secret
- Check token expiration
- Regenerate OAuth token
- Verify API permissions

#### 2. 403 Forbidden  
**Symptoms**: Access denied to specific APIs
**Causes**: Insufficient permissions
**Solutions**:
- Check API client permissions in Central
- Verify required API categories are enabled
- Contact Central administrator for permission updates

#### 3. 429 Rate Limited
**Symptoms**: Too many requests error
**Causes**: Exceeding API rate limits
**Solutions**:
- Implement request throttling
- Add delays between API calls
- Use bulk operations where available
- Monitor API usage in Central

#### 4. 404 Not Found
**Symptoms**: Resource not found errors
**Causes**: Invalid endpoints, missing resources
**Solutions**:
- Verify API endpoint URLs
- Check if resources exist in Central
- Validate customer ID and tenant access

## API Rate Limits

### Central API Limits
```json
{
  "rate_limits": {
    "requests_per_minute": 300,
    "requests_per_hour": 10000,
    "burst_limit": 50,
    "concurrent_connections": 10
  },
  "recommendations": {
    "batch_operations": "Use bulk APIs when available",
    "request_spacing": "Minimum 200ms between requests",
    "error_handling": "Implement exponential backoff",
    "monitoring": "Track rate limit headers"
  }
}
```

### Rate Limit Headers
Monitor these headers in API responses:
- `X-RateLimit-Limit`: Total requests allowed per window
- `X-RateLimit-Remaining`: Remaining requests in current window  
- `X-RateLimit-Reset`: Time when rate limit resets
- `Retry-After`: Seconds to wait before retrying (when rate limited)

## Regional Endpoints

Different regions use different API endpoints:
```json
{
  "regions": {
    "americas": "https://apigw-prod2.central.arubanetworks.com",
    "apac": "https://apigw-apac.central.arubanetworks.com", 
    "emea": "https://apigw-eu.central.arubanetworks.com"
  }
}
```

Make sure to use the correct endpoint for your Central instance region.

## Credential Rotation

### Automated Token Refresh
```javascript
// Example token refresh logic for n8n
const refreshToken = async () => {
  const response = await $http.request({
    method: 'POST',
    url: 'https://central-prod.arubanetworks.com/oauth2/token',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data: {
      grant_type: 'client_credentials',
      client_id: $credentials.client_id,
      client_secret: $credentials.client_secret
    }
  });
  
  return response.access_token;
};
```

This comprehensive credential setup ensures secure, reliable access to Aruba Central APIs for all wireless automation workflows.
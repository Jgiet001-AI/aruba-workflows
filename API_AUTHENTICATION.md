# HPE Aruba API Authentication Guide

This document provides comprehensive authentication information for all HPE Aruba APIs used in n8n workflows.

## Overview

HPE Aruba provides multiple API endpoints across different products, each with specific authentication requirements:

| API | Authentication Method | Token Type | Rate Limits |
|-----|----------------------|------------|-------------|
| Central (Classic) | OAuth 2.0 | Bearer Token | 100 req/min |
| AOS-CX | Basic Auth + Session | Cookie/Token | Device specific |
| EdgeConnect | API Key or Session | X-API-Key | 10 req/sec |
| UXI | Bearer Token | API Token | 60 req/min |

---

## 1. HPE Aruba Central API

### Authentication Method: OAuth 2.0
- **Type**: Client Credentials Grant
- **Token Endpoint**: `https://{region}.central.arubanetworks.com/oauth2/token`
- **Authorization Header**: `Bearer {access_token}`

### Regional Endpoints
```
US West: apigw-uswest4.central.arubanetworks.com
EU Central: apigw-eucentral3.central.arubanetworks.com  
AP Northeast: apigw-apnortheast1.central.arubanetworks.com
```

### Required Credentials
- Client ID (from Central Developer Portal)
- Client Secret (from Central Developer Portal)
- Appropriate scopes (read:monitoring, write:configuration, etc.)

### Rate Limiting
- **Standard**: 100 requests per minute
- **Burst**: Up to 200 requests
- **Headers**: `X-RateLimit-Remaining`, `Retry-After`

### Sample OAuth Flow
```javascript
// Step 1: Get Access Token
POST https://{region}.central.arubanetworks.com/oauth2/token
Headers: Content-Type: application/x-www-form-urlencoded
Body: 
  grant_type=client_credentials
  &client_id={client_id}
  &client_secret={client_secret}
  &scope=read:monitoring write:configuration

// Step 2: Use Token in API Calls
GET https://{region}.central.arubanetworks.com/api/v2/devices
Headers: Authorization: Bearer {access_token}
```

---

## 2. AOS-CX REST API

### Authentication Method: Basic Auth + Session Tokens
- **Initial Auth**: Basic Authentication (username/password)
- **Session Auth**: Cookie-based or Token-based
- **API Version**: v10.08

### Endpoints Structure
```
Base URL: https://{switch_ip}:443/rest/v10.08/
Login: /rest/v10.08/login-sessions
Logout: /rest/v10.08/login-sessions/{session_id}
```

### Authentication Flow
```javascript
// Step 1: Create Session
POST https://{switch_ip}/rest/v10.08/login-sessions
Headers: 
  Authorization: Basic {base64(username:password)}
  Content-Type: application/json

// Step 2: Use Session Cookie
GET https://{switch_ip}/rest/v10.08/system
Headers: Cookie: {session_cookie}
```

### Switch-Specific Considerations
- Each switch maintains independent sessions
- Sessions timeout after inactivity (default: 30 minutes)
- SSL certificate verification often disabled in lab environments
- Multiple concurrent sessions supported

---

## 3. EdgeConnect Orchestrator API

### Authentication Method: API Key or Session-based
- **API Key**: X-API-Key header (recommended for automation)
- **Session**: Login with username/password for web sessions

### Orchestrator Configuration
```
Base URL: https://{orchestrator_url}/api/
Account ID: Required for multi-tenant environments
Organization ID: Required for enterprise deployments
```

### Authentication Options

#### Option A: API Key (Recommended)
```javascript
GET https://{orchestrator_url}/api/appliances
Headers: X-API-Key: {api_key}
```

#### Option B: Session-based
```javascript
// Login
POST https://{orchestrator_url}/api/login
Body: {"username": "user", "password": "pass"}

// Use session cookie
GET https://{orchestrator_url}/api/appliances
Headers: Cookie: orchSession={session_id}
```

### Rate Limiting
- **Standard**: 10 requests per second
- **Batch Operations**: Maximum 50 items per request
- **Long Operations**: Use asynchronous task tracking

---

## 4. UXI API

### Authentication Method: Bearer Token
- **Type**: API Token (generated in UXI Dashboard)
- **Header**: `Authorization: Bearer {token}`
- **Base URL**: `https://api.uxi.aruba.com`

### Token Configuration
```javascript
// Dashboard URL format
https://{customer_id}.dashboard.uxi.aruba.com

// API calls
GET https://api.uxi.aruba.com/api/v1/tests
Headers: Authorization: Bearer {api_token}
```

### Data Access Considerations
- **Customer ID**: Required for dashboard access
- **Data Retention**: 90 days for most metrics
- **Time Zones**: UTC for all timestamps
- **Pagination**: Use limit/offset parameters

---

## n8n Credential Configuration

### Setting Up Credentials in n8n

#### 1. Aruba Central OAuth2
```json
{
  "name": "Aruba Central API",
  "type": "oAuth2Api",
  "data": {
    "authUrl": "https://{region}.central.arubanetworks.com/oauth2/authorize",
    "accessTokenUrl": "https://{region}.central.arubanetworks.com/oauth2/token",
    "clientId": "{your_client_id}",
    "clientSecret": "{your_client_secret}",
    "scope": "read:monitoring write:configuration",
    "authQueryParameters": "response_type=code",
    "authentication": "header"
  }
}
```

#### 2. AOS-CX Basic Auth
```json
{
  "name": "AOS-CX Switch",
  "type": "httpBasicAuth",
  "data": {
    "user": "{switch_username}",
    "password": "{switch_password}"
  }
}
```

#### 3. EdgeConnect API Key
```json
{
  "name": "EdgeConnect API",
  "type": "httpHeaderAuth",
  "data": {
    "name": "X-API-Key",
    "value": "{your_api_key}"
  }
}
```

#### 4. UXI Bearer Token
```json
{
  "name": "UXI API",
  "type": "httpHeaderAuth", 
  "data": {
    "name": "Authorization",
    "value": "Bearer {your_token}"
  }
}
```

---

## Best Practices

### Security
- ✅ Store all credentials in n8n credential store
- ✅ Use environment-specific credentials (dev/staging/prod)
- ✅ Rotate API keys and tokens regularly
- ✅ Implement least-privilege access
- ❌ Never hardcode credentials in workflows
- ❌ Never commit credentials to version control

### Performance
- ✅ Implement rate limiting in workflows
- ✅ Use connection pooling for AOS-CX
- ✅ Cache tokens to reduce authentication calls
- ✅ Implement exponential backoff for retries
- ✅ Monitor API usage and quotas

### Error Handling
- ✅ Handle token expiration gracefully
- ✅ Implement retry logic for network failures
- ✅ Log authentication errors appropriately
- ✅ Provide meaningful error messages
- ✅ Fail securely on authentication errors

### Monitoring
- ✅ Track API response times
- ✅ Monitor rate limit consumption
- ✅ Alert on authentication failures
- ✅ Log all API interactions for audit
- ✅ Track credential rotation schedules

---

## Testing API Connectivity

Use these test endpoints to verify connectivity:

### Central API Health Check
```bash
curl -H "Authorization: Bearer {token}" \
  https://{region}.central.arubanetworks.com/api/v2/devices
```

### AOS-CX System Info
```bash
curl -k -u "{user}:{pass}" \
  https://{switch_ip}/rest/v10.08/system
```

### EdgeConnect Appliances
```bash
curl -H "X-API-Key: {key}" \
  https://{orchestrator}/api/appliances
```

### UXI Tests List
```bash
curl -H "Authorization: Bearer {token}" \
  https://api.uxi.aruba.com/api/v1/tests
```

---

## Troubleshooting

### Common Issues

#### OAuth Token Issues
- **Problem**: `401 Unauthorized` responses
- **Solution**: Verify client credentials and scopes
- **Check**: Token expiration and refresh logic

#### AOS-CX Session Issues  
- **Problem**: Session timeouts during long operations
- **Solution**: Implement session refresh logic
- **Check**: Switch session timeout settings

#### Rate Limiting
- **Problem**: `429 Too Many Requests` errors
- **Solution**: Implement exponential backoff
- **Check**: Rate limit headers in responses

#### SSL Certificate Issues
- **Problem**: SSL verification failures with AOS-CX
- **Solution**: Disable SSL verification in lab environments
- **Check**: Certificate validity and trust chains

---

**Last Updated**: January 2025  
**Version**: 1.0
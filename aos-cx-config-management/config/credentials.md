# AOS-CX Credentials Configuration

## Required Credentials

### 1. AOS-CX Switch Authentication
Create an n8n credential of type "HTTP Header Auth" or "Basic Auth"

#### Option A: Basic Authentication (Recommended)
```json
{
  "name": "AOS-CX Basic Auth",
  "type": "httpBasicAuth",
  "data": {
    "user": "admin",
    "password": "your_switch_password"
  }
}
```

#### Option B: Token Authentication
```json
{
  "name": "AOS-CX Token Auth",
  "type": "httpHeaderAuth", 
  "data": {
    "name": "Authorization",
    "value": "Bearer your_access_token"
  }
}
```

### 2. Switch Management Details
Configure these as n8n environment variables or workflow parameters:

```json
{
  "SWITCH_BASE_URL": "https://192.168.1.100",
  "API_VERSION": "v10.08",
  "VERIFY_SSL": false,
  "TIMEOUT": 30000
}
```

## Security Best Practices

### 1. Switch-Side Configuration
```bash
# Enable REST API on AOS-CX switch
switch(config)# https-server rest access-mode read-write
switch(config)# https-server vrf mgmt

# Create dedicated API user (recommended)
switch(config)# user api-automation group administrators password plaintext YourSecurePassword123
```

### 2. Network Security
- Use HTTPS only (never HTTP)
- Restrict API access to management VRF
- Implement IP allowlists for API clients
- Use strong passwords or certificate-based auth

### 3. n8n Security
- Store credentials in n8n credential store (never in workflow)
- Use environment variables for sensitive config
- Enable workflow-level credential restrictions
- Regular credential rotation (90 days recommended)

## API Endpoint Format

All AOS-CX API calls follow this pattern:
```
https://{switch_ip}/rest/{api_version}/{resource}
```

Examples:
- VLANs: `https://192.168.1.100/rest/v10.08/system/vlans`
- Interfaces: `https://192.168.1.100/rest/v10.08/system/interfaces`
- System: `https://192.168.1.100/rest/v10.08/system`

## Testing Credentials

Use this curl command to verify credentials:
```bash
curl -k -u admin:password \
  -H "Content-Type: application/json" \
  https://192.168.1.100/rest/v10.08/system
```

Expected response: HTTP 200 with system information JSON

## Troubleshooting

### Common Issues
1. **401 Unauthorized**: Check username/password
2. **403 Forbidden**: User lacks necessary permissions
3. **404 Not Found**: API not enabled or wrong URL
4. **SSL Errors**: Use `-k` flag or configure proper certificates

### Debug Steps
1. Verify switch REST API is enabled
2. Test with curl before configuring n8n
3. Check switch logs for authentication failures
4. Validate API version compatibility

## Required Switch Permissions

The API user needs these minimum permissions:
- **System Read**: View system information
- **System Write**: Modify system configuration  
- **VLAN Management**: Create/modify/delete VLANs
- **Interface Management**: Configure port settings
- **ACL Management**: Create/modify security policies
- **Configuration Access**: Backup/restore configurations
# UXI API Credentials Configuration

This guide explains how to configure credentials for the UXI sensors configuration management workflows.

## Prerequisites

- Access to HPE Aruba UXI Dashboard
- UXI API access enabled
- n8n instance with credential management

## UXI API Credentials

### 1. Generate UXI API Token

1. **Log in to UXI Dashboard**:
   - Navigate to your UXI Dashboard: `https://dashboard.uxi.aruba.com`
   - Log in with your credentials

2. **Access API Settings**:
   - Go to Settings → API Access
   - Click "Generate New Token"
   - Copy the generated token securely

3. **Configure Token Permissions**:
   - Ensure the token has the following permissions:
     - Sensor Management: Read, Write, Delete
     - Test Configuration: Read, Write, Delete
     - Analytics & Reporting: Read, Write
     - Data Export: Read

### 2. Configure n8n Credentials

1. **Create UXI API Credential**:
   - In n8n, go to Settings → Credentials
   - Click "New Credential"
   - Select "HTTP Request" type
   - Name: `uxiApi`

2. **Configure Credential Fields**:
   ```json
   {
     "name": "uxiApi",
     "type": "httpHeaderAuth",
     "data": {
       "name": "Authorization",
       "value": "Bearer YOUR_UXI_API_TOKEN"
     }
   }
   ```

3. **Test Credential**:
   - Test the credential with a simple API call
   - Verify access to UXI API endpoints

### 3. Alternative: OAuth 2.0 Configuration

For enterprise environments, OAuth 2.0 is recommended:

1. **Register Application**:
   - Register your application in UXI Dashboard
   - Get Client ID and Client Secret
   - Configure redirect URIs

2. **Configure OAuth in n8n**:
   ```json
   {
     "name": "uxiApiOAuth",
     "type": "oauth2",
     "data": {
       "clientId": "YOUR_CLIENT_ID",
       "clientSecret": "YOUR_CLIENT_SECRET",
       "accessTokenUrl": "https://api.uxi.aruba.com/oauth/token",
       "authUrl": "https://api.uxi.aruba.com/oauth/authorize",
       "scope": "sensors:read sensors:write tests:read tests:write analytics:read reports:write"
     }
   }
   ```

## Slack Notification Credentials

### 1. Create Slack App

1. **Go to Slack API**:
   - Visit: `https://api.slack.com/apps`
   - Click "Create New App"
   - Choose "From scratch"

2. **Configure App**:
   - App Name: "UXI Monitoring"
   - Workspace: Select your workspace
   - Click "Create App"

3. **Add Bot Token Scopes**:
   - Go to OAuth & Permissions
   - Add Bot Token Scopes:
     - `chat:write`
     - `chat:write.public`
     - `channels:read`

4. **Install App**:
   - Click "Install App to Workspace"
   - Copy the Bot User OAuth Token

### 2. Configure Slack Credential in n8n

1. **Create Slack Credential**:
   - In n8n, create new credential
   - Type: "Slack"
   - Name: `slackBot`

2. **Configure Token**:
   ```json
   {
     "name": "slackBot",
     "type": "slackApi",
     "data": {
       "accessToken": "xoxb-YOUR-SLACK-BOT-TOKEN"
     }
   }
   ```

## Email Notification Credentials

### 1. SMTP Configuration

For email notifications, configure SMTP settings:

1. **Create Email Credential**:
   - Type: "SMTP"
   - Name: `emailSMTP`

2. **Configure SMTP Settings**:
   ```json
   {
     "name": "emailSMTP",
     "type": "smtp",
     "data": {
       "host": "smtp.office365.com",
       "port": 587,
       "secure": false,
       "user": "your-email@company.com",
       "password": "your-app-password",
       "from": "uxi-monitoring@company.com"
     }
   }
   ```

### 2. Gmail Configuration

For Gmail SMTP:

```json
{
  "name": "gmailSMTP",
  "type": "smtp",
  "data": {
    "host": "smtp.gmail.com",
    "port": 587,
    "secure": false,
    "user": "your-gmail@gmail.com",
    "password": "your-app-password"
  }
}
```

## Security Best Practices

### 1. Token Management

- **Rotate Tokens Regularly**: Change API tokens every 90 days
- **Use Minimum Permissions**: Grant only necessary permissions
- **Monitor Token Usage**: Review API usage logs regularly
- **Secure Storage**: Store tokens securely in n8n credential vault

### 2. Network Security

- **HTTPS Only**: Always use HTTPS for API calls
- **IP Whitelisting**: Restrict API access to specific IP addresses
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **Audit Logging**: Enable comprehensive audit logging

### 3. Access Control

- **Role-Based Access**: Implement role-based access control
- **Multi-Factor Authentication**: Enable MFA for UXI Dashboard access
- **Regular Reviews**: Review access permissions regularly
- **Principle of Least Privilege**: Grant minimum necessary access

## Environment-Specific Configuration

### Development Environment

```json
{
  "uxi_api_url": "https://api-dev.uxi.aruba.com",
  "credentials": {
    "token": "dev-token",
    "permissions": ["read", "write"]
  },
  "notifications": {
    "slack_channel": "#uxi-dev",
    "email_recipients": ["dev-team@company.com"]
  }
}
```

### Production Environment

```json
{
  "uxi_api_url": "https://api.uxi.aruba.com",
  "credentials": {
    "token": "prod-token",
    "permissions": ["read", "write", "delete"]
  },
  "notifications": {
    "slack_channel": "#uxi-production",
    "email_recipients": ["network-team@company.com", "ops-team@company.com"]
  }
}
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify token validity
   - Check token permissions
   - Ensure correct API endpoint

2. **Rate Limiting**:
   - Implement exponential backoff
   - Monitor API usage
   - Optimize request frequency

3. **Network Connectivity**:
   - Check firewall settings
   - Verify DNS resolution
   - Test network connectivity

### Error Codes

- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: Insufficient permissions
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: UXI API issue

## Credential Testing

### Test UXI API Access

```bash
# Test API connectivity
curl -X GET "https://api.uxi.aruba.com/api/v1/sensors" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### Test Slack Integration

```bash
# Test Slack webhook
curl -X POST YOUR_SLACK_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"text": "UXI monitoring test message"}'
```

## Credential Rotation

### Automated Rotation

Set up automated token rotation:

1. **Schedule Token Refresh**: Every 60 days
2. **Backup Tokens**: Keep backup tokens for continuity
3. **Update Workflows**: Automatically update workflow credentials
4. **Notify Teams**: Alert teams about credential changes

### Manual Rotation Process

1. **Generate New Token**: Create new API token
2. **Update n8n Credentials**: Replace old token in n8n
3. **Test Workflows**: Verify all workflows work with new token
4. **Revoke Old Token**: Disable old token in UXI Dashboard
5. **Document Changes**: Update credential documentation

---

**Security Note**: Never commit credentials to version control. Always use secure credential management systems and follow your organization's security policies.

**Last Updated**: January 2025  
**Version**: 1.0.0
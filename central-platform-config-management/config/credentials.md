# Central Platform Configuration Management - Credentials Guide

## Overview
This document outlines the credentials required for the Central Platform Configuration Management workflows.

## Required Credentials

### 1. Aruba Central Platform API
```json
{
  "name": "Aruba Central Platform API",
  "type": "OAuth 2.0",
  "required_fields": {
    "client_id": "Your OAuth client ID",
    "client_secret": "Your OAuth client secret",
    "access_token": "Generated access token",
    "refresh_token": "Generated refresh token",
    "token_expiry": "Token expiration timestamp"
  },
  "scopes": [
    "read:configuration",
    "write:configuration",
    "read:templates",
    "write:templates",
    "read:devices",
    "write:devices",
    "read:groups",
    "write:groups",
    "read:policies",
    "write:policies",
    "read:services",
    "write:services"
  ]
}
```

### 2. Notification Services

#### Slack Integration
```json
{
  "name": "Slack Webhook",
  "type": "Webhook URL",
  "required_fields": {
    "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
    "channel": "#central-platform-automation",
    "username": "Central Platform Bot"
  }
}
```

#### Email SMTP
```json
{
  "name": "Email SMTP",
  "type": "SMTP",
  "required_fields": {
    "smtp_host": "smtp.company.com",
    "smtp_port": 587,
    "smtp_username": "automation@company.com",
    "smtp_password": "your-smtp-password",
    "from_email": "central-platform@company.com"
  }
}
```

### 3. External Systems (Optional)

#### ServiceNow Integration
```json
{
  "name": "ServiceNow",
  "type": "Basic Auth",
  "required_fields": {
    "instance_url": "https://your-instance.service-now.com",
    "username": "integration-user",
    "password": "integration-password"
  }
}
```

#### Database Storage
```json
{
  "name": "PostgreSQL",
  "type": "Database",
  "required_fields": {
    "host": "db.company.com",
    "port": 5432,
    "database": "central_platform",
    "username": "central_user",
    "password": "database-password"
  }
}
```

## Setting Up Credentials in n8n

### 1. Aruba Central OAuth 2.0 Setup
1. Go to n8n → Credentials
2. Click "Create Credential"
3. Select "OAuth2 API"
4. Configure:
   - **Name**: "Aruba Central Platform API"
   - **Authorization URL**: `https://central.arubanetworks.com/oauth2/authorize`
   - **Access Token URL**: `https://central.arubanetworks.com/oauth2/token`
   - **Client ID**: Your client ID
   - **Client Secret**: Your client secret
   - **Scope**: `read:configuration write:configuration read:templates write:templates`

### 2. Slack Webhook Setup
1. Go to n8n → Credentials
2. Click "Create Credential"
3. Select "Slack Webhook"
4. Configure:
   - **Name**: "Central Platform Slack"
   - **Webhook URL**: Your Slack webhook URL

### 3. Email SMTP Setup
1. Go to n8n → Credentials
2. Click "Create Credential"
3. Select "SMTP"
4. Configure:
   - **Name**: "Central Platform Email"
   - **Host**: Your SMTP host
   - **Port**: 587 (or your SMTP port)
   - **Username**: Your email username
   - **Password**: Your email password

## Security Best Practices

### 1. Credential Rotation
- Rotate OAuth tokens every 90 days
- Update API keys monthly
- Monitor for credential expiration

### 2. Access Control
- Use least privilege principle
- Limit credential access to necessary workflows
- Implement approval workflows for sensitive operations

### 3. Monitoring
- Log all credential usage
- Monitor for unauthorized access
- Set up alerts for credential failures

### 4. Backup
- Backup credential configurations
- Store backups in secure location
- Test credential restore procedures

## Environment-Specific Configurations

### Development Environment
```json
{
  "environment": "development",
  "central_api": {
    "base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "rate_limit": 50
  },
  "notifications": {
    "slack_channel": "#dev-central-platform",
    "email_recipients": ["dev-team@company.com"]
  }
}
```

### Staging Environment
```json
{
  "environment": "staging",
  "central_api": {
    "base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "rate_limit": 75
  },
  "notifications": {
    "slack_channel": "#staging-central-platform",
    "email_recipients": ["qa-team@company.com"]
  }
}
```

### Production Environment
```json
{
  "environment": "production",
  "central_api": {
    "base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "rate_limit": 100
  },
  "notifications": {
    "slack_channel": "#prod-central-platform",
    "email_recipients": ["network-team@company.com", "ops-team@company.com"]
  }
}
```

## Troubleshooting

### Common Issues
1. **Token Expiration**: Implement automatic token refresh
2. **Rate Limiting**: Implement exponential backoff
3. **Network Connectivity**: Add retry logic with delays
4. **Permission Errors**: Verify OAuth scopes and API permissions

### Testing Credentials
Use the provided test endpoints to verify credential functionality:
- Test OAuth token: `GET /api/v2/auth/validate`
- Test Slack webhook: Send test message
- Test email SMTP: Send test email

## Support
For credential-related issues:
- Check n8n execution logs
- Verify API documentation
- Contact network administration team
- Review Aruba Central API documentation

---

**Last Updated**: January 2025  
**Version**: 1.0.0
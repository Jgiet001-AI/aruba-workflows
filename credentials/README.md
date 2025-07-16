# Credential Templates

This directory contains templates for credentials needed by HPE Aruba workflows.

⚠️ **IMPORTANT**: This directory should NEVER contain actual credentials or API keys.

## Available Credential Templates

### Aruba Central API
- Template: `aruba-central-credentials.template.json`
- Required: Client ID, Client Secret, Base URL
- Authentication: OAuth 2.0

### AOS-CX REST API
- Template: `aos-cx-credentials.template.json`
- Required: Username, Password, Switch IPs
- Authentication: Token-based

### EdgeConnect API
- Template: `edgeconnect-credentials.template.json`
- Required: API Key, Orchestrator URL
- Authentication: API Key

### UXI API
- Template: `uxi-credentials.template.json`
- Required: Bearer Token, Dashboard URL
- Authentication: Bearer Token

## Setup Instructions

1. Copy template files and remove `.template` extension
2. Fill in actual credential values
3. Configure in n8n credential store
4. Delete local credential files (keep only templates)

## Security Best Practices

- ✅ Use n8n's built-in credential store
- ✅ Enable credential encryption
- ✅ Rotate credentials regularly
- ❌ Never commit actual credentials to version control
- ❌ Never hardcode credentials in workflows
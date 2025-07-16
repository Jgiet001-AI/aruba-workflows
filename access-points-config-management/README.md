# Access Points Configuration Management

## Overview
Automated configuration management workflows for HPE Aruba wireless access points using n8n. This workflow suite provides comprehensive AP automation including wireless configuration, provisioning, location services, and client policy management.

## Features
- **Wireless Configuration**: SSID management, security settings, radio configurations
- **AP Provisioning**: Zero-touch provisioning, template deployment, bulk configuration
- **Location Services**: Beacon configuration, RTLS setup, analytics integration
- **Client Policy Management**: User authentication, device onboarding, access control
- **Bulk Operations**: Mass AP configuration and firmware updates
- **Compliance Monitoring**: Wireless security compliance and policy enforcement

## File Structure
- `workflow.json` - Main n8n workflow export
- `config/` - Configuration files and credential requirements
- `tests/` - Test data and validation results
- `docs/` - Additional documentation and examples
- `versions/` - Version history and change logs

## API Endpoints Covered
Based on HPE Aruba Central API collection analysis (141 configuration endpoints):
- **SSIDs**: `/central/v2/wlan/ssid` - SSID creation, configuration, security
- **Access Points**: `/central/v1/devices/access_points` - AP management and settings
- **Templates**: `/central/v2/configuration/templates` - Configuration templates
- **Clients**: `/central/v1/clients` - Client management and policies
- **Location**: `/central/v1/location` - Location services and beacons
- **Security**: `/central/v2/security` - Wireless security policies

## Quick Start
1. Import workflow.json into n8n
2. Configure Aruba Central credentials (see config/credentials.md)
3. Update parameters in config/parameters.json
4. Test with sample data in tests/
5. Deploy to production environment

## Requirements
- n8n instance with HTTP Request node
- Aruba Central cloud account with API access
- Valid Central API credentials (client ID/secret or token)
- Network connectivity to Aruba Central API endpoints

## Support
Last Updated: January 2025
Workflow Version: 1.0.0-dev
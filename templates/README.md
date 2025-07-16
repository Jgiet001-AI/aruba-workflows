# Workflow Templates

This directory contains reusable n8n workflow templates for HPE Aruba automation.

## Available Templates

### Core Templates
- `http-request-template.json` - Standard HTTP request configuration for Aruba APIs
- `error-handler-template.json` - Comprehensive error handling pattern
- `webhook-trigger-template.json` - Event-driven workflow triggers
- `schedule-trigger-template.json` - Time-based automation triggers

### Monitoring Templates
- `device-health-template.json` - Device health monitoring workflow
- `alert-notification-template.json` - Alert routing and notification
- `performance-monitoring-template.json` - Network performance tracking

### Configuration Templates
- `config-backup-template.json` - Automated configuration backup
- `compliance-check-template.json` - Configuration compliance verification
- `bulk-update-template.json` - Mass configuration deployment

### Security Templates
- `security-response-template.json` - Security incident response
- `access-control-template.json` - Dynamic access control
- `rogue-detection-template.json` - Unauthorized device detection

## Usage Instructions

1. Import template into n8n workflow editor
2. Customize parameters for your environment
3. Configure credentials and connections
4. Test with sample data
5. Deploy to production

## Template Structure

Each template includes:
- Pre-configured nodes with standard settings
- Error handling and retry logic
- Documentation and comments
- Sample test data
- Configuration parameters

## Contributing

When creating new templates:
- Follow naming convention: `purpose-template.json`
- Include comprehensive error handling
- Add clear documentation
- Test thoroughly before committing
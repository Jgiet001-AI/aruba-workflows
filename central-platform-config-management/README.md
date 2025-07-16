# Central Platform Configuration Management Workflows

## Overview
This directory contains comprehensive n8n workflows for managing the HPE Aruba Central Platform configuration, including template management, cloud services, policy automation, and device group management.

## Workflow Collection

### 1. Template Management Workflow
**File**: `central-platform-template-management-workflow.json`  
**Documentation**: [README-Template-Management.md](README-Template-Management.md)

**Capabilities**:
- Create, update, and delete configuration templates
- Deploy templates to devices and groups
- Validate templates before deployment
- Backup and restore template configurations
- Clone and version templates
- Bulk template deployment

**Key Operations**:
- `create_template` - Create new configuration templates
- `deploy_template` - Deploy templates to target devices
- `validate_template` - Validate template syntax and compatibility
- `bulk_deploy` - Deploy multiple templates simultaneously

### 2. Cloud Services Configuration Workflow
**File**: `central-platform-cloud-services-workflow.json`  
**Documentation**: [README-Cloud-Services.md](README-Cloud-Services.md)

**Capabilities**:
- Configure and manage cloud-based services
- Identity service management (RADIUS, LDAP, SAML)
- Location services and analytics
- Backup and monitoring services
- Service scaling and performance optimization
- Service health monitoring

**Key Operations**:
- `configure_service` - Set up new cloud services
- `service_scaling` - Auto-scale services based on demand
- `service_backup` - Create service backups
- `service_metrics` - Retrieve performance metrics

### 3. Policy and Rule Automation Workflow
**File**: `central-platform-policy-automation-workflow.json`  
**Documentation**: [README-Policy-Automation.md](README-Policy-Automation.md)

**Capabilities**:
- Create and manage network policies
- Deploy policies to devices and groups
- Monitor policy compliance
- Analyze policy impact
- Rollback policy changes
- Audit policy history

**Key Operations**:
- `create_policy` - Create network, QoS, or security policies
- `apply_policy` - Deploy policies to target infrastructure
- `policy_compliance` - Check compliance status
- `policy_rollback` - Rollback to previous policy versions

### 4. Device Group Management Workflow
**File**: `central-platform-device-group-workflow.json`  
**Documentation**: [README-Device-Group-Management.md](README-Device-Group-Management.md)

**Capabilities**:
- Create static and dynamic device groups
- Manage group membership automatically
- Deploy configurations to groups
- Monitor group health and analytics
- Move devices between groups
- Synchronize group membership

**Key Operations**:
- `create_group` - Create device groups (static, dynamic, location-based)
- `add_devices` - Add devices to groups
- `apply_configuration` - Deploy configs to entire groups
- `group_analytics` - Retrieve group performance metrics

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Central Platform Management                  │
├─────────────────┬────────────────┬────────────┬─────────────┤
│    Templates    │ Cloud Services │  Policies  │   Groups    │
├─────────────────┼────────────────┼────────────┼─────────────┤
│ • Create        │ • Identity     │ • Network  │ • Static    │
│ • Deploy        │ • Location     │ • QoS      │ • Dynamic   │
│ • Validate      │ • Analytics    │ • Security │ • Location  │
│ • Version       │ • Backup       │ • Compliance│ • Template │
└─────────────────┴────────────────┴────────────┴─────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  HPE Aruba API  │
                    └─────────────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │  Network Infrastructure │
                └─────────────────────────┘
```

## Quick Start Guide

### 1. Prerequisites
- n8n instance running at `http://192.168.40.100:8006`
- HPE Aruba Central API credentials configured
- Appropriate permissions for Central Platform management
- Slack webhook configured for notifications

### 2. Import Workflows
```bash
# Import all workflows to n8n
# Use n8n UI to import each JSON file
```

### 3. Configure Credentials
Create the following credentials in n8n:
- **Aruba Central API** - OAuth 2.0 credentials
- **Slack** - Webhook URL for notifications

### 4. Test Each Workflow
```bash
# Test template management
curl -X POST http://192.168.40.100:8006/webhook/central-template-management \
  -H "Content-Type: application/json" \
  -d '{"operation": "list_templates"}'

# Test cloud services
curl -X POST http://192.168.40.100:8006/webhook/central-cloud-services \
  -H "Content-Type: application/json" \
  -d '{"operation": "list_services"}'

# Test policy automation
curl -X POST http://192.168.40.100:8006/webhook/central-policy-automation \
  -H "Content-Type: application/json" \
  -d '{"operation": "list_policies"}'

# Test device groups
curl -X POST http://192.168.40.100:8006/webhook/central-device-groups \
  -H "Content-Type: application/json" \
  -d '{"operation": "list_groups"}'
```

## Common Use Cases

### 1. Deploy Standard Configuration
```json
{
  "operation": "create_template",
  "template_data": {
    "name": "Standard Branch Config",
    "type": "device_config",
    "configuration": {...}
  }
}
// Then deploy to group
{
  "operation": "apply_configuration",
  "group_data": {
    "group_id": "branch_offices",
    "template_id": "template_123"
  }
}
```

### 2. Create Security Policy Suite
```json
{
  "operation": "create_policy",
  "policy_data": {
    "policy_name": "Enterprise Security Suite",
    "policy_type": "security_policy",
    "threat_prevention": "enabled",
    "intrusion_detection": "enabled"
  }
}
// Apply to all devices
{
  "operation": "apply_policy",
  "policy_data": {
    "policy_id": "policy_123",
    "target_groups": ["all_devices"]
  }
}
```

### 3. Dynamic Group Management
```json
{
  "operation": "create_group",
  "group_data": {
    "group_name": "Non-Compliant Devices",
    "group_type": "dynamic",
    "membership_rules": [
      {
        "attribute": "compliance_score",
        "operator": "less_than",
        "value": 80
      }
    ]
  }
}
```

### 4. Cloud Service Scaling
```json
{
  "operation": "service_scaling",
  "service_data": {
    "service_id": "analytics_service_001",
    "scaling_action": "auto",
    "cpu_threshold": 75,
    "memory_threshold": 80
  }
}
```

## Best Practices

### 1. Template Management
- Version all templates with semantic versioning
- Validate templates before deployment
- Use variable substitution for flexibility
- Create backups before major changes

### 2. Policy Deployment
- Test policies in lab environment first
- Deploy policies in stages
- Monitor compliance after deployment
- Document all policy changes

### 3. Group Organization
- Use logical naming conventions
- Limit dynamic group complexity
- Regular membership audits
- Document group purposes

### 4. Service Configuration
- Enable auto-scaling for critical services
- Regular backup schedules
- Monitor service health metrics
- Plan for service dependencies

## Error Handling

All workflows implement comprehensive error handling:
- **Validation Errors**: Check input parameters
- **API Errors**: Retry with exponential backoff
- **Configuration Conflicts**: Rollback capabilities
- **Permission Issues**: Clear error messages
- **Network Failures**: Timeout and retry logic

## Monitoring and Notifications

### Slack Notifications
All workflows send notifications to configured Slack channels:
- Operation success/failure
- Deployment progress
- Compliance alerts
- Error notifications

### Metrics Tracking
- Response times
- Success rates
- API call counts
- Resource utilization

## Security Considerations

### Access Control
- OAuth 2.0 authentication required
- Role-based access control (RBAC)
- Audit logging for all operations
- Encrypted credential storage

### Data Protection
- TLS 1.3 for API communications
- Sensitive data masking in logs
- Secure backup storage
- Compliance with security standards

## Troubleshooting

### Common Issues
1. **Authentication Failures**
   - Verify API credentials
   - Check token expiration
   - Confirm permissions

2. **Deployment Failures**
   - Validate template/policy syntax
   - Check device compatibility
   - Review error logs

3. **Performance Issues**
   - Adjust batch sizes
   - Implement rate limiting
   - Monitor API quotas

### Debug Mode
Enable debug logging in any workflow:
```json
{
  "options": {
    "debug": true,
    "verbose_logging": true
  }
}
```

## Maintenance

### Regular Tasks
- Review and update templates monthly
- Audit policy compliance weekly
- Clean up unused groups quarterly
- Update service configurations as needed

### Version Control
- Export workflows regularly
- Track changes in git
- Document modifications
- Test before production

## Support Resources

### Documentation
- Individual workflow READMEs
- HPE Aruba Central API documentation
- n8n workflow documentation
- Community forums

### Contact
- Create issues in project repository
- HPE Aruba support channels
- n8n community support

---

**Last Updated**: January 2025  
**Total Workflows**: 4  
**API Coverage**: 208 Central Platform endpoints  
**Automation Level**: Enterprise-ready
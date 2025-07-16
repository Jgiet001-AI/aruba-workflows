# Central Platform Template Management Workflow

## Overview
This workflow provides comprehensive template management capabilities for the HPE Aruba Central Platform, enabling automated creation, deployment, and lifecycle management of configuration templates.

## Workflow File
`central-platform-template-management-workflow.json`

## Capabilities

### Core Operations
1. **Create Template** - Create new configuration templates
2. **Update Template** - Modify existing templates with versioning
3. **Deploy Template** - Deploy templates to target devices
4. **List Templates** - Retrieve and filter available templates
5. **Delete Template** - Remove templates from the system
6. **Validate Template** - Validate templates before deployment
7. **Backup Template** - Create backups of templates
8. **Restore Template** - Restore templates from backups
9. **Clone Template** - Create copies of existing templates
10. **Bulk Deploy** - Deploy multiple templates simultaneously

### Template Types Supported
- **Device Configuration Templates** - Network device configuration
- **Network Policy Templates** - Network policies and rules
- **Security Profile Templates** - Security configurations
- **Service Configuration Templates** - Service-specific settings

## API Endpoint
```
POST /webhook/central-template-management
```

## Request Format

### Basic Request Structure
```json
{
  "operation": "create_template",
  "template_data": {
    "name": "Template Name",
    "type": "device_config",
    "description": "Template description",
    "configuration": {},
    "variables": {}
  },
  "options": {
    "validation_level": "full",
    "deployment_mode": "staged"
  }
}
```

### Operation-Specific Examples

#### 1. Create Template
```json
{
  "operation": "create_template",
  "template_data": {
    "name": "Corporate Switch Template",
    "type": "device_config",
    "description": "Standard configuration for corporate switches",
    "version": "1.0.0",
    "device_types": ["switch"],
    "config_sections": ["network", "security"],
    "configuration": {
      "vlans": [
        {
          "id": 10,
          "name": "Corporate",
          "description": "Corporate network"
        }
      ],
      "interfaces": [
        {
          "name": "GigabitEthernet0/1",
          "mode": "access",
          "vlan": 10
        }
      ]
    },
    "variables": {
      "corporate_vlan_id": {
        "type": "integer",
        "default": 10,
        "description": "Corporate VLAN ID"
      }
    },
    "required_fields": ["corporate_vlan_id"]
  }
}
```

#### 2. Update Template
```json
{
  "operation": "update_template",
  "template_data": {
    "template_id": "template_123",
    "name": "Updated Corporate Switch Template",
    "version": "1.1.0",
    "description": "Updated with new security policies",
    "configuration": {
      "vlans": [
        {
          "id": 10,
          "name": "Corporate",
          "description": "Corporate network with enhanced security"
        }
      ]
    }
  }
}
```

#### 3. Deploy Template
```json
{
  "operation": "deploy_template",
  "template_data": {
    "template_id": "template_123",
    "target_devices": [
      "device_001",
      "device_002",
      "device_003"
    ],
    "deployment_mode": "staged",
    "batch_size": 5,
    "delay_between_batches": 30,
    "rollback_on_failure": true,
    "variable_overrides": {
      "corporate_vlan_id": 20
    }
  }
}
```

#### 4. List Templates
```json
{
  "operation": "list_templates",
  "options": {
    "limit": 50,
    "offset": 0,
    "sort_by": "created_at",
    "sort_order": "desc",
    "template_type": "device_config",
    "name_filter": "Corporate",
    "status": "active"
  }
}
```

#### 5. Validate Template
```json
{
  "operation": "validate_template",
  "template_data": {
    "template_id": "template_123",
    "target_devices": ["device_001"]
  },
  "options": {
    "validation_level": "full"
  }
}
```

#### 6. Backup Template
```json
{
  "operation": "backup_template",
  "template_data": {
    "template_id": "template_123"
  },
  "options": {
    "backup_name": "corporate_switch_backup_2025_01",
    "include_metadata": true
  }
}
```

#### 7. Clone Template
```json
{
  "operation": "clone_template",
  "template_data": {
    "template_id": "template_123",
    "new_name": "Guest Network Switch Template",
    "new_description": "Template for guest network switches"
  }
}
```

#### 8. Bulk Deploy
```json
{
  "operation": "bulk_deploy",
  "template_data": {
    "deployments": [
      {
        "template_id": "template_123",
        "target_devices": ["device_001", "device_002"]
      },
      {
        "template_id": "template_456",
        "target_devices": ["device_003", "device_004"]
      }
    ]
  },
  "options": {
    "deployment_settings": {
      "mode": "parallel",
      "max_concurrent": 10
    }
  }
}
```

## Response Format

### Success Response
```json
{
  "success": true,
  "operation": "create_template",
  "execution_id": "template-1705404123456-abc123def",
  "timestamp": "2025-01-16T10:30:00.000Z",
  "message": "Template 'Corporate Switch Template' created successfully",
  "template_id": "template_123",
  "data": {
    "template_id": "template_123",
    "name": "Corporate Switch Template",
    "version": "1.0.0",
    "status": "active"
  },
  "metrics": {
    "response_time": "2.3s",
    "api_calls": 1,
    "success_rate": "100%"
  }
}
```

### Error Response
```json
{
  "success": false,
  "operation": "create_template",
  "execution_id": "template-1705404123456-abc123def",
  "timestamp": "2025-01-16T10:30:00.000Z",
  "error": {
    "code": "409",
    "message": "Template with this name already exists",
    "category": "CLIENT_ERROR",
    "retry_recommended": false
  }
}
```

## Template Configuration Examples

### Device Configuration Template
```json
{
  "name": "Standard Access Switch",
  "type": "device_config",
  "device_types": ["switch"],
  "configuration": {
    "system": {
      "hostname": "{{hostname}}",
      "domain": "{{domain}}",
      "dns_servers": ["{{dns_primary}}", "{{dns_secondary}}"]
    },
    "vlans": [
      {
        "id": "{{user_vlan}}",
        "name": "Users",
        "description": "User network"
      },
      {
        "id": "{{mgmt_vlan}}",
        "name": "Management",
        "description": "Management network"
      }
    ],
    "interfaces": [
      {
        "name": "GigabitEthernet0/1-24",
        "mode": "access",
        "vlan": "{{user_vlan}}",
        "port_security": true
      }
    ]
  },
  "variables": {
    "hostname": {
      "type": "string",
      "required": true,
      "description": "Device hostname"
    },
    "domain": {
      "type": "string",
      "default": "company.com",
      "description": "Domain name"
    },
    "user_vlan": {
      "type": "integer",
      "default": 10,
      "description": "User VLAN ID"
    },
    "mgmt_vlan": {
      "type": "integer",
      "default": 100,
      "description": "Management VLAN ID"
    }
  }
}
```

### Network Policy Template
```json
{
  "name": "Guest Network Policy",
  "type": "network_policy",
  "policy_rules": [
    {
      "name": "Guest Internet Access",
      "source": "guest_network",
      "destination": "internet",
      "action": "allow",
      "services": ["http", "https"]
    },
    {
      "name": "Block Internal Access",
      "source": "guest_network",
      "destination": "internal_networks",
      "action": "deny"
    }
  ],
  "enforcement_mode": "enforce",
  "variables": {
    "guest_network": {
      "type": "string",
      "default": "192.168.100.0/24",
      "description": "Guest network subnet"
    }
  }
}
```

### Security Profile Template
```json
{
  "name": "Corporate Security Profile",
  "type": "security_profile",
  "security_settings": {
    "authentication": {
      "method": "802.1X",
      "radius_servers": ["{{radius_primary}}", "{{radius_secondary}}"]
    },
    "authorization": {
      "user_roles": ["employee", "guest", "admin"],
      "default_role": "employee"
    },
    "encryption": {
      "wpa_version": "WPA3",
      "key_management": "PSK"
    }
  },
  "compliance_standards": ["SOC2", "ISO27001"],
  "variables": {
    "radius_primary": {
      "type": "string",
      "required": true,
      "description": "Primary RADIUS server"
    },
    "radius_secondary": {
      "type": "string",
      "required": true,
      "description": "Secondary RADIUS server"
    }
  }
}
```

## Error Handling

### Error Categories
1. **CLIENT_ERROR** (4xx) - Invalid request, no retry
2. **SERVER_ERROR** (5xx) - Server issues, retry recommended
3. **VALIDATION_ERROR** - Template validation failed
4. **DEPLOYMENT_ERROR** - Template deployment failed
5. **PERMISSION_ERROR** - Insufficient permissions

### Common Error Scenarios
- **Template Already Exists** (409) - Template name conflict
- **Template Not Found** (404) - Invalid template ID
- **Validation Failed** (422) - Template validation errors
- **Deployment Failed** (500) - Deployment to devices failed
- **Permission Denied** (403) - Insufficient API permissions

### Retry Logic
- **Automatic Retry**: Server errors (5xx) with exponential backoff
- **Manual Retry**: Client errors (4xx) require manual intervention
- **Retry Count**: Maximum 3 attempts with 2-second delays

## Performance Considerations

### Template Creation
- **Validation Time**: 10-30 seconds for complex templates
- **Batch Processing**: Process templates in batches of 10
- **Concurrent Limit**: Maximum 5 concurrent operations

### Template Deployment
- **Staged Deployment**: Deploy in batches to reduce impact
- **Batch Size**: Recommended 10 devices per batch
- **Delay Between Batches**: 30 seconds minimum
- **Rollback Time**: 5-10 minutes for large deployments

### Template Listing
- **Pagination**: Use limit/offset for large result sets
- **Filtering**: Apply filters to reduce response size
- **Caching**: Results cached for 10 minutes

## Security Features

### Access Control
- **Authentication**: OAuth 2.0 with proper scopes
- **Authorization**: Template-level permissions
- **Audit Trail**: All operations logged with user context

### Data Protection
- **Encryption**: Templates encrypted at rest
- **Backup Security**: Encrypted backups with retention policies
- **Variable Masking**: Sensitive variables masked in logs

### Compliance
- **Template Validation**: Enforced validation before deployment
- **Change Approval**: Optional approval workflows
- **Audit Logging**: Comprehensive audit trail

## Monitoring and Notifications

### Success Notifications
- **Slack**: Real-time notifications to configured channel
- **Email**: Summary notifications for completed operations
- **Webhook**: Custom webhook notifications

### Error Notifications
- **Immediate Alerts**: Critical errors sent immediately
- **Summary Reports**: Daily/weekly error summaries
- **Escalation**: Automatic escalation for repeated failures

### Metrics Tracking
- **Response Time**: API response time monitoring
- **Success Rate**: Operation success rate tracking
- **Template Usage**: Template deployment statistics

## Testing

### Quick Test Examples
```bash
# Create a test template
curl -X POST http://192.168.40.100:8006/webhook/central-template-management \\
  -H "Content-Type: application/json" \\
  -d '{
    "operation": "create_template",
    "template_data": {
      "name": "Test Template",
      "type": "device_config",
      "description": "Test template for validation",
      "configuration": {"test": "value"}
    }
  }'

# List templates
curl -X POST http://192.168.40.100:8006/webhook/central-template-management \\
  -H "Content-Type: application/json" \\
  -d '{
    "operation": "list_templates",
    "options": {"limit": 10}
  }'
```

## Troubleshooting

### Common Issues

#### Template Creation Fails
1. **Check**: Template name uniqueness
2. **Verify**: Required fields are provided
3. **Validate**: Template configuration syntax
4. **Confirm**: API credentials and permissions

#### Deployment Failures
1. **Check**: Target device connectivity
2. **Verify**: Template compatibility with devices
3. **Validate**: Variable values and overrides
4. **Confirm**: Device permissions and access

#### Validation Errors
1. **Review**: Template configuration syntax
2. **Check**: Variable definitions and types
3. **Verify**: Required fields are present
4. **Validate**: Device compatibility

### Support Resources
- **Workflow Logs**: Check n8n execution logs
- **API Documentation**: Aruba Central API reference
- **Template Examples**: Use provided templates as reference
- **Community Support**: HPE Aruba community forums

---

**Last Updated**: January 2025  
**Workflow Version**: 1.0.0  
**API Version**: v2
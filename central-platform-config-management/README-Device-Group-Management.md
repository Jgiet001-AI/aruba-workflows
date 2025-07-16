# Central Platform Device Group Management Workflow

## Overview
This workflow provides comprehensive device group management capabilities for the HPE Aruba Central Platform, enabling automated creation, management, and orchestration of device groups for efficient network administration.

## Workflow File
`central-platform-device-group-workflow.json`

## Capabilities

### Core Operations
1. **Create Group** - Create new device groups
2. **Update Group** - Modify existing groups
3. **Delete Group** - Remove device groups
4. **List Groups** - Retrieve and filter groups
5. **Add Devices** - Add devices to groups
6. **Remove Devices** - Remove devices from groups
7. **Move Devices** - Move devices between groups
8. **Group Status** - Check group status and health
9. **Group Inventory** - Get detailed group inventory
10. **Apply Configuration** - Deploy configurations to groups
11. **Sync Group** - Synchronize group membership
12. **Group Analytics** - Retrieve group analytics

### Group Types Supported
- **Static Groups** - Manual device membership
- **Dynamic Groups** - Rule-based automatic membership
- **Location-Based Groups** - Geographic organization
- **Template-Based Groups** - Template-driven configuration
- **Role-Based Groups** - Functional role grouping

## API Endpoint
```
POST /webhook/central-device-groups
```

## Request Format

### Basic Request Structure
```json
{
  "operation": "create_group",
  "group_data": {
    "group_name": "Group Name",
    "group_type": "static",
    "description": "Group description",
    "group_properties": {},
    "policies": {}
  },
  "options": {
    "notification_channels": ["slack"],
    "include_statistics": true
  }
}
```

### Operation-Specific Examples

#### 1. Create Static Device Group
```json
{
  "operation": "create_group",
  "group_data": {
    "group_name": "Branch Office Switches",
    "group_type": "static",
    "description": "All switches in branch offices",
    "device_ids": ["device_001", "device_002", "device_003"],
    "parent_group_id": "parent_group_123",
    "auto_add_rules": [
      {
        "attribute": "location",
        "operator": "starts_with",
        "value": "branch_"
      }
    ],
    "membership_locked": false,
    "group_properties": {
      "criticality": "high",
      "maintenance_window": "sunday_2am_6am",
      "contact": "network-team@company.com"
    },
    "policies": {
      "configuration": ["branch_switch_policy"],
      "security": ["standard_security_policy"],
      "monitoring": ["enhanced_monitoring"]
    },
    "permissions": {
      "read_users": ["all_users"],
      "write_users": ["network_admins"],
      "admin_users": ["senior_admins"],
      "inherit_parent": true
    }
  }
}
```

#### 2. Create Dynamic Device Group
```json
{
  "operation": "create_group",
  "group_data": {
    "group_name": "Critical Infrastructure",
    "group_type": "dynamic",
    "description": "Automatically includes all critical infrastructure devices",
    "membership_rules": [
      {
        "attribute": "device_type",
        "operator": "in",
        "value": ["switch", "controller"]
      },
      {
        "attribute": "tags",
        "operator": "contains",
        "value": "critical"
      },
      {
        "attribute": "firmware_version",
        "operator": "greater_than",
        "value": "10.0.0"
      }
    ],
    "rule_logic": "AND",
    "evaluation_frequency": "hourly",
    "auto_update": true,
    "automation": {
      "auto_provision": true,
      "auto_configure": true,
      "auto_monitor": true,
      "auto_remediate": false,
      "notification_settings": {
        "membership_changes": true,
        "health_alerts": true
      }
    }
  }
}
```

#### 3. Create Location-Based Group
```json
{
  "operation": "create_group",
  "group_data": {
    "group_name": "California Offices",
    "group_type": "location_based",
    "description": "All devices in California offices",
    "location_hierarchy": ["USA", "California"],
    "include_sublocations": true,
    "location_attributes": {
      "timezone": "America/Los_Angeles",
      "region_code": "US-CA"
    },
    "geo_boundaries": {
      "type": "polygon",
      "coordinates": [
        [-124.409591, 32.534156],
        [-114.131211, 32.534156],
        [-114.131211, 42.009518],
        [-124.409591, 42.009518]
      ]
    }
  }
}
```

#### 4. Add Devices to Group
```json
{
  "operation": "add_devices",
  "group_data": {
    "group_id": "group_123",
    "device_ids": [
      "switch_001",
      "switch_002",
      "ap_001",
      "ap_002"
    ],
    "operation_mode": "add",
    "validate_compatibility": true,
    "apply_group_config": true,
    "inherit_policies": true,
    "device_filters": {
      "device_types": ["switch", "ap"],
      "firmware_versions": ["10.08.*", "8.10.*"],
      "locations": ["building_a", "building_b"]
    },
    "batch_size": 50,
    "notify_device_owners": true
  }
}
```

#### 5. Apply Configuration to Group
```json
{
  "operation": "apply_configuration",
  "group_data": {
    "group_id": "group_123",
    "configuration_type": "template",
    "template_id": "branch_switch_template_v2",
    "template_version": "2.1.0",
    "variable_overrides": {
      "vlan_id": 100,
      "gateway_ip": "10.0.100.1",
      "dns_servers": ["8.8.8.8", "8.8.4.4"]
    },
    "application_mode": "staged",
    "schedule": {
      "start_time": "2025-01-20T02:00:00Z",
      "maintenance_window": 14400
    },
    "batch_size": 25,
    "batch_delay": 60,
    "rollback_enabled": true,
    "backup_before_apply": true,
    "pre_validation": true,
    "compliance_requirements": {
      "standards": ["company_baseline", "pci_dss"],
      "validation_required": true,
      "approval_required": false
    }
  }
}
```

#### 6. Move Devices Between Groups
```json
{
  "operation": "move_devices",
  "group_data": {
    "device_ids": ["device_001", "device_002", "device_003"],
    "source_group_id": "old_group_123",
    "target_group_id": "new_group_456",
    "preserve_config": true,
    "apply_target_policies": true,
    "remove_source_policies": false,
    "validate_move": true
  }
}
```

#### 7. Get Group Inventory
```json
{
  "operation": "group_inventory",
  "group_data": {
    "group_id": "group_123",
    "filters": {
      "device_status": ["online", "offline"],
      "device_types": ["switch", "ap"],
      "last_seen": "24h"
    }
  },
  "options": {
    "include_devices": true,
    "include_subgroups": true,
    "include_statistics": true,
    "include_health": true,
    "include_compliance": true,
    "device_fields": ["id", "name", "type", "status", "location", "firmware", "health_score"],
    "sort_by": "health_score",
    "sort_order": "desc"
  }
}
```

#### 8. Sync Group Membership
```json
{
  "operation": "sync_group",
  "group_data": {
    "group_id": "group_123",
    "sync_type": "full",
    "update_membership": true,
    "update_configuration": true,
    "update_policies": true,
    "force_sync": false
  }
}
```

#### 9. Group Analytics
```json
{
  "operation": "group_analytics",
  "group_data": {
    "group_id": "group_123",
    "metrics": ["device_count", "health_score", "compliance_rate", "uptime", "traffic_volume"],
    "time_range": "7d",
    "aggregation": "avg",
    "group_by": "day"
  }
}
```

## Response Format

### Success Response
```json
{
  "success": true,
  "operation": "create_group",
  "execution_id": "device-group-1705404123456-abc123def",
  "timestamp": "2025-01-16T10:30:00.000Z",
  "message": "Device group 'Branch Office Switches' created successfully",
  "group_id": "group_123",
  "group_name": "Branch Office Switches",
  "group_type": "static",
  "data": {
    "group_id": "group_123",
    "device_count": 25,
    "status": "active",
    "created_at": "2025-01-16T10:30:00.000Z"
  },
  "metrics": {
    "response_time": "1.8s",
    "api_calls": 1,
    "success_rate": "100%"
  }
}
```

### Error Response
```json
{
  "success": false,
  "operation": "add_devices",
  "execution_id": "device-group-1705404123456-abc123def",
  "timestamp": "2025-01-16T10:30:00.000Z",
  "error": {
    "code": "422",
    "message": "One or more devices are invalid or incompatible",
    "category": "CLIENT_ERROR",
    "retry_recommended": false,
    "details": {
      "invalid_devices": ["device_999"],
      "incompatible_devices": ["device_888"],
      "reason": "Devices not found or incompatible with group type"
    }
  }
}
```

## Group Configuration Details

### Static Group Configuration
```json
{
  "static_config": {
    "device_ids": ["array of device IDs"],
    "auto_add_rules": [
      {
        "attribute": "location|type|model|tag",
        "operator": "equals|contains|starts_with|regex",
        "value": "match value"
      }
    ],
    "membership_locked": false,
    "max_devices": 1000
  }
}
```

### Dynamic Group Rules
```json
{
  "dynamic_config": {
    "membership_rules": [
      {
        "attribute": "device_type",
        "operator": "equals",
        "value": "switch"
      },
      {
        "attribute": "firmware_version",
        "operator": "greater_than",
        "value": "10.0.0"
      },
      {
        "attribute": "health_score",
        "operator": "less_than",
        "value": 80
      },
      {
        "attribute": "last_seen",
        "operator": "within",
        "value": "24h"
      }
    ],
    "rule_logic": "AND|OR",
    "evaluation_frequency": "realtime|minute|hourly|daily",
    "auto_update": true
  }
}
```

### Location-Based Configuration
```json
{
  "location_config": {
    "location_hierarchy": ["Country", "State", "City", "Building"],
    "include_sublocations": true,
    "location_attributes": {
      "timezone": "string",
      "region_code": "string",
      "site_code": "string"
    },
    "geo_boundaries": {
      "type": "circle|polygon",
      "center": [longitude, latitude],
      "radius": "number (meters)",
      "coordinates": [[lon, lat], ...]
    }
  }
}
```

### Template-Based Configuration
```json
{
  "template_config": {
    "template_id": "string",
    "template_parameters": {
      "key": "value"
    },
    "auto_apply_template": true,
    "template_version": "latest|specific_version",
    "merge_strategy": "replace|merge|append"
  }
}
```

## Group Policies

### Configuration Policies
```json
{
  "configuration_policies": [
    {
      "policy_id": "config_policy_001",
      "policy_name": "Standard Switch Configuration",
      "apply_order": 1,
      "mandatory": true
    }
  ]
}
```

### Security Policies
```json
{
  "security_policies": [
    {
      "policy_id": "security_policy_001",
      "policy_name": "Enterprise Security Baseline",
      "enforcement_mode": "strict",
      "exceptions": []
    }
  ]
}
```

### Monitoring Policies
```json
{
  "monitoring_policies": [
    {
      "policy_id": "monitor_policy_001",
      "policy_name": "Enhanced Monitoring",
      "metrics": ["cpu", "memory", "interfaces", "errors"],
      "collection_interval": 60,
      "retention_days": 30
    }
  ]
}
```

## Automation Settings

### Auto-Provisioning
```json
{
  "auto_provision": {
    "enabled": true,
    "template_id": "provision_template_001",
    "naming_convention": "{location}_{type}_{index}",
    "ip_allocation": "dhcp|static",
    "vlan_assignment": "dynamic|static"
  }
}
```

### Auto-Configuration
```json
{
  "auto_configure": {
    "enabled": true,
    "trigger": "on_join|scheduled|manual",
    "configuration_source": "template|policy|custom",
    "validation_required": true,
    "rollback_on_failure": true
  }
}
```

### Auto-Remediation
```json
{
  "auto_remediate": {
    "enabled": false,
    "conditions": [
      {
        "metric": "health_score",
        "threshold": 70,
        "action": "restart_service"
      },
      {
        "metric": "config_drift",
        "threshold": 5,
        "action": "restore_config"
      }
    ],
    "approval_required": true
  }
}
```

## Group Analytics Response

### Analytics Data Structure
```json
{
  "group_id": "group_123",
  "time_range": "7d",
  "metrics": {
    "device_count": {
      "current": 150,
      "trend": "+5%",
      "history": [...]
    },
    "health_score": {
      "average": 95.5,
      "min": 78,
      "max": 100,
      "trend": "+2.3%"
    },
    "compliance_rate": {
      "percentage": 98.5,
      "compliant": 148,
      "non_compliant": 2
    },
    "uptime": {
      "average_percentage": 99.95,
      "total_downtime_minutes": 108
    },
    "traffic_volume": {
      "total_gb": 15420,
      "average_mbps": 245,
      "peak_mbps": 8750
    }
  }
}
```

## Error Handling

### Error Categories
1. **CLIENT_ERROR** (4xx) - Invalid request, no retry
2. **SERVER_ERROR** (5xx) - Server issues, retry recommended
3. **VALIDATION_ERROR** - Group or device validation failed
4. **PERMISSION_ERROR** - Insufficient permissions
5. **CAPACITY_ERROR** - Group capacity exceeded

### Common Error Scenarios
- **Group Already Exists** (409) - Group name conflict
- **Group Not Found** (404) - Invalid group ID
- **Invalid Devices** (422) - Device validation failed
- **Capacity Exceeded** (413) - Too many devices for group
- **Permission Denied** (403) - Insufficient permissions

### Retry Logic
- **Automatic Retry**: Server errors (5xx) with exponential backoff
- **Manual Retry**: Client errors (4xx) require correction
- **Retry Count**: Maximum 3 attempts with 2-second delays

## Performance Considerations

### Group Creation
- **Validation Time**: 2-5 seconds
- **Member Addition**: 100ms per device
- **Rule Evaluation**: 1-10 seconds for dynamic groups

### Device Operations
- **Batch Size**: 50-100 devices recommended
- **Processing Time**: 1-2 seconds per device
- **Concurrent Operations**: Maximum 5 per group

### Configuration Deployment
- **Deployment Time**: 30-60 seconds per device
- **Batch Processing**: 25 devices per batch
- **Rollback Time**: 2-5 minutes for full group

## Security Features

### Access Control
- **Authentication**: OAuth 2.0 with group scopes
- **Authorization**: Role-based group management
- **Audit Trail**: All operations logged

### Data Protection
- **Encryption**: Group data encrypted at rest
- **Secure Communication**: TLS 1.3 for API calls
- **Sensitive Data**: Masked in logs and responses

### Compliance
- **Policy Enforcement**: Mandatory policy compliance
- **Change Tracking**: Full audit trail
- **Approval Workflows**: Optional approval gates

## Best Practices

### Group Design
1. **Logical Organization**: Create meaningful group hierarchies
2. **Size Limits**: Keep groups under 1000 devices
3. **Clear Naming**: Use descriptive, consistent names
4. **Documentation**: Document group purposes and rules

### Dynamic Groups
1. **Simple Rules**: Keep membership rules simple
2. **Test Rules**: Validate rules before production
3. **Monitor Changes**: Track membership changes
4. **Performance**: Limit evaluation frequency

### Configuration Management
1. **Template Usage**: Use templates for consistency
2. **Staged Deployment**: Deploy in phases
3. **Validation**: Always validate before applying
4. **Backup**: Create backups before changes

## Testing

### Quick Test Examples
```bash
# Create a test group
curl -X POST http://192.168.40.100:8006/webhook/central-device-groups \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_group",
    "group_data": {
      "group_name": "Test Group",
      "group_type": "static",
      "device_ids": ["device_001"]
    }
  }'

# Add devices to group
curl -X POST http://192.168.40.100:8006/webhook/central-device-groups \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "add_devices",
    "group_data": {
      "group_id": "group_123",
      "device_ids": ["device_002", "device_003"]
    }
  }'

# Get group inventory
curl -X POST http://192.168.40.100:8006/webhook/central-device-groups \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "group_inventory",
    "group_data": {"group_id": "group_123"}
  }'
```

## Troubleshooting

### Common Issues

#### Group Creation Fails
1. **Check**: Group name uniqueness
2. **Verify**: Valid group type
3. **Validate**: Parent group exists
4. **Review**: Permission settings

#### Device Addition Issues
1. **Check**: Device existence
2. **Verify**: Device compatibility
3. **Review**: Group capacity
4. **Validate**: Device status

#### Configuration Failures
1. **Check**: Template validity
2. **Verify**: Device readiness
3. **Review**: Network connectivity
4. **Analyze**: Error logs

### Debug Mode
Enable debug logging:
```json
{
  "options": {
    "debug": true,
    "verbose_logging": true,
    "include_diagnostics": true
  }
}
```

### Support Resources
- **Group Templates**: Pre-built group configurations
- **Rule Builder**: Visual rule creation tool
- **API Documentation**: HPE Aruba Central API reference
- **Community Support**: HPE Aruba community forums

## Integration Examples

### With Policy Automation
```json
{
  "operation": "create_group",
  "group_data": {
    "group_name": "Policy-Managed Devices",
    "group_type": "dynamic",
    "membership_rules": [
      {
        "attribute": "applied_policies",
        "operator": "contains",
        "value": "security_policy_001"
      }
    ],
    "policies": {
      "configuration": ["policy_based_config"],
      "security": ["enhanced_security"]
    }
  }
}
```

### With Template Management
```json
{
  "operation": "apply_configuration",
  "group_data": {
    "group_id": "group_123",
    "configuration_type": "template",
    "template_id": "managed_template_001",
    "template_sync": {
      "auto_update": true,
      "version_tracking": true
    }
  }
}
```

### With Cloud Services
```json
{
  "operation": "create_group",
  "group_data": {
    "group_name": "Cloud-Monitored Devices",
    "group_type": "static",
    "automation": {
      "cloud_services": {
        "monitoring": "enabled",
        "analytics": "enabled",
        "backup": "daily"
      }
    }
  }
}
```

---

**Last Updated**: January 2025  
**Workflow Version**: 1.0.0  
**API Version**: v2
# Central Platform Policy and Rule Automation Workflow

## Overview
This workflow provides comprehensive policy and rule automation capabilities for the HPE Aruba Central Platform, enabling automated creation, deployment, validation, and compliance management of network policies.

## Workflow File
`central-platform-policy-automation-workflow.json`

## Capabilities

### Core Operations
1. **Create Policy** - Create new network policies
2. **Update Policy** - Modify existing policies
3. **Delete Policy** - Remove policies
4. **List Policies** - Retrieve and filter policies
5. **Apply Policy** - Deploy policies to devices/groups
6. **Validate Policy** - Validate policy configuration
7. **Policy Status** - Check policy deployment status
8. **Policy Compliance** - Monitor compliance status
9. **Policy Impact** - Analyze policy impact
10. **Bulk Policy Apply** - Deploy multiple policies
11. **Policy Rollback** - Rollback policy changes
12. **Policy Audit** - Audit policy history

### Policy Types Supported
- **Network Access Policies** - Access control and segmentation
- **QoS Policies** - Quality of Service configuration
- **Security Policies** - Threat prevention and protection
- **Compliance Policies** - Regulatory compliance rules
- **Traffic Policies** - Traffic management and optimization
- **User Policies** - User-based access and authorization

## API Endpoint
```
POST /webhook/central-policy-automation
```

## Request Format

### Basic Request Structure
```json
{
  "operation": "create_policy",
  "policy_data": {
    "policy_name": "Policy Name",
    "policy_type": "network_access",
    "description": "Policy description",
    "rules": [],
    "conditions": {},
    "actions": {}
  },
  "options": {
    "validation_required": true,
    "notification_channels": ["slack"]
  }
}
```

### Operation-Specific Examples

#### 1. Create Network Access Policy
```json
{
  "operation": "create_policy",
  "policy_data": {
    "policy_name": "Guest Network Access Policy",
    "policy_type": "network_access",
    "description": "Restrict guest network access to internet only",
    "version": "1.0.0",
    "enabled": true,
    "priority": 100,
    "source_networks": ["192.168.100.0/24"],
    "destination_networks": ["0.0.0.0/0"],
    "protocols": ["tcp", "udp"],
    "ports": ["80", "443", "53"],
    "action": "allow",
    "logging": true,
    "enforcement_mode": "enforce",
    "conditions": {
      "time_based": [
        {
          "days": ["mon", "tue", "wed", "thu", "fri"],
          "start_time": "08:00",
          "end_time": "18:00"
        }
      ],
      "location_based": [
        {
          "locations": ["building_a", "building_b"],
          "include": true
        }
      ]
    },
    "scope": {
      "device_types": ["switch", "ap"],
      "device_groups": ["guest_network_devices"]
    }
  }
}
```

#### 2. Create QoS Policy
```json
{
  "operation": "create_policy",
  "policy_data": {
    "policy_name": "Voice Priority QoS Policy",
    "policy_type": "qos_policy",
    "description": "Prioritize voice traffic across the network",
    "traffic_classes": [
      {
        "name": "voice",
        "priority": 7,
        "bandwidth_percent": 40,
        "dscp": "EF"
      },
      {
        "name": "video",
        "priority": 5,
        "bandwidth_percent": 30,
        "dscp": "AF41"
      },
      {
        "name": "data",
        "priority": 3,
        "bandwidth_percent": 20,
        "dscp": "AF21"
      },
      {
        "name": "default",
        "priority": 0,
        "bandwidth_percent": 10,
        "dscp": "BE"
      }
    ],
    "queue_configuration": {
      "queuing_method": "weighted_fair",
      "congestion_avoidance": "wred"
    }
  }
}
```

#### 3. Create Security Policy
```json
{
  "operation": "create_policy",
  "policy_data": {
    "policy_name": "Advanced Threat Protection Policy",
    "policy_type": "security_policy",
    "description": "Comprehensive security policy for threat protection",
    "threat_prevention": "enabled",
    "intrusion_detection": "enabled",
    "malware_protection": "enabled",
    "url_filtering": {
      "enabled": true,
      "block_categories": ["malware", "phishing", "gambling", "social_media"],
      "allow_list": ["company.com", "trusted-partner.com"],
      "block_list": ["malicious-site.com"]
    },
    "application_control": {
      "enabled": true,
      "block_applications": ["bittorrent", "tor", "gaming"],
      "bandwidth_limit_applications": {
        "streaming": "10mbps",
        "file_sharing": "5mbps"
      }
    },
    "incident_response": {
      "auto_block": true,
      "block_duration": 3600,
      "notify_soc": true
    }
  }
}
```

#### 4. Apply Policy to Devices
```json
{
  "operation": "apply_policy",
  "policy_data": {
    "policy_id": "policy_123",
    "target_devices": ["device_001", "device_002", "device_003"],
    "target_groups": ["branch_offices", "data_centers"],
    "application_mode": "staged",
    "batch_size": 25,
    "batch_delay": 60,
    "rollback_enabled": true,
    "validation_required": true,
    "test_mode": false,
    "schedule": {
      "start_time": "2025-01-20T02:00:00Z",
      "maintenance_window": 14400
    },
    "variable_overrides": {
      "bandwidth_limit": "100mbps",
      "location": "us-west"
    },
    "compliance_check": {
      "pre_check": true,
      "post_check": true,
      "remediation_enabled": true
    }
  }
}
```

#### 5. Validate Policy
```json
{
  "operation": "validate_policy",
  "policy_data": {
    "policy_id": "policy_123",
    "validation_type": "full",
    "syntax_check": true,
    "logic_check": true,
    "conflict_check": true,
    "dependency_check": true,
    "performance_check": true,
    "target_device_types": ["switch", "ap"],
    "simulation_mode": true
  },
  "options": {
    "detailed_report": true,
    "include_recommendations": true,
    "check_best_practices": true
  }
}
```

#### 6. Check Policy Compliance
```json
{
  "operation": "policy_compliance",
  "policy_data": {
    "policy_id": "policy_123",
    "device_ids": ["device_001", "device_002"],
    "device_groups": ["critical_infrastructure"],
    "check_type": "full",
    "include_drift_analysis": true,
    "generate_remediation": true,
    "severity_threshold": "medium",
    "compliance_standards": ["PCI-DSS", "HIPAA"],
    "time_range": {
      "start_time": "2025-01-01T00:00:00Z",
      "end_time": "2025-01-16T23:59:59Z"
    }
  },
  "options": {
    "report_format": "json",
    "include_details": true,
    "group_by": "device"
  }
}
```

#### 7. Policy Impact Analysis
```json
{
  "operation": "policy_impact",
  "policy_data": {
    "policy_id": "policy_123",
    "analysis_type": "full",
    "target_devices": ["device_001", "device_002"],
    "target_groups": ["production_network"],
    "simulation_duration": 7200,
    "traffic_profile": "peak_hours",
    "include_performance": true
  }
}
```

#### 8. Bulk Policy Application
```json
{
  "operation": "bulk_policy_apply",
  "policy_data": {
    "policy_applications": [
      {
        "policy_id": "security_policy_001",
        "target_groups": ["dmz_devices"],
        "priority": 1
      },
      {
        "policy_id": "qos_policy_002",
        "target_groups": ["voice_devices"],
        "priority": 2
      },
      {
        "policy_id": "access_policy_003",
        "target_devices": ["switch_001", "switch_002"],
        "priority": 3
      }
    ],
    "global_mode": "sequential",
    "rollback_on_failure": true
  },
  "options": {
    "notification_settings": {
      "notify_on_start": true,
      "notify_on_completion": true,
      "channels": ["slack", "email"]
    }
  }
}
```

#### 9. Policy Rollback
```json
{
  "operation": "policy_rollback",
  "policy_data": {
    "policy_id": "policy_123",
    "rollback_version": "1.2.0",
    "target_devices": ["device_001", "device_002"],
    "immediate_rollback": true,
    "preserve_data": true
  }
}
```

## Response Format

### Success Response
```json
{
  "success": true,
  "operation": "create_policy",
  "execution_id": "policy-1705404123456-abc123def",
  "timestamp": "2025-01-16T10:30:00.000Z",
  "message": "Policy 'Guest Network Access Policy' created successfully",
  "policy_id": "policy_123",
  "policy_name": "Guest Network Access Policy",
  "policy_type": "network_access",
  "data": {
    "policy_id": "policy_123",
    "version": "1.0.0",
    "status": "active",
    "created_at": "2025-01-16T10:30:00.000Z"
  },
  "metrics": {
    "response_time": "2.8s",
    "api_calls": 1,
    "success_rate": "100%"
  }
}
```

### Error Response
```json
{
  "success": false,
  "operation": "apply_policy",
  "execution_id": "policy-1705404123456-abc123def",
  "timestamp": "2025-01-16T10:30:00.000Z",
  "error": {
    "code": "422",
    "message": "Policy validation failed - cannot apply",
    "category": "CLIENT_ERROR",
    "retry_recommended": false,
    "details": {
      "validation_errors": [
        "Conflicting rule detected with existing policy",
        "Invalid port range specified"
      ]
    }
  }
}
```

## Policy Configuration Examples

### Network Access Policy Rules
```json
{
  "rules": [
    {
      "rule_id": "rule_001",
      "name": "Allow Web Traffic",
      "source": {
        "networks": ["10.0.0.0/8"],
        "ports": ["any"],
        "users": ["guest_users"]
      },
      "destination": {
        "networks": ["0.0.0.0/0"],
        "ports": ["80", "443"],
        "services": ["http", "https"]
      },
      "action": "allow",
      "logging": true,
      "enabled": true
    },
    {
      "rule_id": "rule_002",
      "name": "Block Internal Access",
      "source": {
        "networks": ["10.0.0.0/8"]
      },
      "destination": {
        "networks": ["192.168.0.0/16", "172.16.0.0/12"]
      },
      "action": "deny",
      "logging": true,
      "enabled": true
    }
  ]
}
```

### QoS Policy Configuration
```json
{
  "qos_rules": {
    "classification": [
      {
        "match": {
          "dscp": "EF",
          "protocol": "udp",
          "ports": ["5060-5061", "16384-32768"]
        },
        "mark": {
          "dscp": "EF",
          "cos": 5
        },
        "queue": "priority"
      }
    ],
    "queuing": {
      "method": "weighted_fair_queuing",
      "queues": [
        {
          "name": "priority",
          "weight": 40,
          "buffer_size": "large"
        },
        {
          "name": "normal",
          "weight": 40,
          "buffer_size": "medium"
        },
        {
          "name": "bulk",
          "weight": 20,
          "buffer_size": "small"
        }
      ]
    },
    "policing": {
      "ingress_rate": "1gbps",
      "egress_rate": "1gbps",
      "burst_size": "128kb"
    }
  }
}
```

### Security Policy Rules
```json
{
  "security_rules": [
    {
      "rule_type": "ips",
      "signatures": ["malware", "exploit", "dos"],
      "action": "block",
      "severity": ["critical", "high"],
      "log": true
    },
    {
      "rule_type": "antivirus",
      "scan_types": ["http", "https", "ftp", "smtp"],
      "action": "clean",
      "quarantine": true
    },
    {
      "rule_type": "url_filter",
      "categories": ["malware", "phishing"],
      "action": "block",
      "redirect_url": "https://blocked.company.com"
    }
  ]
}
```

## Policy Conditions

### Time-Based Conditions
```json
{
  "time_based": [
    {
      "name": "Business Hours",
      "days": ["mon", "tue", "wed", "thu", "fri"],
      "start_time": "08:00",
      "end_time": "18:00",
      "timezone": "America/Los_Angeles"
    },
    {
      "name": "Maintenance Window",
      "days": ["sun"],
      "start_time": "02:00",
      "end_time": "06:00",
      "timezone": "UTC"
    }
  ]
}
```

### Location-Based Conditions
```json
{
  "location_based": [
    {
      "name": "Corporate Offices",
      "locations": ["hq", "branch_1", "branch_2"],
      "include": true
    },
    {
      "name": "Public Areas",
      "locations": ["lobby", "cafeteria"],
      "include": false
    }
  ]
}
```

### Device-Based Conditions
```json
{
  "device_based": [
    {
      "device_types": ["switch", "ap"],
      "models": ["CX6300", "AP-515"],
      "firmware_versions": ["10.08.*", "8.10.*"],
      "include": true
    }
  ]
}
```

## Compliance Reporting

### Compliance Status Response
```json
{
  "compliance_status": "partial",
  "compliance_percentage": 85.5,
  "compliant_devices": 171,
  "non_compliant_devices": 29,
  "total_devices": 200,
  "violations": [
    {
      "device_id": "device_001",
      "violation_type": "configuration_drift",
      "severity": "high",
      "details": "ACL rule missing",
      "remediation": {
        "action": "apply_rule",
        "command": "access-list 100 permit tcp any any eq 443"
      }
    }
  ],
  "compliance_by_standard": {
    "PCI-DSS": 92.0,
    "HIPAA": 88.5,
    "ISO27001": 90.0
  }
}
```

## Error Handling

### Error Categories
1. **CLIENT_ERROR** (4xx) - Invalid request, no retry
2. **SERVER_ERROR** (5xx) - Server issues, retry recommended
3. **VALIDATION_ERROR** - Policy validation failed
4. **CONFLICT_ERROR** - Policy conflicts detected
5. **COMPLIANCE_ERROR** - Compliance check failed

### Common Error Scenarios
- **Policy Already Exists** (409) - Policy name conflict
- **Policy Not Found** (404) - Invalid policy ID
- **Validation Failed** (422) - Policy rules invalid
- **Application Conflict** (409) - Another policy being applied
- **Permission Denied** (403) - Insufficient permissions

### Retry Logic
- **Automatic Retry**: Server errors (5xx) with exponential backoff
- **Manual Retry**: Client errors (4xx) require correction
- **Retry Count**: Maximum 3 attempts with 3-second delays

## Performance Considerations

### Policy Creation
- **Validation Time**: 5-15 seconds for complex policies
- **Rule Limit**: Maximum 1000 rules per policy
- **Concurrent Creation**: Maximum 10 policies

### Policy Application
- **Deployment Time**: 30-60 seconds per device
- **Batch Processing**: 25-50 devices per batch recommended
- **Rollback Time**: 2-5 minutes for full rollback

### Compliance Checking
- **Check Duration**: 1-2 minutes per 100 devices
- **Report Generation**: 10-30 seconds
- **Historical Analysis**: Limited to 90 days

## Security Features

### Access Control
- **Authentication**: OAuth 2.0 with policy scopes
- **Authorization**: Role-based policy management
- **Audit Trail**: All policy operations logged

### Policy Protection
- **Version Control**: Automatic versioning
- **Change Approval**: Optional approval workflow
- **Rollback Protection**: Previous versions preserved

### Compliance
- **Standards Support**: PCI-DSS, HIPAA, ISO27001
- **Audit Logging**: Comprehensive audit trail
- **Change Tracking**: Full change history

## Best Practices

### Policy Design
1. **Start Simple**: Begin with basic rules
2. **Test First**: Always validate before applying
3. **Use Templates**: Leverage policy templates
4. **Document Rules**: Clear descriptions for all rules

### Deployment Strategy
1. **Staged Rollout**: Deploy in phases
2. **Test Groups**: Use pilot groups first
3. **Maintenance Windows**: Schedule during low impact times
4. **Monitor Impact**: Watch performance metrics

### Compliance Management
1. **Regular Checks**: Schedule daily compliance scans
2. **Automated Remediation**: Enable for low-risk violations
3. **Exception Handling**: Document approved exceptions
4. **Trend Analysis**: Monitor compliance trends

## Testing

### Quick Test Examples
```bash
# Create a test policy
curl -X POST http://192.168.40.100:8006/webhook/central-policy-automation \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_policy",
    "policy_data": {
      "policy_name": "Test Access Policy",
      "policy_type": "network_access",
      "source_networks": ["10.0.0.0/24"],
      "destination_networks": ["0.0.0.0/0"],
      "action": "allow"
    }
  }'

# Validate policy
curl -X POST http://192.168.40.100:8006/webhook/central-policy-automation \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "validate_policy",
    "policy_data": {
      "policy_id": "policy_123",
      "validation_type": "full"
    }
  }'

# Check compliance
curl -X POST http://192.168.40.100:8006/webhook/central-policy-automation \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "policy_compliance",
    "policy_data": {
      "policy_id": "policy_123",
      "check_all": true
    }
  }'
```

## Troubleshooting

### Common Issues

#### Policy Creation Fails
1. **Check**: Policy name uniqueness
2. **Verify**: Rule syntax and structure
3. **Validate**: Required fields present
4. **Review**: Policy type compatibility

#### Application Failures
1. **Check**: Target device connectivity
2. **Verify**: Policy compatibility
3. **Review**: Conflicting policies
4. **Validate**: Device capabilities

#### Compliance Issues
1. **Review**: Policy requirements
2. **Check**: Device configurations
3. **Verify**: Measurement accuracy
4. **Analyze**: Violation patterns

### Debug Mode
Enable debug logging:
```json
{
  "options": {
    "debug": true,
    "verbose_logging": true,
    "trace_enabled": true
  }
}
```

### Support Resources
- **Policy Library**: Pre-built policy templates
- **Validation Tools**: Online policy validator
- **API Documentation**: HPE Aruba Central API reference
- **Community Support**: HPE Aruba community forums

## Integration Examples

### With Template Management
```json
{
  "operation": "create_policy",
  "policy_data": {
    "policy_name": "From Template Policy",
    "template_id": "security_template_001",
    "variable_overrides": {
      "allowed_networks": ["10.0.0.0/8"],
      "blocked_sites": ["malicious.com"]
    }
  }
}
```

### With Device Groups
```json
{
  "operation": "apply_policy",
  "policy_data": {
    "policy_id": "policy_123",
    "target_groups": ["group_001", "group_002"],
    "group_filter": {
      "location": "us-west",
      "device_type": "switch"
    }
  }
}
```

### With Cloud Services
```json
{
  "operation": "create_policy",
  "policy_data": {
    "policy_name": "Cloud Service Integration Policy",
    "policy_type": "security_policy",
    "cloud_service_integration": {
      "threat_intelligence": "enabled",
      "reputation_service": "enabled",
      "sandbox_analysis": "enabled"
    }
  }
}
```

---

**Last Updated**: January 2025  
**Workflow Version**: 1.0.0  
**API Version**: v2
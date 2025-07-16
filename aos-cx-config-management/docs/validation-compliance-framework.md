# AOS-CX Validation & Compliance Framework

## Overview
Comprehensive validation and compliance checking framework for AOS-CX configuration management. This framework ensures all configurations meet organizational standards, security requirements, and best practices before deployment.

## Validation Layers

### 1. Input Parameter Validation
**Purpose**: Validate all workflow inputs before processing
**Scope**: VLAN IDs, interface names, IP addresses, policy rules
**Implementation**: Pre-execution validation nodes in all workflows

#### VLAN Validation Rules
```json
{
  "vlan_id": {
    "type": "integer",
    "minimum": 1,
    "maximum": 4094,
    "excluded_ranges": [[1, 1], [4094, 4094]],
    "reserved_vlans": [1, 1002, 1003, 1004, 1005, 4094]
  },
  "vlan_name": {
    "type": "string",
    "pattern": "^[A-Za-z0-9_-]{1,32}$",
    "forbidden_names": ["default", "management", "reserved"]
  },
  "description": {
    "type": "string",
    "max_length": 255,
    "required": false
  }
}
```

#### Interface Validation Rules
```json
{
  "interface_name": {
    "patterns": [
      "^\\d+/\\d+/\\d+$",     // Physical: 1/1/1
      "^lag\\d+$",           // LAG: lag1
      "^vlan\\d+$"           // VLAN: vlan100
    ]
  },
  "admin_state": {
    "enum": ["up", "down"]
  },
  "speed": {
    "enum": ["auto", "10", "100", "1000", "10000", "25000", "40000", "100000"]
  },
  "duplex": {
    "enum": ["auto", "half", "full"]
  }
}
```

#### Policy Validation Rules
```json
{
  "acl_name": {
    "type": "string",
    "pattern": "^[A-Za-z0-9_-]{1,64}$",
    "case_sensitive": false
  },
  "acl_rules": {
    "sequence_number": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2147483647
    },
    "action": {
      "enum": ["permit", "deny"]
    },
    "protocol": {
      "enum": ["tcp", "udp", "icmp", "any", "esp", "gre"]
    }
  }
}
```

### 2. Configuration Syntax Validation
**Purpose**: Ensure configurations are syntactically correct for AOS-CX
**Scope**: JSON payloads, API request structure, parameter combinations
**Implementation**: JSON schema validation and AOS-CX specific rules

#### API Request Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "operation": {
      "type": "string",
      "enum": ["create", "read", "update", "delete", "list"]
    },
    "switch_ip": {
      "type": "string",
      "pattern": "^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$"
    },
    "vlan_id": {
      "type": "integer",
      "minimum": 1,
      "maximum": 4094
    }
  },
  "required": ["operation", "switch_ip"]
}
```

### 3. Business Logic Validation
**Purpose**: Enforce organizational policies and standards
**Scope**: VLAN assignments, security policies, resource limits
**Implementation**: Custom validation functions and rule engines

#### Organizational Policies
```json
{
  "vlan_policies": {
    "user_vlans": {
      "range": [100, 199],
      "naming_convention": "USER_*",
      "description_required": true
    },
    "server_vlans": {
      "range": [200, 299],
      "naming_convention": "SRV_*",
      "security_required": true
    },
    "iot_vlans": {
      "range": [300, 399], 
      "naming_convention": "IOT_*",
      "isolation_required": true
    }
  },
  "interface_policies": {
    "access_ports": {
      "port_security_required": true,
      "max_mac_addresses": 2,
      "dhcp_snooping_required": true
    },
    "trunk_ports": {
      "native_vlan_allowed": [1, 999],
      "max_vlans_per_trunk": 50
    }
  }
}
```

### 4. Security Compliance Validation
**Purpose**: Ensure configurations meet security standards
**Scope**: ACL policies, port security, access controls
**Implementation**: Security rule validation and threat assessment

#### Security Requirements
```json
{
  "security_standards": {
    "password_policies": {
      "min_length": 12,
      "complexity_required": true,
      "expiry_days": 90
    },
    "access_control": {
      "default_deny": true,
      "explicit_permits_required": true,
      "logging_required": true
    },
    "port_security": {
      "required_on_access_ports": true,
      "violation_action": "shutdown",
      "recovery_method": "manual"
    }
  },
  "compliance_frameworks": [
    "SOX", "PCI-DSS", "NIST", "ISO27001"
  ]
}
```

## Compliance Checks

### 1. Configuration Drift Detection
**Purpose**: Identify deviations from approved baselines
**Method**: Compare current configuration against golden templates
**Frequency**: Daily automated checks

```javascript
const driftCheck = {
  baseline_configs: {
    "switch_template_v1": "path/to/baseline.json",
    "security_template_v2": "path/to/security_baseline.json"
  },
  drift_tolerance: {
    "description_changes": "allowed",
    "vlan_additions": "review_required", 
    "security_changes": "forbidden"
  },
  remediation: {
    "auto_fix": ["description", "minor_config"],
    "manual_review": ["vlan_changes", "interface_changes"],
    "immediate_alert": ["security_changes", "acl_modifications"]
  }
};
```

### 2. Policy Compliance Verification
**Purpose**: Verify all configurations comply with organizational policies
**Method**: Rule-based validation against policy database
**Scope**: VLAN assignments, interface configurations, security policies

```javascript
const complianceRules = [
  {
    "rule_id": "VLAN001",
    "description": "VLANs must follow naming convention",
    "condition": "vlan_name.match(/^[A-Z]+_[A-Z0-9_]+$/)",
    "severity": "error",
    "remediation": "Update VLAN name to match ORG_NAME format"
  },
  {
    "rule_id": "INTF001", 
    "description": "Access ports must have port security",
    "condition": "interface.vlan_mode === 'access' && interface.port_security.enable === true",
    "severity": "warning",
    "remediation": "Enable port security on access ports"
  },
  {
    "rule_id": "SEC001",
    "description": "Default deny rule required in ACLs",
    "condition": "acl.rules.some(rule => rule.action === 'deny' && rule.protocol === 'any')",
    "severity": "critical",
    "remediation": "Add explicit deny-all rule at end of ACL"
  }
];
```

### 3. Performance Impact Assessment
**Purpose**: Evaluate configuration changes for performance impact
**Method**: Resource utilization analysis and capacity planning
**Metrics**: CPU, memory, bandwidth, table utilization

```json
{
  "performance_thresholds": {
    "cpu_utilization": {
      "warning": 70,
      "critical": 85
    },
    "memory_utilization": {
      "warning": 80,
      "critical": 90
    },
    "vlan_table_usage": {
      "warning": 75,
      "critical": 90
    },
    "acl_entries": {
      "warning": 1000,
      "critical": 1500
    }
  }
}
```

## Validation Workflows

### 1. Pre-deployment Validation
**Trigger**: Before any configuration change
**Process**:
1. Input parameter validation
2. Syntax validation
3. Business logic validation
4. Security compliance check
5. Performance impact assessment
6. Approval workflow (if required)

### 2. Post-deployment Verification
**Trigger**: After configuration application
**Process**:
1. Configuration readback verification
2. Connectivity testing
3. Performance monitoring
4. Compliance re-verification
5. Documentation update

### 3. Continuous Compliance Monitoring
**Trigger**: Scheduled (daily/weekly)
**Process**:
1. Configuration drift detection
2. Policy compliance audit
3. Security posture assessment
4. Performance trend analysis
5. Remediation planning

## Validation Implementation

### 1. Validation Functions
```javascript
// VLAN validation function
function validateVlan(vlanData) {
  const errors = [];
  
  // ID validation
  if (!vlanData.id || vlanData.id < 1 || vlanData.id > 4094) {
    errors.push("VLAN ID must be between 1 and 4094");
  }
  
  // Reserved VLAN check
  const reservedVlans = [1, 1002, 1003, 1004, 1005, 4094];
  if (reservedVlans.includes(vlanData.id)) {
    errors.push(`VLAN ${vlanData.id} is reserved and cannot be modified`);
  }
  
  // Name validation
  if (!vlanData.name || !/^[A-Za-z0-9_-]{1,32}$/.test(vlanData.name)) {
    errors.push("VLAN name must be 1-32 characters, alphanumeric with _ and -");
  }
  
  return errors;
}

// Interface validation function
function validateInterface(interfaceData) {
  const errors = [];
  
  // Interface name format
  const validPatterns = [
    /^\d+\/\d+\/\d+$/,  // Physical ports
    /^lag\d+$/,         // LAG interfaces
    /^vlan\d+$/         // VLAN interfaces
  ];
  
  if (!validPatterns.some(pattern => pattern.test(interfaceData.name))) {
    errors.push("Invalid interface name format");
  }
  
  // VLAN mode validation
  if (interfaceData.vlan_mode === 'access' && !interfaceData.vlan_tag) {
    errors.push("Access mode requires vlan_tag parameter");
  }
  
  if (interfaceData.vlan_mode === 'trunk' && !interfaceData.vlan_trunks) {
    errors.push("Trunk mode requires vlan_trunks parameter");
  }
  
  return errors;
}
```

### 2. Compliance Checking Engine
```javascript
class ComplianceChecker {
  constructor(rules) {
    this.rules = rules;
  }
  
  checkCompliance(configuration) {
    const results = {
      compliant: true,
      violations: [],
      warnings: []
    };
    
    for (const rule of this.rules) {
      try {
        const isCompliant = this.evaluateRule(rule, configuration);
        if (!isCompliant) {
          const violation = {
            rule_id: rule.rule_id,
            description: rule.description,
            severity: rule.severity,
            remediation: rule.remediation
          };
          
          if (rule.severity === 'critical' || rule.severity === 'error') {
            results.violations.push(violation);
            results.compliant = false;
          } else {
            results.warnings.push(violation);
          }
        }
      } catch (error) {
        console.error(`Error evaluating rule ${rule.rule_id}:`, error);
      }
    }
    
    return results;
  }
  
  evaluateRule(rule, configuration) {
    // Evaluate rule condition against configuration
    return eval(rule.condition);
  }
}
```

## Reporting and Documentation

### 1. Validation Reports
```json
{
  "validation_report": {
    "timestamp": "2025-01-16T10:30:00Z",
    "switch_ip": "192.168.1.100",
    "operation": "vlan_create",
    "validation_results": {
      "input_validation": {
        "status": "passed",
        "errors": []
      },
      "syntax_validation": {
        "status": "passed", 
        "errors": []
      },
      "compliance_check": {
        "status": "failed",
        "violations": [
          {
            "rule_id": "VLAN001",
            "severity": "error",
            "message": "VLAN name does not follow naming convention"
          }
        ]
      }
    },
    "overall_status": "failed",
    "deployment_approved": false
  }
}
```

### 2. Compliance Dashboard
- **Compliance Score**: Overall organizational compliance percentage
- **Violation Trends**: Historical compliance violation patterns
- **Risk Assessment**: Security and operational risk metrics
- **Remediation Tracking**: Progress on fixing compliance issues

### 3. Audit Trail
```json
{
  "audit_entry": {
    "timestamp": "2025-01-16T10:30:00Z",
    "user": "network-automation",
    "operation": "vlan_create",
    "switch_ip": "192.168.1.100",
    "parameters": {
      "vlan_id": 150,
      "vlan_name": "USER_SALES"
    },
    "validation_status": "passed",
    "compliance_status": "compliant", 
    "deployment_status": "successful",
    "change_id": "CHG001234"
  }
}
```

## Testing Validation Framework

### 1. Unit Tests for Validation Functions
```bash
# Test VLAN validation
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-validate" \
  -H "Content-Type: application/json" \
  -d '{
    "test_type": "vlan_validation",
    "test_cases": [
      {"vlan_id": 0, "expected": "fail"},
      {"vlan_id": 150, "vlan_name": "TEST_VLAN", "expected": "pass"},
      {"vlan_id": 4095, "expected": "fail"}
    ]
  }'

# Test compliance rules
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-validate" \
  -H "Content-Type: application/json" \
  -d '{
    "test_type": "compliance_check",
    "configuration": {
      "vlans": [{"id": 100, "name": "invalid_name"}]
    }
  }'
```

### 2. Integration Tests
```bash
# End-to-end validation test
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-test" \
  -H "Content-Type: application/json" \
  -d '{
    "test_scenario": "full_validation_workflow",
    "operations": [
      {"type": "vlan_create", "validation_required": true},
      {"type": "interface_config", "compliance_check": true},
      {"type": "policy_deploy", "security_validation": true}
    ]
  }'
```

This comprehensive validation and compliance framework ensures all AOS-CX configurations meet organizational standards and security requirements while maintaining operational efficiency and auditability.
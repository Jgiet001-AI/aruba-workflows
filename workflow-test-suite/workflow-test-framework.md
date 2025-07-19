# n8n Workflow Test Framework

## Overview
Comprehensive testing framework for Aruba n8n workflows ensuring reliability, security, and performance.

## Test Categories

### 1. Unit Tests (Individual Node Testing)

#### Input Validation Tests
```json
{
  "test_name": "validate_device_id_input",
  "description": "Test device ID validation in input nodes",
  "test_cases": [
    {
      "input": { "device_id": "AP-12345" },
      "expected": "valid",
      "notes": "Valid device ID format"
    },
    {
      "input": { "device_id": "invalid device" },
      "expected": "error",
      "error_message": "Invalid device_id format",
      "notes": "Should reject spaces in device ID"
    },
    {
      "input": { "device_id": "" },
      "expected": "error",
      "error_message": "Missing required field: device_id",
      "notes": "Should reject empty device ID"
    },
    {
      "input": { "device_id": "x".repeat(51) },
      "expected": "error",
      "error_message": "device_id too long",
      "notes": "Should reject overly long device IDs"
    }
  ]
}
```

#### API Request Tests
```json
{
  "test_name": "aruba_api_authentication",
  "description": "Test Aruba API authentication and request formation",
  "test_cases": [
    {
      "scenario": "valid_credentials",
      "mock_response": {
        "status": 200,
        "body": { "access_token": "valid_token" }
      },
      "expected": "success"
    },
    {
      "scenario": "invalid_credentials",
      "mock_response": {
        "status": 401,
        "body": { "error": "unauthorized" }
      },
      "expected": "error",
      "error_handling": "should_retry_with_backoff"
    },
    {
      "scenario": "rate_limited",
      "mock_response": {
        "status": 429,
        "headers": { "Retry-After": "60" }
      },
      "expected": "retry",
      "retry_delay": 60
    }
  ]
}
```

### 2. Integration Tests (Workflow End-to-End)

#### Device Health Monitoring Workflow
```json
{
  "workflow_name": "device-health-monitor-enhanced",
  "test_scenarios": [
    {
      "scenario": "healthy_devices",
      "description": "Test workflow with all healthy devices",
      "input": {
        "device_filter": "all",
        "cpu_critical": 90,
        "memory_critical": 95
      },
      "mock_api_response": {
        "devices": [
          {
            "serial": "AP-12345",
            "name": "Office-AP-01",
            "cpu_usage": 45,
            "memory_usage": 60,
            "temperature": 35,
            "status": "online"
          }
        ]
      },
      "expected_outputs": {
        "total_devices": 1,
        "healthy_devices": 1,
        "warning_devices": 0,
        "critical_devices": 0,
        "total_alerts": 0,
        "notification_sent": "success"
      },
      "expected_notifications": {
        "slack_channel": "#device-health-monitoring",
        "message_contains": "All devices healthy"
      }
    },
    {
      "scenario": "critical_cpu_usage",
      "description": "Test workflow with critical CPU usage",
      "input": {
        "device_filter": "aps",
        "cpu_critical": 85,
        "memory_critical": 90
      },
      "mock_api_response": {
        "devices": [
          {
            "serial": "AP-67890",
            "name": "Warehouse-AP-02",
            "cpu_usage": 92,
            "memory_usage": 75,
            "temperature": 45,
            "status": "online"
          }
        ]
      },
      "expected_outputs": {
        "total_devices": 1,
        "healthy_devices": 0,
        "warning_devices": 0,
        "critical_devices": 1,
        "total_alerts": 1,
        "notification_sent": "alert"
      },
      "expected_notifications": {
        "slack_channel": "#device-health-alerts",
        "message_contains": "CPU usage critical: 92.0%"
      }
    }
  ]
}
```

#### Security Event Response Workflow
```json
{
  "workflow_name": "security-event-response-enhanced",
  "test_scenarios": [
    {
      "scenario": "critical_malware_detection",
      "description": "Test critical malware threat response",
      "input": {
        "event_id": "SEC-001-2024",
        "threat_type": "malware",
        "severity": "critical",
        "device_id": "SW-12345",
        "confidence_score": 0.95,
        "source_ip": "192.168.1.100"
      },
      "expected_threat_score": 95,
      "expected_actions": {
        "isolation_required": true,
        "soc_escalation": true,
        "auto_response_enabled": true
      },
      "expected_api_calls": [
        {
          "endpoint": "/api/v2/security/isolate",
          "method": "POST",
          "body_contains": {
            "device_id": "SW-12345",
            "action": "isolate",
            "rollback_timer": 3600
          }
        }
      ],
      "expected_notifications": {
        "slack_channel": "#soc-alerts",
        "message_contains": "CRITICAL SECURITY EVENT"
      }
    },
    {
      "scenario": "medium_policy_violation",
      "description": "Test medium severity policy violation",
      "input": {
        "event_id": "SEC-002-2024",
        "threat_type": "policy_violation",
        "severity": "medium",
        "device_id": "AP-54321",
        "confidence_score": 0.8
      },
      "expected_threat_score": 40,
      "expected_actions": {
        "isolation_required": false,
        "log_only": true,
        "enhanced_monitoring": false
      },
      "expected_outputs": {
        "response_type": "medium_analyzed",
        "actions_taken": ["threat_analysis_initiated", "trend_analysis_queued"]
      }
    }
  ]
}
```

### 3. Performance Tests

#### Load Testing Configuration
```json
{
  "performance_tests": [
    {
      "test_name": "concurrent_webhook_requests",
      "description": "Test workflow performance under load",
      "configuration": {
        "concurrent_requests": 50,
        "duration_seconds": 300,
        "ramp_up_time": 60
      },
      "test_data": {
        "request_template": {
          "device_filter": "all",
          "include_interfaces": true,
          "include_wireless": true
        },
        "variations": [
          { "device_filter": "switches" },
          { "device_filter": "aps" },
          { "device_filter": "gateways" }
        ]
      },
      "success_criteria": {
        "max_response_time": 30000,
        "min_success_rate": 95,
        "max_error_rate": 5,
        "memory_usage_threshold": "500MB"
      }
    },
    {
      "test_name": "large_device_dataset",
      "description": "Test workflow with large device datasets",
      "configuration": {
        "device_count": 1000,
        "batch_size": 100,
        "concurrent_processing": true
      },
      "success_criteria": {
        "max_processing_time": 120000,
        "memory_efficiency": "linear_scaling",
        "no_timeout_errors": true
      }
    }
  ]
}
```

### 4. Security Tests

#### Authentication and Authorization Tests
```json
{
  "security_tests": [
    {
      "test_name": "credential_validation",
      "description": "Test credential security and validation",
      "test_cases": [
        {
          "scenario": "missing_credentials",
          "input": {},
          "expected": "authentication_error",
          "should_not_expose": "credential_details"
        },
        {
          "scenario": "expired_token",
          "mock_response": {
            "status": 401,
            "body": { "error": "token_expired" }
          },
          "expected": "token_refresh_attempt"
        },
        {
          "scenario": "malicious_input_injection",
          "input": {
            "device_id": "<script>alert('xss')</script>",
            "description": "'; DROP TABLE devices; --"
          },
          "expected": "input_sanitized",
          "should_not_contain": ["<script>", "DROP TABLE", "--"]
        }
      ]
    },
    {
      "test_name": "webhook_security",
      "description": "Test webhook endpoint security",
      "test_cases": [
        {
          "scenario": "oversized_payload",
          "input_size": "10MB",
          "expected": "payload_size_error"
        },
        {
          "scenario": "malformed_json",
          "input": "{ invalid json content",
          "expected": "json_parse_error"
        },
        {
          "scenario": "rate_limiting",
          "request_rate": "1000_per_minute",
          "expected": "rate_limit_protection"
        }
      ]
    }
  ]
}
```

### 5. Error Handling Tests

#### Error Recovery and Resilience Tests
```json
{
  "error_handling_tests": [
    {
      "test_name": "api_failure_recovery",
      "description": "Test workflow behavior during API failures",
      "failure_scenarios": [
        {
          "failure_type": "network_timeout",
          "duration": 30,
          "expected_behavior": "retry_with_exponential_backoff"
        },
        {
          "failure_type": "service_unavailable",
          "status_code": 503,
          "expected_behavior": "circuit_breaker_activation"
        },
        {
          "failure_type": "partial_data_corruption",
          "mock_response": "corrupted_json",
          "expected_behavior": "graceful_degradation"
        }
      ]
    },
    {
      "test_name": "notification_failure_handling",
      "description": "Test behavior when notifications fail",
      "scenarios": [
        {
          "failure": "slack_api_down",
          "expected": "fallback_notification_method"
        },
        {
          "failure": "invalid_slack_channel",
          "expected": "error_logged_continue_processing"
        }
      ]
    }
  ]
}
```

## Test Automation Framework

### Test Execution Script
```bash
#!/bin/bash
# n8n Workflow Test Automation Script

set -e

# Configuration
N8N_BASE_URL="http://192.168.40.100:8006"
TEST_CONFIG_DIR="./workflow-test-suite"
RESULTS_DIR="./test-results"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

# Create results directory
mkdir -p "${RESULTS_DIR}/${TIMESTAMP}"

# Functions
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "${RESULTS_DIR}/${TIMESTAMP}/test.log"
}

test_workflow() {
    local workflow_file=$1
    local test_config=$2
    
    log "Testing workflow: $workflow_file"
    
    # Import workflow to n8n
    local workflow_id=$(curl -s -X POST \
        "${N8N_BASE_URL}/api/v1/workflows" \
        -H "Content-Type: application/json" \
        -d @"$workflow_file" | jq -r '.id')
    
    if [ "$workflow_id" == "null" ]; then
        log "ERROR: Failed to import workflow $workflow_file"
        return 1
    fi
    
    log "Imported workflow with ID: $workflow_id"
    
    # Run test scenarios
    while IFS= read -r scenario; do
        test_scenario "$workflow_id" "$scenario"
    done < <(jq -c '.test_scenarios[]' "$test_config")
    
    # Cleanup
    curl -s -X DELETE "${N8N_BASE_URL}/api/v1/workflows/$workflow_id"
    log "Cleaned up workflow $workflow_id"
}

test_scenario() {
    local workflow_id=$1
    local scenario=$2
    
    local scenario_name=$(echo "$scenario" | jq -r '.scenario')
    log "Running scenario: $scenario_name"
    
    # Extract test input
    local test_input=$(echo "$scenario" | jq '.input')
    
    # Execute workflow
    local execution_id=$(curl -s -X POST \
        "${N8N_BASE_URL}/api/v1/workflows/$workflow_id/execute" \
        -H "Content-Type: application/json" \
        -d "$test_input" | jq -r '.data.executionId')
    
    # Wait for completion
    sleep 5
    
    # Get execution result
    local result=$(curl -s "${N8N_BASE_URL}/api/v1/executions/$execution_id")
    local status=$(echo "$result" | jq -r '.finished')
    
    if [ "$status" == "true" ]; then
        log "✓ Scenario $scenario_name completed successfully"
        validate_output "$scenario" "$result"
    else
        log "✗ Scenario $scenario_name failed"
        echo "$result" > "${RESULTS_DIR}/${TIMESTAMP}/failed_${scenario_name}.json"
    fi
}

validate_output() {
    local expected=$1
    local actual=$2
    
    # Implement output validation logic
    # Compare expected vs actual outputs
    # Generate test report
    
    log "Validating outputs..."
    # Add specific validation logic here
}

# Main execution
main() {
    log "Starting n8n workflow test suite"
    
    # Test device health monitoring workflow
    test_workflow \
        "exported-workflows/device-health-monitor-FIXED.json" \
        "workflow-test-suite/device-health-tests.json"
    
    # Test security event response workflow
    test_workflow \
        "exported-workflows/security-event-response-automation-FIXED.json" \
        "workflow-test-suite/security-response-tests.json"
    
    log "Test suite completed"
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### Continuous Integration Pipeline
```yaml
# .github/workflows/n8n-workflow-tests.yml
name: n8n Workflow Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-workflows:
    runs-on: ubuntu-latest
    
    services:
      n8n:
        image: n8nio/n8n:latest
        ports:
          - 5678:5678
        env:
          N8N_BASIC_AUTH_ACTIVE: false
          N8N_HOST: 0.0.0.0
          N8N_PORT: 5678
          
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Install dependencies
      run: |
        npm install -g newman
        npm install -g jq
        
    - name: Wait for n8n to be ready
      run: |
        timeout 60 bash -c 'until curl -f http://localhost:5678/healthz; do sleep 2; done'
        
    - name: Run workflow tests
      run: |
        chmod +x ./test-automation.sh
        ./test-automation.sh
        
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: test-results/
        
    - name: Generate test report
      run: |
        # Generate HTML test report
        node generate-test-report.js
        
    - name: Comment PR with results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = fs.readFileSync('test-results/summary.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: report
          });
```

## Monitoring and Alerting

### Workflow Health Monitoring
```json
{
  "monitoring_configuration": {
    "health_checks": [
      {
        "name": "workflow_execution_success_rate",
        "description": "Monitor workflow execution success rate",
        "metric": "success_rate",
        "threshold": 95,
        "time_window": "1h",
        "alert_channels": ["#workflow-alerts"]
      },
      {
        "name": "workflow_execution_time",
        "description": "Monitor workflow execution duration",
        "metric": "avg_execution_time",
        "threshold": 30000,
        "time_window": "15m",
        "alert_channels": ["#performance-alerts"]
      },
      {
        "name": "error_rate_spike",
        "description": "Monitor for error rate spikes",
        "metric": "error_rate",
        "threshold": 10,
        "time_window": "5m",
        "alert_channels": ["#critical-alerts"]
      }
    ],
    "metrics_collection": {
      "execution_metrics": true,
      "performance_metrics": true,
      "error_tracking": true,
      "custom_metrics": [
        "device_count_processed",
        "alert_count_generated",
        "api_response_time"
      ]
    }
  }
}
```

### Alerting Rules
```yaml
# Prometheus alerting rules for n8n workflows
groups:
- name: n8n_workflow_alerts
  rules:
  - alert: WorkflowHighErrorRate
    expr: (n8n_workflow_errors_total / n8n_workflow_executions_total) * 100 > 5
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High error rate in n8n workflow"
      description: "Workflow {{ $labels.workflow_name }} has error rate of {{ $value }}%"
      
  - alert: WorkflowExecutionTimeout
    expr: n8n_workflow_execution_duration_seconds > 300
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Workflow execution timeout"
      description: "Workflow {{ $labels.workflow_name }} execution exceeded 5 minutes"
      
  - alert: SecurityWorkflowFailure
    expr: n8n_security_workflow_failures_total > 0
    for: 0s
    labels:
      severity: critical
    annotations:
      summary: "Security workflow failure detected"
      description: "Security workflow {{ $labels.workflow_name }} failed - immediate attention required"
```

## Documentation Standards

### Workflow Documentation Template
```markdown
# Workflow: {{ workflow_name }}

## Overview
{{ workflow_description }}

## Trigger Configuration
- **Type**: {{ trigger_type }}
- **Path**: {{ webhook_path }}
- **Method**: {{ http_method }}
- **Authentication**: {{ auth_required }}

## Input Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| device_filter | string | No | "all" | Filter devices by type |
| thresholds | object | No | {} | Custom alert thresholds |

## Output Format
```json
{
  "status": "success|error",
  "timestamp": "ISO 8601 timestamp",
  "summary": {
    "total_devices": 0,
    "alerts_generated": 0
  },
  "devices": []
}
```

## Error Handling
- **Validation Errors**: Returns 400 with validation details
- **API Errors**: Implements retry with exponential backoff
- **Processing Errors**: Logs error and sends notification

## Monitoring
- **Success Rate**: Target 99%
- **Response Time**: Target <30s
- **Error Rate**: Target <1%

## Testing
- Unit tests: ✓
- Integration tests: ✓
- Performance tests: ✓
- Security tests: ✓

## Dependencies
- Aruba Central API
- Slack Integration
- n8n Credential Store

## Change Log
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release |
```

This comprehensive testing, monitoring, and documentation framework ensures that all Aruba n8n workflows are reliable, secure, performant, and maintainable in production environments.
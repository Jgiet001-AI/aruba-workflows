# AOS-CX Error Handling & Rollback Framework

## Overview
Comprehensive error handling and rollback mechanisms for all AOS-CX configuration management workflows. This framework provides centralized error management, automatic rollback procedures, and recovery strategies.

## Error Categories

### 1. Authentication Errors (401, 403)
**Symptoms**: Invalid credentials, insufficient permissions
**Detection**: HTTP status codes 401, 403
**Recovery Actions**:
- Retry with credential refresh (if token-based)
- Switch to backup credentials
- Notify admin for manual credential check
- Implement exponential backoff for repeated failures

### 2. Validation Errors (400, 422)
**Symptoms**: Invalid input parameters, malformed requests
**Detection**: HTTP status codes 400, 422, validation failures
**Recovery Actions**:
- Return detailed validation error messages
- Provide corrected parameter examples
- Log validation failures for pattern analysis
- No rollback needed (no changes applied)

### 3. Resource Not Found (404)
**Symptoms**: Non-existent VLANs, interfaces, ACLs
**Detection**: HTTP status code 404
**Recovery Actions**:
- For read operations: Return empty result with warning
- For update operations: Offer to create resource first
- For delete operations: Consider operation successful
- Log for inventory sync issues

### 4. Conflict Errors (409)
**Symptoms**: Resource already exists, conflicting configuration
**Detection**: HTTP status code 409
**Recovery Actions**:
- For create operations: Check if existing resource matches intent
- For updates: Attempt to resolve conflicts automatically
- Implement merge strategies for compatible changes
- Escalate to manual resolution for complex conflicts

### 5. Server Errors (500+)
**Symptoms**: Switch internal errors, API service failures
**Detection**: HTTP status codes 500, 502, 503, 504
**Recovery Actions**:
- Immediate rollback to last known good configuration
- Retry after progressive delays (5s, 15s, 45s)
- Switch to backup device if available
- Create incident ticket for infrastructure team

### 6. Network Connectivity Errors
**Symptoms**: Timeouts, connection refused, unreachable host
**Detection**: Network timeout exceptions, connection errors
**Recovery Actions**:
- Retry with increased timeout values
- Attempt connection via backup management interface
- Check network path connectivity
- Implement circuit breaker pattern

## Rollback Strategies

### 1. Configuration Rollback
```json
{
  "rollback_method": "checkpoint_restore",
  "checkpoint_id": "pre_change_{{timestamp}}",
  "validation_required": true,
  "notification_channels": ["#network-alerts", "network-team@company.com"]
}
```

### 2. VLAN Rollback
```json
{
  "rollback_actions": [
    "delete_created_vlans",
    "restore_modified_vlans", 
    "verify_connectivity"
  ],
  "affected_vlans": ["100", "200", "300"],
  "rollback_timeout": 60
}
```

### 3. Interface Rollback
```json
{
  "rollback_actions": [
    "restore_interface_config",
    "verify_port_status",
    "test_connectivity"
  ],
  "affected_interfaces": ["1/1/1", "1/1/2"],
  "emergency_safe_mode": {
    "admin_state": "up",
    "vlan_mode": "access",
    "vlan_tag": 1
  }
}
```

### 4. Policy Rollback
```json
{
  "rollback_actions": [
    "remove_applied_acls",
    "restore_previous_acls",
    "verify_traffic_flow"
  ],
  "affected_policies": ["SECURITY_ACL", "QOS_POLICY"],
  "rollback_verification": true
}
```

## Error Handling Implementation

### 1. Workflow Error Nodes
All workflows include dedicated error handling nodes:
- **Error Trigger**: Catches workflow failures
- **Error Classifier**: Categorizes error types
- **Rollback Dispatcher**: Routes to appropriate rollback procedure
- **Notification Engine**: Sends alerts with recovery actions

### 2. Retry Logic Pattern
```javascript
const maxRetries = 3;
const baseDelay = 2000; // 2 seconds
const backoffMultiplier = 2;

for (let attempt = 1; attempt <= maxRetries; attempt++) {
  try {
    const result = await apiCall();
    return result;
  } catch (error) {
    if (attempt === maxRetries) {
      throw error; // Final failure
    }
    
    const delay = baseDelay * Math.pow(backoffMultiplier, attempt - 1);
    await sleep(delay);
  }
}
```

### 3. Circuit Breaker Implementation
```javascript
const circuitBreaker = {
  failureThreshold: 5,
  resetTimeout: 60000, // 1 minute
  state: 'CLOSED', // CLOSED, OPEN, HALF_OPEN
  failureCount: 0,
  lastFailureTime: null
};

function callWithCircuitBreaker(apiCall) {
  if (circuitBreaker.state === 'OPEN') {
    if (Date.now() - circuitBreaker.lastFailureTime > circuitBreaker.resetTimeout) {
      circuitBreaker.state = 'HALF_OPEN';
    } else {
      throw new Error('Circuit breaker is OPEN');
    }
  }
  
  return apiCall().catch(error => {
    circuitBreaker.failureCount++;
    circuitBreaker.lastFailureTime = Date.now();
    
    if (circuitBreaker.failureCount >= circuitBreaker.failureThreshold) {
      circuitBreaker.state = 'OPEN';
    }
    
    throw error;
  });
}
```

## Recovery Procedures

### 1. Automatic Recovery
**Low-Risk Failures** (validation, not found, timeouts):
- Automatic retry with exponential backoff
- Log error details for analysis
- Continue with next operation if applicable

**Medium-Risk Failures** (conflicts, partial failures):
- Attempt automatic resolution
- Create rollback checkpoint before retry
- Escalate to manual intervention if unresolved

**High-Risk Failures** (server errors, connectivity loss):
- Immediate rollback to safe state
- Stop all related operations
- Alert on-call team immediately

### 2. Manual Recovery
**Escalation Triggers**:
- Multiple consecutive failures
- Critical service impact
- Security-related errors
- Configuration corruption detected

**Recovery Steps**:
1. Access switch via console/SSH
2. Verify current configuration state
3. Apply emergency safe configuration
4. Test basic connectivity
5. Restore from last known good backup
6. Document incident and lessons learned

## Monitoring & Alerting

### 1. Error Metrics
- **Error Rate**: Percentage of failed operations
- **Recovery Time**: Time to restore normal operation
- **Rollback Success Rate**: Effectiveness of rollback procedures
- **Mean Time to Recovery (MTTR)**: Average incident resolution time

### 2. Alert Thresholds
```json
{
  "error_rate_threshold": 5, // % failures per hour
  "consecutive_failures": 3,
  "critical_errors": ["authentication", "server_error", "rollback_failure"],
  "notification_escalation": {
    "immediate": ["#network-alerts"],
    "after_5_minutes": ["network-team@company.com"],
    "after_15_minutes": ["network-oncall@company.com"]
  }
}
```

### 3. Dashboard Integration
- **Real-time Error Monitoring**: Live error counts and categories
- **Recovery Status**: Current recovery operations and progress
- **Historical Analysis**: Error trends and patterns
- **Rollback History**: Track rollback frequency and success rates

## Testing Error Scenarios

### 1. Automated Error Testing
```bash
# Test authentication failure
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d '{"operation": "create", "switch_ip": "192.168.1.100", "vlan_id": 100, "invalid_auth": true}'

# Test validation failure
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d '{"operation": "create", "switch_ip": "invalid_ip", "vlan_id": 99999}'

# Test network timeout
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d '{"operation": "list", "switch_ip": "192.168.999.999"}'
```

### 2. Rollback Testing
```bash
# Test VLAN rollback
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-test" \
  -H "Content-Type: application/json" \
  -d '{"test_type": "vlan_rollback", "trigger_failure": true}'

# Test interface rollback
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-test" \
  -H "Content-Type: application/json" \
  -d '{"test_type": "interface_rollback", "interface": "1/1/1"}'
```

## Best Practices

### 1. Error Prevention
- **Input Validation**: Validate all parameters before API calls
- **Pre-flight Checks**: Verify connectivity and permissions
- **Configuration Validation**: Check configuration syntax before applying
- **Dependency Verification**: Ensure prerequisites are met

### 2. Error Response
- **Consistent Error Format**: Standardized error message structure
- **Actionable Messages**: Include specific remediation steps
- **Context Preservation**: Maintain operation context for debugging
- **Audit Trail**: Log all errors and recovery actions

### 3. Recovery Planning
- **Regular Backup Testing**: Verify backup integrity and restore procedures
- **Disaster Recovery Drills**: Practice recovery scenarios regularly
- **Documentation Updates**: Keep recovery procedures current
- **Team Training**: Ensure team familiarity with recovery processes

## Configuration Files

### Error Handling Configuration
Location: `/config/error-handling.json`
```json
{
  "retry_settings": {
    "max_attempts": 3,
    "base_delay_ms": 2000,
    "backoff_multiplier": 2,
    "timeout_ms": 30000
  },
  "rollback_settings": {
    "auto_rollback_enabled": true,
    "rollback_timeout_ms": 60000,
    "verification_required": true
  },
  "notification_settings": {
    "slack_webhook": "https://hooks.slack.com/...",
    "email_recipients": ["network-team@company.com"],
    "escalation_delay_minutes": 15
  }
}
```

This comprehensive error handling framework ensures robust, reliable operation of all AOS-CX configuration management workflows with automatic recovery capabilities and comprehensive monitoring.
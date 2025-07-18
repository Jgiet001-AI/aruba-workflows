# Security Event Response Automation

## Overview
Automated security incident response workflow that processes security events from HPE Aruba infrastructure and executes appropriate containment, remediation, and notification actions based on threat severity.

## Features

### 🔐 **Automated Threat Response**
- **Intelligent Threat Scoring**: Dynamic threat assessment based on severity and confidence
- **Device Isolation**: Automatic isolation for critical threats (score ≥90)
- **Device Quarantine**: Automatic quarantine for high-severity threats (score 70-89)
- **Policy Updates**: Real-time security policy updates with threat indicators

### 🚨 **Multi-Channel Alerting**
- **Critical Alerts**: Immediate Slack notifications for critical events
- **High Priority Alerts**: Escalated notifications for significant threats
- **SIEM Integration**: Automatic forwarding to security platforms
- **Error Handling**: Dedicated error notifications for failed automation

### 📊 **Comprehensive Logging**
- **Audit Trail**: Complete logging of all security actions
- **Compliance**: Detailed records for regulatory requirements
- **Incident Correlation**: Integration with external SIEM systems
- **Rollback Capability**: Automatic rollback timers for isolation actions

## File Structure
```
security-event-response-automation/
├── workflow.json                    # n8n workflow export
├── config/
│   └── parameters.json             # Configuration parameters
├── tests/
│   ├── api-validation-part1.md     # API testing documentation
│   └── threat-response-framework.py # Comprehensive testing framework
├── docs/
│   └── README.md                   # This documentation
└── versions/                       # Version history
```

## Quick Start

### 1. Import Workflow
```bash
# Import into n8n
curl -X POST "http://192.168.40.100:8006/api/v1/workflows" \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

### 2. Configure Environment Variables
Set the following environment variables in n8n:
```bash
aruba_api_token=your_aruba_central_api_token
siem_webhook_url=https://your-siem.company.com/api/events
siem_api_key=your_siem_api_key
```

### 3. Configure Slack Integration
Set up Slack credentials in n8n for the following channels:
- `#security-critical` - Critical security events
- `#security-alerts` - High priority events  
- `#security-ops` - Operational notifications

### 4. Test Webhook
Send a test security event to the webhook:
```bash
curl -X POST "http://192.168.40.100:8006/webhook/security-event-response" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "test_001",
    "threat_type": "malware_detected",
    "severity": "critical",
    "device_id": "AP001",
    "timestamp": "2025-07-17T14:53:52.359Z",
    "source_ip": "192.168.1.100",
    "source_mac": "00:11:22:33:44:55",
    "confidence_score": 0.95,
    "indicators": ["hash:abc123", "file:evil.exe"],
    "description": "Suspicious executable detected"
  }'
```

## Workflow Process Flow

### 1. **Security Event Webhook** (`webhook-trigger`)
- **Trigger**: POST webhook at `/security-event-response`
- **Input**: Security event data from monitoring systems
- **Output**: Raw event data to processing pipeline

### 2. **Parse Security Event** (`parse-event`)
- **Function**: Validates and enriches incoming security events
- **Processing**:
  - Validates required fields (event_id, threat_type, severity, device_id, timestamp)
  - Calculates dynamic threat score based on severity and confidence
  - Enriches event with processing metadata
- **Threat Scoring**:
  - Low: 25 base score
  - Medium: 50 base score  
  - High: 75 base score
  - Critical: 95 base score
  - Final score = base_score × confidence_multiplier

### 3. **Check Threat Level** (`check-threat-level`)
- **Function**: Routes events based on threat score
- **Decision Logic**:
  - Score ≥90: Critical path (device isolation)
  - Score 70-89: High path (device quarantine)
  - Score <70: Monitoring only

### 4. **Device Isolation** (`isolate-device`)
- **Trigger**: Critical threats (score ≥90)
- **API**: `POST /api/v2/devices/isolate`
- **Features**:
  - Automatic rollback timer (1 hour default)
  - Retry logic (3 attempts with 2s delay)
  - Detailed reason logging

### 5. **Device Quarantine** (`quarantine-device`)  
- **Trigger**: High threats (score 70-89)
- **API**: `POST /api/v2/devices/quarantine`
- **Features**:
  - Less restrictive than isolation
  - Monitoring and investigation mode
  - Preserves network connectivity for analysis

### 6. **Update Security Policy** (`update-security-policy`)
- **Function**: Updates security policies with threat indicators
- **API**: `PUT /api/v2/security/policies/incident_response`
- **Updates**:
  - Threat indicators from event
  - Source IP/MAC blocking
  - 24-hour block duration
  - Automation attribution

### 7. **Alert Notifications**
- **Send Critical Alert** (`send-critical-alert`)
  - Channel: `#security-critical`
  - Rich formatting with incident details
  - Action items and next steps
  
- **Send High Alert** (`send-high-alert`)
  - Channel: `#security-alerts`
  - Escalation for high-priority events
  - Review and validation instructions

### 8. **SIEM Integration** (`log-to-siem`)
- **Function**: Forwards processed events to SIEM
- **API**: Configurable SIEM webhook
- **Data**: Complete event context with automation actions

### 9. **Error Handling**
- **Error Handler** (`error-handler`)
  - Captures workflow failures
  - Creates incident reports
  - Preserves original event data

- **Error Notification** (`error-notification`)
  - Channel: `#security-ops`
  - Manual intervention alerts
  - Full error context and stack traces

## Configuration Parameters

### Security Thresholds
```json
{
  "criticalAlertScore": 80,    // Critical alert threshold
  "autoResponseScore": 90,     // Automated response threshold  
  "isolationScore": 95         // Device isolation threshold
}
```

### Response Actions
```json
{
  "enableAutoIsolation": true,     // Enable automatic device isolation
  "enableAutoRemediation": true,   // Enable automated remediation
  "enableThreatIntelligence": true // Enable threat intelligence feeds
}
```

### Integration Settings
```json
{
  "siemEnabled": true,           // Enable SIEM integration
  "threatIntelEnabled": true,    // Enable threat intelligence
  "soarEnabled": false          // Enable SOAR platform integration
}
```

### Compliance Settings
```json
{
  "logRetentionDays": 365,      // Security log retention
  "auditTrailEnabled": true,    // Enable audit trail
  "encryptionRequired": true    // Require encryption
}
```

## API Dependencies

### HPE Aruba Central APIs
- `POST /api/v2/devices/isolate` - Device isolation
- `POST /api/v2/devices/quarantine` - Device quarantine
- `PUT /api/v2/security/policies/{id}` - Policy updates
- `GET /api/v2/alerts` - Security event retrieval

### External Integrations
- **Slack API** - Multi-channel notifications
- **SIEM Webhook** - Security event forwarding
- **Threat Intelligence** - External threat feeds (optional)

## Security Considerations

### Authentication & Authorization
- **API Tokens**: Secure storage in n8n environment variables
- **Least Privilege**: Minimum required permissions for APIs
- **Token Rotation**: Regular credential rotation recommended

### Data Protection
- **Encryption**: All API communications use HTTPS/TLS
- **Sensitive Data**: No hardcoded secrets in workflow
- **Audit Logging**: Complete audit trail for compliance

### Error Handling
- **Graceful Degradation**: Continues operation on partial failures
- **Retry Logic**: Intelligent retry with exponential backoff
- **Circuit Breaker**: Prevents cascade failures

## Monitoring & Metrics

### Success Metrics
- **Response Time**: Event processing latency
- **Containment Rate**: Percentage of threats contained
- **False Positive Rate**: Automated vs. manual validation

### Failure Metrics  
- **API Failures**: Rate of API call failures
- **Processing Errors**: Event parsing/validation failures
- **Integration Failures**: SIEM/Slack notification failures

### Performance Optimization
- **Parallel Processing**: Concurrent API calls where possible
- **Caching**: Event deduplication and caching
- **Rate Limiting**: Respects API rate limits

## Troubleshooting

### Common Issues

#### API Authentication Failures
```bash
# Check API token validity
curl -H "Authorization: Bearer $ARUBA_API_TOKEN" \
  https://central.arubanetworks.com/api/v2/platform/device_inventory
```

#### Webhook Not Triggering
- Verify webhook URL: `http://192.168.40.100:8006/webhook/security-event-response`
- Check firewall rules and network connectivity
- Validate JSON payload format

#### Slack Notifications Failing
- Verify Slack credentials in n8n
- Check channel permissions
- Validate channel names (#security-critical, #security-alerts, #security-ops)

#### Device Isolation/Quarantine Failures
- Check device connectivity and status
- Verify API permissions for device management
- Review device support for isolation/quarantine features

### Log Analysis
```bash
# Check n8n execution logs
docker logs n8n-container | grep "Security Event Response"

# Monitor workflow executions
curl "http://192.168.40.100:8006/api/v1/executions?workflowId=yMXkcYpg1VQ9dina"
```

## Compliance & Audit

### Regulatory Requirements
- **SOX Compliance**: Complete audit trails for security actions
- **GDPR**: Data protection and privacy considerations
- **HIPAA**: Healthcare-specific security requirements
- **PCI DSS**: Payment card industry standards

### Audit Trail Components
- **Event Processing**: Complete event lifecycle tracking
- **Authorization**: User/system authorization for actions
- **Data Access**: All API calls and data access logged
- **Retention**: Configurable log retention periods

### Reporting
- **Security Metrics**: Automated security dashboards
- **Incident Reports**: Detailed incident analysis
- **Compliance Reports**: Regulatory compliance status
- **Performance Reports**: System performance and optimization

## Integration Examples

### SIEM Integration (Splunk)
```json
{
  "siem_webhook_url": "https://splunk.company.com:8088/services/collector/event",
  "siem_api_key": "Splunk_HEC_Token",
  "source": "aruba_security_automation",
  "sourcetype": "aruba:security:incident"
}
```

### SOAR Integration (Phantom)
```json
{
  "soar_webhook_url": "https://phantom.company.com/rest/container",
  "soar_api_key": "Phantom_API_Token", 
  "container_type": "security_incident",
  "severity": "high"
}
```

### Threat Intelligence (MISP)
```json
{
  "misp_url": "https://misp.company.com/events/restSearch",
  "misp_api_key": "MISP_API_Token",
  "threat_level": "high",
  "distribution": "organization"
}
```

## Version History

### v1.0.0 (2025-07-17)
- Initial release
- Basic threat response automation
- Device isolation and quarantine
- Slack notifications
- SIEM integration
- Comprehensive error handling

### Roadmap
- **v1.1.0**: Advanced threat intelligence integration
- **v1.2.0**: Machine learning-based threat scoring
- **v1.3.0**: Multi-tenant support
- **v1.4.0**: Advanced compliance reporting

## Support

### Documentation
- [HPE Aruba Central API Documentation](https://developer.arubanetworks.com/)
- [n8n Workflow Documentation](https://docs.n8n.io/)
- [Slack API Documentation](https://api.slack.com/)

### Community
- **GitHub Issues**: Report bugs and feature requests
- **Security Team**: Contact security team for incident response
- **DevOps Team**: Contact for infrastructure and deployment issues

### Contact
- **Primary Contact**: Security Operations Team
- **Email**: security-ops@company.com
- **Slack**: #security-automation
- **Emergency**: Follow company incident response procedures

---

**⚠️ Security Notice**: This workflow processes critical security events and performs automated containment actions. Ensure proper testing in non-production environments before deployment. Review all configuration parameters and access controls before enabling in production.

**🔄 Last Updated**: 2025-07-17
**📋 Version**: 1.0.0
**👤 Maintainer**: Network Security Automation Team
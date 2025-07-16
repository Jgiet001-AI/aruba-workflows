# PLANNING.md - HPE Aruba n8n Workflow Automation Technical Planning

**Project**: HPE Aruba Network Automation using n8n  
**Version**: 2.0  
**Last Updated**: January 2025  
**Status**: Active Development

---

## 1. Vision

### Project Vision
Transform network operations by creating an intelligent automation layer that enables network administrators to manage HPE Aruba infrastructure through natural language requests, automated workflows, and proactive monitoring - reducing manual tasks by 75% and improving network reliability.

### Core Objectives
- **Democratize Automation**: Enable network teams to automate without deep programming knowledge
- **Reduce MTTR**: Automate incident detection and response workflows
- **Ensure Compliance**: Continuous configuration monitoring and remediation
- **Optimize Performance**: Proactive network optimization based on real-time metrics
- **Scale Operations**: Manage large networks with minimal human intervention

### Success Metrics
- 75% reduction in manual network tasks
- 50% improvement in incident response time
- 95% configuration compliance rate
- 99.9% workflow execution reliability
- Complete automation coverage for common network operations

---

## 2. Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           User Interface                             │
│                    (Natural Language Requests)                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          Claude Code Layer                           │
│          (Requirement Analysis & Workflow Generation)                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
┌─────────────────────────────┐     ┌─────────────────────────────┐
│        n8n Platform         │     │      Postman MCP            │
│   (Workflow Execution)      │     │    (API Testing)            │
└─────────────────────────────┘     └─────────────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        HPE Aruba APIs                                │
├─────────────┬─────────────┬─────────────┬─────────────┬────────────┤
│   Central   │   AOS-CX    │ EdgeConnect │     UXI     │   Future   │
│     API     │     API     │     API     │     API     │    APIs    │
└─────────────┴─────────────┴─────────────┴─────────────┴────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                    Network Infrastructure                            │
│        (Switches, APs, SD-WAN Devices, Sensors)                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Workflow Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Triggers     │────▶│   Processing    │────▶│    Actions      │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ • Webhooks      │     │ • Data Transform│     │ • API Calls     │
│ • Schedules     │     │ • Logic/Rules   │     │ • Notifications │
│ • Manual        │     │ • Aggregation   │     │ • Updates       │
│ • Events        │     │ • Analysis      │     │ • Remediation   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         ▲                                                │
         │                                                ▼
┌─────────────────┐                          ┌─────────────────┐
│   Monitoring    │                          │  Verification   │
├─────────────────┤                          ├─────────────────┤
│ • Metrics       │                          │ • Status Check  │
│ • Logs          │                          │ • Validation    │
│ • Alerts        │◀─────────────────────────│ • Rollback      │
└─────────────────┘                          └─────────────────┘
```

### Data Flow Architecture

```yaml
Input Sources:
  - HPE Aruba Central: Device inventory, monitoring, alerts
  - AOS-CX Switches: Configuration, status, metrics
  - EdgeConnect: SD-WAN policies, performance data
  - UXI Sensors: User experience metrics, synthetic tests
  - External: ServiceNow, Slack, Email, Custom APIs

Processing Layer:
  - n8n Workflows: Orchestration and automation logic
  - JavaScript Functions: Custom transformations
  - Conditional Logic: Decision trees and routing
  - Data Aggregation: Combine multiple sources

Output Destinations:
  - Network Devices: Configuration changes, commands
  - Notification Systems: Alerts and reports
  - Data Storage: Logs, metrics, audit trails
  - Dashboards: Real-time status and KPIs
```

---

## 3. Technology Stack

### Core Platform
- **n8n** (v1.x)
  - Self-hosted instance at http://192.168.40.100:8006
  - Workflow automation platform
  - Visual workflow builder
  - Extensive node library

### Development Tools
- **Claude Code**
  - AI-powered workflow development
  - Natural language to workflow translation
  - Code generation and optimization
  - Documentation automation

### MCP (Model Context Protocol) Servers
- **n8n-mcp**
  - Direct n8n API integration
  - Workflow CRUD operations
  - Execution management
  - Validation tools

- **postman-mcp**
  - API testing and validation
  - Request/response inspection
  - Authentication testing
  - Rate limit discovery

- **filesystem**
  - Workflow export/import
  - Documentation management
  - Version control
  - Backup operations

- **github**
  - Version control
  - Collaboration
  - CI/CD integration
  - Issue tracking

### HPE Aruba APIs
- **Aruba Central API v2**
  - RESTful API
  - OAuth 2.0 authentication
  - JSON data format
  - Webhook support

- **AOS-CX REST API v10.08**
  - RESTful interface
  - Token-based auth
  - YANG data models
  - Real-time streaming

- **EdgeConnect Orchestrator API**
  - REST/GraphQL hybrid
  - API key authentication
  - Bulk operations
  - Policy management

- **UXI API v1**
  - RESTful API
  - Bearer token auth
  - Metrics streaming
  - Alert webhooks

### Supporting Technologies
- **JavaScript/Node.js**
  - Custom function nodes
  - Data transformations
  - Complex logic implementation

- **JSON**
  - Data format
  - Configuration files
  - API payloads

- **Markdown**
  - Documentation
  - README files
  - Runbooks

- **Git**
  - Version control
  - Branching strategies
  - Collaboration

---

## 4. Required Tools List

### Development Environment

#### Essential Tools
1. **n8n Instance**
   - URL: http://192.168.40.100:8006
   - Version: Latest stable
   - Access: Admin credentials required
   - Purpose: Workflow development and execution

2. **Claude Code Access**
   - MCP servers configured
   - File system access
   - API permissions
   - Purpose: Automated workflow development

3. **Text Editor/IDE**
   - VS Code recommended
   - JSON syntax highlighting
   - JavaScript support
   - Purpose: Manual editing and review

4. **API Testing Tools**
   - Postman (via postman-mcp)
   - cURL for command line
   - Purpose: API validation and testing

#### HPE Aruba Access Requirements
1. **Aruba Central**
   - Developer account
   - API client credentials
   - Appropriate permissions (read/write)
   - Test environment access

2. **AOS-CX Access**
   - Switch management access
   - REST API enabled
   - Authentication tokens
   - Test switches available

3. **EdgeConnect Orchestrator**
   - Orchestrator instance
   - API key generation
   - Policy permissions
   - Test SD-WAN setup

4. **UXI Dashboard**
   - UXI sensor deployment
   - API access enabled
   - Metric access permissions
   - Test sensors configured

### n8n Nodes Required

#### Core Nodes
- **Schedule Trigger**: Timed automation
- **Webhook**: Event-driven workflows  
- **HTTP Request**: API interactions
- **Function**: Custom logic
- **IF**: Conditional branching
- **Set**: Data manipulation
- **Merge**: Data combination

#### Integration Nodes
- **Slack**: Notifications
- **Email**: Alert delivery
- **Postgres**: Data storage
- **Redis**: Caching
- **GitHub**: Version control

#### Utility Nodes
- **Date & Time**: Scheduling logic
- **Crypto**: Security functions
- **Compression**: Data optimization
- **HTML Extract**: Parsing
- **Spreadsheet File**: Reporting

### Credentials Required

#### API Credentials
```yaml
Aruba Central:
  - Client ID
  - Client Secret
  - Access Token
  - Refresh Token
  - Base URL (region-specific)

AOS-CX:
  - Username
  - Password
  - API Token
  - Switch IPs/Hostnames

EdgeConnect:
  - API Key
  - Orchestrator URL
  - Account ID
  - Organization ID

UXI:
  - Bearer Token
  - Dashboard URL
  - Customer ID
```

#### Integration Credentials
```yaml
Notifications:
  - Slack Webhook URLs
  - Email SMTP settings
  - SMS API keys (optional)

Databases:
  - PostgreSQL connection strings
  - Redis connection details

External Systems:
  - ServiceNow instance/credentials
  - LDAP/AD for user lookup
  - Custom API endpoints
```

### Development Tools Configuration

#### Directory Structure
```bash
/Users/jeangiet/Documents/Claude/aruba-workflows/
├── PLANNING.md          # This file
├── TASKS.md            # Task tracking
├── CLAUDE.md           # Claude Code guide
├── README.md           # Project overview
├── credentials/        # Credential templates (not actual values)
├── templates/          # Workflow templates
├── scripts/            # Helper scripts
└── [workflow-dirs]/    # Individual workflows
```

#### Environment Variables
```bash
# n8n Configuration
N8N_HOST=192.168.40.100
N8N_PORT=8006
N8N_PROTOCOL=http
N8N_API_KEY=your-api-key

# File Paths
WORKFLOW_BASE_DIR=/Users/jeangiet/Documents/Claude/aruba-workflows
EXPORT_DIR=/Users/jeangiet/Downloads

# API Endpoints (examples)
ARUBA_CENTRAL_BASE_URL=https://apigw-uswest4.central.arubanetworks.com
AOS_CX_BASE_URL=https://switch-ip:443
EDGECONNECT_BASE_URL=https://orchestrator.example.com
UXI_BASE_URL=https://api.uxi.aruba.com
```

---

## 5. Development Standards

### Workflow Naming Convention
- Format: `kebab-case-descriptive-name`
- Examples:
  - `device-health-monitor`
  - `config-compliance-checker`
  - `security-event-responder`

### Version Control Strategy
- Main branch: Stable workflows
- Feature branches: New workflow development
- Tags: Version releases (v1.0.0, v1.1.0)
- Commit messages: Descriptive and linked to tasks

### Documentation Requirements
- Every workflow must have README.md
- API documentation required
- Test scenarios documented
- Troubleshooting guides
- Change logs maintained

### Testing Standards
- API connectivity tests first
- Sample data for all scenarios
- Error path validation
- Performance benchmarks
- Security review checklist

### Security Guidelines
- No hardcoded credentials
- Use n8n credential store
- Implement least privilege
- Audit all API calls
- Encrypt sensitive data
- Regular credential rotation

---

## 6. Performance Targets

### Workflow Execution
- Single workflow: < 30 seconds average
- Bulk operations: < 5 minutes for 100 devices
- API response time: < 2 seconds per call
- Error recovery: < 1 minute

### Scalability Targets
- Concurrent workflows: 50+
- Devices managed: 10,000+
- API calls/hour: 10,000
- Data retention: 90 days

### Reliability Targets
- Workflow success rate: > 95%
- API availability: > 99.9%
- Error handling: 100% coverage
- Rollback capability: All critical operations

---

## 7. Integration Roadmap

### Phase 1: Core Integrations (Current)
- HPE Aruba Central API
- AOS-CX REST API
- Basic notifications (Slack/Email)
- n8n platform setup

### Phase 2: Extended Integrations
- EdgeConnect Orchestrator
- UXI Sensors
- ServiceNow ITSM
- Advanced monitoring

### Phase 3: Advanced Features
- AI/ML integration for predictions
- Custom dashboards
- Mobile app notifications
- Third-party security tools

### Phase 4: Future Expansions
- Cloud provider integrations
- Container orchestration
- IoT device management
- Advanced analytics

---

## 8. Maintenance Plan

### Regular Maintenance
- **Daily**: Monitor workflow execution logs
- **Weekly**: Review error rates and performance
- **Monthly**: Update credentials and API versions
- **Quarterly**: Security audit and optimization

### Update Procedures
- Test all API changes in dev environment
- Version all workflow changes
- Document breaking changes
- Maintain backward compatibility
- Gradual rollout strategy

### Support Model
- Primary: Claude Code for development
- Secondary: Community documentation
- Escalation: HPE Aruba support
- Knowledge base: Continuous updates

---

## 9. Risk Mitigation

### Technical Risks
- **API Changes**: Version detection, adapter patterns
- **Rate Limiting**: Implement throttling, queue management
- **Network Failures**: Retry logic, circuit breakers
- **Data Loss**: Regular backups, version control

### Operational Risks
- **Credential Expiry**: Monitoring, rotation workflows
- **Workflow Errors**: Comprehensive testing, rollback
- **Performance Issues**: Optimization, caching
- **Security Threats**: Regular audits, encryption

---

## 10. Success Criteria

### Technical Success
- All planned workflows operational
- Performance targets met
- Security standards maintained
- Documentation complete

### Business Success
- 75% automation achieved
- Positive user feedback
- Reduced operational costs
- Improved network reliability

### Knowledge Transfer
- Comprehensive documentation
- Reusable patterns established
- Team trained on workflows
- Maintenance procedures defined

---

**This is a living document. Update regularly as the project evolves.**
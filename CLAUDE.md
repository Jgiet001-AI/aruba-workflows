# CLAUDE.md - HPE Aruba n8n Workflows Guide

Essential guide for building intelligent n8n workflows that automate HPE Aruba networking tasks.

## Quick Start

### Session Initialization
Execute these steps at the beginning of each session:

```javascript
// Required startup sequence
await read_file("/Users/jeangiet/Documents/Claude/aruba-workflows/PLANNING.md");
await read_file("/Users/jeangiet/Documents/Claude/aruba-workflows/TASKS.md");
await n8n_health_check();
```

### Project Overview
- **Role**: Build n8n workflows for HPE Aruba network automation
- **Tools**: n8n-mcp (workflows), postman-mcp (API testing), filesystem (exports)
- **Goal**: Production-ready workflows with monitoring, error handling, and documentation

### Available MCP Servers
```yaml
n8n-mcp: 
  url: "http://192.168.40.100:8006"
  purpose: "Create, update, execute workflows"
  
postman-mcp:
  location: "/Users/jeangiet/Documents/postman-mcp-server/"
  purpose: "Test HPE Aruba APIs before implementation"
  
filesystem:
  paths: ["/Users/jeangiet/Downloads", "/Users/jeangiet/Documents/Claude"]
  purpose: "Save workflow exports, documentation"
```

## Workflow Building Process

### 1. Understand Requirements
Questions to ask the user:
- What specific network task needs automation?
- Which Aruba products are involved? (Central, AOS-CX, EdgeConnect, UXI)
- What triggers this automation? (schedule, event, manual)
- What should happen on success/failure?
- Who needs to be notified?

### 2. Create Workflow Directory Structure
```javascript
// Standard directory for every workflow
const workflowName = "device-health-monitor"; // kebab-case naming
const baseDir = "/Users/jeangiet/Documents/Claude/aruba-workflows";

// Create directory structure
await create_directory(`${baseDir}/${workflowName}`);
await create_directory(`${baseDir}/${workflowName}/config`);
await create_directory(`${baseDir}/${workflowName}/tests`);
await create_directory(`${baseDir}/${workflowName}/docs`);
```

### 3. Test APIs First
```javascript
// Use postman-mcp to validate APIs before implementation
const authTest = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1000,
  content: `Test Aruba Central API authentication for endpoint GET /api/v2/devices with proper OAuth 2.0 flow`
});
```

### 4. Build and Test
```javascript
// Create workflow using n8n-mcp
const workflow = await n8n_create_workflow({
  name: "Monitor Switch Health",
  nodes: [...],
  connections: {...}
});

// Export workflow
const workflowExport = await n8n_get_workflow({ id: workflow.id });
await write_file(
  `${baseDir}/${workflowName}/workflow.json`, 
  JSON.stringify(workflowExport, null, 2)
);
```

## HPE Aruba API Reference

### 1. Aruba Central
```javascript
// Device Management
GET /api/v2/devices - List all devices
GET /api/v2/devices/{serial} - Device details
POST /api/v2/devices/command - Execute commands

// Monitoring
GET /api/v2/monitoring/stats - Performance metrics
GET /api/v2/alerts - Active alerts
POST /api/v2/webhooks - Configure webhooks
```

### 2. AOS-CX (Switches)
```javascript
// System
GET /rest/v10.08/system - System info
GET /rest/v10.08/system/interfaces - All interfaces

// VLANs
GET /rest/v10.08/system/vlans - List VLANs
POST /rest/v10.08/system/vlans - Create VLAN
```

### 3. EdgeConnect (SD-WAN)
```javascript
// Appliances
GET /api/appliances - List appliances
GET /api/appliances/{id}/stats - Performance stats

// Policies
GET /api/policies/qos - QoS policies
POST /api/policies/security - Security rules
```

### 4. UXI
```javascript
// Tests
GET /api/v1/tests - List tests
GET /api/v1/tests/{id}/results - Test results

// Metrics
GET /api/v1/metrics/network - Network metrics
GET /api/v1/metrics/application - App performance
```

## Common Patterns

### Pattern 1: Scheduled Health Monitoring (TESTED & WORKING)
**File**: `monitoring-alerting-workflows/device-health-monitoring-workflow-WORKING.json`

```json
{
  "name": "Device Health Monitor",
  "nodes": [
    {
      "id": "node-1",
      "name": "Every 5 minutes",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {
        "rule": {
          "interval": [{"field": "minutes", "minutesInterval": 5}]
        }
      }
    },
    {
      "id": "node-2",
      "name": "Get Device Health",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [450, 300],
      "parameters": {
        "method": "GET",
        "url": "https://central.arubanetworks.com/api/v2/monitoring/stats",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpHeaderAuth"
      }
    }
  ],
  "connections": {
    "Every 5 minutes": {
      "main": [[{"node": "Get Device Health", "type": "main", "index": 0}]]
    }
  }
}
```

**Key Requirements for n8n Workflows:**
- All nodes must have `id`, `typeVersion`, and `position`
- Connections use node **names**, not IDs
- Use proper parameter structure for each node type

### Pattern 2: Event-Driven Response (TESTED & WORKING)
**File**: `security-event-response-automation/edgeconnect-alert-handler-WORKING.json`

Webhook-based workflow processes EdgeConnect alerts with validation and routing.

**Webhook URL**: `http://192.168.40.100:8006/webhook/edgeconnect-alert`

### Pattern 3: Bulk Configuration
```javascript
// Get devices to configure
const devices = await getDeviceList({ type: 'switch', location: 'datacenter' });

// Apply configuration in batches
for (const batch of chunk(devices, 10)) {
  await Promise.all(batch.map(device => 
    applyConfiguration({
      deviceId: device.id,
      template: 'standard_switch_config',
      variables: { vlan: device.vlan, location: device.location }
    })
  ));
  await sleep(5000); // Wait between batches
}
```

## Error Handling Patterns

### Comprehensive Error Management
```javascript
{
  "name": "Error Handler",
  "type": "n8n-nodes-base.errorTrigger",
  "parameters": {},
  "position": [250, 500]
}
```

### API Error Recovery
```javascript
// Function node for smart retry
const maxRetries = 3;
const retryDelay = 5000;

for (let i = 0; i < maxRetries; i++) {
  try {
    const response = await $http.request(options);
    return [{ json: response }];
  } catch (error) {
    if (error.response?.status === 429) {
      await new Promise(r => setTimeout(r, retryDelay * (i + 1)));
    } else if (error.response?.status >= 500) {
      await new Promise(r => setTimeout(r, retryDelay));
    } else {
      throw error;
    }
  }
}
throw new Error('Max retries exceeded');
```

## Security Best Practices

### Credential Management
```javascript
// Always use n8n credential store
const credentials = $getCredentials('arubaApiAuth');

// Never hardcode secrets
// BAD: const apiKey = "sk-1234567890";
// GOOD: const apiKey = credentials.apiKey;
```

### Input Validation
```javascript
// Validate webhook inputs
const schema = {
  type: 'object',
  properties: {
    deviceId: { type: 'string', pattern: '^[A-Z0-9]{12}$' },
    action: { type: 'string', enum: ['restart', 'update', 'check'] }
  },
  required: ['deviceId', 'action']
};

if (!validateSchema(items[0].json, schema)) {
  throw new Error('Invalid input data');
}
```

## Quick Commands

```javascript
// Create workflow directory structure
const workflowName = "my-new-workflow";
const dirs = [
  `/Users/jeangiet/Documents/Claude/aruba-workflows/${workflowName}`,
  `/Users/jeangiet/Documents/Claude/aruba-workflows/${workflowName}/config`,
  `/Users/jeangiet/Documents/Claude/aruba-workflows/${workflowName}/tests`,
  `/Users/jeangiet/Documents/Claude/aruba-workflows/${workflowName}/docs`
];
for (const dir of dirs) {
  await create_directory(dir);
}

// List available nodes for Aruba automation
await search_nodes({ query: "http webhook schedule" });

// Get node documentation
await get_node_documentation({ nodeType: "nodes-base.httpRequest" });

// Validate workflow
await validate_workflow({ workflow: myWorkflow });

// Test API endpoint with comprehensive scenarios
const apiTest = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1500,
  content: "Test Aruba Central API endpoint /api/v2/devices with authentication, pagination, filtering, and error handling scenarios"
});
```

## Remember

1. **Always test APIs first** using postman-mcp
2. **Create organized directories** for each workflow
3. **Start simple** and add complexity incrementally
4. **Handle errors gracefully** at every step
5. **Document everything** for future maintenance
6. **Use n8n best practices** for node configuration
7. **Secure credentials** using n8n's credential store
8. **Monitor execution** with proper logging
9. **Create reusable patterns** for common tasks
10. **Export and version** all workflows

## Context Management

### Monitor Context Usage
- Track context usage continuously
- **AUTO-COMPACT at 75% utilization (25% remaining)**
- Provide work summary before limits
- Be proactive about context management

### Use `/clear` Command
**MANDATORY `/clear` after completing:**
- Major workflow implementations
- Large-scale API testing and collection creation
- Multi-file documentation updates
- Complex debugging sessions spanning multiple files
- Any task that generates 50+ lines of code/configuration
- Project milestone completions

### Session Handoff Protocol
Before context limits or after major completions:
```markdown
## Session Handoff Summary
### Project: [Name]
### Completed in This Session:
- [List major accomplishments]
- [Files created/modified]
- [Workflows implemented]
- [Tests completed]

### Current Status:
- [What's working]
- [What needs fixes]
- [Immediate next steps]

### Context for Next Session:
- [Key information to remember]
- [Important file locations]
- [Specific implementation details]

**Ready for `/clear` - Major milestone completed**
```

## Task Management

### When Working on Tasks:
1. **Mark completed tasks immediately** in TASKS.md using `[x]`
2. **Add newly discovered tasks** to appropriate milestone
3. **Update CLAUDE.md** with new patterns or learnings
4. **Document blockers** in TASKS.md with notes

## API Development with Postman

### REST API Workflow
1. **Design First**: Create specifications before implementation
2. **Test Continuously**: Implement automated testing
3. **Document Live**: Generate from working collections
4. **Monitor Production**: Set up monitoring/alerting

### Aruba API Testing Patterns with Postman MCP

#### Authentication Flow Testing
```javascript
// Test complete OAuth 2.0 flow for Aruba Central
const authFlowTest = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1500,
  content: `Create comprehensive OAuth 2.0 test flow for Aruba Central API:
    1. Client credentials grant request
    2. Access token validation
    3. Token refresh handling
    4. Expired token scenarios
    5. Invalid credentials handling
    6. Rate limiting on auth endpoints
    
    Include proper error handling and retry logic.`
});
```

#### Device Management API Testing
```javascript
// Batch test device management endpoints
const deviceTestBatch = await mcp__postman_mcp__create_message_batch({
  requests: [
    {
      custom_id: "list_devices",
      params: {
        model: "claude-sonnet-4-20250514",
        max_tokens: 800,
        messages: [{
          role: "user",
          content: "Test GET /api/v2/devices with pagination, filtering by device_type, status, and location"
        }]
      }
    },
    {
      custom_id: "device_details",
      params: {
        model: "claude-sonnet-4-20250514", 
        max_tokens: 800,
        messages: [{
          role: "user",
          content: "Test GET /api/v2/devices/{serial} with valid and invalid serial numbers"
        }]
      }
    }
  ]
});
```

## Test-Driven Development (TDD)

### 1. Write Tests First
- Comprehensive tests from input/output pairs
- **For APIs**: Create Postman collections with test scripts using MCP
- **Do NOT** create implementations or mocks
- Cover happy paths, edge cases, errors
- Make tests independent and repeatable

### 2. Confirm Test Failures
- Run tests, confirm expected failures
- **For APIs**: Execute Postman collections using MCP testing tools
- Show test failures for verification
- Ensure clear, informative output

### 3. Implement to Pass Tests
- Write implementation code only
- **For APIs**: Build endpoints to satisfy Postman tests
- Iterate until 100% pass
- Show results after each change

## Documentation Template

### For Each Workflow Created
```markdown
# Workflow: [Name]

## Purpose
[What this workflow automates]

## Trigger
- Type: [webhook/schedule/manual]
- Configuration: [details]

## Process Flow
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Configuration
- `PARAM_1`: [description] (default: value)
- `PARAM_2`: [description] (required)

## Error Handling
- [Error type 1]: [How it's handled]
- [Error type 2]: [How it's handled]

## Dependencies
- APIs: [which Aruba APIs]
- Credentials: [required credentials]
- External services: [any third-party services]
```

## Directory Structure Templates

### README.md Template
```markdown
# Workflow: [Workflow Name]

## Overview
Brief description of what this workflow automates.

## File Structure
- `workflow.json` - The n8n workflow export
- `config/` - Configuration files and credential requirements
- `tests/` - Test data and results
- `docs/` - Additional documentation

## Quick Start
1. Import workflow.json into n8n
2. Configure credentials (see config/credentials.md)
3. Update parameters in config/parameters.json
4. Test with sample data in tests/
5. Deploy to production

## Support
Contact: [team/person responsible]
Last Updated: [date]
```

## New Discoveries Log

### 2025-07-17: Enhanced Postman MCP Integration for API Testing
- **Discovery**: Postman MCP provides comprehensive API testing capabilities through Claude AI
- **Details**: Available tools include message batching, conversational testing, debugging, and documentation generation
- **Key Features**: 
  - `send_message_to_claude()` for single API test scenarios
  - `create_message_batch()` for parallel endpoint testing
  - `python_bug_buster()` for debugging API integration code
  - `count_message_tokens()` for optimization
- **Impact**: Enables comprehensive TDD workflows for Aruba API integration with n8n workflows

### 2025-07-17: Advanced Context Management with Auto-Compact and Clear Rules
- **Discovery**: Implemented automated context management for complex workflow development sessions
- **Details**: Auto-compact triggers at 75% context usage (25% remaining) with mandatory /clear after major tasks
- **Key Features**:
  - Automatic context compaction when usage reaches 75%
  - Mandatory `/clear` after major workflow implementations, API testing, documentation updates
  - Session handoff summaries for complex multi-session work
  - Context size monitoring with 200+ line triggers
- **Impact**: Prevents context overflow, maintains session efficiency, enables complex long-running automation projects

This comprehensive guide ensures you can efficiently build reliable, secure, and maintainable n8n workflows for HPE Aruba network automation with proper organization.
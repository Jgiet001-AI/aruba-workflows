# CLAUDE.md - HPE Aruba n8n Workflows Guide

Comprehensive guide for building intelligent n8n workflows that automate HPE Aruba networking tasks.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Session Management](#session-management)
3. [Workflow Development Process](#workflow-development-process)
4. [API Reference & Testing](#api-reference--testing)
5. [Common Patterns](#common-patterns)
6. [Development Methodologies](#development-methodologies)
7. [Quality Assurance](#quality-assurance)
8. [Project Management](#project-management)
9. [Reference & Templates](#reference--templates)

---

## Quick Start

### Session Initialization Checklist
At the beginning of each session, execute these steps:

1. **Read Planning Documents**: Check project context and strategy
2. **Review Tasks**: Check pending tasks and current milestone
3. **Verify Environment**: Confirm n8n connectivity and MCP availability
4. **Check Workflows**: See existing workflows to avoid duplication

```javascript
// Required startup sequence
await read_file("/Users/jeangiet/Documents/Claude/aruba-workflows/PLANNING.md");
await read_file("/Users/jeangiet/Documents/Claude/aruba-workflows/TASKS.md");
await n8n_health_check();
await list_directory("/Users/jeangiet/Documents/Claude/aruba-workflows");
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

---

## Session Management

## Task Management

### When Working on Tasks:
1. **Mark completed tasks immediately** in TASKS.md using `[x]`
2. **Add newly discovered tasks** to appropriate milestone
3. **Update CLAUDE.md** with new patterns or learnings
4. **Document blockers** in TASKS.md with notes

```javascript
// Example: Marking task complete
const tasksContent = await read_file("TASKS.md");
const updatedTasks = tasksContent.replace(
  "- [ ] Create device health monitoring workflow",
  "- [x] Create device health monitoring workflow"
);
await write_file("TASKS.md", updatedTasks);

// Example: Adding new discovery to CLAUDE.md
const discovery = `
### New Pattern Discovered: ${new Date().toISOString().split('T')[0]}
- **Pattern**: Batch processing for AOS-CX improves performance
- **Details**: Process switches in groups of 10 with 5s delay
- **Example**: See bulk-config-updater workflow
`;
const claudeMd = await read_file("CLAUDE.md");
await write_file("CLAUDE.md", claudeMd + "\n" + discovery);
```

### Updating CLAUDE.md with New Discoveries
When you discover new patterns, API behaviors, or solutions:
1. Add them to the relevant section
2. Include date of discovery
3. Provide working example
4. Update any affected patterns

Example sections to update:
- **API Integration Patterns** - New API endpoints or behaviors
- **Common Workflow Patterns** - Reusable workflow designs
- **Error Handling Patterns** - New error scenarios and solutions
- **Performance Optimization** - Speed improvements discovered
- **Common Issues & Solutions** - Problems encountered and fixes

## Quick Context

**Your Role**: Build n8n workflows that automate HPE Aruba networking tasks based on user requirements.
**Available Tools**: n8n-mcp for workflow creation, postman-mcp for API testing, filesystem for exports
**Target**: Create production-ready workflows with monitoring, error handling, and documentation

## Available MCP Servers

### Primary Tools
```yaml
n8n-mcp: 
  url: "http://192.168.40.100:8006"
  use_for: "Create, update, execute workflows"
  
postman-mcp:
  location: "/Users/jeangiet/Documents/postman-mcp-server/"
  use_for: "Test HPE Aruba APIs before implementation"
  
filesystem:
  paths: 
    - "/Users/jeangiet/Downloads"
    - "/Users/jeangiet/Documents/Claude"
  use_for: "Save workflow exports, documentation"
```

## Workflow Building Process

### 1. Understand Requirements
```javascript
// Questions to ask the user:
- What specific network task needs automation?
- Which Aruba products are involved? (Central, AOS-CX, EdgeConnect, UXI)
- What triggers this automation? (schedule, event, manual)
- What should happen on success/failure?
- Who needs to be notified?
```

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
await create_directory(`${baseDir}/${workflowName}/versions`);

// Create initial files
await write_file(`${baseDir}/${workflowName}/README.md`, workflowReadmeTemplate);
await write_file(`${baseDir}/${workflowName}/config/parameters.json`, defaultParams);
```

### 3. Test APIs First
```javascript
// Use postman-mcp to validate APIs before implementation:

// Test API authentication and basic connectivity
const authTest = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1000,
  content: `Test Aruba Central API authentication for endpoint GET /api/v2/devices with proper OAuth 2.0 flow and explain response structure`
});

// Create comprehensive API test collection
const collectionTest = await mcp__postman_mcp__create_message_batch({
  requests: [
    {
      custom_id: "aruba_central_auth",
      params: {
        model: "claude-sonnet-4-20250514",
        max_tokens: 800,
        messages: [{
          role: "user", 
          content: "Create OAuth 2.0 authentication test for Aruba Central API"
        }]
      }
    },
    {
      custom_id: "aruba_devices_endpoint",
      params: {
        model: "claude-sonnet-4-20250514",
        max_tokens: 800,
        messages: [{
          role: "user",
          content: "Design comprehensive tests for /api/v2/devices endpoint including error scenarios"
        }]
      }
    }
  ]
});

// Test specific API scenarios
const deviceHealthTest = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1200,
  content: `Create test scenarios for Aruba device health monitoring API:
    - Normal device status check
    - High CPU/memory usage scenarios 
    - Network connectivity issues
    - Authentication failures
    - Rate limiting responses`
});

// Save comprehensive API test results
await write_file(`${baseDir}/${workflowName}/tests/api-validation.json`, {
  authentication: authTest,
  collection_tests: collectionTest,
  device_health_scenarios: deviceHealthTest,
  timestamp: new Date().toISOString()
});

// Create validation report
const validationReport = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514", 
  max_tokens: 1000,
  content: `Generate API validation report for Aruba Central integration including:
    - Endpoint availability
    - Authentication methods
    - Rate limits discovered
    - Error response formats
    - Recommended retry strategies`
});

await write_file(`${baseDir}/${workflowName}/tests/validation-report.md`, validationReport.content[0].text);
```

### 4. Design Workflow Structure
```javascript
// Standard workflow pattern
const workflowStructure = {
  trigger: "webhook|schedule|manual",
  dataCollection: "API calls to gather info",
  processing: "Transform and analyze data",
  decision: "Conditional logic",
  action: "Execute changes",
  verification: "Confirm success",
  notification: "Alert stakeholders"
};
```

### 5. Build and Test
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

// Validate before deployment
await validate_workflow({ workflow });

// Document test results
await write_file(
  `${baseDir}/${workflowName}/tests/test-results.md`,
  testResultsMarkdown
);
```

## HPE Aruba API Reference

### Available APIs and Common Endpoints

#### 1. Aruba Central
```javascript
// Device Management
GET /api/v2/devices - List all devices
GET /api/v2/devices/{serial} - Device details
POST /api/v2/devices/command - Execute commands

// Monitoring
GET /api/v2/monitoring/stats - Performance metrics
GET /api/v2/alerts - Active alerts
POST /api/v2/webhooks - Configure webhooks

// Configuration
GET /api/v2/configuration/templates - List templates
POST /api/v2/configuration/apply - Apply config
```

#### 2. AOS-CX (Switches)
```javascript
// System
GET /rest/v10.08/system - System info
GET /rest/v10.08/system/interfaces - All interfaces

// VLANs
GET /rest/v10.08/system/vlans - List VLANs
POST /rest/v10.08/system/vlans - Create VLAN

// Ports
GET /rest/v10.08/system/interfaces/{port} - Port details
PUT /rest/v10.08/system/interfaces/{port} - Update port
```

#### 3. EdgeConnect (SD-WAN)
```javascript
// Appliances
GET /api/appliances - List appliances
GET /api/appliances/{id}/stats - Performance stats

// Policies
GET /api/policies/qos - QoS policies
POST /api/policies/security - Security rules
```

#### 4. UXI
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
          "interval": [
            {
              "field": "minutes",
              "minutesInterval": 5
            }
          ]
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
        "nodeCredentialType": "httpHeaderAuth",
        "options": {
          "timeout": 30000
        }
      }
    },
    {
      "id": "node-3",
      "name": "Check CPU Threshold",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [650, 300],
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "id": "condition-1",
              "leftValue": "={{$json.cpu_usage}}",
              "rightValue": 80,
              "operator": {
                "type": "number",
                "operation": "gt"
              }
            }
          ],
          "combinator": "and"
        }
      }
    },
    {
      "id": "node-4",
      "name": "Send Alert",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [850, 200],
      "parameters": {
        "functionCode": "// Send alert notification\nconst deviceName = $input.first().json.device_name || 'Unknown Device';\nconst cpuUsage = $input.first().json.cpu_usage || 0;\n\nreturn [{\n  json: {\n    message: `High CPU usage detected on ${deviceName}: ${cpuUsage}%`,\n    severity: 'warning',\n    timestamp: new Date().toISOString(),\n    device: deviceName,\n    metric: 'cpu_usage',\n    value: cpuUsage,\n    threshold: 80\n  }\n}];"
      }
    }
  ],
  "connections": {
    "Every 5 minutes": {
      "main": [
        [
          {
            "node": "Get Device Health",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Device Health": {
      "main": [
        [
          {
            "node": "Check CPU Threshold",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Check CPU Threshold": {
      "main": [
        [
          {
            "node": "Send Alert",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1",
    "saveDataErrorExecution": "all",
    "saveDataSuccessExecution": "all",
    "saveManualExecutions": true,
    "saveExecutionProgress": true
  },
  "active": false
}
```

**Key Requirements for n8n Workflows:**
- All nodes must have `id`, `typeVersion`, and `position`
- Connections use node **names**, not IDs
- Use proper parameter structure for each node type

### Pattern 2: Event-Driven Response (TESTED & WORKING)
**File**: `security-event-response-automation/edgeconnect-alert-handler-WORKING.json`

This webhook-based workflow processes EdgeConnect alerts with validation and routing:

```json
{
  "name": "EdgeConnect Alert Handler",
  "nodes": [
    {
      "id": "webhook-1",
      "name": "EdgeConnect Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "parameters": {
        "path": "edgeconnect-alert",
        "httpMethod": "POST",
        "responseMode": "responseNode"
      }
    },
    {
      "id": "validate-1", 
      "name": "Validate Input",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [450, 300],
      "parameters": {
        "functionCode": "// Validate EdgeConnect alert payload\nconst payload = $input.first().json;\n\nif (!payload.alert_type || !payload.device_id || !payload.severity) {\n  throw new Error('Invalid EdgeConnect alert payload: missing required fields');\n}\n\n// Parse and enrich the alert\nreturn [{\n  json: {\n    ...payload,\n    processed_at: new Date().toISOString(),\n    source: 'EdgeConnect',\n    validated: true\n  }\n}];"
      }
    },
    {
      "id": "route-1",
      "name": "Route by Severity", 
      "type": "n8n-nodes-base.switch",
      "typeVersion": 3,
      "position": [650, 300],
      "parameters": {
        "values": {
          "options": [
            {
              "conditions": {
                "conditions": [
                  {
                    "leftValue": "={{$json.severity}}",
                    "rightValue": "critical",
                    "operator": {
                      "type": "string",
                      "operation": "equals"
                    }
                  }
                ]
              },
              "outputIndex": 0
            },
            {
              "conditions": {
                "conditions": [
                  {
                    "leftValue": "={{$json.severity}}",
                    "rightValue": "warning", 
                    "operator": {
                      "type": "string",
                      "operation": "equals"
                    }
                  }
                ]
              },
              "outputIndex": 1
            }
          ]
        }
      }
    }
  ],
  "connections": {
    "EdgeConnect Webhook": {
      "main": [[{"node": "Validate Input", "type": "main", "index": 0}]]
    },
    "Validate Input": {
      "main": [[{"node": "Route by Severity", "type": "main", "index": 0}]]
    },
    "Route by Severity": {
      "main": [
        [{"node": "Handle Critical", "type": "main", "index": 0}],
        [{"node": "Handle Warning", "type": "main", "index": 0}]
      ]
    }
  }
}
```

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
      variables: {
        vlan: device.vlan,
        location: device.location
      }
    })
  ));
  
  // Wait between batches
  await sleep(5000);
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

// Connect to notification node
{
  "name": "Error Notification",
  "type": "n8n-nodes-base.emailSend",
  "parameters": {
    "toEmail": "network-team@company.com",
    "subject": "Workflow Error: {{$node.error.node}}",
    "text": "Error: {{$node.error.message}}\n\nWorkflow: {{$workflow.name}}\nTime: {{$now}}"
  }
}
```

### API Error Recovery
```javascript
// Function node for smart retry
const maxRetries = 3;
const retryDelay = 5000;

for (let i = 0; i < maxRetries; i++) {
  try {
    // Make API call
    const response = await $http.request(options);
    return [{ json: response }];
  } catch (error) {
    if (error.response?.status === 429) {
      // Rate limited - wait longer
      await new Promise(r => setTimeout(r, retryDelay * (i + 1)));
    } else if (error.response?.status >= 500) {
      // Server error - retry
      await new Promise(r => setTimeout(r, retryDelay));
    } else {
      // Client error - don't retry
      throw error;
    }
  }
}

throw new Error('Max retries exceeded');
```

## Workflow Optimization

### Performance Tips
```javascript
// 1. Batch API calls
const batchSize = 50;
const results = [];

for (let i = 0; i < items.length; i += batchSize) {
  const batch = items.slice(i, i + batchSize);
  const batchResults = await processBatch(batch);
  results.push(...batchResults);
}

// 2. Cache frequently used data
const cacheKey = `device_list_${location}`;
let devices = cache.get(cacheKey);

if (!devices) {
  devices = await fetchDevices(location);
  cache.set(cacheKey, devices, 300); // 5 min cache
}

// 3. Parallel processing
const results = await Promise.all([
  getDeviceHealth(deviceId),
  getDeviceConfig(deviceId),
  getDeviceAlerts(deviceId)
]);
```

## Testing Workflows

### Pre-deployment Checklist
```markdown
- [ ] Test with sample data
- [ ] Verify error handling paths
- [ ] Check API rate limits
- [ ] Validate credentials
- [ ] Test rollback procedures
- [ ] Confirm notifications work
- [ ] Document configuration options
```

### Testing Code
```javascript
// Use n8n's test webhook
const testWebhook = {
  url: "http://192.168.40.100:8006/webhook-test/abc123",
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: {
    test: true,
    device: "test-switch-01",
    metrics: {
      cpu: 85,
      memory: 70,
      temperature: 45
    }
  }
};
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

## Monitoring
- Success metric: [what indicates success]
- Failure alerts: [who gets notified]

## Dependencies
- APIs: [which Aruba APIs]
- Credentials: [required credentials]
- External services: [any third-party services]
```

## Quick Commands

```javascript
// CONTEXT MANAGEMENT: Check usage before major operations
const contextUsage = getCurrentContextUsage();
if (contextUsage >= 0.75) {
  // Provide summary and compact immediately
  console.log(`Context at ${Math.round(contextUsage * 100)}% - Compacting now`);
}

// Create workflow directory structure
const workflowName = "my-new-workflow";
const dirs = [
  `/Users/jeangiet/Documents/Claude/aruba-workflows/${workflowName}`,
  `/Users/jeangiet/Documents/Claude/aruba-workflows/${workflowName}/config`,
  `/Users/jeangiet/Documents/Claude/aruba-workflows/${workflowName}/tests`,
  `/Users/jeangiet/Documents/Claude/aruba-workflows/${workflowName}/docs`,
  `/Users/jeangiet/Documents/Claude/aruba-workflows/${workflowName}/versions`
];
for (const dir of dirs) {
  await create_directory(dir);
}

// After completing workflow creation - USE /clear
console.log("Workflow creation complete - Ready for /clear command");

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

// Create batch tests for multiple API endpoints
const batchApiTests = await mcp__postman_mcp__create_message_batch({
  requests: [
    {
      custom_id: "devices_test",
      params: {
        model: "claude-sonnet-4-20250514",
        max_tokens: 1000,
        messages: [{ role: "user", content: "Test /api/v2/devices endpoint" }]
      }
    },
    {
      custom_id: "alerts_test", 
      params: {
        model: "claude-sonnet-4-20250514",
        max_tokens: 1000,
        messages: [{ role: "user", content: "Test /api/v2/alerts endpoint" }]
      }
    },
    {
      custom_id: "stats_test",
      params: {
        model: "claude-sonnet-4-20250514", 
        max_tokens: 1000,
        messages: [{ role: "user", content: "Test /api/v2/monitoring/stats endpoint" }]
      }
    }
  ]
});

// Debug code issues with Python Bug Buster
const debugAssistance = await mcp__postman_mcp__python_bug_buster({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1200
});

// Count tokens for API documentation
const tokenCount = await mcp__postman_mcp__count_message_tokens({
  model: "claude-sonnet-4-20250514",
  messages: [
    { role: "user", content: "Generate comprehensive API documentation for Aruba Central device management" }
  ]
});
```

## Common Issues & Solutions

### Issue: API Authentication Fails
```javascript
// Solution: Check credential configuration
const testAuth = {
  url: "https://central.arubanetworks.com/api/v2/auth/validate",
  headers: {
    "Authorization": `Bearer ${credentials.accessToken}`,
    "X-API-Version": "2"
  }
};
```

### Issue: Workflow Times Out
```javascript
// Solution: Increase timeout and add progress tracking
{
  "options": {
    "timeout": 120000, // 2 minutes
    "maxContentLength": 50000000 // 50MB
  }
}
```

### Issue: Rate Limiting
```javascript
// Solution: Implement rate limit handling
const rateLimiter = {
  maxRequests: 100,
  perMinute: 60,
  backoffMultiplier: 2
};
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
11. **AUTO-COMPACT at 75% context usage** (25% remaining)
12. **Use `/clear` after completing major tasks** (workflows, collections, documentation)
13. **Monitor context continuously** and provide summaries before limits
14. **Create session handoffs** for complex multi-session work

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
- `versions/` - Version history

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

### config/parameters.json Template
```json
{
  "environment": {
    "description": "Target environment",
    "default": "production",
    "options": ["development", "staging", "production"]
  },
  "alertThresholds": {
    "cpu": {
      "description": "CPU usage threshold for alerts (%)",
      "default": 80,
      "min": 50,
      "max": 95
    },
    "memory": {
      "description": "Memory usage threshold for alerts (%)",
      "default": 85,
      "min": 50,
      "max": 95
    }
  },
  "notificationChannels": {
    "slack": {
      "description": "Slack channel for alerts",
      "default": "#network-alerts"
    },
    "email": {
      "description": "Email addresses for critical alerts",
      "default": ["network-team@company.com"]
    }
  }
}
```

This guide ensures you can efficiently build reliable, secure, and maintainable n8n workflows for HPE Aruba network automation with proper organization.

---

## New Discoveries Log

### 2025-07-17: Enhanced Postman MCP Integration for API Testing
- **Discovery**: Postman MCP provides comprehensive API testing capabilities through Claude AI
- **Details**: Available tools include message batching, conversational testing, debugging, and documentation generation
- **Implementation**: Integrated mcp__postman_mcp__ tools throughout CLAUDE.md for complete API testing workflows
- **Key Features**: 
  - `send_message_to_claude()` for single API test scenarios
  - `create_message_batch()` for parallel endpoint testing
  - `multiple_conversational_turns()` for workflow testing
  - `python_bug_buster()` for debugging API integration code
  - `create_website()` for generating API documentation
  - `count_message_tokens()` for optimization
- **Impact**: Enables comprehensive TDD workflows for Aruba API integration with n8n workflows

### 2025-07-17: Advanced Context Management with Auto-Compact and Clear Rules
- **Discovery**: Implemented automated context management for complex workflow development sessions
- **Details**: Auto-compact triggers at 75% context usage (25% remaining) with mandatory /clear after major tasks
- **Implementation**: Added comprehensive context monitoring, session handoff protocols, and auto-clear triggers
- **Key Features**:
  - Automatic context compaction when usage reaches 75%
  - Mandatory `/clear` after major workflow implementations, API testing, documentation updates
  - Session handoff summaries for complex multi-session work
  - Context size monitoring with 200+ line triggers
  - Big task completion markers (workflows, collections, validations)
- **Impact**: Prevents context overflow, maintains session efficiency, enables complex long-running automation projects

### [Add new patterns, solutions, and learnings here with dates]

<!-- Example format:
### 2025-01-20: Bulk API Processing Pattern
- **Discovery**: AOS-CX API performs better with batched requests
- **Details**: Group 10-15 devices per request with 2s delays between batches
- **Implementation**: See `bulk-config-updater` workflow
- **Performance**: 3x faster than individual requests

### 2025-01-21: Rate Limit Handling for Central API
- **Discovery**: Central API has undocumented 100 req/min limit
- **Details**: Implement exponential backoff starting at 5s
- **Implementation**: Added to HTTP Request error handling
- **Impact**: Reduced 429 errors by 95%

### 2025-01-16: Complete API Endpoint Extraction via Postman API
- **Discovery**: Successfully extracted 1,397 endpoints from all HPE Aruba collections
- **Details**: Used Postman API key to programmatically access all collections
- **Implementation**: Created `fetch_postman_collections.py` script for automated extraction
- **Results**: Complete coverage of GET(751), POST(294), PUT(150), PATCH(19), DELETE(183)

### 2025-01-16: Product-Based Configuration Management Categorization
- **Discovery**: Logical product categorization enables targeted n8n workflows
- **Details**: 15 product categories identified with configuration-specific endpoints
- **Top Categories**: Central Platform (208 config), Access Points (141 config), AOS-CX (81 config)
- **Implementation**: Created `categorize_by_product.py` for automated product classification
- **Priority**: HIGH for Central/APs/AOS-CX, MEDIUM for EdgeConnect, LOW for specialized services

## Context Management

### Monitor Context Usage
- Track context usage continuously
- **AUTO-COMPACT at 75% utilization (25% remaining)**
- Provide work summary before limits
- Be proactive about context management

### Automatic Context Compaction (25% Rule)
When context usage reaches 75% (25% remaining):
```javascript
// Auto-compact trigger
const contextUsage = getCurrentContextUsage();
if (contextUsage >= 0.75) {
  // Immediately provide summary and compact
  return `## Context Usage Alert: ${Math.round(contextUsage * 100)}%

### Work Summary
- Current task: ${currentTask}
- Completed: ${completedItems}
- In progress: ${inProgressItems}
- Next steps: ${nextSteps}

### Key Discoveries
${keyFindings}

### Files Modified
${modifiedFiles}

**COMPACTING NOW** - Context at ${Math.round(contextUsage * 100)}%`;
}
```

### Use `/clear` Command
**MANDATORY `/clear` after completing:**
- Major workflow implementations (like our n8n workflow builds)
- Large-scale API testing and collection creation
- Multi-file documentation updates
- Complex debugging sessions spanning multiple files
- Any task that generates 50+ lines of code/configuration
- Project milestone completions

Use `/clear` between:
- Unrelated tasks or features
- Completed TDD cycles
- Different codebase sections
- Lengthy debugging sessions
- Cluttered context

### Auto-Clear Triggers
**Immediately use `/clear` after:**
```javascript
// Big task completion triggers
const bigTaskMarkers = [
  'Successfully created n8n workflow',
  'Completed comprehensive API testing',
  'Generated multiple Postman collections', 
  'Updated extensive documentation',
  'Implemented complex automation',
  'Finished multi-step validation',
  'Completed project milestone'
];

// Context size triggers
const contextLines = getContextLineCount();
if (contextLines > 200 || taskComplexity === 'high') {
  executeCommand('/clear');
}
```

### Context Compaction Strategy
When approaching 75% context usage:
1. **Immediate Summary**: Provide comprehensive work summary
2. **Key Findings**: Document important discoveries
3. **File Status**: List all modified files and locations
4. **Next Steps**: Clear action items for continuation
5. **Execute Compact**: Use tools to reduce context while preserving essential information

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

### Create Snapshots at Milestones
When completing significant work:
1. Summarize accomplishments
2. Note current codebase state
3. List pending tasks
4. Highlight important decisions
5. Provide file locations and changes

**Snapshot triggers**: TDD cycles, features, bug fixes, code reviews

### Handle Session Continuations
- Review provided snapshots
- Confirm codebase understanding
- Identify next priority tasks
- Continue established patterns

---

## Planning Documentation Workflow

### When to Create Planning Documents
- New features or major changes
- Complex multi-step problems
- Substantial project scope
- Multi-session work

### Create planning.md
**Required sections**:
1. **Project Overview**: Description, success criteria, constraints
2. **Technical Approach**: Architecture, technology choices, integrations
3. **Implementation Strategy**: Workflows (TDD/visual/etc.), git strategy, testing
4. **Context Management**: Session boundaries, snapshots, handoffs
5. **Risk Assessment**: Challenges, dependencies, fallbacks

### Create tasks.md
**Structure**:
```markdown
# Tasks for [Project Name]

## Phase 1: Setup and Research
- [ ] Task with acceptance criteria
- [ ] Workflow: [TDD/Visual/Standard]
- [ ] Context usage: [Low/Medium/High]
- [ ] Dependencies: [List]
- [ ] Files: [List]
```

### Follow Planning Strictly
- Adhere to documents **to the letter**
- No deviations without user approval
- Reference frequently during implementation
- Update tasks.md as completed
- Move finished tasks to "Completed" section

### Handle Vague Prompts
**Context enrichment process**:
1. **Analyze context**: Review codebase patterns, git history, structure
2. **Enrich prompt**: Suggest approaches, acceptance criteria, workflows
3. **Present proposal**: "Based on codebase context, I suggest..."
4. **Seek confirmation**: Get approval before proceeding

---

## Git and GitHub Operations

### Git Operations
- **History analysis**: Search commits for changes, ownership, design decisions
- **Commit messages**: Auto-compose using changes and context
- **Complex operations**: Reverting, rebase conflicts, patch comparison

### GitHub Operations
- **Pull requests**: Generate from diff and context (understand "pr" shorthand)
- **Code review**: Fix comments and push to PR branch
- **Build fixes**: Resolve failing builds and linter warnings
- **Issue management**: Categorize, triage, bulk operations

---

## API Development with Postman

### REST API Workflow
1. **Design First**: Create specifications before implementation
2. **Test Continuously**: Implement automated testing
3. **Document Live**: Generate from working collections
4. **Monitor Production**: Set up monitoring/alerting

### Integration Testing
**Test types**: Unit API, integration, contract, performance, security
**Test scripts**:
```javascript
pm.test("Status code is 200", () => pm.response.to.have.status(200));
pm.test("Schema validation", () => pm.response.to.have.jsonSchema(schema));
```

### API Documentation
Use Markdown for rich documentation:
- Example requests/responses
- Parameter constraints
- Authentication setup
- Error code explanations

### Scenario Testing
- Data-driven testing with iteration
- Multi-step workflow testing
- Edge case and error path scenarios

### Security & Authorization
- API key, Bearer token, OAuth implementation
- Input validation and injection protection
- Rate limiting and access control testing

---

## Test-Driven Development (TDD)

### 1. Write Tests First
- Comprehensive tests from input/output pairs
- **For APIs**: Create Postman collections with test scripts using MCP
- **Do NOT** create implementations or mocks
- Cover happy paths, edge cases, errors
- Make tests independent and repeatable

```javascript
// Example: Create comprehensive API test collection for Aruba Central
const apiTestCollection = await mcp__postman_mcp__create_message_batch({
  requests: [
    {
      custom_id: "auth_flow_test",
      params: {
        model: "claude-sonnet-4-20250514",
        max_tokens: 1000,
        messages: [{
          role: "user",
          content: `Create complete OAuth 2.0 authentication test suite for Aruba Central API including:
            - Valid credentials test
            - Invalid credentials test
            - Token expiration handling
            - Refresh token flow
            - Rate limiting scenarios`
        }]
      }
    },
    {
      custom_id: "device_management_tests",
      params: {
        model: "claude-sonnet-4-20250514",
        max_tokens: 1200,
        messages: [{
          role: "user", 
          content: `Create device management API test scenarios:
            - List all devices (GET /api/v2/devices)
            - Get device details by serial (GET /api/v2/devices/{serial})
            - Device command execution (POST /api/v2/devices/command)
            - Filter devices by type and status
            - Pagination testing
            - Invalid device serial handling
            - Permission denied scenarios`
        }]
      }
    },
    {
      custom_id: "monitoring_tests",
      params: {
        model: "claude-sonnet-4-20250514",
        max_tokens: 1000,
        messages: [{
          role: "user",
          content: `Create monitoring API test scenarios:
            - Performance metrics retrieval
            - Alert management
            - Webhook configuration
            - Real-time data streaming
            - Historical data queries`
        }]
      }
    }
  ]
});

// Get batch results and create test files
const batchResults = await mcp__postman_mcp__get_message_batch_result({
  msg_batch_id: apiTestCollection.id
});

// Save test collection for TDD workflow
await write_file(`${baseDir}/${workflowName}/tests/tdd-api-collection.json`, 
  JSON.stringify(batchResults, null, 2));
```

### 2. Confirm Test Failures
- Run tests, confirm expected failures
- **For APIs**: Execute Postman collections using MCP testing tools
- **Do NOT** write implementation code
- Show test failures for verification
- Ensure clear, informative output

```javascript
// Execute API tests and confirm failures before implementation
const testExecution = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1500,
  content: `Execute the test collection for Aruba Central API and show expected failures:
    1. Authentication should fail with invalid credentials
    2. Device endpoints should return 401 without auth
    3. Monitoring endpoints should handle rate limiting
    4. Error responses should match expected format
    
    Show test results with clear failure messages and expected vs actual outcomes.`
});

// Create multiple conversational test scenarios
const testConversation = await mcp__postman_mcp__multiple_conversational_turns({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1000,
  messages: [
    {
      role: "user",
      content: "Run authentication test for Aruba Central API"
    },
    {
      role: "assistant", 
      content: "Test failed as expected - no authentication credentials provided"
    },
    {
      role: "user",
      content: "Now test device listing endpoint without auth"
    },
    {
      role: "assistant",
      content: "401 Unauthorized returned as expected"
    },
    {
      role: "user",
      content: "Test monitoring stats with invalid device ID"
    }
  ]
});

// Document test failures for verification
await write_file(`${baseDir}/${workflowName}/tests/test-failures-log.md`, `
# Test Execution Results - Expected Failures

## Test Execution: ${new Date().toISOString()}

${testExecution.content[0].text}

## Conversational Test Results

${JSON.stringify(testConversation, null, 2)}

## Next Steps
- Implement authentication flow
- Create device management endpoints
- Add monitoring capabilities
- Implement error handling
`);
```

### 3. Commit Tests
- Commit with messages like "Add tests for [feature]"
- Include Postman collections for APIs
- Only commit when comprehensive

### 4. Implement to Pass Tests
- Write implementation code only
- **For APIs**: Build endpoints to satisfy Postman tests
- **Do NOT** modify tests
- Iterate until 100% pass
- Show results after each change

### 5. Commit Implementation
- Commit with "Implement [feature] - all tests passing"
- Only when ALL tests pass
- Verify clean, well-structured code

### TDD Best Practices
- Explicit about TDD methodology
- Separate test/implementation phases
- Use Postman automation for APIs
- Don't rush red-green-refactor cycle

---

## Complex Problem Solving

### 1. Research Phase
- Read relevant files/URLs first
- **Do NOT** write code during research
- Use subagents for complex investigations
- Document findings for planning

### 2. Planning Phase (Create Documentation)
- **Create planning.md and tasks.md** for substantial work
- Use extended thinking ("think", "think hard", "think harder", "ultrathink")
- Get explicit user approval
- Enrich vague prompts using codebase context

### 3. Implementation Phase (Follow Documentation)
- **Follow planning.md and tasks.md strictly**
- Execute tasks in specified order
- Apply specified workflows (TDD, visual, etc.)
- Update tasks.md as completed
- No deviations without approval

### 4. Completion Phase
- Verify all tasks completed
- Commit and create PRs as planned
- Update documentation as specified
- Create completion snapshot

---

## Visual Development Workflow

### Setup and Process
- Use screenshot tools (Puppeteer, simulator, manual)
- Accept visual mocks via copy/paste or file paths
- Implement designs based on mocks
- Take screenshots and compare with targets
- Iterate until visual match achieved (2-3 iterations typical)

---

## Quality Assurance & Code Review

### Quality Checks
**Code**: Linters, formatters, conventions, error handling, security
**APIs**: Postman testing, schema validation, performance, security
**Testing**: Integration, E2E, performance, security, accessibility
**Documentation**: API docs (Postman-generated), inline comments, README, ADRs, changelog

### Self-Review Process
1. Functionality review (acceptance criteria)
2. API contract review (schema matching)
3. Performance review (optimization opportunities)
4. Security review (validation, best practices)
5. Documentation review (Postman accuracy)
6. Maintainability review (readability, structure)
7. Integration review (patterns, conventions)

---

## Error Recovery & Debugging

### Test Failures
1. Isolate failing test
2. Examine failure message
3. Check environment/dependencies
4. Verify test setup/teardown
5. Use debugging tools
6. Document root cause and fix

### Implementation Blockers
1. Document issue clearly
2. Research similar problems
3. Propose alternatives
4. Seek clarification
5. Update planning if needed

### Conflict Resolution
- **Merge conflicts**: Analyze carefully, preserve functionality, test thoroughly
- **Planning conflicts**: Alert user, propose solutions, get approval

---

## Security & Performance

### Security Checklist
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Authentication verification
- [ ] Authorization checks
- [ ] Secure data handling
- [ ] HTTPS enforcement
- [ ] Rate limiting

### Performance Considerations
- Database optimization (N+1, indexing)
- Bundle size optimization
- Caching strategies
- Memory usage patterns
- API response times

---

## Documentation Standards

### Required Documentation
**Features**: README, API docs (Postman-generated), configuration, troubleshooting
**APIs**: Collections, authentication guides, error codes, rate limiting
**Code**: Function docs, business logic, performance notes, security implications
**Architecture**: ADRs, system diagrams, integration points, deployment requirements

### API Documentation with Postman
1. Create working collections using MCP tools
2. Add rich Markdown descriptions
3. Include realistic examples
4. Document scenarios and edge cases
5. Generate and publish documentation

```javascript
// Generate comprehensive API documentation
const apiDocs = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514",
  max_tokens: 2000,
  content: `Generate comprehensive API documentation for HPE Aruba Central including:
    - Authentication guide with OAuth 2.0 flow
    - All device management endpoints
    - Monitoring and alerting APIs
    - Configuration management APIs
    - Rate limiting and error handling
    - SDK examples in Python and JavaScript
    - Common use cases and workflows`
});

// Create website with API documentation
const websiteDocs = await mcp__postman_mcp__create_website({
  model: "claude-sonnet-4-20250514",
  max_tokens: 2000
});

// Save documentation
await write_file(`${baseDir}/docs/api-documentation.md`, apiDocs.content[0].text);
await write_file(`${baseDir}/docs/api-website.html`, websiteDocs.content[0].text);
```

### Aruba API Testing Patterns with Postman MCP

#### Pattern 1: Authentication Flow Testing
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

#### Pattern 2: Device Management API Testing
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
    },
    {
      custom_id: "device_commands",
      params: {
        model: "claude-sonnet-4-20250514",
        max_tokens: 1000,
        messages: [{
          role: "user",
          content: "Test POST /api/v2/devices/command for reboot, config sync, and firmware update commands"
        }]
      }
    }
  ]
});
```

#### Pattern 3: Monitoring and Alerting API Testing
```javascript
// Test monitoring endpoints with performance scenarios
const monitoringTests = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1500,
  content: `Design monitoring API test scenarios for Aruba Central:
    
    Performance Metrics Testing:
    - CPU, memory, temperature thresholds
    - Interface utilization stats
    - Radio performance metrics
    - Historical data queries
    
    Alert Management Testing:
    - Create/update alert rules
    - Test alert firing conditions  
    - Webhook delivery testing
    - Alert acknowledgment and clearing
    
    Include edge cases for high-volume data and rate limiting.`
});
```

#### Pattern 4: Configuration Management Testing
```javascript
// Test configuration management workflows
const configTests = await mcp__postman_mcp__multiple_conversational_turns({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1200,
  messages: [
    {
      role: "user",
      content: "Test configuration template creation for Aruba APs"
    },
    {
      role: "assistant",
      content: "Creating template test with SSID, security, and radio settings..."
    },
    {
      role: "user", 
      content: "Now test template application to device groups"
    },
    {
      role: "assistant",
      content: "Testing bulk template deployment with rollback scenarios..."
    },
    {
      role: "user",
      content: "Test configuration validation and conflict detection"
    }
  ]
});
```

#### Pattern 5: Error Handling and Edge Cases
```javascript
// Comprehensive error scenario testing
const errorHandlingTests = await mcp__postman_mcp__send_message_to_claude({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1800,
  content: `Create comprehensive error handling tests for Aruba APIs:
    
    Authentication Errors:
    - Invalid credentials (401)
    - Expired tokens (401) 
    - Insufficient permissions (403)
    - Rate limiting (429)
    
    Request Errors:
    - Invalid device serial (404)
    - Malformed JSON (400)
    - Missing required fields (400)
    - Invalid enum values (400)
    
    Server Errors:
    - Service unavailable (503)
    - Internal server error (500)
    - Timeout scenarios
    - Network connectivity issues
    
    Include retry strategies and exponential backoff patterns.`
});
```

---

## Project Lifecycle Management

### Project Initialization
- Directory structure, version control, .gitignore
- Development environment, dependencies
- Testing framework, documentation structure
- Coding standards, linting configuration

### Feature Development Lifecycle
1. **Planning**: Create planning.md and tasks.md
2. **Development**: Follow planned workflows
3. **Quality Assurance**: Run full QA checklist
4. **Documentation**: Update all relevant docs
5. **Review**: Self-review and prepare for user review
6. **Integration**: Merge with proper commits
7. **Verification**: Confirm integrated functionality

### Production Readiness Checklist
- [ ] All tests passing
- [ ] Security review completed
- [ ] Performance requirements met
- [ ] Documentation updated
- [ ] Configuration externalized
- [ ] Monitoring in place
- [ ] Error handling robust
- [ ] Rollback procedure tested

---

## Final Verification & Completion

### Before Declaring Work Complete
**Functionality**: Acceptance criteria met, tests passing, error handling
**Code Quality**: Conventions followed, no anti-patterns, security practices
**Documentation**: Comments, API docs, README, changelog
**Integration**: Clean integration, no breaking changes, migrations work
**Project Management**: Planning updated, tasks complete, clear commits, user informed

### Completion Summary Template
```markdown
## Work Completion Summary
### Completed Tasks: [List from tasks.md]
### Key Deliverables: [Main features/components]
### Technical Decisions: [Important architectural decisions]
### Testing Coverage: [Testing summary]
### Documentation Updated: [Created/updated docs]
### Next Steps: [Recommended follow-up]
### Quality Assurance: [QA checklist confirmation]
```

---

## General Development Principles

### Documentation and Planning
- Create planning documents for significant work
- Follow planning strictly once agreed
- Update documentation as work progresses
- Use planning for session consistency
- Enrich vague prompts with context

### Communication Style
- Be explicit about approach and reasoning
- Reference planning documents in decisions
- Ask for clarification when ambiguous
- Explain complex decisions and trade-offs

### Code Quality
- Follow existing patterns from planning
- Write clean, readable code
- Comment complex logic
- Use meaningful names
- Ensure implementation matches planned architecture

### Workflow Integration
- Include API development strategy in planning when applicable
- Use Postman collections in TDD for APIs
- Generate API documentation from working collections
- Include Postman collections in context snapshots
- Version control collections alongside code
- Verify API testing completion through collection runs

This comprehensive guide ensures Claude Code operates at maximum effectiveness while maintaining high quality standards and clear communication throughout the development process.
# CLAUDE.md - Claude Code Guide for Building HPE Aruba n8n Workflows

This guide helps Claude Code build intelligent n8n workflows for HPE Aruba network automation based on user requirements.

## Start of Every Conversation

**IMPORTANT: At the beginning of each session, Claude Code must:**
1. **Read PLANNING.md** - Check for project context and strategic direction
2. **Check TASKS.md** - Review pending tasks and current milestone
3. **Verify environment** - Confirm n8n connectivity and MCP availability
4. **Check workflow directory** - See existing workflows to avoid duplication

```javascript
// Start of session checklist
await read_file("/Users/jeangiet/Documents/Claude/aruba-workflows/PLANNING.md");
await read_file("/Users/jeangiet/Documents/Claude/aruba-workflows/TASKS.md");
await n8n_health_check();
await list_directory("/Users/jeangiet/Documents/Claude/aruba-workflows");
```

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
// Use postman-mcp to validate:
await testArubaAPI({
  collection: "HPE Aruba Networking Central",
  endpoint: "/api/v2/devices",
  method: "GET",
  auth: "Bearer token"
});

// Save API test results
await write_file(`${baseDir}/${workflowName}/tests/api-validation.json`, testResults);
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

## Common Workflow Patterns

### Pattern 1: Scheduled Health Monitoring
```javascript
{
  "nodes": [
    {
      "name": "Every 5 minutes",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{ "field": "minutes", "minutesInterval": 5 }]
        }
      },
      "position": [250, 300]
    },
    {
      "name": "Get Device Health",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://{{region}}.central.arubanetworks.com/api/v2/monitoring/stats",
        "authentication": "predefinedCredentialType",
        "credentialsName": "Aruba Central API",
        "options": {
          "timeout": 30000,
          "retry": {
            "maxTries": 3,
            "waitBetweenTries": 2000
          }
        }
      },
      "position": [450, 300]
    },
    {
      "name": "Check Thresholds",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{$json.cpu_usage}}",
              "operation": "larger",
              "value2": 80
            }
          ]
        }
      },
      "position": [650, 300]
    },
    {
      "name": "Send Alert",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#network-alerts",
        "text": "High CPU usage detected on {{$json.device_name}}: {{$json.cpu_usage}}%"
      },
      "position": [850, 200]
    }
  ]
}
```

### Pattern 2: Event-Driven Response
```javascript
{
  "trigger": {
    "type": "webhook",
    "path": "/aruba-alert",
    "method": "POST"
  },
  "processor": {
    "type": "function",
    "code": `
      // Parse alert data
      const alert = items[0].json;
      
      // Determine severity
      const severity = alert.level || 'info';
      
      // Route based on type
      if (alert.type === 'security') {
        return [{ json: { ...alert, action: 'immediate' } }];
      } else if (alert.type === 'performance') {
        return [{ json: { ...alert, action: 'monitor' } }];
      }
      
      return items;
    `
  }
}
```

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

// List available nodes for Aruba automation
await search_nodes({ query: "http webhook schedule" });

// Get node documentation
await get_node_documentation({ nodeType: "nodes-base.httpRequest" });

// Validate workflow
await validate_workflow({ workflow: myWorkflow });

// Test API endpoint
await send_message_to_claude({
  model: "claude-3-sonnet",
  max_tokens: 1000,
  content: "Test Aruba Central API endpoint /api/v2/devices"
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
- Alert at 75% utilization (25% remaining)
- Provide work summary before limits
- Be proactive about context management

### Use `/clear` Command
Use `/clear` between:
- Unrelated tasks or features
- Completed TDD cycles
- Different codebase sections
- Lengthy debugging sessions
- Cluttered context

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
- **For APIs**: Create Postman collections with test scripts
- **Do NOT** create implementations or mocks
- Cover happy paths, edge cases, errors
- Make tests independent and repeatable

### 2. Confirm Test Failures
- Run tests, confirm expected failures
- **For APIs**: Execute Postman collections
- **Do NOT** write implementation code
- Show test failures for verification
- Ensure clear, informative output

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
1. Create working collections
2. Add rich Markdown descriptions
3. Include realistic examples
4. Document scenarios and edge cases
5. Generate and publish documentation

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
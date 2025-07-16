/**
 * HPE Aruba n8n Direct Workflow Builder Engine
 * 
 * This engine provides the core functionality for building n8n workflows
 * directly within the n8n platform using programmatic interfaces.
 */

const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const TemplateEngine = require('./template-engine');
const ValidationEngine = require('./validation-engine');
const N8nApiInterface = require('./n8n-api-interface');
const RequirementParser = require('./requirement-parser');

class WorkflowBuilderEngine {
  constructor(config) {
    this.config = {
      n8nUrl: config.n8nUrl || 'http://192.168.40.100:8006',
      apiKey: config.apiKey,
      defaultCredentials: config.defaultCredentials || {},
      ...config
    };

    this.templateEngine = new TemplateEngine(this.config);
    this.validationEngine = new ValidationEngine(this.config);
    this.n8nApi = new N8nApiInterface(this.config);
    this.requirementParser = new RequirementParser(this.config);
  }

  /**
   * Build a workflow from natural language requirements
   * @param {Object} requirements - The workflow requirements
   * @returns {Object} Generated workflow object
   */
  async buildFromRequirement(requirements) {
    try {
      console.log('🔧 Building workflow from requirements:', requirements.description);

      // Parse requirements into structured format
      const parsedRequirements = await this.requirementParser.parse(requirements);

      // Select appropriate template
      const template = await this.templateEngine.selectTemplate(parsedRequirements);

      // Generate workflow from template
      const workflow = await this.generateWorkflow(template, parsedRequirements);

      // Validate workflow
      const validation = await this.validationEngine.validate(workflow);
      if (!validation.isValid) {
        throw new Error(`Workflow validation failed: ${validation.errors.join(', ')}`);
      }

      console.log('✅ Workflow built successfully:', workflow.name);
      return workflow;

    } catch (error) {
      console.error('❌ Error building workflow:', error.message);
      throw error;
    }
  }

  /**
   * Build a workflow from a template
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Template parameters
   * @returns {Object} Generated workflow object
   */
  async buildFromTemplate(template, parameters) {
    try {
      console.log('🔧 Building workflow from template:', template.name);

      // Validate template parameters
      const validationResult = await this.templateEngine.validateParameters(template, parameters);
      if (!validationResult.isValid) {
        throw new Error(`Template parameters invalid: ${validationResult.errors.join(', ')}`);
      }

      // Generate workflow from template
      const workflow = await this.generateWorkflow(template, parameters);

      console.log('✅ Workflow built from template successfully:', workflow.name);
      return workflow;

    } catch (error) {
      console.error('❌ Error building workflow from template:', error.message);
      throw error;
    }
  }

  /**
   * Generate workflow object from template and parameters
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Workflow parameters
   * @returns {Object} Generated workflow object
   */
  async generateWorkflow(template, parameters) {
    const workflowId = uuidv4();
    const workflowName = parameters.name || `${template.name}-${Date.now()}`;

    const workflow = {
      id: workflowId,
      name: workflowName,
      active: false,
      nodes: [],
      connections: {},
      settings: {
        executionOrder: 'v1',
        saveManualExecutions: true,
        callerPolicy: 'workflowsFromSameOwner',
        errorWorkflow: parameters.errorWorkflow || null
      },
      staticData: null,
      tags: parameters.tags || [],
      meta: {
        templateId: template.id,
        generated: new Date().toISOString(),
        version: '1.0.0',
        description: parameters.description || template.description
      }
    };

    // Generate nodes based on template
    const nodes = await this.generateNodes(template, parameters);
    workflow.nodes = nodes;

    // Generate connections based on template
    const connections = await this.generateConnections(template, nodes);
    workflow.connections = connections;

    return workflow;
  }

  /**
   * Generate nodes based on template and parameters
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Workflow parameters
   * @returns {Array} Array of workflow nodes
   */
  async generateNodes(template, parameters) {
    const nodes = [];
    let position = { x: 250, y: 300 };

    // Generate trigger node
    const triggerNode = await this.generateTriggerNode(template, parameters, position);
    nodes.push(triggerNode);
    position.x += 200;

    // Generate validation node if required
    if (template.requiresValidation) {
      const validationNode = await this.generateValidationNode(template, parameters, position);
      nodes.push(validationNode);
      position.x += 200;
    }

    // Generate operation routing node
    const routingNode = await this.generateRoutingNode(template, parameters, position);
    nodes.push(routingNode);
    position.x += 200;

    // Generate API operation nodes
    const apiNodes = await this.generateApiNodes(template, parameters, position);
    nodes.push(...apiNodes);
    position.x += 200 * apiNodes.length;

    // Generate response processing node
    const responseNode = await this.generateResponseNode(template, parameters, position);
    nodes.push(responseNode);
    position.x += 200;

    // Generate error handling node
    const errorNode = await this.generateErrorNode(template, parameters, { x: position.x, y: position.y + 200 });
    nodes.push(errorNode);

    // Generate notification nodes
    const notificationNodes = await this.generateNotificationNodes(template, parameters, position);
    nodes.push(...notificationNodes);

    return nodes;
  }

  /**
   * Generate trigger node
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Workflow parameters
   * @param {Object} position - Node position
   * @returns {Object} Trigger node
   */
  async generateTriggerNode(template, parameters, position) {
    const triggerType = parameters.trigger || template.trigger || 'manual';
    
    const baseNode = {
      id: uuidv4(),
      name: 'Trigger',
      type: this.getTriggerNodeType(triggerType),
      typeVersion: 1,
      position: [position.x, position.y]
    };

    switch (triggerType) {
      case 'schedule':
        return {
          ...baseNode,
          type: 'n8n-nodes-base.scheduleTrigger',
          parameters: {
            rule: {
              interval: this.parseScheduleInterval(parameters.schedule || '*/5 * * * *')
            }
          }
        };

      case 'webhook':
        return {
          ...baseNode,
          type: 'n8n-nodes-base.webhook',
          parameters: {
            httpMethod: parameters.httpMethod || 'POST',
            path: parameters.webhookPath || `aruba-${template.name.toLowerCase()}`,
            responseMode: 'responseNode',
            options: {
              rawBody: false
            }
          }
        };

      case 'manual':
      default:
        return {
          ...baseNode,
          type: 'n8n-nodes-base.manualTrigger',
          parameters: {}
        };
    }
  }

  /**
   * Generate validation node
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Workflow parameters
   * @param {Object} position - Node position
   * @returns {Object} Validation node
   */
  async generateValidationNode(template, parameters, position) {
    return {
      id: uuidv4(),
      name: 'Input Validation',
      type: 'n8n-nodes-base.function',
      typeVersion: 1,
      position: [position.x, position.y],
      parameters: {
        functionCode: this.generateValidationCode(template, parameters)
      }
    };
  }

  /**
   * Generate routing node for operation selection
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Workflow parameters
   * @param {Object} position - Node position
   * @returns {Object} Routing node
   */
  async generateRoutingNode(template, parameters, position) {
    return {
      id: uuidv4(),
      name: 'Operation Router',
      type: 'n8n-nodes-base.if',
      typeVersion: 1,
      position: [position.x, position.y],
      parameters: {
        conditions: {
          string: template.operations.map(op => ({
            value1: '={{$json.operation}}',
            operation: 'equal',
            value2: op.name
          }))
        }
      }
    };
  }

  /**
   * Generate API operation nodes
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Workflow parameters
   * @param {Object} position - Node position
   * @returns {Array} Array of API nodes
   */
  async generateApiNodes(template, parameters, position) {
    const nodes = [];
    let currentPosition = { ...position };

    for (const operation of template.operations) {
      const apiNode = {
        id: uuidv4(),
        name: `${operation.name} Operation`,
        type: 'n8n-nodes-base.httpRequest',
        typeVersion: 3,
        position: [currentPosition.x, currentPosition.y],
        parameters: {
          url: this.buildApiUrl(template, parameters, operation),
          method: operation.method || 'GET',
          authentication: 'predefinedCredentialType',
          nodeCredentialType: this.getCredentialType(template.apiType),
          sendHeaders: true,
          headerParameters: {
            parameters: [
              {
                name: 'Content-Type',
                value: 'application/json'
              },
              {
                name: 'Accept',
                value: 'application/json'
              }
            ]
          },
          options: {
            timeout: 30000,
            retry: {
              enabled: true,
              maxTries: 3,
              waitBetweenTries: 2000
            },
            response: {
              response: {
                neverError: true,
                responseFormat: 'json'
              }
            }
          }
        }
      };

      // Add request body for POST/PUT operations
      if (operation.method === 'POST' || operation.method === 'PUT') {
        apiNode.parameters.body = {
          mimeType: 'application/json',
          content: this.generateRequestBody(template, parameters, operation)
        };
      }

      nodes.push(apiNode);
      currentPosition.y += 100;
    }

    return nodes;
  }

  /**
   * Generate response processing node
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Workflow parameters
   * @param {Object} position - Node position
   * @returns {Object} Response processing node
   */
  async generateResponseNode(template, parameters, position) {
    return {
      id: uuidv4(),
      name: 'Process Response',
      type: 'n8n-nodes-base.function',
      typeVersion: 1,
      position: [position.x, position.y],
      parameters: {
        functionCode: this.generateResponseProcessingCode(template, parameters)
      }
    };
  }

  /**
   * Generate error handling node
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Workflow parameters
   * @param {Object} position - Node position
   * @returns {Object} Error handling node
   */
  async generateErrorNode(template, parameters, position) {
    return {
      id: uuidv4(),
      name: 'Error Handler',
      type: 'n8n-nodes-base.errorTrigger',
      typeVersion: 1,
      position: [position.x, position.y],
      parameters: {}
    };
  }

  /**
   * Generate notification nodes
   * @param {Object} template - The workflow template
   * @param {Object} parameters - Workflow parameters
   * @param {Object} position - Node position
   * @returns {Array} Array of notification nodes
   */
  async generateNotificationNodes(template, parameters, position) {
    const nodes = [];
    let currentPosition = { ...position };

    // Generate success notification
    if (parameters.notifications?.slack) {
      const slackNode = {
        id: uuidv4(),
        name: 'Success Notification',
        type: 'n8n-nodes-base.slack',
        typeVersion: 1,
        position: [currentPosition.x, currentPosition.y],
        parameters: {
          channel: parameters.notifications.slack,
          text: this.generateSuccessNotificationText(template, parameters),
          username: 'n8n-aruba-bot',
          iconEmoji: ':white_check_mark:'
        }
      };
      nodes.push(slackNode);
      currentPosition.y += 100;
    }

    // Generate error notification
    if (parameters.notifications?.email) {
      const emailNode = {
        id: uuidv4(),
        name: 'Error Notification',
        type: 'n8n-nodes-base.emailSend',
        typeVersion: 2,
        position: [currentPosition.x, currentPosition.y + 200],
        parameters: {
          toEmail: parameters.notifications.email,
          subject: `${template.name} Error Alert`,
          text: this.generateErrorNotificationText(template, parameters)
        }
      };
      nodes.push(emailNode);
    }

    return nodes;
  }

  /**
   * Generate connections between nodes
   * @param {Object} template - The workflow template
   * @param {Array} nodes - Array of workflow nodes
   * @returns {Object} Connections object
   */
  async generateConnections(template, nodes) {
    const connections = {};

    // Find nodes by name
    const findNode = (name) => nodes.find(node => node.name === name);

    const triggerNode = findNode('Trigger');
    const validationNode = findNode('Input Validation');
    const routingNode = findNode('Operation Router');
    const responseNode = findNode('Process Response');
    const errorNode = findNode('Error Handler');
    const successNotification = findNode('Success Notification');
    const errorNotification = findNode('Error Notification');

    // Connect trigger to validation (if exists) or routing
    const firstNode = validationNode || routingNode;
    if (triggerNode && firstNode) {
      connections[triggerNode.id] = {
        main: [[{ node: firstNode.id, type: 'main', index: 0 }]]
      };
    }

    // Connect validation to routing (if validation exists)
    if (validationNode && routingNode) {
      connections[validationNode.id] = {
        main: [[{ node: routingNode.id, type: 'main', index: 0 }]]
      };
    }

    // Connect routing to API nodes
    const apiNodes = nodes.filter(node => node.name.includes('Operation'));
    if (routingNode && apiNodes.length > 0) {
      connections[routingNode.id] = {
        main: apiNodes.map(node => [{ node: node.id, type: 'main', index: 0 }])
      };
    }

    // Connect API nodes to response processing
    if (responseNode) {
      apiNodes.forEach(apiNode => {
        connections[apiNode.id] = {
          main: [[{ node: responseNode.id, type: 'main', index: 0 }]]
        };
      });
    }

    // Connect response processing to success notification
    if (responseNode && successNotification) {
      connections[responseNode.id] = {
        main: [[{ node: successNotification.id, type: 'main', index: 0 }]]
      };
    }

    // Connect error handler to error notification
    if (errorNode && errorNotification) {
      connections[errorNode.id] = {
        main: [[{ node: errorNotification.id, type: 'main', index: 0 }]]
      };
    }

    return connections;
  }

  /**
   * Test a workflow with sample data
   * @param {Object} workflow - The workflow to test
   * @param {Object} testData - Test data and configuration
   * @returns {Object} Test results
   */
  async test(workflow, testData) {
    try {
      console.log('🧪 Testing workflow:', workflow.name);

      // Create temporary workflow for testing
      const tempWorkflow = await this.n8nApi.createWorkflow({
        ...workflow,
        name: `${workflow.name}-test-${Date.now()}`,
        active: false
      });

      // Execute workflow with test data
      const execution = await this.n8nApi.executeWorkflow(tempWorkflow.id, testData.sampleData);

      // Wait for execution to complete
      const result = await this.n8nApi.waitForExecution(execution.id, 30000);

      // Clean up temporary workflow
      await this.n8nApi.deleteWorkflow(tempWorkflow.id);

      console.log('✅ Workflow test completed');
      return {
        success: result.finished,
        executionTime: result.stoppedAt - result.startedAt,
        data: result.data,
        error: result.error
      };

    } catch (error) {
      console.error('❌ Error testing workflow:', error.message);
      throw error;
    }
  }

  /**
   * Deploy a workflow to n8n
   * @param {Object} workflow - The workflow to deploy
   * @param {Object} options - Deployment options
   * @returns {Object} Deployment result
   */
  async deploy(workflow, options = {}) {
    try {
      console.log('🚀 Deploying workflow:', workflow.name);

      // Validate workflow before deployment
      const validation = await this.validationEngine.validate(workflow);
      if (!validation.isValid) {
        throw new Error(`Workflow validation failed: ${validation.errors.join(', ')}`);
      }

      // Create workflow in n8n
      const deployedWorkflow = await this.n8nApi.createWorkflow(workflow);

      // Activate workflow if specified
      if (options.activate !== false) {
        await this.n8nApi.activateWorkflow(deployedWorkflow.id);
      }

      console.log('✅ Workflow deployed successfully:', deployedWorkflow.id);
      return {
        id: deployedWorkflow.id,
        name: deployedWorkflow.name,
        active: deployedWorkflow.active,
        url: `${this.config.n8nUrl}/workflow/${deployedWorkflow.id}`
      };

    } catch (error) {
      console.error('❌ Error deploying workflow:', error.message);
      throw error;
    }
  }

  /**
   * Update an existing workflow
   * @param {string} workflowId - The workflow ID to update
   * @param {Object} updates - Workflow updates
   * @returns {Object} Updated workflow
   */
  async update(workflowId, updates) {
    try {
      console.log('🔄 Updating workflow:', workflowId);

      // Get existing workflow
      const existingWorkflow = await this.n8nApi.getWorkflow(workflowId);

      // Merge updates
      const updatedWorkflow = { ...existingWorkflow, ...updates };

      // Validate updated workflow
      const validation = await this.validationEngine.validate(updatedWorkflow);
      if (!validation.isValid) {
        throw new Error(`Workflow validation failed: ${validation.errors.join(', ')}`);
      }

      // Update workflow in n8n
      const result = await this.n8nApi.updateWorkflow(workflowId, updatedWorkflow);

      console.log('✅ Workflow updated successfully');
      return result;

    } catch (error) {
      console.error('❌ Error updating workflow:', error.message);
      throw error;
    }
  }

  /**
   * Get workflow execution history
   * @param {string} workflowId - The workflow ID
   * @param {Object} options - Query options
   * @returns {Array} Execution history
   */
  async getExecutionHistory(workflowId, options = {}) {
    try {
      const executions = await this.n8nApi.getExecutions(workflowId, options);
      return executions.map(execution => ({
        id: execution.id,
        startedAt: execution.startedAt,
        stoppedAt: execution.stoppedAt,
        finished: execution.finished,
        mode: execution.mode,
        data: execution.data
      }));

    } catch (error) {
      console.error('❌ Error getting execution history:', error.message);
      throw error;
    }
  }

  // Helper methods
  getTriggerNodeType(triggerType) {
    const types = {
      'schedule': 'n8n-nodes-base.scheduleTrigger',
      'webhook': 'n8n-nodes-base.webhook',
      'manual': 'n8n-nodes-base.manualTrigger'
    };
    return types[triggerType] || types.manual;
  }

  parseScheduleInterval(schedule) {
    // Convert cron expression to n8n interval format
    const parts = schedule.split(' ');
    if (parts[0].startsWith('*/')) {
      return [{ field: 'minutes', minutesInterval: parseInt(parts[0].substring(2)) }];
    }
    return [{ field: 'cronExpression', cronExpression: schedule }];
  }

  buildApiUrl(template, parameters, operation) {
    const baseUrl = parameters.baseUrl || template.baseUrl;
    const endpoint = operation.endpoint || template.endpoint;
    return `${baseUrl}${endpoint}`.replace(/\{\{(\w+)\}\}/g, (match, key) => {
      return parameters[key] || match;
    });
  }

  getCredentialType(apiType) {
    const types = {
      'aos-cx': 'arubaOsCxApi',
      'central': 'arubaApi',
      'edgeconnect': 'edgeConnectApi',
      'uxi': 'uxiApi'
    };
    return types[apiType] || 'httpBasicAuth';
  }

  generateRequestBody(template, parameters, operation) {
    if (operation.requestBody) {
      return JSON.stringify(operation.requestBody);
    }
    return '={{JSON.stringify($json)}}';
  }

  generateValidationCode(template, parameters) {
    return `
// Input validation for ${template.name}
const items = $input.all();
const errors = [];

for (const item of items) {
  const data = item.json;
  
  // Add validation logic based on template requirements
  ${template.validation || '// No specific validation required'}
  
  if (errors.length > 0) {
    throw new Error('Validation failed: ' + errors.join(', '));
  }
}

return items;
`;
  }

  generateResponseProcessingCode(template, parameters) {
    return `
// Response processing for ${template.name}
const items = $input.all();
const processedItems = [];

for (const item of items) {
  const response = item.json;
  
  // Process response based on template requirements
  const processedData = {
    operation: response.operation || 'unknown',
    success: response.status < 400,
    status: response.status,
    message: response.message || 'Operation completed',
    data: response.data || response,
    timestamp: new Date().toISOString()
  };
  
  processedItems.push({ json: processedData });
}

return processedItems;
`;
  }

  generateSuccessNotificationText(template, parameters) {
    return `:white_check_mark: *${template.name} - Operation Successful*

*Operation:* {{ $json.operation }}
*Status:* {{ $json.message }}
*Timestamp:* {{ $json.timestamp }}

\`\`\`json
{{ JSON.stringify($json.data, null, 2) }}
\`\`\``;
  }

  generateErrorNotificationText(template, parameters) {
    return `Error occurred in ${template.name} workflow:

Error: {{ $node.error.message }}
Node: {{ $node.error.node }}
Timestamp: {{ $now }}

Workflow: {{ $workflow.name }}
Execution ID: {{ $execution.id }}

Please check the workflow execution for more details.`;
  }
}

module.exports = WorkflowBuilderEngine;
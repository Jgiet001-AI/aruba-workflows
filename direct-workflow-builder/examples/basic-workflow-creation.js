/**
 * Basic Workflow Creation Example
 * 
 * This example demonstrates how to use the Direct Workflow Builder
 * to create workflows programmatically.
 */

const WorkflowBuilderEngine = require('../workflow-builder-engine');
const N8nApiInterface = require('../n8n-api-interface');

// Configuration
const config = {
  n8nUrl: 'http://192.168.40.100:8006',
  // apiKey: 'your-api-key-here', // Add your API key if authentication is required
  timeout: 30000
};

/**
 * Example 1: Create a simple AOS-CX VLAN monitoring workflow
 */
async function createVlanMonitoringWorkflow() {
  console.log('📋 Creating VLAN monitoring workflow...');
  
  const builder = new WorkflowBuilderEngine(config);
  
  try {
    // Initialize the builder
    await builder.templateEngine.initialize();
    
    // Build workflow from requirements
    const workflow = await builder.buildFromRequirement({
      name: 'AOS-CX VLAN Health Monitor',
      description: 'Monitor VLAN health on AOS-CX switches every 5 minutes',
      apiType: 'aos-cx',
      trigger: 'schedule',
      schedule: '*/5 * * * *', // Every 5 minutes
      switchIp: '192.168.1.10',
      operations: ['list', 'read'],
      thresholds: {
        vlanCount: 50 // Alert if more than 50 VLANs
      },
      notifications: {
        slack: '#network-alerts',
        email: 'admin@company.com'
      }
    });
    
    // Test the workflow
    console.log('🧪 Testing workflow...');
    const testResult = await builder.test(workflow, {
      sampleData: { operation: 'list', switch_ip: '192.168.1.10' }
    });
    
    if (testResult.success) {
      console.log('✅ Workflow test passed');
      
      // Deploy the workflow
      console.log('🚀 Deploying workflow...');
      const deployment = await builder.deploy(workflow, { activate: true });
      
      console.log('✅ Workflow deployed successfully:');
      console.log('   - ID:', deployment.id);
      console.log('   - Name:', deployment.name);
      console.log('   - URL:', deployment.url);
      console.log('   - Active:', deployment.active);
      
      return deployment;
    } else {
      console.error('❌ Workflow test failed:', testResult.error);
      return null;
    }
    
  } catch (error) {
    console.error('❌ Error creating workflow:', error.message);
    throw error;
  }
}

/**
 * Example 2: Create a workflow from a template
 */
async function createWorkflowFromTemplate() {
  console.log('📋 Creating workflow from template...');
  
  const builder = new WorkflowBuilderEngine(config);
  
  try {
    // Initialize the builder
    await builder.templateEngine.initialize();
    
    // Get the AOS-CX VLAN management template
    const template = builder.templateEngine.getTemplate('aos-cx-vlan-management');
    
    // Build workflow from template
    const workflow = await builder.buildFromTemplate(template, {
      name: 'Production VLAN Manager',
      description: 'Manage production VLANs on datacenter switches',
      switchIp: '192.168.1.20',
      vlanId: 100,
      vlanName: 'Production-VLAN',
      vlanDescription: 'Production network VLAN',
      notifications: {
        slack: '#datacenter-ops'
      }
    });
    
    // Validate the workflow
    console.log('🔍 Validating workflow...');
    const validation = await builder.validationEngine.validate(workflow);
    
    if (validation.isValid) {
      console.log('✅ Workflow validation passed');
      
      // Deploy the workflow
      const deployment = await builder.deploy(workflow, { activate: false });
      
      console.log('✅ Workflow created successfully:');
      console.log('   - ID:', deployment.id);
      console.log('   - Name:', deployment.name);
      console.log('   - Template:', template.name);
      
      return deployment;
    } else {
      console.error('❌ Workflow validation failed:', validation.errors);
      return null;
    }
    
  } catch (error) {
    console.error('❌ Error creating workflow from template:', error.message);
    throw error;
  }
}

/**
 * Example 3: Create a Central API monitoring workflow
 */
async function createCentralMonitoringWorkflow() {
  console.log('📋 Creating Central API monitoring workflow...');
  
  const builder = new WorkflowBuilderEngine(config);
  
  try {
    // Initialize the builder
    await builder.templateEngine.initialize();
    
    // Build workflow from requirements
    const workflow = await builder.buildFromRequirement({
      name: 'Central Device Health Monitor',
      description: 'Monitor device health via Aruba Central API',
      apiType: 'central',
      trigger: 'schedule',
      schedule: '*/10 * * * *', // Every 10 minutes
      region: 'us-west-1',
      deviceType: 'switch',
      operations: ['devices', 'monitor', 'alerts'],
      thresholds: {
        cpu: 80,
        memory: 85,
        temperature: 65
      },
      notifications: {
        slack: '#central-alerts',
        email: 'network-team@company.com'
      }
    });
    
    // Test the workflow
    console.log('🧪 Testing workflow...');
    const testResult = await builder.test(workflow, {
      sampleData: { 
        operation: 'devices', 
        region: 'us-west-1',
        device_type: 'switch'
      }
    });
    
    if (testResult.success) {
      console.log('✅ Workflow test passed');
      
      // Deploy the workflow
      const deployment = await builder.deploy(workflow, { activate: true });
      
      console.log('✅ Central monitoring workflow deployed:');
      console.log('   - ID:', deployment.id);
      console.log('   - Schedule: Every 10 minutes');
      console.log('   - Region:', 'us-west-1');
      
      return deployment;
    } else {
      console.error('❌ Workflow test failed:', testResult.error);
      return null;
    }
    
  } catch (error) {
    console.error('❌ Error creating Central monitoring workflow:', error.message);
    throw error;
  }
}

/**
 * Example 4: Create a webhook-triggered response workflow
 */
async function createWebhookResponseWorkflow() {
  console.log('📋 Creating webhook response workflow...');
  
  const builder = new WorkflowBuilderEngine(config);
  
  try {
    // Initialize the builder
    await builder.templateEngine.initialize();
    
    // Build workflow from requirements
    const workflow = await builder.buildFromRequirement({
      name: 'Network Alert Response',
      description: 'Respond to network alerts via webhook',
      trigger: 'webhook',
      webhookPath: 'network-alert-response',
      httpMethod: 'POST',
      operations: ['process', 'respond'],
      notifications: {
        slack: '#incident-response',
        email: 'oncall@company.com'
      }
    });
    
    // Deploy the workflow
    const deployment = await builder.deploy(workflow, { activate: true });
    
    // Get webhook URL
    const webhookUrl = builder.n8nApi.getWebhookUrl(deployment.id, 'network-alert-response');
    
    console.log('✅ Webhook response workflow deployed:');
    console.log('   - ID:', deployment.id);
    console.log('   - Webhook URL:', webhookUrl);
    console.log('   - Method: POST');
    
    return { deployment, webhookUrl };
    
  } catch (error) {
    console.error('❌ Error creating webhook response workflow:', error.message);
    throw error;
  }
}

/**
 * Example 5: Test n8n API connectivity
 */
async function testN8nConnectivity() {
  console.log('🔗 Testing n8n API connectivity...');
  
  const n8nApi = new N8nApiInterface(config);
  
  try {
    // Test connection
    const connectionTest = await n8nApi.testConnection();
    
    if (connectionTest.success) {
      console.log('✅ n8n API connection successful');
      console.log('   - Version:', connectionTest.version);
      
      // Get basic information
      const workflows = await n8nApi.getWorkflows();
      const credentials = await n8nApi.getCredentials();
      
      console.log('📊 n8n Instance Information:');
      console.log('   - Workflows:', workflows.length);
      console.log('   - Credentials:', credentials.length);
      
      return true;
    } else {
      console.error('❌ n8n API connection failed:', connectionTest.error);
      return false;
    }
    
  } catch (error) {
    console.error('❌ Error testing n8n connectivity:', error.message);
    return false;
  }
}

/**
 * Example 6: List available templates
 */
async function listAvailableTemplates() {
  console.log('📋 Listing available templates...');
  
  const builder = new WorkflowBuilderEngine(config);
  
  try {
    // Initialize the builder
    await builder.templateEngine.initialize();
    
    // Get all templates
    const templates = builder.templateEngine.getAllTemplates();
    
    console.log('📚 Available Templates:');
    templates.forEach(template => {
      console.log(`   - ${template.name} (${template.id})`);
      console.log(`     Category: ${template.category}`);
      console.log(`     API Type: ${template.apiType}`);
      console.log(`     Trigger: ${template.trigger}`);
      console.log(`     Description: ${template.description}`);
      console.log('');
    });
    
    return templates;
    
  } catch (error) {
    console.error('❌ Error listing templates:', error.message);
    throw error;
  }
}

/**
 * Main execution function
 */
async function main() {
  console.log('🚀 Direct Workflow Builder Examples');
  console.log('=====================================');
  
  try {
    // Test connectivity first
    const isConnected = await testN8nConnectivity();
    if (!isConnected) {
      console.error('❌ Cannot connect to n8n API. Please check your configuration.');
      return;
    }
    
    // List available templates
    await listAvailableTemplates();
    
    // Run examples
    console.log('\n🔧 Running workflow creation examples...\n');
    
    // Example 1: VLAN monitoring
    await createVlanMonitoringWorkflow();
    
    console.log('\n' + '='.repeat(50) + '\n');
    
    // Example 2: Template-based workflow
    await createWorkflowFromTemplate();
    
    console.log('\n' + '='.repeat(50) + '\n');
    
    // Example 3: Central monitoring
    await createCentralMonitoringWorkflow();
    
    console.log('\n' + '='.repeat(50) + '\n');
    
    // Example 4: Webhook response
    await createWebhookResponseWorkflow();
    
    console.log('\n✅ All examples completed successfully!');
    
  } catch (error) {
    console.error('❌ Error running examples:', error.message);
    process.exit(1);
  }
}

// Run examples if this file is executed directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  createVlanMonitoringWorkflow,
  createWorkflowFromTemplate,
  createCentralMonitoringWorkflow,
  createWebhookResponseWorkflow,
  testN8nConnectivity,
  listAvailableTemplates
};
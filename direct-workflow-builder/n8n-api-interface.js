/**
 * n8n API Interface for Direct Workflow Builder
 * 
 * Provides direct integration with n8n platform via REST API
 */

const axios = require('axios');

class N8nApiInterface {
  constructor(config) {
    this.config = {
      baseUrl: config.n8nUrl || 'http://192.168.40.100:8006',
      apiKey: config.apiKey,
      timeout: config.timeout || 30000,
      ...config
    };

    this.client = axios.create({
      baseURL: this.config.baseUrl,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
        ...(this.config.apiKey && { 'X-N8N-API-KEY': this.config.apiKey })
      }
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      response => response,
      error => {
        const errorMessage = error.response?.data?.message || error.message;
        console.error('❌ n8n API Error:', errorMessage);
        throw new Error(`n8n API Error: ${errorMessage}`);
      }
    );
  }

  /**
   * Test connection to n8n API
   * @returns {Object} Connection test result
   */
  async testConnection() {
    try {
      const response = await this.client.get('/rest/settings');
      return {
        success: true,
        version: response.data.version,
        settings: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get all workflows
   * @param {Object} options - Query options
   * @returns {Array} Array of workflows
   */
  async getWorkflows(options = {}) {
    try {
      const params = new URLSearchParams();
      if (options.active !== undefined) params.append('active', options.active);
      if (options.tags) params.append('tags', options.tags);

      const response = await this.client.get(`/rest/workflows?${params}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error('❌ Error getting workflows:', error.message);
      throw error;
    }
  }

  /**
   * Get workflow by ID
   * @param {string} workflowId - Workflow ID
   * @returns {Object} Workflow object
   */
  async getWorkflow(workflowId) {
    try {
      const response = await this.client.get(`/rest/workflows/${workflowId}`);
      return response.data;
    } catch (error) {
      console.error('❌ Error getting workflow:', error.message);
      throw error;
    }
  }

  /**
   * Create a new workflow
   * @param {Object} workflowData - Workflow data
   * @returns {Object} Created workflow
   */
  async createWorkflow(workflowData) {
    try {
      console.log('🔧 Creating workflow:', workflowData.name);
      
      const response = await this.client.post('/rest/workflows', workflowData);
      
      console.log('✅ Workflow created successfully:', response.data.id);
      return response.data;
    } catch (error) {
      console.error('❌ Error creating workflow:', error.message);
      throw error;
    }
  }

  /**
   * Update an existing workflow
   * @param {string} workflowId - Workflow ID
   * @param {Object} workflowData - Updated workflow data
   * @returns {Object} Updated workflow
   */
  async updateWorkflow(workflowId, workflowData) {
    try {
      console.log('🔄 Updating workflow:', workflowId);
      
      const response = await this.client.put(`/rest/workflows/${workflowId}`, workflowData);
      
      console.log('✅ Workflow updated successfully');
      return response.data;
    } catch (error) {
      console.error('❌ Error updating workflow:', error.message);
      throw error;
    }
  }

  /**
   * Delete a workflow
   * @param {string} workflowId - Workflow ID
   * @returns {boolean} Success status
   */
  async deleteWorkflow(workflowId) {
    try {
      console.log('🗑️  Deleting workflow:', workflowId);
      
      await this.client.delete(`/rest/workflows/${workflowId}`);
      
      console.log('✅ Workflow deleted successfully');
      return true;
    } catch (error) {
      console.error('❌ Error deleting workflow:', error.message);
      throw error;
    }
  }

  /**
   * Activate a workflow
   * @param {string} workflowId - Workflow ID
   * @returns {Object} Activated workflow
   */
  async activateWorkflow(workflowId) {
    try {
      console.log('▶️  Activating workflow:', workflowId);
      
      const response = await this.client.post(`/rest/workflows/${workflowId}/activate`);
      
      console.log('✅ Workflow activated successfully');
      return response.data;
    } catch (error) {
      console.error('❌ Error activating workflow:', error.message);
      throw error;
    }
  }

  /**
   * Deactivate a workflow
   * @param {string} workflowId - Workflow ID
   * @returns {Object} Deactivated workflow
   */
  async deactivateWorkflow(workflowId) {
    try {
      console.log('⏸️  Deactivating workflow:', workflowId);
      
      const response = await this.client.post(`/rest/workflows/${workflowId}/deactivate`);
      
      console.log('✅ Workflow deactivated successfully');
      return response.data;
    } catch (error) {
      console.error('❌ Error deactivating workflow:', error.message);
      throw error;
    }
  }

  /**
   * Execute a workflow
   * @param {string} workflowId - Workflow ID
   * @param {Object} inputData - Input data for execution
   * @returns {Object} Execution result
   */
  async executeWorkflow(workflowId, inputData = {}) {
    try {
      console.log('🚀 Executing workflow:', workflowId);
      
      const response = await this.client.post(`/rest/workflows/${workflowId}/execute`, {
        inputData
      });
      
      console.log('✅ Workflow execution started:', response.data.id);
      return response.data;
    } catch (error) {
      console.error('❌ Error executing workflow:', error.message);
      throw error;
    }
  }

  /**
   * Get workflow executions
   * @param {string} workflowId - Workflow ID
   * @param {Object} options - Query options
   * @returns {Array} Array of executions
   */
  async getExecutions(workflowId, options = {}) {
    try {
      const params = new URLSearchParams();
      if (options.limit) params.append('limit', options.limit);
      if (options.status) params.append('status', options.status);
      if (options.includeData) params.append('includeData', options.includeData);

      const response = await this.client.get(`/rest/executions?workflowId=${workflowId}&${params}`);
      return response.data.data || response.data;
    } catch (error) {
      console.error('❌ Error getting executions:', error.message);
      throw error;
    }
  }

  /**
   * Get execution by ID
   * @param {string} executionId - Execution ID
   * @returns {Object} Execution object
   */
  async getExecution(executionId) {
    try {
      const response = await this.client.get(`/rest/executions/${executionId}`);
      return response.data;
    } catch (error) {
      console.error('❌ Error getting execution:', error.message);
      throw error;
    }
  }

  /**
   * Stop a running execution
   * @param {string} executionId - Execution ID
   * @returns {Object} Stop result
   */
  async stopExecution(executionId) {
    try {
      console.log('⏹️  Stopping execution:', executionId);
      
      const response = await this.client.post(`/rest/executions/${executionId}/stop`);
      
      console.log('✅ Execution stopped successfully');
      return response.data;
    } catch (error) {
      console.error('❌ Error stopping execution:', error.message);
      throw error;
    }
  }

  /**
   * Delete an execution
   * @param {string} executionId - Execution ID
   * @returns {boolean} Success status
   */
  async deleteExecution(executionId) {
    try {
      console.log('🗑️  Deleting execution:', executionId);
      
      await this.client.delete(`/rest/executions/${executionId}`);
      
      console.log('✅ Execution deleted successfully');
      return true;
    } catch (error) {
      console.error('❌ Error deleting execution:', error.message);
      throw error;
    }
  }

  /**
   * Wait for execution to complete
   * @param {string} executionId - Execution ID
   * @param {number} timeout - Timeout in milliseconds
   * @returns {Object} Completed execution
   */
  async waitForExecution(executionId, timeout = 30000) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      const execution = await this.getExecution(executionId);
      
      if (execution.finished || execution.stoppedAt) {
        return execution;
      }
      
      // Wait 1 second before checking again
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    throw new Error(`Execution ${executionId} did not complete within ${timeout}ms`);
  }

  /**
   * Get available node types
   * @returns {Array} Array of node types
   */
  async getNodeTypes() {
    try {
      const response = await this.client.get('/rest/node-types');
      return response.data;
    } catch (error) {
      console.error('❌ Error getting node types:', error.message);
      throw error;
    }
  }

  /**
   * Get node type definition
   * @param {string} nodeType - Node type name
   * @returns {Object} Node type definition
   */
  async getNodeType(nodeType) {
    try {
      const response = await this.client.get(`/rest/node-types/${nodeType}`);
      return response.data;
    } catch (error) {
      console.error('❌ Error getting node type:', error.message);
      throw error;
    }
  }

  /**
   * Get all credentials
   * @returns {Array} Array of credentials
   */
  async getCredentials() {
    try {
      const response = await this.client.get('/rest/credentials');
      return response.data.data || response.data;
    } catch (error) {
      console.error('❌ Error getting credentials:', error.message);
      throw error;
    }
  }

  /**
   * Get credential by ID
   * @param {string} credentialId - Credential ID
   * @returns {Object} Credential object
   */
  async getCredential(credentialId) {
    try {
      const response = await this.client.get(`/rest/credentials/${credentialId}`);
      return response.data;
    } catch (error) {
      console.error('❌ Error getting credential:', error.message);
      throw error;
    }
  }

  /**
   * Create a new credential
   * @param {Object} credentialData - Credential data
   * @returns {Object} Created credential
   */
  async createCredential(credentialData) {
    try {
      console.log('🔐 Creating credential:', credentialData.name);
      
      const response = await this.client.post('/rest/credentials', credentialData);
      
      console.log('✅ Credential created successfully');
      return response.data;
    } catch (error) {
      console.error('❌ Error creating credential:', error.message);
      throw error;
    }
  }

  /**
   * Update an existing credential
   * @param {string} credentialId - Credential ID
   * @param {Object} credentialData - Updated credential data
   * @returns {Object} Updated credential
   */
  async updateCredential(credentialId, credentialData) {
    try {
      console.log('🔄 Updating credential:', credentialId);
      
      const response = await this.client.put(`/rest/credentials/${credentialId}`, credentialData);
      
      console.log('✅ Credential updated successfully');
      return response.data;
    } catch (error) {
      console.error('❌ Error updating credential:', error.message);
      throw error;
    }
  }

  /**
   * Delete a credential
   * @param {string} credentialId - Credential ID
   * @returns {boolean} Success status
   */
  async deleteCredential(credentialId) {
    try {
      console.log('🗑️  Deleting credential:', credentialId);
      
      await this.client.delete(`/rest/credentials/${credentialId}`);
      
      console.log('✅ Credential deleted successfully');
      return true;
    } catch (error) {
      console.error('❌ Error deleting credential:', error.message);
      throw error;
    }
  }

  /**
   * Test a credential
   * @param {string} credentialId - Credential ID
   * @returns {Object} Test result
   */
  async testCredential(credentialId) {
    try {
      console.log('🧪 Testing credential:', credentialId);
      
      const response = await this.client.post(`/rest/credentials/${credentialId}/test`);
      
      console.log('✅ Credential test completed');
      return response.data;
    } catch (error) {
      console.error('❌ Error testing credential:', error.message);
      throw error;
    }
  }

  /**
   * Get available credential types
   * @returns {Array} Array of credential types
   */
  async getCredentialTypes() {
    try {
      const response = await this.client.get('/rest/credential-types');
      return response.data;
    } catch (error) {
      console.error('❌ Error getting credential types:', error.message);
      throw error;
    }
  }

  /**
   * Get workflow settings
   * @returns {Object} Workflow settings
   */
  async getSettings() {
    try {
      const response = await this.client.get('/rest/settings');
      return response.data;
    } catch (error) {
      console.error('❌ Error getting settings:', error.message);
      throw error;
    }
  }

  /**
   * Update workflow settings
   * @param {Object} settings - Updated settings
   * @returns {Object} Updated settings
   */
  async updateSettings(settings) {
    try {
      console.log('⚙️  Updating settings');
      
      const response = await this.client.patch('/rest/settings', settings);
      
      console.log('✅ Settings updated successfully');
      return response.data;
    } catch (error) {
      console.error('❌ Error updating settings:', error.message);
      throw error;
    }
  }

  /**
   * Get workflow statistics
   * @returns {Object} Workflow statistics
   */
  async getStatistics() {
    try {
      const response = await this.client.get('/rest/workflows/statistics');
      return response.data;
    } catch (error) {
      console.error('❌ Error getting statistics:', error.message);
      throw error;
    }
  }

  /**
   * Import workflows from JSON
   * @param {Object} workflowsData - Workflows data
   * @returns {Array} Array of imported workflows
   */
  async importWorkflows(workflowsData) {
    try {
      console.log('📥 Importing workflows');
      
      const response = await this.client.post('/rest/workflows/import', workflowsData);
      
      console.log('✅ Workflows imported successfully');
      return response.data;
    } catch (error) {
      console.error('❌ Error importing workflows:', error.message);
      throw error;
    }
  }

  /**
   * Export workflows to JSON
   * @param {Array} workflowIds - Array of workflow IDs to export
   * @returns {Object} Exported workflows data
   */
  async exportWorkflows(workflowIds) {
    try {
      console.log('📤 Exporting workflows');
      
      const params = new URLSearchParams();
      workflowIds.forEach(id => params.append('ids', id));
      
      const response = await this.client.get(`/rest/workflows/export?${params}`);
      
      console.log('✅ Workflows exported successfully');
      return response.data;
    } catch (error) {
      console.error('❌ Error exporting workflows:', error.message);
      throw error;
    }
  }

  /**
   * Get webhook URL for a workflow
   * @param {string} workflowId - Workflow ID
   * @param {string} webhookPath - Webhook path
   * @returns {string} Webhook URL
   */
  getWebhookUrl(workflowId, webhookPath) {
    return `${this.config.baseUrl}/webhook/${webhookPath}`;
  }

  /**
   * Get test webhook URL
   * @param {string} webhookPath - Webhook path
   * @returns {string} Test webhook URL
   */
  getTestWebhookUrl(webhookPath) {
    return `${this.config.baseUrl}/webhook-test/${webhookPath}`;
  }

  /**
   * Health check for n8n instance
   * @returns {Object} Health check result
   */
  async healthCheck() {
    try {
      const response = await this.client.get('/rest/health');
      return {
        status: 'healthy',
        data: response.data
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message
      };
    }
  }

  /**
   * Get n8n version information
   * @returns {Object} Version information
   */
  async getVersion() {
    try {
      const response = await this.client.get('/rest/version');
      return response.data;
    } catch (error) {
      console.error('❌ Error getting version:', error.message);
      throw error;
    }
  }

  /**
   * Bulk operations helper
   * @param {Array} operations - Array of operations
   * @param {number} batchSize - Batch size for processing
   * @returns {Array} Array of results
   */
  async bulkOperations(operations, batchSize = 10) {
    const results = [];
    
    for (let i = 0; i < operations.length; i += batchSize) {
      const batch = operations.slice(i, i + batchSize);
      const batchPromises = batch.map(operation => operation());
      
      try {
        const batchResults = await Promise.all(batchPromises);
        results.push(...batchResults);
      } catch (error) {
        console.error('❌ Error in bulk operation batch:', error.message);
        throw error;
      }
      
      // Small delay between batches to avoid rate limiting
      if (i + batchSize < operations.length) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }
    
    return results;
  }
}

module.exports = N8nApiInterface;
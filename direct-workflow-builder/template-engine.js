/**
 * Template Engine for HPE Aruba n8n Workflow Builder
 * 
 * Manages workflow templates, composition, and parameter validation
 */

const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');

class TemplateEngine {
  constructor(config) {
    this.config = config;
    this.templates = new Map();
    this.templateDirectory = path.join(__dirname, 'templates');
  }

  /**
   * Initialize template engine and load templates
   */
  async initialize() {
    try {
      await this.loadTemplates();
      console.log('✅ Template engine initialized with', this.templates.size, 'templates');
    } catch (error) {
      console.error('❌ Error initializing template engine:', error.message);
      throw error;
    }
  }

  /**
   * Load all templates from the templates directory
   */
  async loadTemplates() {
    try {
      // Load base templates
      const baseTemplates = await this.loadTemplateFile('base-templates.json');
      baseTemplates.forEach(template => this.templates.set(template.id, template));

      // Load Aruba-specific templates
      const arubaTemplates = await this.loadTemplateFile('aruba-specific-templates.json');
      arubaTemplates.forEach(template => this.templates.set(template.id, template));

      // Load composite templates
      const compositeTemplates = await this.loadTemplateFile('composite-templates.json');
      compositeTemplates.forEach(template => this.templates.set(template.id, template));

    } catch (error) {
      console.error('❌ Error loading templates:', error.message);
      throw error;
    }
  }

  /**
   * Load templates from a JSON file
   * @param {string} filename - Template file name
   * @returns {Array} Array of templates
   */
  async loadTemplateFile(filename) {
    try {
      const filePath = path.join(this.templateDirectory, filename);
      const data = await fs.readFile(filePath, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      console.warn(`⚠️  Template file ${filename} not found or invalid, using defaults`);
      return this.getDefaultTemplates(filename);
    }
  }

  /**
   * Get default templates if file doesn't exist
   * @param {string} filename - Template file name
   * @returns {Array} Default templates
   */
  getDefaultTemplates(filename) {
    switch (filename) {
      case 'base-templates.json':
        return this.getBaseTemplates();
      case 'aruba-specific-templates.json':
        return this.getArubaTemplates();
      case 'composite-templates.json':
        return this.getCompositeTemplates();
      default:
        return [];
    }
  }

  /**
   * Get base workflow templates
   * @returns {Array} Base templates
   */
  getBaseTemplates() {
    return [
      {
        id: 'basic-api-workflow',
        name: 'Basic API Workflow',
        description: 'Basic template for API-based workflows',
        category: 'base',
        trigger: 'manual',
        requiresValidation: true,
        apiType: 'generic',
        operations: [
          {
            name: 'get',
            method: 'GET',
            endpoint: '/api/endpoint'
          }
        ],
        parameters: {
          baseUrl: { type: 'string', required: true },
          endpoint: { type: 'string', required: true }
        },
        validation: `
          if (!data.baseUrl) errors.push('baseUrl is required');
          if (!data.endpoint) errors.push('endpoint is required');
        `
      },
      {
        id: 'scheduled-monitoring',
        name: 'Scheduled Monitoring',
        description: 'Template for scheduled monitoring workflows',
        category: 'monitoring',
        trigger: 'schedule',
        requiresValidation: true,
        apiType: 'generic',
        operations: [
          {
            name: 'monitor',
            method: 'GET',
            endpoint: '/api/status'
          }
        ],
        parameters: {
          schedule: { type: 'string', default: '*/5 * * * *' },
          threshold: { type: 'number', default: 80 }
        },
        validation: `
          if (data.threshold && (data.threshold < 0 || data.threshold > 100)) {
            errors.push('threshold must be between 0 and 100');
          }
        `
      },
      {
        id: 'webhook-handler',
        name: 'Webhook Handler',
        description: 'Template for webhook-triggered workflows',
        category: 'event',
        trigger: 'webhook',
        requiresValidation: true,
        apiType: 'generic',
        operations: [
          {
            name: 'process',
            method: 'POST',
            endpoint: '/api/process'
          }
        ],
        parameters: {
          webhookPath: { type: 'string', required: true },
          httpMethod: { type: 'string', default: 'POST' }
        },
        validation: `
          if (!data.webhookPath) errors.push('webhookPath is required');
          if (data.httpMethod && !['GET', 'POST', 'PUT', 'DELETE'].includes(data.httpMethod)) {
            errors.push('httpMethod must be GET, POST, PUT, or DELETE');
          }
        `
      }
    ];
  }

  /**
   * Get Aruba-specific templates
   * @returns {Array} Aruba templates
   */
  getArubaTemplates() {
    return [
      {
        id: 'aos-cx-vlan-management',
        name: 'AOS-CX VLAN Management',
        description: 'Template for AOS-CX VLAN CRUD operations',
        category: 'aos-cx',
        trigger: 'manual',
        requiresValidation: true,
        apiType: 'aos-cx',
        baseUrl: 'https://{{switchIp}}',
        operations: [
          {
            name: 'create',
            method: 'POST',
            endpoint: '/rest/v10.08/system/vlans',
            requestBody: {
              id: '{{vlanId}}',
              name: '{{vlanName}}',
              description: '{{vlanDescription}}'
            }
          },
          {
            name: 'read',
            method: 'GET',
            endpoint: '/rest/v10.08/system/vlans/{{vlanId}}'
          },
          {
            name: 'update',
            method: 'PUT',
            endpoint: '/rest/v10.08/system/vlans/{{vlanId}}',
            requestBody: {
              name: '{{vlanName}}',
              description: '{{vlanDescription}}'
            }
          },
          {
            name: 'delete',
            method: 'DELETE',
            endpoint: '/rest/v10.08/system/vlans/{{vlanId}}'
          },
          {
            name: 'list',
            method: 'GET',
            endpoint: '/rest/v10.08/system/vlans'
          }
        ],
        parameters: {
          switchIp: { type: 'string', required: true },
          vlanId: { type: 'number', required: true, min: 1, max: 4094 },
          vlanName: { type: 'string', required: true },
          vlanDescription: { type: 'string', default: '' }
        },
        validation: `
          if (!data.switchIp) errors.push('switchIp is required');
          if (!data.vlanId) errors.push('vlanId is required');
          if (data.vlanId && (data.vlanId < 1 || data.vlanId > 4094)) {
            errors.push('vlanId must be between 1 and 4094');
          }
          if (!data.vlanName) errors.push('vlanName is required');
        `
      },
      {
        id: 'aos-cx-interface-config',
        name: 'AOS-CX Interface Configuration',
        description: 'Template for AOS-CX interface configuration',
        category: 'aos-cx',
        trigger: 'manual',
        requiresValidation: true,
        apiType: 'aos-cx',
        baseUrl: 'https://{{switchIp}}',
        operations: [
          {
            name: 'configure',
            method: 'PUT',
            endpoint: '/rest/v10.08/system/interfaces/{{interfaceId}}',
            requestBody: {
              admin: '{{adminStatus}}',
              description: '{{description}}'
            }
          },
          {
            name: 'read',
            method: 'GET',
            endpoint: '/rest/v10.08/system/interfaces/{{interfaceId}}'
          },
          {
            name: 'list',
            method: 'GET',
            endpoint: '/rest/v10.08/system/interfaces'
          }
        ],
        parameters: {
          switchIp: { type: 'string', required: true },
          interfaceId: { type: 'string', required: true },
          adminStatus: { type: 'string', default: 'up' },
          description: { type: 'string', default: '' }
        },
        validation: `
          if (!data.switchIp) errors.push('switchIp is required');
          if (!data.interfaceId) errors.push('interfaceId is required');
          if (data.adminStatus && !['up', 'down'].includes(data.adminStatus)) {
            errors.push('adminStatus must be up or down');
          }
        `
      },
      {
        id: 'central-device-monitoring',
        name: 'Aruba Central Device Monitoring',
        description: 'Template for monitoring devices via Aruba Central',
        category: 'central',
        trigger: 'schedule',
        requiresValidation: true,
        apiType: 'central',
        baseUrl: 'https://{{region}}.central.arubanetworks.com',
        operations: [
          {
            name: 'monitor',
            method: 'GET',
            endpoint: '/api/v2/monitoring/stats'
          },
          {
            name: 'devices',
            method: 'GET',
            endpoint: '/api/v2/devices'
          },
          {
            name: 'alerts',
            method: 'GET',
            endpoint: '/api/v2/alerts'
          }
        ],
        parameters: {
          region: { type: 'string', required: true },
          deviceType: { type: 'string', default: 'all' },
          threshold: { type: 'number', default: 80 }
        },
        validation: `
          if (!data.region) errors.push('region is required');
          if (data.threshold && (data.threshold < 0 || data.threshold > 100)) {
            errors.push('threshold must be between 0 and 100');
          }
        `
      },
      {
        id: 'central-wireless-config',
        name: 'Central Wireless Configuration',
        description: 'Template for wireless configuration via Aruba Central',
        category: 'central',
        trigger: 'manual',
        requiresValidation: true,
        apiType: 'central',
        baseUrl: 'https://{{region}}.central.arubanetworks.com',
        operations: [
          {
            name: 'create_ssid',
            method: 'POST',
            endpoint: '/api/v2/wireless/ssid',
            requestBody: {
              ssid: '{{ssidName}}',
              security: '{{securityType}}',
              passphrase: '{{passphrase}}'
            }
          },
          {
            name: 'update_ssid',
            method: 'PUT',
            endpoint: '/api/v2/wireless/ssid/{{ssidId}}',
            requestBody: {
              ssid: '{{ssidName}}',
              security: '{{securityType}}'
            }
          },
          {
            name: 'delete_ssid',
            method: 'DELETE',
            endpoint: '/api/v2/wireless/ssid/{{ssidId}}'
          },
          {
            name: 'list_ssids',
            method: 'GET',
            endpoint: '/api/v2/wireless/ssid'
          }
        ],
        parameters: {
          region: { type: 'string', required: true },
          ssidName: { type: 'string', required: true },
          securityType: { type: 'string', default: 'wpa2' },
          passphrase: { type: 'string', default: '' }
        },
        validation: `
          if (!data.region) errors.push('region is required');
          if (!data.ssidName) errors.push('ssidName is required');
          if (data.securityType && !['open', 'wpa2', 'wpa3'].includes(data.securityType)) {
            errors.push('securityType must be open, wpa2, or wpa3');
          }
        `
      }
    ];
  }

  /**
   * Get composite templates (combinations of multiple templates)
   * @returns {Array} Composite templates
   */
  getCompositeTemplates() {
    return [
      {
        id: 'full-switch-setup',
        name: 'Full Switch Setup',
        description: 'Complete switch configuration including VLANs and interfaces',
        category: 'composite',
        trigger: 'manual',
        requiresValidation: true,
        apiType: 'aos-cx',
        baseTemplates: ['aos-cx-vlan-management', 'aos-cx-interface-config'],
        operations: [
          {
            name: 'setup',
            method: 'POST',
            endpoint: '/rest/v10.08/system/setup',
            template: 'aos-cx-vlan-management'
          },
          {
            name: 'configure',
            method: 'PUT',
            endpoint: '/rest/v10.08/system/configure',
            template: 'aos-cx-interface-config'
          }
        ],
        parameters: {
          switchIp: { type: 'string', required: true },
          vlans: { type: 'array', required: true },
          interfaces: { type: 'array', required: true }
        },
        validation: `
          if (!data.switchIp) errors.push('switchIp is required');
          if (!data.vlans || !Array.isArray(data.vlans)) errors.push('vlans array is required');
          if (!data.interfaces || !Array.isArray(data.interfaces)) errors.push('interfaces array is required');
        `
      },
      {
        id: 'comprehensive-monitoring',
        name: 'Comprehensive Network Monitoring',
        description: 'Complete monitoring solution for all device types',
        category: 'composite',
        trigger: 'schedule',
        requiresValidation: true,
        apiType: 'central',
        baseTemplates: ['central-device-monitoring', 'scheduled-monitoring'],
        operations: [
          {
            name: 'monitor_devices',
            method: 'GET',
            endpoint: '/api/v2/monitoring/devices',
            template: 'central-device-monitoring'
          },
          {
            name: 'monitor_performance',
            method: 'GET',
            endpoint: '/api/v2/monitoring/performance',
            template: 'scheduled-monitoring'
          }
        ],
        parameters: {
          region: { type: 'string', required: true },
          schedule: { type: 'string', default: '*/5 * * * *' },
          deviceTypes: { type: 'array', default: ['switch', 'ap', 'gateway'] },
          thresholds: { type: 'object', default: { cpu: 80, memory: 85 } }
        },
        validation: `
          if (!data.region) errors.push('region is required');
          if (data.deviceTypes && !Array.isArray(data.deviceTypes)) {
            errors.push('deviceTypes must be an array');
          }
        `
      }
    ];
  }

  /**
   * Select appropriate template based on requirements
   * @param {Object} requirements - Parsed requirements
   * @returns {Object} Selected template
   */
  async selectTemplate(requirements) {
    // Simple template selection logic - can be enhanced with AI/ML
    const templates = Array.from(this.templates.values());

    // Filter by category if specified
    let candidates = templates;
    if (requirements.category) {
      candidates = templates.filter(t => t.category === requirements.category);
    }

    // Filter by API type if specified
    if (requirements.apiType) {
      candidates = candidates.filter(t => t.apiType === requirements.apiType);
    }

    // Filter by trigger type if specified
    if (requirements.trigger) {
      candidates = candidates.filter(t => t.trigger === requirements.trigger);
    }

    // Score templates based on requirements match
    const scoredTemplates = candidates.map(template => ({
      template,
      score: this.scoreTemplate(template, requirements)
    }));

    // Sort by score and return the best match
    scoredTemplates.sort((a, b) => b.score - a.score);

    if (scoredTemplates.length === 0) {
      throw new Error('No suitable template found for requirements');
    }

    return scoredTemplates[0].template;
  }

  /**
   * Score a template based on how well it matches requirements
   * @param {Object} template - Template to score
   * @param {Object} requirements - Requirements to match
   * @returns {number} Score (higher is better)
   */
  scoreTemplate(template, requirements) {
    let score = 0;

    // Category match
    if (requirements.category && template.category === requirements.category) {
      score += 10;
    }

    // API type match
    if (requirements.apiType && template.apiType === requirements.apiType) {
      score += 10;
    }

    // Trigger type match
    if (requirements.trigger && template.trigger === requirements.trigger) {
      score += 8;
    }

    // Operations match
    if (requirements.operations) {
      const templateOps = template.operations.map(op => op.name);
      const matchingOps = requirements.operations.filter(op => templateOps.includes(op));
      score += matchingOps.length * 2;
    }

    // Keywords match
    if (requirements.keywords) {
      const templateText = (template.name + ' ' + template.description).toLowerCase();
      const matchingKeywords = requirements.keywords.filter(keyword =>
        templateText.includes(keyword.toLowerCase())
      );
      score += matchingKeywords.length;
    }

    return score;
  }

  /**
   * Get template by ID
   * @param {string} templateId - Template ID
   * @returns {Object} Template object
   */
  getTemplate(templateId) {
    const template = this.templates.get(templateId);
    if (!template) {
      throw new Error(`Template ${templateId} not found`);
    }
    return template;
  }

  /**
   * Get all templates
   * @returns {Array} Array of all templates
   */
  getAllTemplates() {
    return Array.from(this.templates.values());
  }

  /**
   * Get templates by category
   * @param {string} category - Template category
   * @returns {Array} Array of templates in category
   */
  getTemplatesByCategory(category) {
    return Array.from(this.templates.values()).filter(t => t.category === category);
  }

  /**
   * Validate template parameters
   * @param {Object} template - Template object
   * @param {Object} parameters - Parameters to validate
   * @returns {Object} Validation result
   */
  async validateParameters(template, parameters) {
    const errors = [];
    const warnings = [];

    // Check required parameters
    for (const [paramName, paramDef] of Object.entries(template.parameters || {})) {
      if (paramDef.required && !parameters[paramName]) {
        errors.push(`Required parameter '${paramName}' is missing`);
        continue;
      }

      const value = parameters[paramName];
      if (value === undefined && paramDef.default !== undefined) {
        parameters[paramName] = paramDef.default;
        continue;
      }

      // Type validation
      if (value !== undefined) {
        const typeError = this.validateParameterType(paramName, value, paramDef);
        if (typeError) {
          errors.push(typeError);
        }
      }
    }

    // Check for unknown parameters
    for (const paramName of Object.keys(parameters)) {
      if (!template.parameters || !template.parameters[paramName]) {
        warnings.push(`Unknown parameter '${paramName}' provided`);
      }
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      parameters
    };
  }

  /**
   * Validate parameter type
   * @param {string} paramName - Parameter name
   * @param {*} value - Parameter value
   * @param {Object} paramDef - Parameter definition
   * @returns {string|null} Error message or null if valid
   */
  validateParameterType(paramName, value, paramDef) {
    const type = paramDef.type;

    switch (type) {
      case 'string':
        if (typeof value !== 'string') {
          return `Parameter '${paramName}' must be a string`;
        }
        break;

      case 'number':
        if (typeof value !== 'number' || isNaN(value)) {
          return `Parameter '${paramName}' must be a number`;
        }
        if (paramDef.min !== undefined && value < paramDef.min) {
          return `Parameter '${paramName}' must be at least ${paramDef.min}`;
        }
        if (paramDef.max !== undefined && value > paramDef.max) {
          return `Parameter '${paramName}' must be at most ${paramDef.max}`;
        }
        break;

      case 'boolean':
        if (typeof value !== 'boolean') {
          return `Parameter '${paramName}' must be a boolean`;
        }
        break;

      case 'array':
        if (!Array.isArray(value)) {
          return `Parameter '${paramName}' must be an array`;
        }
        break;

      case 'object':
        if (typeof value !== 'object' || value === null || Array.isArray(value)) {
          return `Parameter '${paramName}' must be an object`;
        }
        break;

      default:
        // Unknown type, skip validation
        break;
    }

    return null;
  }

  /**
   * Create a new template
   * @param {Object} templateData - Template data
   * @returns {Object} Created template
   */
  async createTemplate(templateData) {
    const template = {
      id: templateData.id || uuidv4(),
      name: templateData.name,
      description: templateData.description,
      category: templateData.category || 'custom',
      trigger: templateData.trigger || 'manual',
      requiresValidation: templateData.requiresValidation !== false,
      apiType: templateData.apiType || 'generic',
      baseUrl: templateData.baseUrl || '',
      operations: templateData.operations || [],
      parameters: templateData.parameters || {},
      validation: templateData.validation || '',
      created: new Date().toISOString(),
      version: '1.0.0'
    };

    // Validate template structure
    const validation = await this.validateTemplate(template);
    if (!validation.isValid) {
      throw new Error(`Template validation failed: ${validation.errors.join(', ')}`);
    }

    // Add to templates
    this.templates.set(template.id, template);

    return template;
  }

  /**
   * Update an existing template
   * @param {string} templateId - Template ID
   * @param {Object} updates - Template updates
   * @returns {Object} Updated template
   */
  async updateTemplate(templateId, updates) {
    const existingTemplate = this.getTemplate(templateId);
    const updatedTemplate = { ...existingTemplate, ...updates };

    // Validate updated template
    const validation = await this.validateTemplate(updatedTemplate);
    if (!validation.isValid) {
      throw new Error(`Template validation failed: ${validation.errors.join(', ')}`);
    }

    // Update in templates
    this.templates.set(templateId, updatedTemplate);

    return updatedTemplate;
  }

  /**
   * Delete a template
   * @param {string} templateId - Template ID
   * @returns {boolean} Success status
   */
  async deleteTemplate(templateId) {
    if (!this.templates.has(templateId)) {
      throw new Error(`Template ${templateId} not found`);
    }

    this.templates.delete(templateId);
    return true;
  }

  /**
   * Validate template structure
   * @param {Object} template - Template to validate
   * @returns {Object} Validation result
   */
  async validateTemplate(template) {
    const errors = [];

    // Required fields
    if (!template.id) errors.push('Template ID is required');
    if (!template.name) errors.push('Template name is required');
    if (!template.description) errors.push('Template description is required');

    // Operations validation
    if (!template.operations || !Array.isArray(template.operations)) {
      errors.push('Template operations must be an array');
    } else {
      template.operations.forEach((op, index) => {
        if (!op.name) errors.push(`Operation ${index} missing name`);
        if (!op.method) errors.push(`Operation ${index} missing method`);
        if (!op.endpoint) errors.push(`Operation ${index} missing endpoint`);
      });
    }

    // Parameters validation
    if (template.parameters && typeof template.parameters !== 'object') {
      errors.push('Template parameters must be an object');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Compose multiple templates into a single template
   * @param {Array} templateIds - Array of template IDs to compose
   * @param {Object} compositionConfig - Configuration for composition
   * @returns {Object} Composed template
   */
  async composeTemplates(templateIds, compositionConfig) {
    const templates = templateIds.map(id => this.getTemplate(id));
    
    const composedTemplate = {
      id: compositionConfig.id || uuidv4(),
      name: compositionConfig.name || 'Composed Template',
      description: compositionConfig.description || 'Composed from multiple templates',
      category: 'composite',
      trigger: compositionConfig.trigger || 'manual',
      requiresValidation: true,
      apiType: compositionConfig.apiType || templates[0].apiType,
      baseTemplates: templateIds,
      operations: [],
      parameters: {},
      validation: ''
    };

    // Merge operations from all templates
    templates.forEach(template => {
      composedTemplate.operations.push(...template.operations);
    });

    // Merge parameters from all templates
    templates.forEach(template => {
      Object.assign(composedTemplate.parameters, template.parameters);
    });

    // Combine validation code
    const validationCode = templates
      .map(template => template.validation)
      .filter(validation => validation)
      .join('\n\n');
    
    composedTemplate.validation = validationCode;

    // Validate composed template
    const validation = await this.validateTemplate(composedTemplate);
    if (!validation.isValid) {
      throw new Error(`Composed template validation failed: ${validation.errors.join(', ')}`);
    }

    return composedTemplate;
  }

  /**
   * Export templates to JSON
   * @param {Array} templateIds - Template IDs to export (optional, exports all if not provided)
   * @returns {string} JSON string of templates
   */
  async exportTemplates(templateIds = null) {
    const templates = templateIds 
      ? templateIds.map(id => this.getTemplate(id))
      : this.getAllTemplates();

    return JSON.stringify(templates, null, 2);
  }

  /**
   * Import templates from JSON
   * @param {string} jsonData - JSON string of templates
   * @returns {Array} Array of imported template IDs
   */
  async importTemplates(jsonData) {
    const templates = JSON.parse(jsonData);
    const importedIds = [];

    for (const templateData of templates) {
      const template = await this.createTemplate(templateData);
      importedIds.push(template.id);
    }

    return importedIds;
  }
}

module.exports = TemplateEngine;
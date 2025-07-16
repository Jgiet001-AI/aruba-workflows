# Helper Scripts

This directory contains utility scripts to support HPE Aruba workflow development.

## Available Scripts

### Development Scripts
- `test-api-connectivity.js` - Test all HPE Aruba API endpoints
- `validate-workflow.js` - Validate workflow JSON structure
- `export-workflows.js` - Bulk export workflows from n8n
- `import-workflows.js` - Bulk import workflows to n8n

### Utility Scripts
- `generate-test-data.js` - Create sample data for testing
- `check-credentials.js` - Verify credential configuration
- `monitor-performance.js` - Track workflow execution metrics
- `cleanup-logs.js` - Archive and clean workflow logs

### Deployment Scripts
- `deploy-production.js` - Deploy workflows to production
- `rollback-workflows.js` - Rollback to previous versions
- `backup-configs.js` - Backup workflow configurations
- `update-credentials.js` - Rotate and update API credentials

## Usage

Most scripts can be run with Node.js:

```bash
node scripts/test-api-connectivity.js
node scripts/validate-workflow.js path/to/workflow.json
```

## Configuration

Scripts use environment variables for configuration:
- `N8N_HOST`: n8n instance host (default: 192.168.40.100)
- `N8N_PORT`: n8n instance port (default: 8006)
- `N8N_PROTOCOL`: HTTP/HTTPS (default: http)
- `WORKFLOW_DIR`: Base workflow directory

## Dependencies

Scripts require:
- Node.js 16+
- npm packages: axios, fs-extra, chalk
- Environment variables configured
- n8n instance accessible

## Development Guidelines

When creating new scripts:
- Use consistent error handling
- Include progress indicators
- Add comprehensive logging
- Support dry-run mode
- Document all parameters
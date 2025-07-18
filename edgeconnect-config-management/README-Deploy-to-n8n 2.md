# EdgeConnect Workflows - Deploy to n8n Guide

## Overview
This guide provides step-by-step instructions for importing and configuring the EdgeConnect automation workflows in your n8n instance.

## Prerequisites
- n8n instance running at `http://192.168.40.100:8006`
- n8n API access (web interface or API key)
- EdgeConnect Orchestrator credentials
- Slack webhook URLs for notifications

## Step 1: Configure EdgeConnect Credentials in n8n

### 1.1 Create EdgeConnect Orchestrator Credential

1. Open n8n web interface: `http://192.168.40.100:8006`
2. Go to **Settings** → **Credentials**
3. Click **+ Add Credential**
4. Select **HTTP Header Auth**
5. Configure as follows:

```json
{
  "name": "EdgeConnect Orchestrator API",
  "headerAuth": {
    "name": "X-AUTH-TOKEN",
    "value": "YOUR_EDGECONNECT_API_TOKEN"
  }
}
```

### 1.2 Create Slack Notification Credentials

1. Add another credential for Slack
2. Select **Slack** credential type
3. Configure webhook URLs:
   - Success notifications: `#network-automation`
   - Alerts/Failures: `#network-alerts`

## Step 2: Import EdgeConnect Workflows

### 2.1 EdgeConnect SD-WAN Policy Management

1. Go to **Workflows** in n8n
2. Click **+ Add Workflow**
3. Click **Import** (⋯ menu)
4. Copy and paste the content from: `edgeconnect-sdwan-policy-workflow.json`
5. Save as "EdgeConnect SD-WAN Policy Management"

**Webhook Endpoint**: `/edgeconnect-policy`

**Operations Supported**:
- `create_network_segment_policy`
- `update_network_segment_policy`
- `delete_network_segment_policy`
- `list_network_segment_policies`
- `create_tunnel_policy`
- `update_tunnel_policy`
- `delete_tunnel_policy`
- `list_tunnel_policies`
- `create_route_policy`
- `update_route_policy`
- `delete_route_policy`
- `list_route_policies`
- `backup_all_policies`
- `restore_policies`

### 2.2 EdgeConnect Appliance Provisioning

1. Import: `edgeconnect-appliance-provisioning-workflow.json`
2. Save as "EdgeConnect Appliance Provisioning"

**Webhook Endpoint**: `/edgeconnect-provisioning`

**Operations Supported**:
- `create_branch_config` (with templates: small_branch, medium_branch, large_branch)
- `update_branch_config`
- `delete_branch_config`
- `list_branch_configs`
- `create_hub_config` (with templates: regional_hub, datacenter_hub)
- `update_hub_config`
- `delete_hub_config`
- `list_hub_configs`
- `create_hub_cluster` (with templates: ha_cluster, load_balance_cluster)
- `update_hub_cluster`
- `delete_hub_cluster`
- `list_hub_clusters`
- `create_microbranch_dc`
- `update_microbranch_dc`
- `delete_microbranch_dc`
- `get_admin_status`
- `set_admin_status`
- `get_topology`
- `update_topology`

### 2.3 EdgeConnect Performance Monitoring

1. Import: `edgeconnect-performance-monitoring-workflow.json`
2. Save as "EdgeConnect Performance Monitoring"

**Schedule**: Every 5 minutes
**Features**:
- Gateway performance statistics
- Tunnel health monitoring
- Policy compliance tracking
- Usage analytics
- Intelligent threshold-based alerting

### 2.4 EdgeConnect Backup & Restore

1. Import: `edgeconnect-backup-restore-workflow.json`
2. Save as "EdgeConnect Backup & Restore"

**Triggers**:
- **Webhook**: `/edgeconnect-backup` (manual operations)
- **Schedule**: Daily at 2:00 AM (automated backups)

**Operations Supported**:
- `backup_all`
- `backup_policies`
- `backup_branch_configs`
- `backup_hub_configs`
- `backup_route_policies`
- `restore_configuration`
- `list_backups`
- `verify_backup`
- `cleanup_old_backups`

## Step 3: Configure Environment Variables

In each workflow, update the following environment variables:

### 3.1 Common Variables
```javascript
// Update these in the "Initialize" or "Validate Input" nodes
const config = {
  orchestratorHost: 'your-orchestrator.example.com',  // Replace with actual host
  authToken: 'your-auth-token-here',                   // Use credential reference
  nodeType: 'group',                                   // or 'global'
  nodeId: 'Your-Group-Name'                           // Replace with actual group
};
```

### 3.2 Monitoring Specific Variables
```javascript
// In the performance monitoring workflow
const config = {
  thresholds: {
    cpu: 80,
    memory: 85,
    bandwidth: 90,
    tunnelLatency: 100,    // ms
    packetLoss: 1.0,       // percent
    jitter: 10             // ms
  },
  targets: {
    gateways: [
      'EC001234567890',    // Replace with actual gateway serials
      'EC001234567891',
      'EC001234567892'
    ],
    clusters: [
      'primary-hub-cluster',     // Replace with actual cluster names
      'secondary-hub-cluster'
    ],
    policies: [
      'global-qos-policy',       // Replace with actual policy names
      'wan-optimization-policy',
      'security-policy'
    ]
  }
};
```

### 3.3 Backup Specific Variables
```javascript
// In the backup workflow
const config = {
  backupLocation: '/path/to/backup/directory/',  // Update backup path
  retentionDays: 30,
  compress: true,
  verifyBackup: true
};
```

## Step 4: Test Workflows

### 4.1 Test Policy Management
```bash
# Test network segment policy creation
curl -X POST http://192.168.40.100:8006/webhook/edgeconnect-policy \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_network_segment_policy",
    "orchestrator_host": "your-orchestrator.example.com",
    "auth_token": "your-token",
    "policy_name": "test-policy",
    "policy_data": {
      "segment": "test-segment",
      "priority": 100
    }
  }'
```

### 4.2 Test Appliance Provisioning
```bash
# Test branch configuration with template
curl -X POST http://192.168.40.100:8006/webhook/edgeconnect-provisioning \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_branch_config",
    "orchestrator_host": "your-orchestrator.example.com",
    "auth_token": "your-token",
    "config_data": {
      "template": "small_branch"
    }
  }'
```

### 4.3 Test Backup Operations
```bash
# Test full backup
curl -X POST http://192.168.40.100:8006/webhook/edgeconnect-backup \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "backup_all",
    "orchestrator_host": "your-orchestrator.example.com",
    "auth_token": "your-token"
  }'
```

## Step 5: Monitor Workflow Execution

### 5.1 Check Workflow Status
1. Go to **Executions** in n8n
2. Monitor execution logs for each workflow
3. Check for any errors in the execution details

### 5.2 Slack Notifications
- **Success notifications**: Check `#network-automation`
- **Warning/Error alerts**: Check `#network-alerts`

### 5.3 Performance Monitoring
The performance monitoring workflow runs every 5 minutes and will:
- Collect gateway statistics
- Monitor tunnel health
- Check policy compliance
- Send alerts when thresholds are exceeded

## Step 6: Production Deployment Checklist

### 6.1 Security Configuration
- [ ] Replace all placeholder credentials with actual values
- [ ] Use n8n credential store for sensitive data
- [ ] Verify HTTPS endpoints for production
- [ ] Configure proper authentication scopes

### 6.2 Monitoring Configuration
- [ ] Adjust performance thresholds for your environment
- [ ] Configure appropriate notification channels
- [ ] Set up proper backup retention policies
- [ ] Test error handling and rollback procedures

### 6.3 Operational Readiness
- [ ] Document escalation procedures
- [ ] Train operations team on workflow management
- [ ] Set up monitoring dashboards
- [ ] Configure log retention and analysis

## Troubleshooting

### Common Issues

**1. Authentication Failures**
- Verify EdgeConnect Orchestrator credentials
- Check API token validity and permissions
- Ensure correct orchestrator URL

**2. Network Connectivity**
- Verify n8n can reach EdgeConnect Orchestrator
- Check firewall rules and network routing
- Test API connectivity manually

**3. Workflow Execution Errors**
- Check n8n execution logs
- Verify input parameter format
- Review error messages in Slack notifications

**4. Performance Issues**
- Monitor API rate limits
- Adjust timeout settings if needed
- Review batch processing configuration

### Support Contacts
- **Network Team**: `#network-automation`
- **Critical Issues**: `#network-alerts`
- **Documentation**: This README and individual workflow documentation

## Next Steps

Once all workflows are deployed and tested:

1. **Schedule regular reviews** of workflow performance
2. **Monitor** EdgeConnect automation effectiveness
3. **Optimize** based on operational feedback
4. **Expand** automation to additional network operations
5. **Document** lessons learned and best practices

---

**Last Updated**: January 16, 2025
**Version**: 1.0
**Workflows**: 4 EdgeConnect automation workflows covering 143 API endpoints
# AOS-CX Configuration Backup & Restore Workflow

## Overview

This n8n workflow provides comprehensive configuration backup and restore capabilities for HPE Aruba AOS-CX switches. It supports automated daily backups, manual on-demand operations, configuration comparison, and emergency restore procedures with full error handling and notification systems.

## Features

### Core Operations
- **Automated Backup**: Daily scheduled backups at 2 AM
- **Manual Backup**: On-demand backup via webhook trigger
- **Configuration Restore**: Restore from any backup file with validation
- **Configuration Comparison**: Compare current config vs backup files
- **Backup Management**: List, cleanup, and manage backup files
- **Checkpoint Creation**: Automatic checkpoints during backup process

### Advanced Features
- **Multi-Backup Type Support**: Running config and startup config
- **Compression**: Optional backup file compression
- **Retention Management**: Automatic cleanup of old backups (30-day default)
- **Configuration Validation**: Backup file integrity and format validation
- **Verification**: Post-restore configuration verification
- **Multi-Switch Support**: Handle multiple switches via parameterization

### Error Handling & Notifications
- **Comprehensive Error Handling**: Network, API, file system, and validation errors
- **Smart Retry Logic**: Configurable retry for transient failures
- **Real-time Notifications**: Slack and email alerts for success/failure
- **Detailed Logging**: Complete audit trail of all operations
- **Rollback Support**: Emergency rollback capabilities

## Workflow File

**Location**: `/Users/jeangiet/Documents/Claude/aruba-workflows/aos-cx-config-management/aos-cx-backup-restore-workflow.json`

## API Endpoints Used

### Configuration Backup
- `GET /rest/v10.08/system` - Get system information
- `GET /rest/v10.08/fullconfigs/running-config` - Get running configuration
- `GET /rest/v10.08/fullconfigs/startup-config` - Get startup configuration

### Configuration Restore
- `PUT /rest/v10.08/fullconfigs/startup-config` - Update startup configuration
- `POST /rest/v10.08/system/config/cfg_restore` - Restore configuration

### Checkpoint Management
- `POST /rest/v10.08/system/config/checkpoint` - Create configuration checkpoint

## Input Parameters

### Required Parameters
- `operation`: Operation to perform
  - Options: `backup`, `restore`, `compare`, `list_backups`, `create_checkpoint`
- `switch_ip`: IP address of target AOS-CX switch (required for backup/restore)

### Optional Parameters
- `backup_type`: Type of configuration to backup
  - Options: `running` (default), `startup`
- `backup_name`: Custom backup filename (auto-generated if not provided)
- `restore_file`: Backup file to restore from (required for restore operation)
- `compression_enabled`: Enable backup compression (default: `true`)
- `retention_days`: Number of days to keep backups (default: `30`)
- `compare_configs`: Compare current vs backup before restore (default: `false`)

## Usage Examples

### 1. Manual Backup (via Webhook)

```bash
# Webhook URL: http://192.168.40.100:8006/webhook/aos-cx-backup-restore

# Basic backup
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "backup",
    "switch_ip": "192.168.1.100",
    "backup_type": "running"
  }'

# Backup with custom name and compression
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "backup",
    "switch_ip": "192.168.1.100",
    "backup_type": "running",
    "backup_name": "pre_maintenance_backup_2025_01_16",
    "compression_enabled": true
  }'

# Startup configuration backup
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "backup",
    "switch_ip": "192.168.1.100",
    "backup_type": "startup",
    "backup_name": "startup_config_backup"
  }'
```

### 2. Configuration Restore

```bash
# Restore from backup file
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "restore",
    "switch_ip": "192.168.1.100",
    "restore_file": "pre_maintenance_backup_2025_01_16.json.gz"
  }'

# Restore with configuration comparison
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "restore",
    "switch_ip": "192.168.1.100",
    "restore_file": "emergency_restore_backup.json",
    "compare_configs": true
  }'
```

### 3. Configuration Comparison

```bash
# Compare current config with backup
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "compare",
    "switch_ip": "192.168.1.100",
    "backup_name": "baseline_config_2025_01_01.json"
  }'
```

### 4. Backup Management

```bash
# List all backups
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list_backups"
  }'

# List backups with custom retention
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "list_backups",
    "retention_days": 60
  }'
```

### 5. Create Checkpoint

```bash
# Create configuration checkpoint
curl -X POST "http://192.168.40.100:8006/webhook/aos-cx-backup-restore" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_checkpoint",
    "switch_ip": "192.168.1.100"
  }'
```

## Backup File Structure

### Backup File Format
```json
{
  "metadata": {
    "backup_timestamp": "2025-01-16T14:30:00.000Z",
    "backup_type": "running",
    "device_info": {
      "hostname": "switch-core-01",
      "software_version": "10.08.1010",
      "platform_name": "8320",
      "serial_number": "AB123456",
      "model": "JL479A",
      "mgmt_ip": "192.168.1.100"
    },
    "backup_size": 1024000,
    "backup_name": "scheduled_backup_2025-01-16_1642091234567",
    "compression_enabled": true,
    "api_version": "v10.08",
    "backup_method": "REST_API"
  },
  "configuration": {
    "System": {...},
    "Port": {...},
    "VLAN": {...},
    "Interface": {...}
  },
  "created_by": "AOS-CX Backup & Restore Workflow",
  "workflow_version": "1.0.0"
}
```

### Compressed File Format
```json
{
  "compressed": true,
  "original_size": 1024000,
  "data": "base64-encoded-compressed-data"
}
```

## File Storage

### Backup Directory
- **Path**: `/Users/jeangiet/Documents/Claude/aruba-workflows/aos-cx-config-management/backups/`
- **Naming Convention**: `{backup_name}.json` or `{backup_name}.json.gz`
- **Auto-generated Names**: `{switch_ip}_{backup_type}_{date}_{timestamp}`

### File Organization
```
backups/
├── 192.168.1.100_running_2025-01-16_1642091234567.json.gz
├── 192.168.1.100_startup_2025-01-16_1642091234567.json
├── pre_maintenance_backup_2025_01_16.json.gz
├── emergency_restore_backup.json
└── baseline_config_2025_01_01.json
```

## Scheduling

### Automated Daily Backup
- **Schedule**: Daily at 2:00 AM (America/New_York timezone)
- **Operation**: Backup running configuration
- **Features**: 
  - Compression enabled
  - 30-day retention
  - Automatic checkpoint creation
  - Slack/email notifications

### Customizing Schedule
To modify the backup schedule, update the "Daily Backup Schedule" node:
```json
{
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "hours",
          "hoursInterval": 6  // Every 6 hours
        }
      ]
    },
    "timezone": "America/New_York"
  }
}
```

## Error Handling

### Network Errors
- **Connectivity Issues**: 3 retry attempts with 2-second delays
- **Timeout Handling**: 30-60 second timeouts based on operation
- **Certificate Issues**: Proper HTTPS handling

### API Errors
- **Authentication Failures**: Immediate notification
- **Rate Limiting**: Exponential backoff retry
- **Invalid Responses**: Comprehensive validation

### File System Errors
- **Directory Access**: Permission validation
- **Disk Space**: Storage availability checks
- **File Corruption**: Integrity validation

### Validation Errors
- **IP Address Format**: Regex validation
- **Parameter Validation**: Required field checks
- **Backup File Format**: Structure validation

## Notification Configuration

### Slack Notifications
- **Channel**: `#network-automation`
- **Success Messages**: Detailed operation summaries
- **Error Messages**: Comprehensive error details and troubleshooting steps
- **Color Coding**: Green (success), Yellow (warning), Red (error)

### Email Notifications
- **Recipients**: `network-team@company.com`
- **HTML Format**: Rich formatting with technical details
- **Subject Lines**: Operation-specific subjects
- **Attachments**: Relevant operation details

## Credentials Configuration

### Required Credentials
Create in n8n Credential Store:

#### AOS-CX Switch Authentication
- **Credential Type**: HTTP Header Auth
- **Name**: `AOS-CX API Auth`
- **Header Name**: `Authorization`
- **Header Value**: `Bearer {your-api-token}`

#### Slack Integration
- **Credential Type**: Slack OAuth2 API
- **Name**: `Slack Network Alerts`
- **Configuration**: Webhook URL or OAuth token

#### Email Configuration
- **Credential Type**: SMTP
- **Name**: `Network Team Email`
- **Configuration**: SMTP server details

## Security Considerations

### Data Protection
- **Credential Storage**: Use n8n credential store only
- **Backup Encryption**: Consider encrypting sensitive backup files
- **Access Control**: Restrict webhook access to authorized networks
- **Audit Trail**: Complete logging of all operations

### Network Security
- **HTTPS Only**: All API communications use HTTPS
- **Token Rotation**: Regular API token rotation recommended
- **Network Isolation**: Deploy n8n in secure network segment

## Troubleshooting

### Common Issues

#### 1. Backup File Not Found
**Error**: "Failed to process backup file: ENOENT: no such file or directory"
**Solution**: 
- Verify backup file exists in backup directory
- Check filename spelling and extension
- Ensure proper file permissions

#### 2. Authentication Failure
**Error**: "401 Unauthorized"
**Solution**:
- Verify API token is valid and not expired
- Check credentials configuration in n8n
- Confirm switch REST API is enabled

#### 3. Network Connectivity
**Error**: "ECONNREFUSED" or "ETIMEDOUT"
**Solution**:
- Verify switch IP address is reachable
- Check network firewall rules
- Confirm switch HTTPS interface is enabled

#### 4. Insufficient Storage
**Error**: "ENOSPC: no space left on device"
**Solution**:
- Check available disk space
- Run backup cleanup with shorter retention period
- Move old backups to external storage

#### 5. Configuration Restore Failure
**Error**: "Configuration restore failed"
**Solution**:
- Verify backup file integrity
- Check configuration compatibility
- Ensure switch has sufficient resources

### Debugging Steps

1. **Check Switch Connectivity**
   ```bash
   ping 192.168.1.100
   curl -k https://192.168.1.100/rest/v10.08/system
   ```

2. **Verify API Access**
   ```bash
   curl -k -H "Authorization: Bearer YOUR_TOKEN" \
     https://192.168.1.100/rest/v10.08/system
   ```

3. **Check Backup Directory**
   ```bash
   ls -la /Users/jeangiet/Documents/Claude/aruba-workflows/aos-cx-config-management/backups/
   df -h /Users/jeangiet/Documents/Claude/aruba-workflows/
   ```

4. **Validate Backup File**
   ```bash
   cat backup_file.json | jq '.metadata'
   ```

## Performance Considerations

### Optimization Tips
- **Batch Operations**: Process multiple switches sequentially to avoid overwhelming
- **Compression**: Enable compression for large configurations
- **Retention**: Balance retention period with storage requirements
- **Scheduling**: Stagger backups across multiple switches

### Resource Usage
- **Memory**: ~50MB per backup operation
- **Storage**: 1-10MB per backup (depending on configuration size)
- **Network**: Minimal bandwidth requirements
- **CPU**: Low CPU usage

## Integration

### ServiceNow Integration
Add ServiceNow ticket creation for failed operations:
```javascript
// In error handler, add ServiceNow ticket creation
const ticketData = {
  short_description: `AOS-CX Backup Failure: ${switchIp}`,
  description: `Backup operation failed: ${errorMessage}`,
  category: 'Network',
  subcategory: 'Configuration Management',
  priority: 2
};
```

### Monitoring Integration
Connect to monitoring systems:
- **Prometheus**: Export metrics via webhook
- **Grafana**: Create dashboards for backup status
- **Datadog**: Send backup events and metrics

## Best Practices

### Backup Strategy
- **Daily Automation**: Use scheduled daily backups for baseline protection
- **Change Management**: Manual backups before configuration changes
- **Testing**: Regular restore testing to verify backup integrity
- **Documentation**: Maintain backup logs and change documentation

### Security
- **Token Rotation**: Rotate API tokens quarterly
- **Access Control**: Limit webhook access to authorized systems
- **Encryption**: Encrypt backups containing sensitive information
- **Monitoring**: Monitor all backup and restore operations

### Maintenance
- **Regular Testing**: Test restore procedures monthly
- **Cleanup**: Monitor storage usage and retention policies
- **Updates**: Keep workflow updated with latest API versions
- **Documentation**: Update procedures with any environment changes

## Support and Maintenance

### Monitoring Checklist
- [ ] Daily backup completion status
- [ ] Storage usage and cleanup effectiveness
- [ ] Error rates and failure patterns
- [ ] API token expiration dates
- [ ] Network connectivity status

### Monthly Tasks
- [ ] Test restore procedure with sample backup
- [ ] Review and optimize retention policies
- [ ] Update API tokens if needed
- [ ] Verify notification channels are working
- [ ] Review backup file integrity

### Quarterly Tasks
- [ ] Full disaster recovery test
- [ ] Review and update security configurations
- [ ] Validate backup file formats with new switch firmware
- [ ] Update documentation with any changes
- [ ] Performance review and optimization

## Version History

- **v1.0.0** (2025-01-16): Initial release
  - Complete backup and restore functionality
  - Automated scheduling and retention management
  - Comprehensive error handling and notifications
  - Multi-operation support (backup, restore, compare, list)
  - Configuration validation and verification

## Related Workflows

- **VLAN Management**: `/aos-cx-config-management/aos-cx-vlan-management-workflow.json`
- **Interface Configuration**: `/aos-cx-config-management/aos-cx-interface-configuration-workflow.json`
- **Policy Deployment**: `/aos-cx-config-management/aos-cx-policy-deployment-workflow.json`

---

**Generated by**: AOS-CX Backup & Restore Workflow v1.0.0  
**Last Updated**: January 16, 2025  
**Contact**: Network Automation Team
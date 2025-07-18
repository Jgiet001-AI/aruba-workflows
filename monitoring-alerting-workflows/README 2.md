# HPE Aruba Network Monitoring & Alerting Workflows

**Version**: 1.0.0  
**Created**: January 2025  
**Last Updated**: January 2025

## Overview

This directory contains comprehensive n8n workflows for monitoring and alerting across the entire HPE Aruba network infrastructure. These workflows provide real-time monitoring, intelligent alerting, and automated response capabilities for network health, performance, and security.

## 🚀 Features

### Core Capabilities
- **Device Health Monitoring**: Real-time monitoring of all network devices
- **Performance Monitoring**: Network performance metrics and optimization
- **Alert Aggregation**: Intelligent alert correlation and deduplication
- **Automated Response**: Proactive issue remediation and escalation
- **Multi-Platform Support**: Central, AOS-CX, EdgeConnect, and UXI integration
- **Real-time Notifications**: Slack, email, and webhook notifications

### Supported Integrations
- **HPE Aruba Central**: Device inventory, health, and performance monitoring
- **AOS-CX Switches**: Interface monitoring, VLAN status, and performance metrics
- **EdgeConnect SD-WAN**: WAN performance, tunnel health, and policy compliance
- **UXI Sensors**: User experience monitoring and synthetic testing
- **External Systems**: ServiceNow, Slack, email, and custom webhooks

## 📁 Directory Structure

```
monitoring-alerting-workflows/
├── README.md                                    # This file
├── device-health-monitoring-workflow.json      # Device health monitoring
├── network-performance-monitoring-workflow.json # Network performance monitoring
├── alert-aggregation-workflow.json             # Alert aggregation and correlation
├── config/
│   ├── parameters.json                         # Configuration parameters
│   └── credentials.md                          # Credential setup guide
├── tests/
│   ├── device-health-test-examples.json       # Device health monitoring tests
│   ├── performance-monitoring-test-examples.json # Performance monitoring tests
│   └── alert-aggregation-test-examples.json   # Alert aggregation tests
├── docs/
│   ├── device-health-monitoring-guide.md      # Device health monitoring guide
│   ├── performance-monitoring-guide.md        # Performance monitoring guide
│   └── alert-aggregation-guide.md             # Alert aggregation guide
└── versions/
    └── [workflow-name]-v1.0.0.json            # Version history
```

## 🔧 Workflows

### 1. Device Health Monitoring Workflow
**File**: `device-health-monitoring-workflow.json`
**Schedule**: Every 5 minutes
**Webhook**: `/device-health-monitoring` (for manual triggers)

#### Monitored Metrics:
- **CPU Usage**: Device processor utilization
- **Memory Usage**: RAM and storage utilization
- **Temperature**: Device temperature monitoring
- **Interface Status**: Port up/down status and utilization
- **Power Status**: PoE consumption and power supply health
- **Firmware Version**: Version compliance and update status

#### Supported Devices:
- **Aruba Central**: All managed devices via Central API
- **AOS-CX Switches**: Direct switch monitoring via REST API
- **EdgeConnect Appliances**: SD-WAN device health monitoring
- **Access Points**: Wireless AP health and performance
- **UXI Sensors**: Sensor health and connectivity

#### Alert Thresholds:
- **CPU**: >80% for 10 minutes
- **Memory**: >85% for 5 minutes
- **Temperature**: >75°C
- **Interface**: Down for >2 minutes
- **Power**: >90% PoE consumption

### 2. Network Performance Monitoring Workflow
**File**: `network-performance-monitoring-workflow.json`
**Schedule**: Every 1 minute
**Webhook**: `/network-performance-monitoring`

#### Performance Metrics:
- **Bandwidth Utilization**: Interface throughput and capacity
- **Latency**: End-to-end network latency
- **Packet Loss**: Network reliability metrics
- **Jitter**: Network stability measurements
- **Application Performance**: Application-specific metrics from UXI
- **User Experience Scores**: Real user experience data

#### Monitoring Sources:
- **Central API**: Device performance metrics
- **AOS-CX SNMP**: Switch interface statistics
- **EdgeConnect**: WAN performance and tunnel metrics
- **UXI API**: User experience and synthetic testing
- **Custom Probes**: Synthetic transaction monitoring

#### Performance Thresholds:
- **Bandwidth**: >90% utilization for 5 minutes
- **Latency**: >100ms average for 10 minutes
- **Packet Loss**: >1% for 5 minutes
- **Jitter**: >20ms for 10 minutes
- **User Experience**: Score <7/10 for 15 minutes

### 3. Alert Aggregation Workflow
**File**: `alert-aggregation-workflow.json`
**Trigger**: Webhook (receives alerts from all sources)
**Webhook**: `/alert-aggregation`

#### Alert Sources:
- **Device Health Monitoring**: Device-specific alerts
- **Performance Monitoring**: Performance degradation alerts
- **Security Events**: Security policy violations
- **Configuration Changes**: Unauthorized configuration changes
- **External Systems**: Third-party monitoring tools

#### Alert Processing:
- **Deduplication**: Remove duplicate alerts within time window
- **Correlation**: Group related alerts from multiple sources
- **Prioritization**: Assign severity levels (Critical, High, Medium, Low)
- **Escalation**: Route alerts to appropriate teams
- **Enrichment**: Add context and troubleshooting information

#### Alert Routing:
- **Critical**: Immediate notification to on-call engineer
- **High**: Notification to network operations team
- **Medium**: Email notification to team leads
- **Low**: Dashboard notification only

## 🛠️ Setup and Configuration

### Prerequisites
1. **n8n Platform**: Version 1.x or higher
2. **HPE Aruba Access**: Central, AOS-CX, EdgeConnect, UXI credentials
3. **Notification Channels**: Slack, email, ServiceNow (optional)
4. **Monitoring Tools**: Additional monitoring integration (optional)

### Quick Start

1. **Import Workflows**:
   ```bash
   # Copy workflow files to your n8n instance
   cp *.json /path/to/n8n/workflows/
   ```

2. **Configure Credentials**:
   - Add all HPE Aruba API credentials in n8n
   - Configure notification channels (Slack, email)
   - Set up monitoring tool integrations

3. **Configure Monitoring Parameters**:
   Edit `config/parameters.json` to customize thresholds and settings

4. **Test Workflows**:
   ```bash
   # Test device health monitoring
   curl -X POST http://your-n8n-instance/webhook/device-health-monitoring \\
     -H "Content-Type: application/json" \\
     -d '{"test": true, "device_type": "switch"}'
   ```

### Configuration Parameters

Edit `config/parameters.json` to customize:

```json
{
  "monitoring_intervals": {
    "device_health": "5m",
    "performance": "1m",
    "alert_processing": "real-time"
  },
  "alert_thresholds": {
    "cpu_usage": 80,
    "memory_usage": 85,
    "temperature": 75,
    "bandwidth_utilization": 90,
    "latency": 100,
    "packet_loss": 1
  },
  "notification_settings": {
    "slack_channel": "#network-alerts",
    "email_recipients": ["network-team@company.com"],
    "escalation_timeout": "15m"
  },
  "data_retention": {
    "metrics": "90d",
    "alerts": "365d",
    "logs": "30d"
  }
}
```

## 📊 Monitoring Dashboard Integration

### Supported Dashboards
- **Grafana**: Time-series metrics visualization
- **Elastic Stack**: Log aggregation and search
- **ServiceNow**: ITSM integration
- **Slack**: Real-time team notifications
- **Custom Dashboards**: API endpoints for custom integrations

### Key Performance Indicators (KPIs)
- **Network Uptime**: 99.9% target
- **Mean Time to Detection (MTTD)**: <2 minutes
- **Mean Time to Resolution (MTTR)**: <15 minutes
- **False Positive Rate**: <5%
- **Alert Resolution Rate**: >95%

## 🔒 Security and Compliance

### Security Features
- **Encrypted Communications**: All API calls use HTTPS/TLS
- **Credential Management**: Secure credential storage in n8n
- **Access Control**: Role-based access to monitoring data
- **Audit Logging**: Complete activity logging
- **Data Privacy**: Compliance with data protection regulations

### Compliance Monitoring
- **Configuration Compliance**: Baseline configuration monitoring
- **Security Policy Compliance**: Security standard adherence
- **Regulatory Compliance**: Industry-specific requirements
- **Change Management**: Automated change tracking

## 📈 Performance Optimization

### Optimization Features
- **Intelligent Polling**: Adaptive polling intervals based on device status
- **Data Compression**: Efficient data transmission and storage
- **Caching**: Reduce API calls through intelligent caching
- **Load Balancing**: Distribute monitoring load across multiple instances
- **Resource Management**: Optimize CPU and memory usage

### Scalability
- **Horizontal Scaling**: Support for multiple n8n instances
- **Device Limit**: Monitor 10,000+ devices simultaneously
- **Alert Volume**: Process 10,000+ alerts per hour
- **Data Throughput**: Handle high-volume metric ingestion

## 🚨 Alert Management

### Alert Lifecycle
1. **Detection**: Automatic threshold-based detection
2. **Validation**: Confirm alert conditions
3. **Enrichment**: Add context and troubleshooting info
4. **Routing**: Send to appropriate teams
5. **Escalation**: Escalate unresolved alerts
6. **Resolution**: Track resolution and close alerts

### Alert Categories
- **Device Alerts**: Hardware and software issues
- **Performance Alerts**: Performance degradation
- **Security Alerts**: Security policy violations
- **Configuration Alerts**: Unauthorized changes
- **Network Alerts**: Connectivity and routing issues

## 📚 API Reference

### Device Health Monitoring APIs

#### Aruba Central
- `GET /monitoring/v1/devices/{device_id}/health` - Device health status
- `GET /monitoring/v1/devices/{device_id}/utilization` - Resource utilization
- `GET /monitoring/v1/devices/{device_id}/interfaces` - Interface statistics

#### AOS-CX
- `GET /rest/v10.08/system/cpu` - CPU utilization
- `GET /rest/v10.08/system/memory` - Memory utilization
- `GET /rest/v10.08/system/temperature` - Temperature sensors

#### EdgeConnect
- `GET /api/v1/appliances/{id}/health` - Appliance health
- `GET /api/v1/appliances/{id}/performance` - Performance metrics
- `GET /api/v1/tunnels/{id}/status` - Tunnel health

#### UXI
- `GET /api/v1/sensors/{id}/health` - Sensor health
- `GET /api/v1/tests/{id}/results` - Test results
- `GET /api/v1/metrics/network` - Network metrics

## 🧪 Testing

### Test Scenarios
1. **Device Health Tests**: Simulate device failures and recovery
2. **Performance Tests**: Test threshold-based alerting
3. **Alert Processing Tests**: Validate alert aggregation and routing
4. **Integration Tests**: End-to-end monitoring workflow testing
5. **Load Tests**: High-volume alert processing

### Test Files
- **Device Health Tests**: `tests/device-health-test-examples.json`
- **Performance Tests**: `tests/performance-monitoring-test-examples.json`
- **Alert Tests**: `tests/alert-aggregation-test-examples.json`

## 🔄 Maintenance

### Regular Maintenance
- **Daily**: Review alert dashboard and performance metrics
- **Weekly**: Analyze alert trends and optimize thresholds
- **Monthly**: Review and update monitoring configurations
- **Quarterly**: Performance optimization and capacity planning

### Backup and Recovery
- **Configuration Backup**: Automated backup of monitoring configurations
- **Historical Data**: Long-term metric and alert data retention
- **Disaster Recovery**: Monitoring system recovery procedures

## 📞 Support and Troubleshooting

### Common Issues
- **High False Positive Rate**: Adjust alert thresholds
- **Missing Alerts**: Check device connectivity and credentials
- **Performance Issues**: Optimize polling intervals and caching
- **Integration Problems**: Verify API credentials and network connectivity

### Support Resources
- **Documentation**: Comprehensive guides in `docs/` directory
- **Community**: n8n community forums and support
- **Professional Support**: HPE Aruba support services
- **Emergency**: 24/7 network operations center

## 🏆 Best Practices

### Monitoring Best Practices
1. **Baseline Establishment**: Create performance baselines
2. **Threshold Tuning**: Regularly adjust alert thresholds
3. **Documentation**: Maintain comprehensive documentation
4. **Testing**: Regular testing of monitoring workflows
5. **Optimization**: Continuous performance optimization

### Alert Management Best Practices
1. **Minimize False Positives**: Tune thresholds to reduce noise
2. **Meaningful Alerts**: Ensure alerts provide actionable information
3. **Escalation Procedures**: Clear escalation paths and procedures
4. **Resolution Tracking**: Track and analyze alert resolution
5. **Continuous Improvement**: Regular review and optimization

---

## 🎯 **Integration with Existing Workflows**

This monitoring suite integrates seamlessly with all existing configuration management workflows:

- **AOS-CX Config Management**: Monitors health after configuration changes
- **Access Points Config Management**: Monitors wireless performance and AP health
- **Central Platform Config Management**: Monitors platform services and policies
- **EdgeConnect Config Management**: Monitors SD-WAN performance and policies

## 🚀 **Next Steps**

1. **Deploy Monitoring Workflows**: Import and configure all monitoring workflows
2. **Configure Notifications**: Set up Slack, email, and ServiceNow integration
3. **Establish Baselines**: Create performance baselines for all devices
4. **Optimize Thresholds**: Tune alert thresholds based on environment
5. **Create Dashboards**: Build comprehensive monitoring dashboards

---

**Note**: This monitoring suite provides comprehensive visibility into your HPE Aruba network infrastructure. Always test thoroughly in a non-production environment before deploying to production systems.

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Created by**: Claude Code Automation
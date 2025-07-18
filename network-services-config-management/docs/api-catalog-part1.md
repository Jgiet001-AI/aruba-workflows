# HPE Aruba Network Services API Configuration Endpoints Catalog

## Overview
This catalog documents 111+ HPE Aruba Network Services API endpoints organized by primary service categories, focusing on automation opportunities for enterprise network management.

---

## 1. IDS/IPS Configuration Management (28 Endpoints)

### 1.1 Intrusion Detection System Setup
| Endpoint | Method | Description | Priority |
|----------|---------|-------------|----------|
| `/api/v1/ids/policies` | GET, POST | Retrieve/Create IDS policies | High |
| `/api/v1/ids/policies/{policy_id}` | GET, PUT, DELETE | Manage specific IDS policy | High |
| `/api/v1/ids/sensors` | GET, POST | Configure IDS sensors | High |
| `/api/v1/ids/sensors/{sensor_id}` | GET, PUT, DELETE | Manage specific sensor | High |
| `/api/v1/ids/sensors/{sensor_id}/status` | GET | Get sensor operational status | Medium |
| `/api/v1/ids/profiles` | GET, POST | Detection profiles management | High |
| `/api/v1/ids/profiles/{profile_id}` | GET, PUT, DELETE | Specific profile operations | High |

### 1.2 Intrusion Prevention System Rules
| Endpoint | Method | Description | Priority |
|----------|---------|-------------|----------|
| `/api/v1/ips/rules` | GET, POST | IPS rule management | High |
| `/api/v1/ips/rules/{rule_id}` | GET, PUT, DELETE | Individual rule operations | High |
| `/api/v1/ips/rules/bulk` | POST, PUT | Bulk rule operations | High |
| `/api/v1/ips/signatures` | GET, POST | Signature management | High |
| `/api/v1/ips/signatures/{sig_id}` | GET, PUT, DELETE | Individual signature ops | High |
| `/api/v1/ips/signatures/import` | POST | Import signature packages | Medium |
| `/api/v1/ips/custom-rules` | GET, POST | Custom rule creation | Medium |

### 1.3 Security Rule Deployment
| Endpoint | Method | Description | Priority |
|----------|---------|-------------|----------|
| `/api/v1/security/rules/deploy` | POST | Deploy security rules | High |
| `/api/v1/security/rules/rollback` | POST | Rollback rule deployment | High |
| `/api/v1/security/rules/validate` | POST | Validate rule syntax | High |
| `/api/v1/security/rules/schedule` | GET, POST | Schedule rule deployment | Medium |
| `/api/v1/security/rules/templates` | GET, POST | Rule templates | Medium |

### 1.4 Threat Signature Updates
| Endpoint | Method | Description | Priority |
|----------|---------|-------------|----------|
| `/api/v1/threats/signatures/update` | POST | Update threat signatures | High |
| `/api/v1/threats/signatures/schedule` | GET, POST | Schedule updates | Medium |
| `/api/v1/threats/signatures/status` | GET | Update status check | Medium |
| `/api/v1/threats/intelligence/feeds` | GET, POST | Threat intel feeds | Medium |
| `/api/v1/threats/intelligence/feeds/{feed_id}` | GET, PUT, DELETE | Individual feed management | Medium |
| `/api/v1/threats/whitelist` | GET, POST | Whitelist management | Medium |
| `/api/v1/threats/blacklist` | GET, POST | Blacklist management | Medium |
| `/api/v1/threats/reputation` | GET | IP reputation lookup | Low |
| `/api/v1/threats/analysis` | GET | Threat analysis reports | Low |

**Configuration Example:**
```json
{
  "ips_rule": {
    "name": "Block_Malicious_IPs",
    "action": "block",
    "severity": "high",
    "source_ip": "any",
    "destination_ip": "internal_network",
    "protocol": "tcp",
    "enabled": true,
    "log_action": true
  }
}
```

---

## 2. SIEM Server Management (32 Endpoints)

### 2.1 SIEM Integration Setup
| Endpoint | Method | Description | Priority |
|----------|---------|-------------|----------|
| `/api/v1/siem/connectors` | GET, POST | SIEM connector management | High |
| `/api/v1/siem/connectors/{connector_id}` | GET, PUT, DELETE | Individual connector ops | High |
| `/api/v1/siem/connectors/{connector_id}/test` | POST | Test connector connection | High |
| `/api/v1/siem/servers` | GET, POST | SIEM server registration | High |
| `/api/v1/siem/servers/{server_id}` | GET, PUT, DELETE | Server management | High |
| `/api/v1/siem/servers/{server_id}/status` | GET | Server health check | Medium |
| `/api/v1/siem/authentication` | GET, POST | Auth configuration | High |
| `/api/v1/siem/certificates` | GET, POST | SSL certificate management | Medium |

### 2.2 Log Collection and Forwarding
| Endpoint | Method | Description | Priority |
|----------|---------|-------------|----------|
| `/api/v1/logs/collectors` | GET, POST | Log collector configuration | High |
| `/api/v1/logs/collectors/{collector_id}` | GET, PUT, DELETE | Individual collector ops | High |
| `/api/v1/logs/forwarding/rules` | GET, POST | Log forwarding rules | High |
| `/api/v1/logs/forwarding/rules/{rule_id}` | GET, PUT, DELETE | Individual rule management | High |
| `/api/v1/logs/formats` | GET, POST | Log format configuration | Medium |
| `/api/v1/logs/filters` | GET, POST | Log filtering rules | Medium |
| `/api/v1/logs/retention` | GET, POST | Log retention policies | Medium |
| `/api/v1/logs/compression` | GET, POST | Log compression settings | Low |

### 2.3 Event Correlation Rules
| Endpoint | Method | Description | Priority |
|----------|---------|-------------|----------|
| `/api/v1/events/correlation/rules` | GET, POST | Correlation rule management | High |
| `/api/v1/events/correlation/rules/{rule_id}` | GET, PUT, DELETE | Individual rule ops | High |
| `/api/v1/events/correlation/templates` | GET, POST | Rule templates | Medium |
| `/api/v1/events/correlation/test` | POST | Test correlation rules | Medium |
| `/api/v1/events/thresholds` | GET, POST | Event threshold configuration | Medium |
| `/api/v1/events/aggregation` | GET, POST | Event aggregation rules | Medium |
| `/api/v1/events/enrichment` | GET, POST | Event enrichment rules | Medium |
| `/api/v1/events/normalization` | GET, POST | Event normalization | Medium |

## Continued in api-catalog-part2.md...
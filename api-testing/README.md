# HPE Aruba API Testing Suite

**Version**: 1.0  
**Created**: January 17, 2025  
**Last Updated**: January 17, 2025  

## Overview

This directory contains comprehensive API testing collections for HPE Aruba network automation APIs. The testing suite includes Postman collections for all major Aruba products, validation reports, and performance testing scenarios.

## Directory Structure

```
api-testing/
├── README.md                                    # This file
├── postman-collections/                         # Postman collection files
│   ├── aruba-central-api-tests.json            # Aruba Central API tests
│   ├── aos-cx-switch-api-tests.json            # AOS-CX switch API tests
│   ├── edgeconnect-sdwan-api-tests.json        # EdgeConnect SD-WAN API tests
│   └── uxi-sensor-api-tests.json               # UXI sensor API tests
├── test-scenarios/                              # Test scenario documentation
├── validation-results/                          # Test validation reports
│   └── comprehensive-api-validation-report.md  # Main validation report
└── performance-tests/                           # Performance testing results
```

## Available Collections

### 1. Aruba Central API Tests
- **File**: `postman-collections/aruba-central-api-tests.json`
- **Authentication**: OAuth 2.0 client credentials flow
- **Coverage**: Device management, monitoring, configuration management
- **Endpoints**: 12 endpoints tested
- **Features**: OAuth flow, device CRUD, monitoring, templates

### 2. AOS-CX Switch API Tests
- **File**: `postman-collections/aos-cx-switch-api-tests.json`
- **Authentication**: Session-based with cookies
- **Coverage**: VLAN management, interface configuration, policy deployment
- **Endpoints**: 13 endpoints tested
- **Features**: VLAN CRUD, interface management, ACL policies, system config

### 3. EdgeConnect SD-WAN API Tests
- **File**: `postman-collections/edgeconnect-sdwan-api-tests.json`
- **Authentication**: X-Auth-Token based
- **Coverage**: Policy management, appliance provisioning, performance monitoring
- **Endpoints**: 13 endpoints tested
- **Features**: Policy CRUD, appliance management, performance monitoring, config management

### 4. UXI Sensor API Tests
- **File**: `postman-collections/uxi-sensor-api-tests.json`
- **Authentication**: Bearer token
- **Coverage**: Sensor management, test configuration, analytics reporting
- **Endpoints**: 14 endpoints tested
- **Features**: Sensor CRUD, test configuration, analytics, reporting

## Quick Start

### Prerequisites
- Postman installed
- Access to HPE Aruba APIs
- Valid API credentials for each product

### Setup Instructions

1. **Import Collections**
   ```bash
   # Import all collections into Postman
   # File → Import → Select JSON files from postman-collections/
   ```

2. **Configure Environment Variables**
   ```javascript
   // Aruba Central
   base_url: "https://apigw-prod2.central.arubanetworks.com"
   auth_url: "https://app.central.arubanetworks.com"
   client_id: "your_client_id"
   client_secret: "your_client_secret"

   // AOS-CX Switch
   base_url: "https://switch-ip-address"
   username: "admin"
   password: "your_password"

   // EdgeConnect
   base_url: "https://orchestrator.example.com"
   username: "admin"
   password: "your_password"

   // UXI Sensor
   base_url: "https://api.uxi.aruba.com"
   bearer_token: "your_bearer_token"
   ```

3. **Run Tests**
   ```bash
   # Option 1: Run individual collections in Postman
   # Option 2: Use Newman for command-line execution
   newman run postman-collections/aruba-central-api-tests.json
   ```

## Test Categories

### Authentication Tests
- OAuth 2.0 flows (Central)
- Session management (AOS-CX)
- Token validation (EdgeConnect, UXI)
- Error handling for invalid credentials

### CRUD Operations
- Create resources with validation
- Read/retrieve resource details
- Update resource configurations
- Delete resources with cleanup

### Monitoring and Analytics
- Performance metrics collection
- Real-time data streaming
- Historical data queries
- Alert management

### Configuration Management
- Template management
- Backup and restore operations
- Configuration validation
- Compliance checking

## Test Features

### Comprehensive Validation
- Status code validation
- Response time validation (< 5 seconds)
- JSON schema validation
- Error response validation
- Data type validation

### Error Handling
- Invalid credential handling
- Rate limiting responses
- Network error scenarios
- Timeout handling
- Rollback capabilities

### Security Testing
- Authentication validation
- Authorization boundary testing
- Input sanitization
- Token management
- Session security

### Performance Testing
- Response time benchmarks
- Concurrent request handling
- Load testing scenarios
- Resource cleanup efficiency

## Usage Examples

### Running Authentication Tests
```javascript
// 1. Run authentication collection first
// 2. Verify tokens are stored in global variables
// 3. Proceed with other test collections

// Example: Aruba Central OAuth
POST {{auth_url}}/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_id={{client_id}}&
client_secret={{client_secret}}&
scope=all
```

### Running CRUD Tests
```javascript
// 1. Ensure authentication is complete
// 2. Run CRUD operations in sequence
// 3. Verify cleanup procedures

// Example: AOS-CX VLAN Creation
POST {{base_url}}/rest/v10.08/system/vlans/{{test_vlan_id}}
Cookie: sessionId={{session_id}}
Content-Type: application/json

{
  "name": "Test_VLAN_{{$randomInt}}",
  "description": "Test VLAN for API validation",
  "admin": "up"
}
```

### Running Monitoring Tests
```javascript
// 1. Ensure authentication is complete
// 2. Run monitoring endpoints
// 3. Validate metrics and alerts

// Example: Central Performance Stats
GET {{base_url}}/monitoring/v1/statistics/device?timerange=3H&device_type=ap
Authorization: Bearer {{access_token}}
```

## Integration with n8n Workflows

### Pre-deployment Testing
Use collections to validate APIs before implementing n8n workflows:

```javascript
// 1. Run relevant API tests
// 2. Verify all endpoints are accessible
// 3. Validate response formats
// 4. Check error handling
// 5. Proceed with n8n workflow development
```

### Health Monitoring
Set up regular API health checks:

```javascript
// 1. Schedule collection runs
// 2. Monitor response times
// 3. Check error rates
// 4. Alert on failures
// 5. Maintain API reliability
```

## Performance Benchmarks

### Response Time Targets
- **Aruba Central**: < 5 seconds
- **AOS-CX**: < 3 seconds
- **EdgeConnect**: < 5 seconds
- **UXI**: < 2 seconds

### Success Rate Targets
- **All APIs**: > 95% success rate
- **Authentication**: > 99% success rate
- **CRUD Operations**: > 95% success rate
- **Monitoring**: > 98% success rate

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify credentials are correct
   - Check token expiration
   - Validate API permissions
   - Test network connectivity

2. **Test Failures**
   - Check API endpoint availability
   - Verify request format
   - Validate response structure
   - Check rate limiting

3. **Performance Issues**
   - Monitor response times
   - Check network latency
   - Verify API load
   - Optimize request patterns

### Debug Steps
1. Check collection variables
2. Verify authentication status
3. Test individual requests
4. Review error responses
5. Check API documentation

## Maintenance

### Regular Updates
- Update collections for API changes
- Refresh authentication credentials
- Validate test scenarios
- Update performance benchmarks

### Version Control
- Track collection changes
- Document API updates
- Maintain test coverage
- Update documentation

## Contributing

### Adding New Tests
1. Follow existing test patterns
2. Include comprehensive validation
3. Add error handling
4. Update documentation
5. Test thoroughly

### Reporting Issues
- Provide detailed error descriptions
- Include request/response examples
- Specify collection and test names
- Include environment details

## Support

For issues or questions:
1. Check the comprehensive validation report
2. Review test documentation
3. Verify API credentials
4. Test individual endpoints
5. Contact system administrators

## Related Files

- [Comprehensive API Validation Report](validation-results/comprehensive-api-validation-report.md)
- [Project Planning](../PLANNING.md)
- [Task Management](../TASKS.md)
- [n8n Workflow Documentation](../README.md)

---

**Note**: This testing suite is designed to work with the HPE Aruba n8n workflow automation project. All collections are integrated with the existing workflow development and deployment processes.
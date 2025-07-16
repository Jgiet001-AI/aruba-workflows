# Aruba Central Location Services Workflow

## Overview

This comprehensive n8n workflow automates beacon and location services configuration for Aruba Central, providing complete RTLS (Real-Time Location System) setup, beacon management, geofencing, and location analytics capabilities.

## Features

### Core Location Services
- **RTLS Setup**: Real-Time Location System configuration with positioning algorithms
- **Beacon Configuration**: iBeacon and Eddystone beacon setup and management
- **Geofencing**: Create and manage geofences with trigger actions
- **AP Location Setting**: Set precise coordinates for access points
- **Analytics Setup**: Configure location analytics and data collection
- **Proximity Services**: Configure proximity-based actions and notifications

### Environment Templates
Pre-configured templates for different environments:
- **Retail**: Customer analytics, heat maps, dwell time tracking
- **Healthcare**: Asset tracking, patient flow, staff efficiency
- **Corporate**: Workspace utilization, desk usage, meeting room optimization
- **Education**: Attendance tracking, space utilization, safety monitoring
- **Manufacturing**: Equipment tracking, safety zones, efficiency monitoring
- **Hospitality**: Guest services, way-finding, service optimization

### Advanced Features
- **Multi-operation Support**: Handle multiple location service operations in a single call
- **Error Handling**: Comprehensive error categorization with rollback capabilities
- **Input Validation**: Complete parameter validation for all location service configurations
- **Rollback System**: Automatic rollback for failed critical operations
- **Environment-specific Configuration**: Intelligent configuration based on deployment environment
- **Real-time Notifications**: Slack and email alerts for all operations

## API Endpoints Covered

### Location Sites Management
- `GET /location/v1/sites` - List location-enabled sites
- `GET /location/v1/sites/{site_id}/campus` - Get campus/floor plans
- `POST /location/v1/sites/{site_id}/campus` - Create campus/floor
- `PUT /location/v1/sites/{site_id}/campus/{campus_id}` - Update campus
- `GET /location/v1/sites/{site_id}/building` - Get building information
- `POST /location/v1/sites/{site_id}/building` - Create building

### Access Point Location Management
- `GET /location/v1/aps` - Get location-enabled access points
- `PUT /location/v1/aps/{serial}/location` - Set AP location coordinates

### Beacon Management
- `GET /location/v1/beacons` - List beacon configurations
- `POST /location/v1/beacons` - Create beacon configuration
- `PUT /location/v1/beacons/{beacon_id}` - Update beacon settings
- `DELETE /location/v1/beacons/{beacon_id}` - Delete beacon

### Analytics and Geofencing
- `GET /location/v1/clients` - Get client location data
- `GET /location/v1/analytics/presence` - Get presence analytics
- `POST /location/v1/geofences` - Create geofence
- `PUT /location/v1/geofences/{fence_id}` - Update geofence

## Supported Operations

### 1. setup_rtls
Configure Real-Time Location System for a site.

**Parameters:**
- `site_id` (required): Central site identifier
- `campus_name`: Campus or facility name
- `accuracy_mode`: "high", "medium", "low" (default: "high")
- `update_interval`: Location update interval in seconds (default: 30)
- `positioning_algorithm`: Algorithm type (default: "trilateration")
- `enable_analytics`: Enable location analytics (default: true)
- `minimum_aps`: Minimum APs required for positioning (default: 3)

### 2. configure_beacon
Set up iBeacon and/or Eddystone beacons.

**Parameters:**
- `site_id` (required): Central site identifier
- `beacon_type` (required): "ibeacon", "eddystone", or "both"
- `beacon_uuid`: iBeacon UUID (default: auto-generated)
- `beacon_major`: iBeacon major ID (default: 1)
- `beacon_minor`: iBeacon minor ID (default: 1)
- `beacon_power`: Transmit power in dBm (-12 to 4, default: -12)
- `beacon_interval`: Advertisement interval in ms (100-10000, default: 1000)
- `eddystone_url`: Eddystone URL beacon content

### 3. create_geofence
Create geofences with boundary definitions.

**Parameters:**
- `site_id` (required): Central site identifier
- `geofence_name` (required): Geofence identifier
- `geofence_coordinates` (required): Array of boundary coordinates (minimum 3 points)
- `geofence_type`: "enter", "exit", "dwell" (default: "enter")

### 4. set_ap_location
Set precise coordinates for access points.

**Parameters:**
- `site_id` (required): Central site identifier
- `ap_serial` (required): Access point serial number
- `ap_coordinates` (required): Object with x, y, z coordinates
- `floor_name`: Floor designation
- `building_name`: Building identifier

### 5. analytics_setup
Configure location analytics and data collection.

**Parameters:**
- `site_id` (required): Central site identifier
- `analytics_enabled`: Enable analytics (default: true)
- `asset_tracking`: Enable asset tracking (default: true)
- `retention_days`: Data retention period (default: 30)
- `export_format`: Data export format (default: "json")
- `real_time_updates`: Enable real-time updates (default: true)
- `privacy_mode`: Privacy setting (default: "anonymized")

### 6. proximity_config
Configure proximity-based services.

**Parameters:**
- `site_id` (required): Central site identifier
- `proximity_distance`: Trigger distance in meters (default: 2)
- `proximity_action`: Action type (default: "notify")
- `proximity_message`: Message content (default: "Welcome!")

## Usage Examples

### 1. Setup RTLS for Retail Environment

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-location-services \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "setup_rtls",
    "site_id": "site123",
    "site_name": "Main Store",
    "campus_name": "Retail Campus",
    "environment_type": "retail",
    "accuracy_mode": "high",
    "update_interval": 15,
    "enable_analytics": true,
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "customer123"
  }'
```

### 2. Configure iBeacon for Way-finding

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-location-services \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "configure_beacon",
    "site_id": "site123",
    "beacon_type": "ibeacon",
    "beacon_uuid": "E2C56DB5-DFFB-48D2-B060-D0F5A71096E0",
    "beacon_major": 100,
    "beacon_minor": 1,
    "beacon_power": -8,
    "beacon_interval": 500,
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "customer123"
  }'
```

### 3. Create Geofence for Safety Zone

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-location-services \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "create_geofence",
    "site_id": "site123",
    "geofence_name": "Emergency Exit Zone",
    "geofence_type": "enter",
    "geofence_coordinates": [
      {"x": 0, "y": 0},
      {"x": 10, "y": 0},
      {"x": 10, "y": 10},
      {"x": 0, "y": 10}
    ],
    "environment_type": "manufacturing",
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "customer123"
  }'
```

### 4. Set AP Location for Positioning

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-location-services \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "set_ap_location",
    "site_id": "site123",
    "ap_serial": "CNF7G9X123",
    "ap_coordinates": {
      "x": 25.5,
      "y": 15.0,
      "z": 3.0
    },
    "floor_name": "Floor 1",
    "building_name": "Main Building",
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "customer123"
  }'
```

### 5. Setup Location Analytics

```bash
curl -X POST http://192.168.40.100:8006/webhook/aruba-location-services \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "analytics_setup",
    "site_id": "site123",
    "analytics_enabled": true,
    "asset_tracking": true,
    "retention_days": 90,
    "real_time_updates": true,
    "privacy_mode": "anonymized",
    "environment_type": "healthcare",
    "central_base_url": "https://apigw-uswest4.central.arubanetworks.com",
    "customer_id": "customer123"
  }'
```

## Environment-Specific Templates

### Retail Environment
- **Focus**: Customer analytics, heat maps, dwell time
- **Beacon Density**: High (for detailed customer tracking)
- **Geofence Types**: Entrance, department sections, checkout areas
- **Privacy Level**: High (customer data protection)

### Healthcare Environment
- **Focus**: Asset tracking, patient flow, staff efficiency
- **Beacon Density**: Medium (balance between tracking and privacy)
- **Geofence Types**: Patient rooms, departments, emergency exits
- **Privacy Level**: Maximum (HIPAA compliance)

### Corporate Environment
- **Focus**: Workspace utilization, desk usage, meeting room optimization
- **Beacon Density**: Medium (office space optimization)
- **Geofence Types**: Floors, departments, meeting rooms
- **Privacy Level**: Medium (employee privacy balance)

### Education Environment
- **Focus**: Attendance, space utilization, safety monitoring
- **Beacon Density**: Medium (campus-wide coverage)
- **Geofence Types**: Classrooms, library, cafeteria, emergency areas
- **Privacy Level**: High (student privacy protection)

### Manufacturing Environment
- **Focus**: Equipment tracking, safety zones, efficiency monitoring
- **Beacon Density**: High (detailed equipment tracking)
- **Geofence Types**: Production lines, safety zones, storage areas
- **Privacy Level**: Low (operational focus over privacy)

### Hospitality Environment
- **Focus**: Guest services, way-finding, service optimization
- **Beacon Density**: High (enhanced guest experience)
- **Geofence Types**: Lobby, restaurants, amenities, rooms
- **Privacy Level**: Medium (guest experience vs privacy)

## Beacon Configuration Templates

### Proximity Marketing (Retail)
```json
{
  "beacon_type": "both",
  "beacon_power": -12,
  "beacon_interval": 100,
  "proximity_distance": 1,
  "proximity_action": "promotion",
  "proximity_message": "Special offer nearby!"
}
```

### Way-finding and Navigation
```json
{
  "beacon_type": "eddystone",
  "eddystone_url": "https://company.com/directions",
  "beacon_power": -8,
  "beacon_interval": 500,
  "proximity_distance": 3
}
```

### Asset Tracking (Healthcare)
```json
{
  "beacon_type": "ibeacon",
  "beacon_power": -4,
  "beacon_interval": 1000,
  "asset_tracking": true,
  "privacy_mode": "maximum"
}
```

### Emergency Mustering Points
```json
{
  "beacon_type": "both",
  "beacon_power": 0,
  "beacon_interval": 200,
  "proximity_action": "emergency_alert"
}
```

## Response Format

### Success Response
```json
{
  "status": "success",
  "operation": "configure_beacon",
  "site_id": "site123",
  "workflow_id": "location-configure_beacon-1642345678901",
  "timestamp": "2025-01-16T20:00:00.000Z",
  "summary": {
    "total_operations": 1,
    "successful": 1,
    "failed": 0,
    "success_rate": 100
  },
  "results": [
    {
      "operation": "configure_beacon",
      "status": "success",
      "message": "Beacon configured: ibeacon",
      "id": "beacon_456",
      "data": {
        "beacon_id": "beacon_456",
        "uuid": "E2C56DB5-DFFB-48D2-B060-D0F5A71096E0",
        "major": 100,
        "minor": 1
      }
    }
  ],
  "errors": [],
  "recommendations": [
    "Test beacon signal strength and range",
    "Verify mobile app beacon detection",
    "Monitor beacon battery status if applicable",
    "Document beacon deployment map"
  ],
  "next_steps": {
    "verification_required": false,
    "rollback_available": true,
    "monitoring_enabled": true
  }
}
```

### Error Response
```json
{
  "status": "failure",
  "operation": "configure_beacon",
  "site_id": "site123",
  "errors": [
    {
      "operation": "configure_beacon",
      "error_category": "validation_error",
      "error_message": "Invalid beacon_uuid format",
      "suggested_action": "Check input parameters and try again"
    }
  ],
  "rollback": {
    "status": "completed",
    "actions_executed": 0,
    "errors": 0
  }
}
```

## Error Handling

### Error Categories
- **validation_error**: Invalid input parameters
- **authentication_error**: API credential issues
- **authorization_error**: Insufficient permissions
- **resource_not_found**: Site or resource doesn't exist
- **conflict_error**: Resource already exists
- **rate_limit_error**: API rate limiting
- **server_error**: Aruba Central server issues
- **processing_error**: Workflow processing issues

### Rollback Capabilities
The workflow automatically creates rollback actions for:
- **RTLS Setup**: Delete created campus configuration
- **Beacon Configuration**: Remove configured beacons
- **Geofence Creation**: Delete created geofences

## Monitoring and Notifications

### Slack Notifications
Real-time alerts sent to `#network-alerts` channel including:
- Operation status and success rate
- Detailed error information with suggested actions
- Rollback status for failed operations
- Environment-specific recommendations

### Email Notifications
Detailed email reports sent to network team including:
- Complete operation summary
- Error details with categorization
- Rollback information
- Workflow execution logs reference

## Security Features

### Input Validation
- UUID format validation for iBeacons
- Coordinate range validation
- URL format validation for Eddystone beacons
- Parameter type and range checking

### Privacy Compliance
- Configurable privacy modes (anonymized, maximum)
- Environment-specific privacy settings
- Data retention controls
- Secure credential handling

### API Security
- Bearer token authentication
- Proper header configuration
- Rate limiting awareness
- Secure credential storage

## Performance Optimization

### Efficient Processing
- Parallel operation processing where possible
- Smart error categorization for faster resolution
- Optimized API call patterns
- Caching for frequently accessed data

### Rate Limiting
- Built-in retry logic with exponential backoff
- Rate limit detection and handling
- Queue management for bulk operations
- API call optimization

## Testing and Validation

### Pre-deployment Testing
- Input parameter validation
- API connectivity verification
- Credential validation
- Rollback procedure testing

### Operational Testing
- Signal strength verification
- Location accuracy testing
- Geofence trigger validation
- Analytics data quality checks

## Best Practices

### Deployment Recommendations
1. **Start Small**: Begin with a single beacon or geofence for testing
2. **Verify Coverage**: Ensure adequate AP coverage for RTLS accuracy
3. **Test Thoroughly**: Validate beacon detection and geofence triggers
4. **Monitor Performance**: Track location accuracy and system performance
5. **Document Everything**: Maintain accurate location service documentation

### Maintenance Guidelines
1. **Regular Validation**: Verify beacon functionality and signal strength
2. **Update Coordinates**: Keep AP location data current and accurate
3. **Monitor Analytics**: Review location analytics for data quality
4. **Privacy Compliance**: Regularly audit privacy settings and data retention
5. **Performance Tuning**: Optimize configuration based on usage patterns

## Support and Troubleshooting

### Common Issues
1. **Beacon Not Detected**: Check power level, interval, and mobile app configuration
2. **Inaccurate Positioning**: Verify AP locations and increase beacon count
3. **Geofence Not Triggering**: Check coordinate accuracy and trigger sensitivity
4. **Analytics Data Missing**: Verify analytics configuration and retention settings

### Support Contacts
- **Technical Issues**: network-team@company.com
- **API Issues**: Aruba Central Support
- **Workflow Issues**: n8n administrator

## Version History

- **v1.0.0**: Initial release with complete location services automation
- **Features**: RTLS, beacon configuration, geofencing, analytics, proximity services
- **Environment Templates**: 6 environment-specific configurations
- **Error Handling**: Comprehensive error categorization and rollback

---

**Last Updated**: January 16, 2025  
**Workflow File**: `aruba-central-location-services-workflow.json`  
**Webhook URL**: `http://192.168.40.100:8006/webhook/aruba-location-services`
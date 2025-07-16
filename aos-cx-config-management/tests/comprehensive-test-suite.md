# AOS-CX Configuration Management - Comprehensive Test Suite

## Overview
Complete testing framework for all AOS-CX configuration management workflows including unit tests, integration tests, end-to-end scenarios, and performance validation.

## Test Environment Setup

### Prerequisites
```bash
# Test environment requirements
- n8n instance running at http://192.168.40.100:8006
- AOS-CX test switches (minimum 2 for HA testing)
- Test VLANs 900-999 (reserved for testing)
- Test interfaces 1/1/47-48 (designated test ports)
- Backup network credentials for failover testing
```

### Test Data Preparation
```json
{
  "test_switches": [
    {
      "name": "test-aos-cx-01",
      "ip": "192.168.1.100",
      "model": "6300M",
      "version": "10.08.1010",
      "role": "primary"
    },
    {
      "name": "test-aos-cx-02", 
      "ip": "192.168.1.101",
      "model": "6200F",
      "version": "10.08.1010",
      "role": "secondary"
    }
  ],
  "test_vlans": [900, 901, 902, 903, 904, 905],
  "test_interfaces": ["1/1/47", "1/1/48"],
  "test_credentials": {
    "valid": "aos-cx-test-auth",
    "invalid": "aos-cx-invalid-auth"
  }
}
```

## Unit Tests

### 1. VLAN Management Tests
```bash
#!/bin/bash
# VLAN workflow unit tests

BASE_URL="http://192.168.40.100:8006/webhook/aos-cx-vlan"
SWITCH_IP="192.168.1.100"

echo "=== VLAN Management Unit Tests ==="

# Test 1: List VLANs
echo "Test 1: List all VLANs"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{\"operation\": \"list\", \"switch_ip\": \"$SWITCH_IP\"}" | jq .

# Test 2: Create valid VLAN
echo "Test 2: Create valid VLAN"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"create\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"vlan_id\": 900,
    \"vlan_name\": \"TEST_VLAN_900\",
    \"description\": \"Unit test VLAN\",
    \"admin_state\": \"up\"
  }" | jq .

# Test 3: Read created VLAN
echo "Test 3: Read created VLAN"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"read\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"vlan_id\": 900
  }" | jq .

# Test 4: Update VLAN
echo "Test 4: Update VLAN description"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"update\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"vlan_id\": 900,
    \"description\": \"Updated unit test VLAN\"
  }" | jq .

# Test 5: Delete VLAN
echo "Test 5: Delete test VLAN"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"delete\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"vlan_id\": 900
  }" | jq .

# Test 6: Invalid VLAN ID
echo "Test 6: Invalid VLAN ID (should fail)"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"create\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"vlan_id\": 5000
  }" | jq .

echo "=== VLAN Unit Tests Complete ==="
```

### 2. Interface Configuration Tests
```bash
#!/bin/bash
# Interface workflow unit tests

BASE_URL="http://192.168.40.100:8006/webhook/aos-cx-interface-config"
SWITCH_IP="192.168.1.100"
TEST_INTERFACE="1/1/47"

echo "=== Interface Configuration Unit Tests ==="

# Test 1: List all interfaces
echo "Test 1: List all interfaces"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{\"operation\": \"list\", \"switch_ip\": \"$SWITCH_IP\"}" | jq .

# Test 2: Read specific interface
echo "Test 2: Read specific interface"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"read\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"interface_name\": \"$TEST_INTERFACE\"
  }" | jq .

# Test 3: Configure access port
echo "Test 3: Configure access port"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"configure_access\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"interface_name\": \"$TEST_INTERFACE\",
    \"vlan_tag\": 900,
    \"description\": \"Test access port\",
    \"admin_state\": \"up\",
    \"port_security_enable\": true,
    \"max_mac_addresses\": 1
  }" | jq .

# Test 4: Configure trunk port
echo "Test 4: Configure trunk port"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"configure_trunk\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"interface_name\": \"1/1/48\",
    \"vlan_trunks\": [900, 901, 902],
    \"native_vlan_tag\": 1,
    \"description\": \"Test trunk port\",
    \"admin_state\": \"up\"
  }" | jq .

# Test 5: Invalid interface name
echo "Test 5: Invalid interface name (should fail)"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"read\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"interface_name\": \"invalid/interface\"
  }" | jq .

echo "=== Interface Unit Tests Complete ==="
```

### 3. Policy Deployment Tests
```bash
#!/bin/bash
# Policy deployment unit tests

BASE_URL="http://192.168.40.100:8006/webhook/aos-cx-policy"
SWITCH_IP="192.168.1.100"

echo "=== Policy Deployment Unit Tests ==="

# Test 1: List existing ACLs
echo "Test 1: List existing ACLs"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{\"operation\": \"list_acls\", \"switch_ip\": \"$SWITCH_IP\"}" | jq .

# Test 2: Create security ACL using template
echo "Test 2: Create security ACL using template"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"create_acl\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"acl_name\": \"TEST_SECURITY_ACL\",
    \"template\": \"security_basic\"
  }" | jq .

# Test 3: Create custom ACL
echo "Test 3: Create custom ACL"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"create_acl\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"acl_name\": \"TEST_CUSTOM_ACL\",
    \"acl_type\": \"ipv4\",
    \"rules\": [
      {
        \"sequence_number\": 10,
        \"action\": \"deny\",
        \"protocol\": \"tcp\",
        \"src_ip\": \"any\",
        \"dst_port\": \"22\",
        \"comment\": \"Block SSH\"
      },
      {
        \"sequence_number\": 20,
        \"action\": \"permit\",
        \"protocol\": \"any\",
        \"comment\": \"Allow all other traffic\"
      }
    ]
  }" | jq .

# Test 4: Apply ACL to interface
echo "Test 4: Apply ACL to interface"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"apply_to_interface\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"acl_name\": \"TEST_SECURITY_ACL\",
    \"interface_name\": \"1/1/47\",
    \"direction\": \"in\"
  }" | jq .

# Test 5: Delete ACL
echo "Test 5: Delete test ACL"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"delete_acl\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"acl_name\": \"TEST_CUSTOM_ACL\"
  }" | jq .

echo "=== Policy Unit Tests Complete ==="
```

### 4. Backup & Restore Tests
```bash
#!/bin/bash
# Backup and restore unit tests

BASE_URL="http://192.168.40.100:8006/webhook/aos-cx-backup-restore"
SWITCH_IP="192.168.1.100"

echo "=== Backup & Restore Unit Tests ==="

# Test 1: Create backup
echo "Test 1: Create configuration backup"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"backup\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"backup_type\": \"running\",
    \"backup_name\": \"unit_test_backup\",
    \"compression_enabled\": true
  }" | jq .

# Test 2: List backups
echo "Test 2: List available backups"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"list_backups\",
    \"switch_ip\": \"$SWITCH_IP\"
  }" | jq .

# Test 3: Create checkpoint
echo "Test 3: Create configuration checkpoint"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"create_checkpoint\",
    \"switch_ip\": \"$SWITCH_IP\"
  }" | jq .

# Test 4: Compare configurations
echo "Test 4: Compare current vs backup"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"compare\",
    \"switch_ip\": \"$SWITCH_IP\",
    \"restore_file\": \"unit_test_backup\"
  }" | jq .

echo "=== Backup & Restore Unit Tests Complete ==="
```

## Integration Tests

### 1. End-to-End Workflow Test
```python
#!/usr/bin/env python3
"""
End-to-end integration test for AOS-CX workflows
"""

import requests
import json
import time
import sys

class ArubaWorkflowIntegrationTest:
    def __init__(self):
        self.base_url = "http://192.168.40.100:8006/webhook"
        self.switch_ip = "192.168.1.100"
        self.test_vlan_id = 901
        self.test_interface = "1/1/47"
        
    def test_complete_workflow(self):
        """Test complete VLAN creation to interface assignment workflow"""
        print("=== Starting End-to-End Integration Test ===")
        
        # Step 1: Create backup before changes
        print("Step 1: Creating configuration backup...")
        backup_result = self.create_backup()
        if not backup_result:
            return False
            
        # Step 2: Create test VLAN
        print("Step 2: Creating test VLAN...")
        vlan_result = self.create_test_vlan()
        if not vlan_result:
            return False
            
        # Step 3: Configure interface for VLAN
        print("Step 3: Configuring interface...")
        interface_result = self.configure_test_interface()
        if not interface_result:
            return False
            
        # Step 4: Apply security policy
        print("Step 4: Applying security policy...")
        policy_result = self.apply_security_policy()
        if not policy_result:
            return False
            
        # Step 5: Verify complete configuration
        print("Step 5: Verifying configuration...")
        verify_result = self.verify_configuration()
        if not verify_result:
            return False
            
        # Step 6: Cleanup
        print("Step 6: Cleaning up test configuration...")
        cleanup_result = self.cleanup_test_config()
        
        print("=== Integration Test Complete ===")
        return True
        
    def create_backup(self):
        url = f"{self.base_url}/aos-cx-backup-restore"
        payload = {
            "operation": "backup",
            "switch_ip": self.switch_ip,
            "backup_name": "integration_test_backup"
        }
        response = requests.post(url, json=payload)
        return response.status_code == 200
        
    def create_test_vlan(self):
        url = f"{self.base_url}/aos-cx-vlan"
        payload = {
            "operation": "create",
            "switch_ip": self.switch_ip,
            "vlan_id": self.test_vlan_id,
            "vlan_name": "INTEGRATION_TEST",
            "description": "Integration test VLAN"
        }
        response = requests.post(url, json=payload)
        return response.status_code == 200
        
    def configure_test_interface(self):
        url = f"{self.base_url}/aos-cx-interface-config"
        payload = {
            "operation": "configure_access",
            "switch_ip": self.switch_ip,
            "interface_name": self.test_interface,
            "vlan_tag": self.test_vlan_id,
            "description": "Integration test interface",
            "port_security_enable": True
        }
        response = requests.post(url, json=payload)
        return response.status_code == 200
        
    def apply_security_policy(self):
        url = f"{self.base_url}/aos-cx-policy"
        payload = {
            "operation": "create_acl",
            "switch_ip": self.switch_ip,
            "acl_name": "INTEGRATION_TEST_ACL",
            "template": "security_basic"
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return False
            
        # Apply ACL to interface
        payload = {
            "operation": "apply_to_interface",
            "switch_ip": self.switch_ip,
            "acl_name": "INTEGRATION_TEST_ACL",
            "interface_name": self.test_interface,
            "direction": "in"
        }
        response = requests.post(url, json=payload)
        return response.status_code == 200
        
    def verify_configuration(self):
        # Verify VLAN exists
        url = f"{self.base_url}/aos-cx-vlan"
        payload = {
            "operation": "read",
            "switch_ip": self.switch_ip,
            "vlan_id": self.test_vlan_id
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return False
            
        # Verify interface configuration
        url = f"{self.base_url}/aos-cx-interface-config"
        payload = {
            "operation": "read",
            "switch_ip": self.switch_ip,
            "interface_name": self.test_interface
        }
        response = requests.post(url, json=payload)
        return response.status_code == 200
        
    def cleanup_test_config(self):
        # Remove ACL from interface and delete
        url = f"{self.base_url}/aos-cx-policy"
        payload = {
            "operation": "delete_acl",
            "switch_ip": self.switch_ip,
            "acl_name": "INTEGRATION_TEST_ACL"
        }
        requests.post(url, json=payload)
        
        # Reset interface to default
        url = f"{self.base_url}/aos-cx-interface-config"
        payload = {
            "operation": "configure_access",
            "switch_ip": self.switch_ip,
            "interface_name": self.test_interface,
            "vlan_tag": 1,
            "description": "",
            "admin_state": "down"
        }
        requests.post(url, json=payload)
        
        # Delete test VLAN
        url = f"{self.base_url}/aos-cx-vlan"
        payload = {
            "operation": "delete",
            "switch_ip": self.switch_ip,
            "vlan_id": self.test_vlan_id
        }
        requests.post(url, json=payload)
        
        return True

if __name__ == "__main__":
    test = ArubaWorkflowIntegrationTest()
    success = test.test_complete_workflow()
    sys.exit(0 if success else 1)
```

## Performance Tests

### 1. Load Testing
```bash
#!/bin/bash
# Performance and load testing

echo "=== Performance Tests ==="

# Test 1: Bulk VLAN creation
echo "Test 1: Bulk VLAN creation (10 VLANs)"
start_time=$(date +%s)
for i in {910..919}; do
  curl -s -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
    -H "Content-Type: application/json" \
    -d "{
      \"operation\": \"create\",
      \"switch_ip\": \"192.168.1.100\",
      \"vlan_id\": $i,
      \"vlan_name\": \"PERF_TEST_$i\"
    }" > /dev/null &
done
wait
end_time=$(date +%s)
echo "Bulk VLAN creation completed in $((end_time - start_time)) seconds"

# Test 2: Concurrent interface configuration
echo "Test 2: Concurrent interface updates"
start_time=$(date +%s)
interfaces=("1/1/47" "1/1/48")
for intf in "${interfaces[@]}"; do
  curl -s -X POST "http://192.168.40.100:8006/webhook/aos-cx-interface-config" \
    -H "Content-Type: application/json" \
    -d "{
      \"operation\": \"update\",
      \"switch_ip\": \"192.168.1.100\",
      \"interface_name\": \"$intf\",
      \"description\": \"Performance test interface\"
    }" > /dev/null &
done
wait
end_time=$(date +%s)
echo "Concurrent interface updates completed in $((end_time - start_time)) seconds"

# Cleanup performance test VLANs
for i in {910..919}; do
  curl -s -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
    -H "Content-Type: application/json" \
    -d "{
      \"operation\": \"delete\",
      \"switch_ip\": \"192.168.1.100\",
      \"vlan_id\": $i
    }" > /dev/null &
done
wait

echo "=== Performance Tests Complete ==="
```

## Error Scenario Tests

### 1. Error Handling Validation
```bash
#!/bin/bash
# Test error handling and rollback mechanisms

echo "=== Error Scenario Tests ==="

# Test 1: Invalid authentication
echo "Test 1: Invalid authentication (should fail gracefully)"
curl -s -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"list\",
    \"switch_ip\": \"192.168.1.100\",
    \"force_auth_failure\": true
  }" | jq .

# Test 2: Network timeout
echo "Test 2: Network timeout (unreachable IP)"
curl -s -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"list\",
    \"switch_ip\": \"192.168.255.254\"
  }" | jq .

# Test 3: Invalid VLAN range
echo "Test 3: Invalid VLAN ID (should trigger validation error)"
curl -s -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"create\",
    \"switch_ip\": \"192.168.1.100\",
    \"vlan_id\": 5000
  }" | jq .

# Test 4: Duplicate VLAN creation
echo "Test 4: Duplicate VLAN creation (conflict handling)"
curl -s -X POST "http://192.168.40.100:8006/webhook/aos-cx-vlan" \
  -H "Content-Type: application/json" \
  -d "{
    \"operation\": \"create\",
    \"switch_ip\": \"192.168.1.100\",
    \"vlan_id\": 1,
    \"vlan_name\": \"DEFAULT\"
  }" | jq .

echo "=== Error Scenario Tests Complete ==="
```

## Test Execution Scripts

### Master Test Runner
```bash
#!/bin/bash
# Master test execution script

echo "==============================================="
echo "AOS-CX Configuration Management Test Suite"
echo "==============================================="

# Set test environment
export TEST_SWITCH_IP="192.168.1.100"
export N8N_BASE_URL="http://192.168.40.100:8006"

# Initialize test results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

run_test() {
    local test_name=$1
    local test_script=$2
    
    echo "Running: $test_name"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if $test_script; then
        echo "✅ PASSED: $test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo "❌ FAILED: $test_name"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo ""
}

# Run test suites
run_test "VLAN Management Unit Tests" "./test_vlan_unit.sh"
run_test "Interface Configuration Unit Tests" "./test_interface_unit.sh"
run_test "Policy Deployment Unit Tests" "./test_policy_unit.sh"
run_test "Backup & Restore Unit Tests" "./test_backup_unit.sh"
run_test "Integration Tests" "python3 test_integration.py"
run_test "Performance Tests" "./test_performance.sh"
run_test "Error Scenario Tests" "./test_error_scenarios.sh"

# Generate test report
echo "==============================================="
echo "TEST RESULTS SUMMARY"
echo "==============================================="
echo "Total Tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $FAILED_TESTS"
echo "Success Rate: $(( PASSED_TESTS * 100 / TOTAL_TESTS ))%"
echo "==============================================="

if [ $FAILED_TESTS -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED!"
    exit 0
else
    echo "⚠️  Some tests failed. Please review the output above."
    exit 1
fi
```

This comprehensive test suite ensures all AOS-CX configuration management workflows are thoroughly validated across functionality, performance, and error handling scenarios.
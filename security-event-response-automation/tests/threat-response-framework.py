"""
HPE Aruba Threat Response Testing Framework
Comprehensive test scripts for automated security incident response
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import pytest
from unittest.mock import Mock, patch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DeviceStatus(Enum):
    NORMAL = "normal"
    QUARANTINED = "quarantined"
    ISOLATED = "isolated"
    BLOCKED = "blocked"

class SecurityActionType(Enum):
    ISOLATE = "isolate"
    QUARANTINE = "quarantine"
    BLOCK = "block"
    POLICY_UPDATE = "policy_update"
    ROLLBACK = "rollback"

@dataclass
class ThreatEvent:
    event_id: str
    timestamp: datetime
    threat_type: str
    severity: ThreatLevel
    source_ip: str
    source_mac: str
    device_id: str
    description: str
    indicators: List[str]
    confidence_score: float

@dataclass
class SecurityAction:
    action_id: str
    action_type: SecurityActionType
    device_id: str
    timestamp: datetime
    parameters: Dict
    rollback_timer: Optional[int] = None
    status: str = "pending"
    result: Optional[Dict] = None

class ArubaSecurityAPI:
    """HPE Aruba Security API Client"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None
        self.rate_limit_delay = 0.1
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            },
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make API request with error handling and rate limiting"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            await asyncio.sleep(self.rate_limit_delay)
            
            async with self.session.request(method, url, json=data) as response:
                response_data = await response.json()
                
                if response.status == 429:  # Rate limited
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Retrying after {retry_after} seconds")
                    await asyncio.sleep(retry_after)
                    return await self._make_request(method, endpoint, data)
                
                if response.status >= 400:
                    raise Exception(f"API error {response.status}: {response_data}")
                
                return response_data
                
        except aiohttp.ClientError as e:
            logger.error(f"Network error: {e}")
            raise
    
    async def isolate_device(self, device_id: str, rollback_timer: int = None) -> Dict:
        """Isolate a compromised device"""
        data = {
            "device_id": device_id,
            "action": "isolate",
            "rollback_timer": rollback_timer
        }
        return await self._make_request('POST', '/api/v2/devices/isolate', data)
    
    async def quarantine_device(self, device_id: str, reason: str = None) -> Dict:
        """Quarantine a suspicious device"""
        data = {
            "device_id": device_id,
            "action": "quarantine",
            "reason": reason
        }
        return await self._make_request('POST', '/api/v2/devices/quarantine', data)
    
    async def mass_quarantine(self, device_ids: List[str], reason: str = None) -> Dict:
        """Quarantine multiple devices simultaneously"""
        data = {
            "device_ids": device_ids,
            "action": "mass_quarantine",
            "reason": reason
        }
        return await self._make_request('POST', '/api/v2/devices/quarantine', data)
    
    async def update_security_policy(self, policy_id: str, policy_data: Dict) -> Dict:
        """Update security policy"""
        return await self._make_request('PUT', f'/api/v2/security/policies/{policy_id}', policy_data)
    
    async def block_threat(self, threat_data: Dict) -> Dict:
        """Block malicious IPs/MACs"""
        return await self._make_request('POST', '/api/v2/security/block', threat_data)
    
    async def get_threats(self, limit: int = 100, severity: str = None) -> Dict:
        """Get real-time threat intelligence"""
        params = {"limit": limit}
        if severity:
            params["severity"] = severity
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return await self._make_request('GET', f'/api/v2/security/threats?{query_string}')
    
    async def get_device_status(self, device_id: str) -> Dict:
        """Get device status"""
        return await self._make_request('GET', f'/api/v2/devices/{device_id}/status')
    
    async def rollback_action(self, action_id: str) -> Dict:
        """Rollback a security action"""
        data = {"action_id": action_id}
        return await self._make_request('POST', '/api/v2/security/rollback', data)

class ThreatResponseOrchestrator:
    """Orchestrates automated threat response workflows"""
    
    def __init__(self, api_client: ArubaSecurityAPI):
        self.api = api_client
        self.active_actions: Dict[str, SecurityAction] = {}
        self.threat_policies = {
            ThreatLevel.LOW: {"action": "monitor", "duration": 300},
            ThreatLevel.MEDIUM: {"action": "quarantine", "duration": 1800},
            ThreatLevel.HIGH: {"action": "isolate", "duration": 3600},
            ThreatLevel.CRITICAL: {"action": "isolate", "duration": 7200}
        }
    
    async def process_threat_event(self, threat: ThreatEvent) -> List[SecurityAction]:
        """Process a threat event and execute appropriate response"""
        actions = []
        policy = self.threat_policies.get(threat.severity)
        
        if not policy:
            logger.warning(f"No policy defined for threat level {threat.severity}")
            return actions
        
        if policy["action"] == "monitor":
            logger.info(f"Monitoring threat {threat.event_id}")
            return actions
        
        # Create security action
        action = SecurityAction(
            action_id=f"action_{int(time.time())}_{threat.event_id}",
            action_type=SecurityActionType(policy["action"]),
            device_id=threat.device_id,
            timestamp=datetime.now(),
            parameters={
                "threat_id": threat.event_id,
                "severity": threat.severity.value,
                "confidence": threat.confidence_score
            },
            rollback_timer=policy["duration"]
        )
        
        try:
            if action.action_type == SecurityActionType.QUARANTINE:
                result = await self.api.quarantine_device(
                    threat.device_id, 
                    f"Automated response to {threat.threat_type}"
                )
            elif action.action_type == SecurityActionType.ISOLATE:
                result = await self.api.isolate_device(
                    threat.device_id,
                    rollback_timer=policy["duration"]
                )
            
            action.status = "completed"
            action.result = result
            self.active_actions[action.action_id] = action
            
            logger.info(f"Executed {action.action_type.value} for device {threat.device_id}")
            actions.append(action)
            
        except Exception as e:
            logger.error(f"Failed to execute action {action.action_type.value}: {e}")
            action.status = "failed"
            action.result = {"error": str(e)}
        
        return actions

# Test scenarios and fixtures
class SecurityTestScenarios:
    """Security incident test scenarios"""
    
    @staticmethod
    def create_malware_detection() -> ThreatEvent:
        """Simulate malware detection event"""
        return ThreatEvent(
            event_id="malware_001",
            timestamp=datetime.now(),
            threat_type="malware_detected",
            severity=ThreatLevel.CRITICAL,
            source_ip="192.168.1.100",
            source_mac="00:11:22:33:44:55",
            device_id="AP001",
            description="Suspicious executable detected",
            indicators=["hash:abc123", "file:evil.exe"],
            confidence_score=0.95
        )
    
    @staticmethod
    def create_intrusion_attempt() -> ThreatEvent:
        """Simulate intrusion attempt"""
        return ThreatEvent(
            event_id="intrusion_001",
            timestamp=datetime.now(),
            threat_type="intrusion_attempt",
            severity=ThreatLevel.HIGH,
            source_ip="10.0.0.50",
            source_mac="00:AA:BB:CC:DD:EE",
            device_id="SW001",
            description="Multiple failed authentication attempts",
            indicators=["brute_force", "failed_auth"],
            confidence_score=0.87
        )
    
    @staticmethod
    def create_data_exfiltration() -> ThreatEvent:
        """Simulate data exfiltration event"""
        return ThreatEvent(
            event_id="exfil_001",
            timestamp=datetime.now(),
            threat_type="data_exfiltration",
            severity=ThreatLevel.CRITICAL,
            source_ip="172.16.0.25",
            source_mac="00:FF:EE:DD:CC:BB",
            device_id="AP002",
            description="Large data transfer to suspicious destination",
            indicators=["data_volume", "external_dest"],
            confidence_score=0.92
        )

# Pytest test cases
class TestThreatResponseAPI:
    """Test cases for threat response APIs"""
    
    @pytest.fixture
    async def api_client(self):
        """Create API client fixture"""
        client = ArubaSecurityAPI(
            base_url="https://central.arubanetworks.com",
            api_key="test_api_key"
        )
        async with client:
            yield client
    
    @pytest.fixture
    def orchestrator(self, api_client):
        """Create orchestrator fixture"""
        return ThreatResponseOrchestrator(api_client)
    
    @pytest.mark.asyncio
    async def test_device_isolation(self, api_client):
        """Test device isolation functionality"""
        device_id = "TEST_DEVICE_001"
        rollback_timer = 3600  # 1 hour
        
        # Mock the API response
        with patch.object(api_client, '_make_request') as mock_request:
            mock_request.return_value = {
                "status": "success",
                "action_id": "isolation_123",
                "device_id": device_id,
                "isolated": True,
                "rollback_at": (datetime.now() + timedelta(seconds=rollback_timer)).isoformat()
            }
            
            result = await api_client.isolate_device(device_id, rollback_timer)
            
            assert result["status"] == "success"
            assert result["device_id"] == device_id
            assert result["isolated"] is True
            
            # Verify API call
            mock_request.assert_called_once_with(
                'POST', 
                '/api/v2/devices/isolate',
                {
                    "device_id": device_id,
                    "action": "isolate",
                    "rollback_timer": rollback_timer
                }
            )
    
    @pytest.mark.asyncio
    async def test_mass_quarantine(self, api_client):
        """Test mass quarantine for coordinated attacks"""
        device_ids = ["AP001", "AP002", "AP003"]
        reason = "Coordinated malware attack detected"
        
        with patch.object(api_client, '_make_request') as mock_request:
            mock_request.return_value = {
                "status": "success",
                "quarantined_count": len(device_ids),
                "failed_count": 0,
                "details": [
                    {"device_id": device_id, "status": "quarantined"} 
                    for device_id in device_ids
                ]
            }
            
            result = await api_client.mass_quarantine(device_ids, reason)
            
            assert result["status"] == "success"
            assert result["quarantined_count"] == 3
            assert result["failed_count"] == 0
    
    @pytest.mark.asyncio
    async def test_automated_threat_response(self, orchestrator):
        """Test automated threat response workflow"""
        # Create test threat event
        threat = SecurityTestScenarios.create_malware_detection()
        
        # Mock API calls
        with patch.object(orchestrator.api, 'isolate_device') as mock_isolate:
            mock_isolate.return_value = {
                "status": "success",
                "action_id": "auto_isolate_123",
                "device_id": threat.device_id
            }
            
            actions = await orchestrator.process_threat_event(threat)
            
            assert len(actions) == 1
            assert actions[0].action_type == SecurityActionType.ISOLATE
            assert actions[0].device_id == threat.device_id
            assert actions[0].status == "completed"
            
            # Verify isolation was called
            mock_isolate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_rate_limiting_handling(self, api_client):
        """Test rate limiting and retry logic"""
        device_id = "TEST_DEVICE_002"
        
        # Mock rate limited response followed by success
        responses = [
            Exception("API error 429: Rate limited"),
            {
                "status": "success",
                "action_id": "retry_123",
                "device_id": device_id
            }
        ]
        
        with patch.object(api_client, '_make_request') as mock_request:
            mock_request.side_effect = responses
            
            with patch('asyncio.sleep'):  # Mock sleep to speed up test
                result = await api_client.isolate_device(device_id)
                
                assert result["status"] == "success"
                assert mock_request.call_count == 2  # Initial + retry
    
    @pytest.mark.asyncio
    async def test_compliance_logging(self, orchestrator):
        """Test comprehensive audit trail logging"""
        threat = SecurityTestScenarios.create_data_exfiltration()
        
        with patch.object(orchestrator.api, 'isolate_device') as mock_isolate:
            mock_isolate.return_value = {"status": "success", "action_id": "log_test_123"}
            
            actions = await orchestrator.process_threat_event(threat)
            
            action = actions[0]
            
            # Verify audit information is captured
            assert action.action_id is not None
            assert action.timestamp is not None
            assert action.parameters["threat_id"] == threat.event_id
            assert action.parameters["severity"] == threat.severity.value
            assert action.parameters["confidence"] == threat.confidence_score
            
            # Verify action is tracked
            assert action.action_id in orchestrator.active_actions

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
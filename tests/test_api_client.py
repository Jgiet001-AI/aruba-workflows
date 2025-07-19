"""
Comprehensive test suite for the enhanced HPE Aruba API client.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from aiohttp import ClientError, ClientTimeout

# Import our improved modules
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_client import ArubaAPIClient, ValidationError, APIError

class TestArubaAPIClient:
    """Test cases for ArubaAPIClient with comprehensive coverage."""
    
    def test_init_valid_params(self):
        """Test successful initialization with valid parameters."""
        client = ArubaAPIClient("https://api.example.com", "valid_api_key_123")
        assert client.base_url == "https://api.example.com"
        assert client._api_key == "valid_api_key_123"
        assert client.timeout == 30
    
    def test_init_invalid_base_url(self):
        """Test initialization fails with invalid base URL."""
        with pytest.raises(ValueError, match="HTTPS required"):
            ArubaAPIClient("http://api.example.com", "valid_key")
        
        with pytest.raises(ValueError, match="Invalid base URL"):
            ArubaAPIClient("not-a-url", "valid_key")
        
        with pytest.raises(ValueError, match="non-empty string"):
            ArubaAPIClient("", "valid_key")
    
    def test_init_invalid_api_key(self):
        """Test initialization fails with invalid API key."""
        with pytest.raises(ValueError, match="non-empty string"):
            ArubaAPIClient("https://api.example.com", "")
        
        with pytest.raises(ValueError, match="too short"):
            ArubaAPIClient("https://api.example.com", "short")
        
        with pytest.raises(ValueError, match="non-empty string"):
            ArubaAPIClient("https://api.example.com", None)
    
    def test_validate_device_id_valid(self):
        """Test device ID validation with valid IDs."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        # Valid device IDs
        valid_ids = [
            "AP-123",
            "switch_01",
            "device.test",
            "SW-001-Floor-2",
            "a1b2c3d4e5"
        ]
        
        for device_id in valid_ids:
            client.validate_device_id(device_id)  # Should not raise
    
    def test_validate_device_id_invalid(self):
        """Test device ID validation with invalid IDs."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        # Invalid device IDs
        invalid_cases = [
            ("", "non-empty string"),
            (None, "non-empty string"),
            ("device with spaces", "invalid characters"),
            ("device@invalid", "invalid characters"),
            ("x" * 51, "invalid characters"),  # Too long
            ("device<script>", "invalid characters"),
            ("device/slash", "invalid characters")
        ]
        
        for device_id, expected_error in invalid_cases:
            with pytest.raises(ValidationError, match=expected_error):
                client.validate_device_id(device_id)
    
    def test_validate_http_method(self):
        """Test HTTP method validation."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        # Valid methods
        assert client.validate_http_method("get") == "GET"
        assert client.validate_http_method("POST") == "POST"
        assert client.validate_http_method("Put") == "PUT"
        
        # Invalid methods
        with pytest.raises(ValidationError, match="Invalid HTTP method"):
            client.validate_http_method("INVALID")
        
        with pytest.raises(ValidationError, match="non-empty string"):
            client.validate_http_method("")
        
        with pytest.raises(ValidationError, match="non-empty string"):
            client.validate_http_method(None)
    
    def test_construct_url(self):
        """Test URL construction."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        # Valid endpoints
        assert client._construct_url("/api/v1/test") == "https://api.example.com/api/v1/test"
        assert client._construct_url("api/v1/test") == "https://api.example.com/api/v1/test"
        
        # Test URL validation
        with patch('api_client.urljoin', return_value="http://malicious.com/api"):
            with pytest.raises(ValueError, match="Invalid URL constructed"):
                client._construct_url("/api/test")
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager functionality."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        async with client:
            assert client.session is not None
            assert 'Authorization' in client.session.headers
            assert client.session.headers['Authorization'] == 'Bearer valid_key_123'
        
        # Session should be closed after context
        assert client.session.closed
    
    @pytest.mark.asyncio
    async def test_make_request_success(self):
        """Test successful API request."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        # Mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"status": "success"})
        
        with patch.object(client, 'session') as mock_session:
            mock_session.request = AsyncMock(return_value=mock_response)
            mock_session.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            
            result = await client._make_request("GET", "/api/test")
            
            assert result == {"status": "success"}
            mock_session.request.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_make_request_rate_limiting(self):
        """Test rate limiting handling."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        # Mock rate limited response followed by success
        rate_limited_response = AsyncMock()
        rate_limited_response.status = 429
        rate_limited_response.headers = {'Retry-After': '1'}
        
        success_response = AsyncMock()
        success_response.status = 200
        success_response.json = AsyncMock(return_value={"status": "success"})
        
        with patch.object(client, 'session') as mock_session:
            # First call returns rate limited, second succeeds
            mock_session.request = AsyncMock(side_effect=[
                rate_limited_response,
                success_response
            ])
            mock_session.__aenter__ = AsyncMock(side_effect=[
                rate_limited_response,
                success_response
            ])
            mock_session.__aexit__ = AsyncMock(return_value=None)
            
            with patch('asyncio.sleep') as mock_sleep:
                result = await client._make_request("GET", "/api/test")
                
                assert result == {"status": "success"}
                mock_sleep.assert_called()  # Should have slept for retry
    
    @pytest.mark.asyncio
    async def test_make_request_error_handling(self):
        """Test API error handling."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        # Test different error status codes
        error_cases = [
            (400, "Bad request"),
            (401, "Authentication failed"),
            (403, "Access denied"),
            (404, "Resource not found"),
            (500, "Internal server error")
        ]
        
        for status_code, expected_message in error_cases:
            mock_response = AsyncMock()
            mock_response.status = status_code
            mock_response.json = AsyncMock(return_value={"error": "test error"})
            
            with patch.object(client, 'session') as mock_session:
                mock_session.request = AsyncMock(return_value=mock_response)
                mock_session.__aenter__ = AsyncMock(return_value=mock_response)
                mock_session.__aexit__ = AsyncMock(return_value=None)
                
                with pytest.raises(APIError, match=expected_message):
                    await client._make_request("GET", "/api/test")
    
    @pytest.mark.asyncio
    async def test_make_request_network_error(self):
        """Test network error handling."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        with patch.object(client, 'session') as mock_session:
            mock_session.request = AsyncMock(side_effect=ClientError("Network error"))
            
            with pytest.raises(APIError, match="Network connection failed"):
                await client._make_request("GET", "/api/test")
    
    @pytest.mark.asyncio
    async def test_make_request_timeout(self):
        """Test request timeout handling."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        with patch.object(client, 'session') as mock_session:
            mock_session.request = AsyncMock(side_effect=asyncio.TimeoutError())
            
            with pytest.raises(APIError, match="Request timeout"):
                await client._make_request("GET", "/api/test")
    
    @pytest.mark.asyncio
    async def test_get_device_status(self):
        """Test get device status method."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        expected_response = {"device_id": "AP-123", "status": "online"}
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response
            
            result = await client.get_device_status("AP-123")
            
            assert result == expected_response
            mock_request.assert_called_once_with('GET', '/api/v2/devices/AP-123/status')
    
    @pytest.mark.asyncio
    async def test_isolate_device_valid(self):
        """Test device isolation with valid parameters."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        expected_response = {"status": "isolated", "device_id": "AP-123"}
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response
            
            result = await client.isolate_device("AP-123", rollback_timer=3600)
            
            assert result == expected_response
            mock_request.assert_called_once_with(
                'POST', 
                '/api/v2/devices/isolate',
                {
                    "device_id": "AP-123",
                    "action": "isolate", 
                    "rollback_timer": 3600
                }
            )
    
    @pytest.mark.asyncio
    async def test_isolate_device_invalid_timer(self):
        """Test device isolation with invalid rollback timer."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        with pytest.raises(ValidationError, match="between 0 and 86400"):
            await client.isolate_device("AP-123", rollback_timer=90000)
        
        with pytest.raises(ValidationError, match="between 0 and 86400"):
            await client.isolate_device("AP-123", rollback_timer=-1)
    
    @pytest.mark.asyncio
    async def test_quarantine_device(self):
        """Test device quarantine functionality."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        expected_response = {"status": "quarantined", "device_id": "AP-123"}
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response
            
            result = await client.quarantine_device("AP-123", reason="Security threat detected")
            
            assert result == expected_response
            mock_request.assert_called_once_with(
                'POST',
                '/api/v2/devices/quarantine',
                {
                    "device_id": "AP-123",
                    "action": "quarantine",
                    "reason": "Security threat detected"
                }
            )
    
    @pytest.mark.asyncio 
    async def test_quarantine_device_long_reason(self):
        """Test quarantine with reason too long."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        long_reason = "x" * 201  # 201 characters
        
        with pytest.raises(ValidationError, match="Reason too long"):
            await client.quarantine_device("AP-123", reason=long_reason)
    
    @pytest.mark.asyncio
    async def test_get_threats_valid(self):
        """Test threat retrieval with valid parameters."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        expected_response = {"threats": [], "count": 0}
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response
            
            result = await client.get_threats(limit=50, severity="high")
            
            assert result == expected_response
            mock_request.assert_called_once_with(
                'GET',
                '/api/v2/security/threats',
                params={"limit": "50", "severity": "high"}
            )
    
    @pytest.mark.asyncio
    async def test_get_threats_invalid_params(self):
        """Test threat retrieval with invalid parameters."""
        client = ArubaAPIClient("https://api.example.com", "valid_key_123")
        
        # Invalid limit
        with pytest.raises(ValidationError, match="between 1 and 1000"):
            await client.get_threats(limit=0)
        
        with pytest.raises(ValidationError, match="between 1 and 1000"):
            await client.get_threats(limit=1001)
        
        # Invalid severity
        with pytest.raises(ValidationError, match="Invalid severity"):
            await client.get_threats(severity="invalid")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
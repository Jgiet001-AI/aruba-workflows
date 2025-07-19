"""
Enhanced API client for HPE Aruba services with improved security and error handling.
"""

import asyncio
import logging
import re
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin, urlparse, urlencode
import aiohttp

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Raised when input validation fails"""
    pass

class APIError(Exception):
    """Raised when API requests fail"""
    pass

class ArubaAPIClient:
    """
    Enhanced HPE Aruba API client with security and performance improvements.
    
    Features:
    - HTTPS enforcement
    - Input validation
    - Rate limiting
    - Secure error handling
    - Thread safety
    """
    
    # Valid HTTP methods
    VALID_HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
    
    # Device ID validation pattern
    DEVICE_ID_PATTERN = re.compile(r'^[A-Za-z0-9._-]{1,50}$')
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for the API (must use HTTPS)
            api_key: API authentication key
            timeout: Request timeout in seconds
            
        Raises:
            ValueError: If base_url doesn't use HTTPS or api_key is invalid
        """
        self._validate_base_url(base_url)
        self._validate_api_key(api_key)
        
        self.base_url = base_url.rstrip('/')
        self._api_key = api_key
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
        self._lock = asyncio.Lock()
        self.rate_limit_delay = 0.1
    
    def _validate_base_url(self, base_url: str) -> None:
        """Validate base URL format and security."""
        if not base_url or not isinstance(base_url, str):
            raise ValueError("base_url must be a non-empty string")
        
        if not base_url.startswith('https://'):
            raise ValueError("HTTPS required for API connections")
        
        parsed = urlparse(base_url)
        if not parsed.netloc:
            raise ValueError("Invalid base URL format")
    
    def _validate_api_key(self, api_key: str) -> None:
        """Validate API key format."""
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API key must be a non-empty string")
        
        if len(api_key) < 10:
            raise ValueError("API key too short (minimum 10 characters)")
    
    def validate_device_id(self, device_id: str) -> None:
        """
        Validate device ID format.
        
        Args:
            device_id: Device identifier to validate
            
        Raises:
            ValidationError: If device ID format is invalid
        """
        if not device_id or not isinstance(device_id, str):
            raise ValidationError("device_id must be a non-empty string")
        
        if not self.DEVICE_ID_PATTERN.match(device_id):
            raise ValidationError(
                "device_id must contain only alphanumeric characters, "
                "dots, hyphens, and underscores (max 50 chars)"
            )
    
    def validate_http_method(self, method: str) -> str:
        """
        Validate and normalize HTTP method.
        
        Args:
            method: HTTP method to validate
            
        Returns:
            Normalized uppercase HTTP method
            
        Raises:
            ValidationError: If method is invalid
        """
        if not method or not isinstance(method, str):
            raise ValidationError("HTTP method must be a non-empty string")
        
        method_upper = method.upper()
        if method_upper not in self.VALID_HTTP_METHODS:
            raise ValidationError(f"Invalid HTTP method: {method}")
        
        return method_upper
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'Bearer {self._api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'HPE-Aruba-Automation/1.0'
            },
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(limit=10)  # Connection pooling
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def _construct_url(self, endpoint: str) -> str:
        """
        Safely construct API URL.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Complete API URL
            
        Raises:
            ValueError: If URL construction fails
        """
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        
        url = urljoin(self.base_url, endpoint)
        parsed = urlparse(url)
        
        if not parsed.scheme == 'https' or not parsed.netloc:
            raise ValueError(f"Invalid URL constructed: {url}")
        
        return url
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request with comprehensive error handling.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            APIError: If request fails
        """
        method = self.validate_http_method(method)
        url = self._construct_url(endpoint)
        
        # Add query parameters if provided
        if params:
            encoded_params = urlencode(params)
            url = f"{url}?{encoded_params}"
        
        async with self._lock:
            try:
                await asyncio.sleep(self.rate_limit_delay)
                
                async with self.session.request(method, url, json=data) as response:
                    # Handle rate limiting
                    if response.status == 429:
                        retry_after = int(response.headers.get('Retry-After', 60))
                        logger.warning(f"Rate limited, retrying after {retry_after}s")
                        await asyncio.sleep(retry_after)
                        return await self._make_request(method, endpoint, data, params)
                    
                    # Parse response
                    try:
                        response_data = await response.json()
                    except aiohttp.ContentTypeError:
                        response_data = {"error": "Invalid JSON response"}
                    
                    # Handle errors
                    if response.status >= 400:
                        error_msg = self._format_error_message(response.status)
                        
                        logger.error("API request failed", extra={
                            "status_code": response.status,
                            "endpoint": endpoint,
                            "method": method,
                            "error_type": "api_error"
                        })
                        
                        raise APIError(f"{error_msg} (Status: {response.status})")
                    
                    return response_data
                    
            except aiohttp.ClientError as e:
                logger.error("Network connection failed", extra={
                    "endpoint": endpoint,
                    "error_type": type(e).__name__
                })
                raise APIError("Network connection failed")
            except asyncio.TimeoutError:
                logger.error("Request timeout", extra={
                    "endpoint": endpoint,
                    "timeout": self.timeout
                })
                raise APIError("Request timeout")
    
    def _format_error_message(self, status_code: int) -> str:
        """Format user-friendly error message based on status code."""
        error_messages = {
            400: "Bad request - invalid parameters",
            401: "Authentication failed",
            403: "Access denied - insufficient permissions",
            404: "Resource not found",
            409: "Conflict - resource already exists",
            422: "Validation error",
            429: "Rate limit exceeded",
            500: "Internal server error",
            502: "Bad gateway",
            503: "Service unavailable"
        }
        
        return error_messages.get(status_code, "Request failed")
    
    async def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """
        Get device status information.
        
        Args:
            device_id: Device identifier
            
        Returns:
            Device status data
        """
        self.validate_device_id(device_id)
        return await self._make_request('GET', f'/api/v2/devices/{device_id}/status')
    
    async def isolate_device(
        self, 
        device_id: str, 
        rollback_timer: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Isolate a device for security purposes.
        
        Args:
            device_id: Device to isolate
            rollback_timer: Automatic rollback time in seconds (max 86400)
            
        Returns:
            Isolation result
        """
        self.validate_device_id(device_id)
        
        if rollback_timer is not None:
            if not isinstance(rollback_timer, int) or not (0 <= rollback_timer <= 86400):
                raise ValidationError("rollback_timer must be between 0 and 86400 seconds")
        
        data = {
            "device_id": device_id,
            "action": "isolate",
            "rollback_timer": rollback_timer
        }
        
        return await self._make_request('POST', '/api/v2/devices/isolate', data)
    
    async def quarantine_device(
        self, 
        device_id: str, 
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Quarantine a device.
        
        Args:
            device_id: Device to quarantine
            reason: Reason for quarantine
            
        Returns:
            Quarantine result
        """
        self.validate_device_id(device_id)
        
        if reason and len(reason) > 200:
            raise ValidationError("Reason too long (max 200 characters)")
        
        data = {
            "device_id": device_id,
            "action": "quarantine",
            "reason": reason
        }
        
        return await self._make_request('POST', '/api/v2/devices/quarantine', data)
    
    async def get_threats(
        self, 
        limit: int = 100, 
        severity: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get threat intelligence data.
        
        Args:
            limit: Maximum number of threats to return
            severity: Filter by severity level
            
        Returns:
            Threat data
        """
        if not isinstance(limit, int) or not (1 <= limit <= 1000):
            raise ValidationError("Limit must be between 1 and 1000")
        
        params = {"limit": str(limit)}
        
        if severity:
            valid_severities = {"low", "medium", "high", "critical"}
            if severity.lower() not in valid_severities:
                raise ValidationError(f"Invalid severity: {severity}")
            params["severity"] = severity.lower()
        
        return await self._make_request('GET', '/api/v2/security/threats', params=params)
"""
Optimized data extraction and categorization for HPE Aruba API endpoints.
"""

import json
import logging
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import requests

logger = logging.getLogger(__name__)

class DataExtractionError(Exception):
    """Raised when data extraction fails"""
    pass

class PostmanDataExtractor:
    """
    Enhanced Postman API data extractor with performance optimizations.
    
    Features:
    - Comprehensive error handling
    - Input validation
    - Performance optimizations
    - Memory-efficient processing
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the data extractor.
        
        Args:
            api_key: Postman API key
            
        Raises:
            ValueError: If API key is invalid
        """
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API key must be a non-empty string")
        
        self.api_key = api_key
        self.base_url = "https://api.getpostman.com"
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json",
            "User-Agent": "HPE-Aruba-Extractor/1.0"
        })
        
        # Performance optimization: category lookup cache
        self._category_cache: Dict[int, str] = {}
    
    def get_collections(self) -> List[Dict[str, Any]]:
        """
        Fetch all collections from Postman workspace.
        
        Returns:
            List of collection metadata
            
        Raises:
            DataExtractionError: If request fails
        """
        try:
            response = self.session.get(
                f"{self.base_url}/collections",
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("collections", [])
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch collections: {e}")
            raise DataExtractionError(f"Collection fetch failed: {e}")
    
    def get_collection_details(self, collection_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch detailed collection data with validation.
        
        Args:
            collection_id: Collection identifier
            
        Returns:
            Collection details or None if failed
        """
        if not collection_id or not isinstance(collection_id, str):
            logger.warning("Invalid collection ID provided")
            return None
        
        try:
            response = self.session.get(
                f"{self.base_url}/collections/{collection_id}",
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("collection")
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch collection {collection_id}: {e}")
            return None
    
    def extract_url_safely(self, url_data: Any) -> str:
        """
        Safely extract URL from various Postman formats.
        
        Args:
            url_data: URL data in various formats
            
        Returns:
            Extracted URL string or 'unknown'
        """
        if url_data is None:
            return "unknown"
        
        try:
            if isinstance(url_data, str) and url_data.strip():
                return url_data.strip()
            
            elif isinstance(url_data, dict):
                # Try 'raw' field first
                if "raw" in url_data and isinstance(url_data["raw"], str):
                    raw_url = url_data["raw"].strip()
                    if raw_url:
                        return raw_url
                
                # Construct from host and path
                if "host" in url_data and "path" in url_data:
                    host = url_data["host"]
                    path = url_data["path"]
                    
                    if isinstance(host, list):
                        host = ".".join(str(h) for h in host if h)
                    else:
                        host = str(host) if host else ""
                    
                    if isinstance(path, list):
                        path = "/".join(str(p) for p in path if p is not None)
                    else:
                        path = str(path) if path is not None else ""
                    
                    if host and path is not None:
                        protocol = url_data.get("protocol", "https")
                        return f"{protocol}://{host}/{path}"
            
        except (TypeError, AttributeError) as e:
            logger.debug(f"URL extraction failed: {e}")
        
        return "unknown"
    
    def validate_endpoint_data(self, endpoint: Dict[str, Any]) -> bool:
        """
        Validate endpoint data structure.
        
        Args:
            endpoint: Endpoint dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["name", "method", "url"]
        return (
            isinstance(endpoint, dict) and
            all(field in endpoint for field in required_fields) and
            all(isinstance(endpoint[field], str) for field in required_fields)
        )
    
    def extract_endpoints_from_item(
        self, 
        item: Dict[str, Any], 
        endpoints: List[Dict[str, Any]], 
        path_prefix: str = ""
    ) -> None:
        """
        Recursively extract endpoints with enhanced validation.
        
        Args:
            item: Collection item to process
            endpoints: List to append endpoints to
            path_prefix: Current path prefix
        """
        if not isinstance(item, dict):
            return
        
        if "request" in item:
            request = item["request"]
            if isinstance(request, dict) and "url" in request:
                # Validate and normalize HTTP method
                method = request.get("method", "GET")
                if isinstance(method, str):
                    method = method.upper()
                    if method not in {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}:
                        method = "GET"
                else:
                    method = "GET"
                
                endpoint = {
                    "name": str(item.get("name", "Unnamed")),
                    "method": method,
                    "url": self.extract_url_safely(request["url"]),
                    "description": str(item.get("description", "")),
                    "path": f"{path_prefix}/{item.get('name', 'unnamed')}".strip("/")
                }
                
                # Add headers if present
                if "header" in request and isinstance(request["header"], list):
                    headers = []
                    for header in request["header"]:
                        if isinstance(header, dict) and "key" in header:
                            headers.append({
                                header.get("key", ""): header.get("value", "")
                            })
                    if headers:
                        endpoint["headers"] = headers
                
                # Add body information if present
                if "body" in request and isinstance(request["body"], dict):
                    body_type = request["body"].get("mode", "none")
                    endpoint["body_type"] = body_type
                    if body_type == "raw" and "raw" in request["body"]:
                        # Limit body example size for memory efficiency
                        raw_body = request["body"]["raw"]
                        if isinstance(raw_body, str) and len(raw_body) <= 1000:
                            endpoint["body_example"] = raw_body
                
                if self.validate_endpoint_data(endpoint):
                    endpoints.append(endpoint)
                else:
                    logger.debug(f"Skipping invalid endpoint: {endpoint.get('name', 'unknown')}")
        
        # Process nested items (folders)
        if "item" in item and isinstance(item["item"], list):
            folder_name = str(item.get("name", "folder"))
            new_path = f"{path_prefix}/{folder_name}" if path_prefix else folder_name
            
            for sub_item in item["item"]:
                self.extract_endpoints_from_item(sub_item, endpoints, new_path)
    
    def save_data_safely(
        self, 
        data: Any, 
        file_path: Path, 
        description: str = "data"
    ) -> None:
        """
        Safely save data to JSON file with error handling.
        
        Args:
            data: Data to save
            file_path: Target file path
            description: Description for error messages
            
        Raises:
            DataExtractionError: If save operation fails
        """
        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully saved {description} to {file_path}")
            
        except (OSError, IOError, json.JSONEncodeError) as e:
            error_msg = f"Failed to save {description}: {e}"
            logger.error(error_msg)
            raise DataExtractionError(error_msg)

class EndpointCategorizer:
    """
    Optimized endpoint categorization with improved performance.
    """
    
    # Pre-compiled category keywords for better performance
    CATEGORY_KEYWORDS = {
        "device_management": {
            "device", "switch", "gateway", "appliance", "inventory", 
            "hardware", "equipment", "unit"
        },
        "configuration": {
            "config", "template", "setting", "parameter", "profile",
            "preferences", "setup", "deployment"
        },
        "monitoring": {
            "monitor", "stats", "metric", "health", "status", "uptime",
            "performance", "telemetry", "analytics"
        },
        "authentication": {
            "auth", "login", "token", "credential", "oauth", "cert",
            "certificate", "session", "access"
        },
        "network_policies": {
            "policy", "rule", "acl", "vlan", "routing", "qos",
            "firewall", "security", "access-control"
        },
        "wireless": {
            "wireless", "wifi", "ssid", "ap", "radio", "wlan",
            "beacon", "mesh", "rf", "antenna"
        },
        "switching": {
            "port", "interface", "trunk", "lag", "stp", "lldp",
            "spanning-tree", "ethernet", "link"
        },
        "security": {
            "security", "firewall", "ips", "threat", "intrusion",
            "malware", "vulnerability", "compliance"
        }
    }
    
    def __init__(self, endpoints_file: Path):
        """
        Initialize categorizer with file validation.
        
        Args:
            endpoints_file: Path to endpoints JSON file
            
        Raises:
            DataExtractionError: If file loading fails
        """
        self.endpoints_file = Path(endpoints_file)
        self.endpoints: List[Dict[str, Any]] = []
        self.product_categories: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # Performance optimization: pre-compile regex patterns
        self._device_id_pattern = re.compile(r'/device[s]?/([^/]+)')
        
        self.load_endpoints()
    
    def load_endpoints(self) -> None:
        """Load and validate endpoints from JSON file."""
        try:
            if not self.endpoints_file.exists():
                raise FileNotFoundError(f"Endpoints file not found: {self.endpoints_file}")
            
            with open(self.endpoints_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError("Endpoints file must contain a JSON array")
            
            # Validate endpoint structure
            valid_endpoints = []
            for i, endpoint in enumerate(data):
                if self._validate_endpoint_structure(endpoint, i):
                    valid_endpoints.append(endpoint)
            
            self.endpoints = valid_endpoints
            logger.info(f"Loaded {len(self.endpoints)} valid endpoints for categorization")
            
        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
            error_msg = f"Failed to load endpoints: {e}"
            logger.error(error_msg)
            raise DataExtractionError(error_msg)
    
    def _validate_endpoint_structure(self, endpoint: Any, index: int) -> bool:
        """
        Validate individual endpoint structure.
        
        Args:
            endpoint: Endpoint data to validate
            index: Index for error reporting
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(endpoint, dict):
            logger.warning(f"Skipping invalid endpoint at index {index}: not a dictionary")
            return False
        
        required_fields = ["url", "name", "method"]
        for field in required_fields:
            value = endpoint.get(field)
            if not isinstance(value, str):
                logger.warning(f"Skipping endpoint at index {index}: invalid {field}")
                return False
        
        return True
    
    def categorize_endpoints_optimized(self) -> None:
        """
        Categorize endpoints using optimized algorithm.
        """
        for endpoint in self.endpoints:
            # Combine text fields for efficient searching
            search_text = " ".join([
                str(endpoint.get('url', '')),
                str(endpoint.get('name', '')),
                str(endpoint.get('description', '')),
                str(endpoint.get('folder', ''))
            ]).lower()
            
            # Find best matching category
            category = self._find_best_category(search_text)
            self.product_categories[category].append(endpoint)
    
    def _find_best_category(self, search_text: str) -> str:
        """
        Find the best matching category for search text.
        
        Args:
            search_text: Combined text to categorize
            
        Returns:
            Category name
        """
        category_scores = {}
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in search_text)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            # Return category with highest score
            return max(category_scores.items(), key=lambda x: x[1])[0]
        
        # Fallback categorization by URL patterns
        if '/device' in search_text or '/switch' in search_text:
            return "device_management"
        elif '/ap' in search_text or '/access' in search_text:
            return "wireless"
        elif '/config' in search_text or '/template' in search_text:
            return "configuration"
        
        return "other"
    
    def generate_summary_report(self, output_dir: Path) -> Dict[str, Any]:
        """
        Generate comprehensive categorization summary.
        
        Args:
            output_dir: Output directory for reports
            
        Returns:
            Summary statistics
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate statistics
            summary = {
                "total_endpoints": len(self.endpoints),
                "categories": {},
                "top_categories": [],
                "processing_timestamp": datetime.now().isoformat()
            }
            
            # Category statistics
            for category, endpoints in self.product_categories.items():
                summary["categories"][category] = {
                    "count": len(endpoints),
                    "percentage": round((len(endpoints) / len(self.endpoints)) * 100, 2),
                    "methods": self._count_methods(endpoints)
                }
            
            # Top categories by count
            summary["top_categories"] = sorted(
                summary["categories"].items(),
                key=lambda x: x[1]["count"],
                reverse=True
            )[:10]
            
            # Save detailed data
            self._save_categorization_data(output_dir)
            
            # Save summary
            summary_file = output_dir / "categorization_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Generated categorization summary: {summary_file}")
            return summary
            
        except Exception as e:
            error_msg = f"Failed to generate summary: {e}"
            logger.error(error_msg)
            raise DataExtractionError(error_msg)
    
    def _count_methods(self, endpoints: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count HTTP methods in endpoint list."""
        method_counts = defaultdict(int)
        for endpoint in endpoints:
            method = endpoint.get("method", "UNKNOWN")
            method_counts[method] += 1
        return dict(method_counts)
    
    def _save_categorization_data(self, output_dir: Path) -> None:
        """Save categorized endpoint data."""
        categorized_file = output_dir / "endpoints_by_category.json"
        with open(categorized_file, 'w', encoding='utf-8') as f:
            json.dump(dict(self.product_categories), f, indent=2, ensure_ascii=False)
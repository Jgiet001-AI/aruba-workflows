"""
Test suite for data extraction and categorization modules.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import our improved modules
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_extractor import PostmanDataExtractor, EndpointCategorizer, DataExtractionError

class TestPostmanDataExtractor:
    """Test cases for PostmanDataExtractor."""
    
    def test_init_valid_api_key(self):
        """Test successful initialization."""
        extractor = PostmanDataExtractor("valid_api_key_123")
        assert extractor.api_key == "valid_api_key_123"
        assert extractor.base_url == "https://api.getpostman.com"
    
    def test_init_invalid_api_key(self):
        """Test initialization with invalid API key."""
        with pytest.raises(ValueError, match="non-empty string"):
            PostmanDataExtractor("")
        
        with pytest.raises(ValueError, match="non-empty string"):
            PostmanDataExtractor(None)
    
    def test_extract_url_safely_string(self):
        """Test URL extraction from string."""
        extractor = PostmanDataExtractor("test_key")
        
        assert extractor.extract_url_safely("https://api.example.com") == "https://api.example.com"
        assert extractor.extract_url_safely("  https://api.example.com  ") == "https://api.example.com"
        assert extractor.extract_url_safely("") == "unknown"
        assert extractor.extract_url_safely(None) == "unknown"
    
    def test_extract_url_safely_dict_raw(self):
        """Test URL extraction from dict with raw field."""
        extractor = PostmanDataExtractor("test_key")
        
        url_data = {"raw": "https://api.example.com/test"}
        assert extractor.extract_url_safely(url_data) == "https://api.example.com/test"
        
        url_data = {"raw": "  https://api.example.com/test  "}
        assert extractor.extract_url_safely(url_data) == "https://api.example.com/test"
        
        url_data = {"raw": ""}
        assert extractor.extract_url_safely(url_data) == "unknown"
    
    def test_extract_url_safely_dict_host_path(self):
        """Test URL extraction from dict with host and path."""
        extractor = PostmanDataExtractor("test_key")
        
        # List format
        url_data = {
            "protocol": "https",
            "host": ["api", "example", "com"],
            "path": ["v1", "test"]
        }
        assert extractor.extract_url_safely(url_data) == "https://api.example.com/v1/test"
        
        # String format
        url_data = {
            "protocol": "https",
            "host": "api.example.com",
            "path": "v1/test"
        }
        assert extractor.extract_url_safely(url_data) == "https://api.example.com/v1/test"
        
        # Missing protocol (should default to https)
        url_data = {
            "host": ["api", "example", "com"],
            "path": ["v1", "test"]
        }
        assert extractor.extract_url_safely(url_data) == "https://api.example.com/v1/test"
    
    def test_extract_url_safely_malformed(self):
        """Test URL extraction with malformed data."""
        extractor = PostmanDataExtractor("test_key")
        
        # Invalid dict structures
        assert extractor.extract_url_safely({"invalid": "data"}) == "unknown"
        assert extractor.extract_url_safely({"host": None, "path": None}) == "unknown"
        assert extractor.extract_url_safely(123) == "unknown"
        assert extractor.extract_url_safely([]) == "unknown"
    
    def test_validate_endpoint_data(self):
        """Test endpoint data validation."""
        extractor = PostmanDataExtractor("test_key")
        
        # Valid endpoint
        valid_endpoint = {
            "name": "Test Endpoint",
            "method": "GET", 
            "url": "https://api.example.com/test"
        }
        assert extractor.validate_endpoint_data(valid_endpoint) is True
        
        # Invalid endpoints
        invalid_cases = [
            {},  # Empty dict
            {"name": "Test"},  # Missing fields
            {"name": 123, "method": "GET", "url": "test"},  # Wrong types
            None,  # Not a dict
            {"name": "", "method": "GET", "url": "test"}  # Empty required field
        ]
        
        for invalid_endpoint in invalid_cases:
            assert extractor.validate_endpoint_data(invalid_endpoint) is False
    
    @patch('requests.Session.get')
    def test_get_collections_success(self, mock_get):
        """Test successful collection fetching."""
        extractor = PostmanDataExtractor("test_key")
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "collections": [
                {"id": "123", "name": "Test Collection"}
            ]
        }
        mock_get.return_value = mock_response
        
        collections = extractor.get_collections()
        
        assert len(collections) == 1
        assert collections[0]["name"] == "Test Collection"
        mock_get.assert_called_once()
    
    @patch('requests.Session.get')
    def test_get_collections_failure(self, mock_get):
        """Test collection fetching failure."""
        extractor = PostmanDataExtractor("test_key")
        
        mock_get.side_effect = Exception("Network error")
        
        with pytest.raises(DataExtractionError, match="Collection fetch failed"):
            extractor.get_collections()
    
    @patch('requests.Session.get')
    def test_get_collection_details_success(self, mock_get):
        """Test successful collection detail fetching."""
        extractor = PostmanDataExtractor("test_key")
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "collection": {"id": "123", "info": {"name": "Test"}}
        }
        mock_get.return_value = mock_response
        
        details = extractor.get_collection_details("123")
        
        assert details is not None
        assert details["id"] == "123"
    
    @patch('requests.Session.get')
    def test_get_collection_details_failure(self, mock_get):
        """Test collection detail fetching failure."""
        extractor = PostmanDataExtractor("test_key")
        
        mock_get.side_effect = Exception("Network error")
        
        details = extractor.get_collection_details("123")
        assert details is None
    
    def test_get_collection_details_invalid_id(self):
        """Test collection detail fetching with invalid ID."""
        extractor = PostmanDataExtractor("test_key")
        
        assert extractor.get_collection_details("") is None
        assert extractor.get_collection_details(None) is None
    
    def test_extract_endpoints_from_item_request(self):
        """Test endpoint extraction from request item."""
        extractor = PostmanDataExtractor("test_key")
        endpoints = []
        
        request_item = {
            "name": "Test Request",
            "request": {
                "method": "GET",
                "url": "https://api.example.com/test",
                "header": [{"key": "Authorization", "value": "Bearer token"}],
                "body": {"mode": "raw", "raw": '{"test": "data"}'}
            },
            "description": "Test description"
        }
        
        extractor.extract_endpoints_from_item(request_item, endpoints)
        
        assert len(endpoints) == 1
        endpoint = endpoints[0]
        assert endpoint["name"] == "Test Request"
        assert endpoint["method"] == "GET"
        assert endpoint["url"] == "https://api.example.com/test"
        assert endpoint["description"] == "Test description"
        assert "headers" in endpoint
        assert endpoint["body_type"] == "raw"
    
    def test_extract_endpoints_from_item_folder(self):
        """Test endpoint extraction from folder item."""
        extractor = PostmanDataExtractor("test_key")
        endpoints = []
        
        folder_item = {
            "name": "Test Folder",
            "item": [
                {
                    "name": "Nested Request",
                    "request": {
                        "method": "POST",
                        "url": "https://api.example.com/nested"
                    }
                }
            ]
        }
        
        extractor.extract_endpoints_from_item(folder_item, endpoints, "root")
        
        assert len(endpoints) == 1
        endpoint = endpoints[0]
        assert endpoint["name"] == "Nested Request"
        assert endpoint["path"] == "root/Test Folder/Nested Request"
    
    def test_extract_endpoints_from_item_invalid(self):
        """Test endpoint extraction with invalid data."""
        extractor = PostmanDataExtractor("test_key")
        endpoints = []
        
        # Invalid item types
        invalid_items = [
            None,
            "not a dict",
            {"invalid": "structure"},
            {"request": "not a dict"},
            {"request": {"method": 123}}  # Invalid method type
        ]
        
        for item in invalid_items:
            extractor.extract_endpoints_from_item(item, endpoints)
        
        # Should not have added any endpoints
        assert len(endpoints) == 0
    
    def test_save_data_safely_success(self):
        """Test successful data saving."""
        extractor = PostmanDataExtractor("test_key")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.json"
            test_data = {"test": "data"}
            
            extractor.save_data_safely(test_data, file_path, "test data")
            
            assert file_path.exists()
            with open(file_path, 'r') as f:
                saved_data = json.load(f)
            assert saved_data == test_data
    
    def test_save_data_safely_failure(self):
        """Test data saving failure."""
        extractor = PostmanDataExtractor("test_key")
        
        # Try to save to invalid path
        invalid_path = Path("/invalid/path/test.json")
        
        with pytest.raises(DataExtractionError, match="Failed to save"):
            extractor.save_data_safely({"test": "data"}, invalid_path)

class TestEndpointCategorizer:
    """Test cases for EndpointCategorizer."""
    
    def create_test_endpoints_file(self, endpoints_data):
        """Helper to create temporary endpoints file."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(endpoints_data, temp_file)
        temp_file.close()
        return Path(temp_file.name)
    
    def test_init_success(self):
        """Test successful initialization."""
        test_data = [
            {"name": "Test", "url": "https://api.test.com", "method": "GET"}
        ]
        
        endpoints_file = self.create_test_endpoints_file(test_data)
        
        try:
            categorizer = EndpointCategorizer(endpoints_file)
            assert len(categorizer.endpoints) == 1
            assert categorizer.endpoints[0]["name"] == "Test"
        finally:
            endpoints_file.unlink()
    
    def test_init_file_not_found(self):
        """Test initialization with non-existent file."""
        non_existent_file = Path("/non/existent/file.json")
        
        with pytest.raises(DataExtractionError, match="Failed to load endpoints"):
            EndpointCategorizer(non_existent_file)
    
    def test_init_invalid_json(self):
        """Test initialization with invalid JSON."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        temp_file.write("invalid json content")
        temp_file.close()
        
        try:
            with pytest.raises(DataExtractionError, match="Failed to load endpoints"):
                EndpointCategorizer(Path(temp_file.name))
        finally:
            Path(temp_file.name).unlink()
    
    def test_init_wrong_data_type(self):
        """Test initialization with wrong data type."""
        test_data = {"not": "a list"}
        
        endpoints_file = self.create_test_endpoints_file(test_data)
        
        try:
            with pytest.raises(DataExtractionError, match="JSON array"):
                EndpointCategorizer(endpoints_file)
        finally:
            endpoints_file.unlink()
    
    def test_validate_endpoint_structure_valid(self):
        """Test endpoint structure validation with valid data."""
        test_data = [{"name": "test", "url": "test", "method": "GET"}]
        endpoints_file = self.create_test_endpoints_file(test_data)
        
        try:
            categorizer = EndpointCategorizer(endpoints_file)
            
            valid_endpoint = {"name": "Test", "url": "https://api.test.com", "method": "GET"}
            assert categorizer._validate_endpoint_structure(valid_endpoint, 0) is True
        finally:
            endpoints_file.unlink()
    
    def test_validate_endpoint_structure_invalid(self):
        """Test endpoint structure validation with invalid data."""
        test_data = [{"name": "test", "url": "test", "method": "GET"}]
        endpoints_file = self.create_test_endpoints_file(test_data)
        
        try:
            categorizer = EndpointCategorizer(endpoints_file)
            
            invalid_cases = [
                "not a dict",
                {"name": "Test"},  # Missing fields
                {"name": 123, "url": "test", "method": "GET"},  # Wrong type
                {"name": "", "url": "test", "method": "GET"},  # Empty required field
            ]
            
            for i, invalid_endpoint in enumerate(invalid_cases):
                assert categorizer._validate_endpoint_structure(invalid_endpoint, i) is False
        finally:
            endpoints_file.unlink()
    
    def test_find_best_category_device_management(self):
        """Test category detection for device management."""
        test_data = [{"name": "test", "url": "test", "method": "GET"}]
        endpoints_file = self.create_test_endpoints_file(test_data)
        
        try:
            categorizer = EndpointCategorizer(endpoints_file)
            
            # Test device management keywords
            device_texts = [
                "get device status",
                "switch configuration",
                "appliance management",
                "hardware inventory"
            ]
            
            for text in device_texts:
                category = categorizer._find_best_category(text)
                assert category == "device_management"
        finally:
            endpoints_file.unlink()
    
    def test_find_best_category_configuration(self):
        """Test category detection for configuration."""
        test_data = [{"name": "test", "url": "test", "method": "GET"}]
        endpoints_file = self.create_test_endpoints_file(test_data)
        
        try:
            categorizer = EndpointCategorizer(endpoints_file)
            
            config_texts = [
                "config template",
                "update settings",
                "profile management",
                "setup parameters"
            ]
            
            for text in config_texts:
                category = categorizer._find_best_category(text)
                assert category == "configuration"
        finally:
            endpoints_file.unlink()
    
    def test_find_best_category_fallback(self):
        """Test category fallback logic."""
        test_data = [{"name": "test", "url": "test", "method": "GET"}]
        endpoints_file = self.create_test_endpoints_file(test_data)
        
        try:
            categorizer = EndpointCategorizer(endpoints_file)
            
            # Test URL-based fallbacks
            fallback_cases = [
                ("/device/status", "device_management"),
                ("/switch/config", "device_management"),
                ("/ap/settings", "wireless"),
                ("/config/template", "configuration"),
                ("random unmatched text", "other")
            ]
            
            for text, expected_category in fallback_cases:
                category = categorizer._find_best_category(text)
                assert category == expected_category
        finally:
            endpoints_file.unlink()
    
    def test_categorize_endpoints_optimized(self):
        """Test optimized endpoint categorization."""
        test_data = [
            {"name": "Device Status", "url": "/api/device/status", "method": "GET", "description": "Get device status"},
            {"name": "Config Template", "url": "/api/config/template", "method": "POST", "description": "Create config template"},
            {"name": "Monitor Stats", "url": "/api/monitor/stats", "method": "GET", "description": "Get monitoring statistics"}
        ]
        
        endpoints_file = self.create_test_endpoints_file(test_data)
        
        try:
            categorizer = EndpointCategorizer(endpoints_file)
            categorizer.categorize_endpoints_optimized()
            
            # Check categorization results
            assert len(categorizer.product_categories["device_management"]) == 1
            assert len(categorizer.product_categories["configuration"]) == 1
            assert len(categorizer.product_categories["monitoring"]) == 1
            
            # Verify endpoint assignment
            device_endpoint = categorizer.product_categories["device_management"][0]
            assert device_endpoint["name"] == "Device Status"
        finally:
            endpoints_file.unlink()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
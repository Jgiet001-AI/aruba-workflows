#!/usr/bin/env python3
"""
HPE Aruba Postman Collection API Extractor

This script uses the Postman API to programmatically extract all endpoint information
from HPE Aruba Networking collections. It provides comprehensive endpoint mapping
for n8n workflow development.

Requirements:
- Postman API key (set as POSTMAN_API_KEY environment variable)
- requests library: pip install requests

Usage:
    export POSTMAN_API_KEY=your_postman_api_key_here
    python fetch_postman_collections.py
"""

import os
import requests
import json
import time
from typing import Dict, List, Any, Optional

class PostmanAPIExtractor:
    """Extract and analyze HPE Aruba endpoints from Postman collections."""
    
    def __init__(self, api_key: str):
        """Initialize with Postman API key."""
        self.api_key = api_key
        self.base_url = "https://api.getpostman.com"
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_collections(self) -> List[Dict[str, Any]]:
        """Fetch all collections from Postman workspace."""
        try:
            response = self.session.get(f"{self.base_url}/collections")
            response.raise_for_status()
            return response.json().get("collections", [])
        except requests.RequestException as e:
            print(f"❌ Error fetching collections: {e}")
            return []
    
    def get_collection_details(self, collection_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed collection data."""
        try:
            response = self.session.get(f"{self.base_url}/collections/{collection_id}")
            response.raise_for_status()
            return response.json().get("collection")
        except requests.RequestException as e:
            print(f"❌ Error fetching collection {collection_id}: {e}")
            return None
    
    def extract_endpoints_from_item(self, item: Dict[str, Any], endpoints: List[Dict[str, Any]], path_prefix: str = "") -> None:
        """Recursively extract endpoints from collection items."""
        if "request" in item:
            # This is an actual request
            request = item["request"]
            if isinstance(request, dict) and "url" in request:
                endpoint = {
                    "name": item.get("name", "Unnamed"),
                    "method": request.get("method", "GET"),
                    "url": self._extract_url(request["url"]),
                    "description": item.get("description", ""),
                    "path": f"{path_prefix}/{item.get('name', 'unnamed')}".strip("/")
                }
                
                # Extract headers
                if "header" in request:
                    endpoint["headers"] = [
                        {h.get("key"): h.get("value")} 
                        for h in request["header"] 
                        if isinstance(h, dict)
                    ]
                
                # Extract body
                if "body" in request and request["body"]:
                    endpoint["body_type"] = request["body"].get("mode", "none")
                    if endpoint["body_type"] == "raw":
                        endpoint["body_example"] = request["body"].get("raw", "")
                
                endpoints.append(endpoint)
        
        # Process nested items (folders)
        if "item" in item:
            folder_name = item.get("name", "folder")
            new_path = f"{path_prefix}/{folder_name}" if path_prefix else folder_name
            for sub_item in item["item"]:
                self.extract_endpoints_from_item(sub_item, endpoints, new_path)
    
    def _extract_url(self, url_data: Any) -> str:
        """Extract URL string from various Postman URL formats."""
        if isinstance(url_data, str):
            return url_data
        elif isinstance(url_data, dict):
            if "raw" in url_data:
                return url_data["raw"]
            elif "host" in url_data and "path" in url_data:
                host = ".".join(url_data["host"]) if isinstance(url_data["host"], list) else str(url_data["host"])
                path = "/".join(url_data["path"]) if isinstance(url_data["path"], list) else str(url_data["path"])
                protocol = url_data.get("protocol", "https")
                return f"{protocol}://{host}/{path}"
        return "unknown"
    
    def categorize_endpoints(self, endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Categorize endpoints for n8n workflow development."""
        categories = {
            "device_management": [],
            "configuration": [],
            "monitoring": [],
            "authentication": [],
            "network_policies": [],
            "users_groups": [],
            "alerts_events": [],
            "reports_analytics": [],
            "wireless": [],
            "switching": [],
            "security": [],
            "cloud_services": [],
            "other": []
        }
        
        # Keywords for categorization
        category_keywords = {
            "device_management": ["device", "switch", "gateway", "appliance", "inventory"],
            "configuration": ["config", "template", "setting", "parameter", "profile"],
            "monitoring": ["monitor", "stats", "metric", "health", "status", "uptime"],
            "authentication": ["auth", "login", "token", "credential", "oauth", "cert"],
            "network_policies": ["policy", "rule", "acl", "vlan", "routing", "qos"],
            "users_groups": ["user", "group", "client", "guest", "role", "permission"],
            "alerts_events": ["alert", "event", "notification", "webhook", "alarm"],
            "reports_analytics": ["report", "analytic", "insight", "dashboard", "log"],
            "wireless": ["wireless", "wifi", "ssid", "ap", "radio", "wlan"],
            "switching": ["port", "interface", "trunk", "lag", "stp", "lldp"],
            "security": ["security", "firewall", "ips", "threat", "intrusion"],
            "cloud_services": ["cloud", "service", "subscription", "license", "saas"]
        }
        
        for endpoint in endpoints:
            categorized = False
            endpoint_text = f"{endpoint['name']} {endpoint['url']} {endpoint['description']}".lower()
            
            for category, keywords in category_keywords.items():
                if any(keyword in endpoint_text for keyword in keywords):
                    categories[category].append(endpoint)
                    categorized = True
                    break
            
            if not categorized:
                categories["other"].append(endpoint)
        
        return categories
    
    def generate_n8n_recommendations(self, categorized_endpoints: Dict[str, Any]) -> Dict[str, Any]:
        """Generate n8n workflow recommendations based on endpoints."""
        recommendations = {}
        
        workflow_patterns = {
            "device_management": {
                "workflow_type": "Device Lifecycle Management",
                "triggers": ["Schedule (daily health check)", "Webhook (device events)"],
                "common_flows": ["Device discovery → Health check → Alert if issues"],
                "suggested_nodes": ["HTTP Request", "IF", "Email/Slack", "Set"]
            },
            "configuration": {
                "workflow_type": "Configuration Management",
                "triggers": ["Manual trigger", "Schedule (backup)", "Webhook (config change)"],
                "common_flows": ["Backup config → Apply template → Validate → Rollback if needed"],
                "suggested_nodes": ["HTTP Request", "Code", "IF", "Error Trigger"]
            },
            "monitoring": {
                "workflow_type": "Monitoring & Alerting",
                "triggers": ["Schedule (every 5-15 min)", "Webhook (alert events)"],
                "common_flows": ["Collect metrics → Check thresholds → Alert if exceeded"],
                "suggested_nodes": ["Schedule Trigger", "HTTP Request", "IF", "Slack/Email"]
            },
            "authentication": {
                "workflow_type": "Authentication Management",
                "triggers": ["Schedule (token refresh)", "Manual trigger"],
                "common_flows": ["Check token expiry → Refresh if needed → Update credentials"],
                "suggested_nodes": ["HTTP Request", "Credentials", "Set", "IF"]
            }
        }
        
        for category, endpoints in categorized_endpoints.items():
            if endpoints and category in workflow_patterns:
                recommendations[category] = {
                    **workflow_patterns[category],
                    "endpoint_count": len(endpoints),
                    "priority": "high" if len(endpoints) > 20 else "medium" if len(endpoints) > 5 else "low",
                    "sample_endpoints": endpoints[:3]  # First 3 as examples
                }
        
        return recommendations
    
    def save_results(self, output_dir: str, all_endpoints: List[Dict[str, Any]], 
                     categorized_endpoints: Dict[str, Any], recommendations: Dict[str, Any],
                     raw_collections: List[Dict[str, Any]]) -> None:
        """Save all extracted data to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save raw collections data
        with open(f"{output_dir}/raw_collections_data.json", "w") as f:
            json.dump(raw_collections, f, indent=2)
        
        # Save all endpoints
        with open(f"{output_dir}/all_aruba_endpoints.json", "w") as f:
            json.dump(all_endpoints, f, indent=2)
        
        # Save categorized endpoints
        with open(f"{output_dir}/n8n_endpoint_categories.json", "w") as f:
            json.dump(categorized_endpoints, f, indent=2)
        
        # Save n8n recommendations
        with open(f"{output_dir}/n8n_workflow_recommendations.json", "w") as f:
            json.dump(recommendations, f, indent=2)
        
        # Generate summary statistics
        summary = {
            "total_endpoints": len(all_endpoints),
            "total_collections": len(raw_collections),
            "endpoints_by_method": {},
            "endpoints_by_category": {k: len(v) for k, v in categorized_endpoints.items()},
            "extraction_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Count by HTTP method
        for endpoint in all_endpoints:
            method = endpoint.get("method", "UNKNOWN")
            summary["endpoints_by_method"][method] = summary["endpoints_by_method"].get(method, 0) + 1
        
        with open(f"{output_dir}/collections_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        # Generate HTTP methods summary
        methods_summary = {}
        for endpoint in all_endpoints:
            method = endpoint.get("method", "UNKNOWN")
            if method not in methods_summary:
                methods_summary[method] = []
            methods_summary[method].append({
                "name": endpoint.get("name"),
                "url": endpoint.get("url"),
                "category": self._find_category(endpoint, categorized_endpoints)
            })
        
        with open(f"{output_dir}/http_methods_summary.json", "w") as f:
            json.dump(methods_summary, f, indent=2)
        
        print(f"\n📁 Results saved to: {output_dir}/")
        print(f"   - all_aruba_endpoints.json ({len(all_endpoints)} endpoints)")
        print(f"   - n8n_endpoint_categories.json ({len(categorized_endpoints)} categories)")
        print(f"   - n8n_workflow_recommendations.json")
        print(f"   - collections_summary.json")
        print(f"   - http_methods_summary.json")
        print(f"   - raw_collections_data.json")
    
    def _find_category(self, endpoint: Dict[str, Any], categorized_endpoints: Dict[str, Any]) -> str:
        """Find which category an endpoint belongs to."""
        for category, endpoints in categorized_endpoints.items():
            if endpoint in endpoints:
                return category
        return "unknown"

def main():
    """Main execution"""
    api_key = os.getenv("POSTMAN_API_KEY")
    if not api_key:
        print("Error: POSTMAN_API_KEY environment variable not set")
        print("Please set your Postman API key: export POSTMAN_API_KEY=your_key_here")
        return
    output_dir = "/Users/jeangiet/Documents/Claude/aruba-workflows/postman-api-results"
    
    print("🚀 HPE Aruba Postman API Extractor")
    print("="*50)
    
    # Initialize extractor
    extractor = PostmanAPIExtractor(api_key)
    
    # Step 1: Get all collections
    print("\n📋 Fetching collections...")
    collections = extractor.get_collections()
    
    if not collections:
        print("❌ No collections found or API error")
        return
    
    # Filter for Aruba collections
    aruba_collections = [
        col for col in collections 
        if any(keyword in col.get("name", "").lower() 
               for keyword in ["aruba", "hpe", "central", "aos", "edgeconnect", "uxi"])
    ]
    
    print(f"📦 Found {len(collections)} total collections")
    print(f"🎯 Found {len(aruba_collections)} Aruba-related collections:")
    for col in aruba_collections:
        print(f"   - {col['name']}")
    
    # Step 2: Extract detailed data
    print(f"\n🔍 Extracting detailed endpoint data...")
    all_endpoints = []
    detailed_collections = []
    
    for i, collection in enumerate(aruba_collections, 1):
        print(f"   Processing {i}/{len(aruba_collections)}: {collection['name']}")
        
        details = extractor.get_collection_details(collection['id'])
        if details:
            detailed_collections.append(details)
            
            # Extract endpoints from this collection
            collection_endpoints = []
            if "item" in details:
                for item in details["item"]:
                    extractor.extract_endpoints_from_item(item, collection_endpoints)
            
            # Add collection context to each endpoint
            for endpoint in collection_endpoints:
                endpoint["collection_name"] = details.get("info", {}).get("name", "Unknown")
                endpoint["collection_id"] = collection['id']
            
            all_endpoints.extend(collection_endpoints)
            print(f"      → {len(collection_endpoints)} endpoints found")
        
        # Rate limiting
        time.sleep(0.5)
    
    print(f"\n✅ Extracted {len(all_endpoints)} total endpoints from {len(detailed_collections)} collections")
    
    # Step 3: Categorize endpoints
    print(f"\n🏷️  Categorizing endpoints for n8n workflows...")
    categorized_endpoints = extractor.categorize_endpoints(all_endpoints)
    
    print("📊 Category breakdown:")
    for category, endpoints in categorized_endpoints.items():
        if endpoints:
            print(f"   {category}: {len(endpoints)} endpoints")
    
    # Step 4: Generate n8n recommendations
    print(f"\n🎯 Generating n8n workflow recommendations...")
    recommendations = extractor.generate_n8n_recommendations(categorized_endpoints)
    
    # Step 5: Save all results
    print(f"\n💾 Saving results...")
    extractor.save_results(output_dir, all_endpoints, categorized_endpoints, 
                          recommendations, detailed_collections)
    
    # Step 6: Print summary for n8n workflow development
    print(f"\n🎉 HPE Aruba API Analysis Complete!")
    print("="*50)
    print(f"📈 Summary:")
    print(f"   Total Endpoints: {len(all_endpoints)}")
    print(f"   Collections Analyzed: {len(detailed_collections)}")
    print(f"   Categories Created: {len([k for k, v in categorized_endpoints.items() if v])}")
    print(f"   Workflow Recommendations: {len(recommendations)}")
    
    print(f"\n🚀 Top Priority n8n Workflows:")
    high_priority = {k: v for k, v in recommendations.items() if v.get('priority') == 'high'}
    for category, rec in high_priority.items():
        print(f"\n   📝 {rec['workflow_type']} ({category.replace('_', ' ').title()})")
        print(f"      Endpoints: {rec['endpoint_count']}")
        print(f"      Triggers: {', '.join(rec['triggers'])}")
        
        print(f"      Sample Endpoints:")
        for endpoint in rec['sample_endpoints']:
            method = endpoint.get('method', 'GET')
            name = endpoint.get('name', 'Unnamed')
            print(f"         {method}: {name}")
            if 'url' in endpoint:
                print(f"            URL: {endpoint['url']}")
        
        print(f"      Suggested n8n Nodes: {', '.join(rec['suggested_nodes'])}")
    
    print(f"\n🔧 Next Steps for n8n Development:")
    print(f"   1. Review categorized endpoints in: {output_dir}/n8n_endpoint_categories.json")
    print(f"   2. Start with high-priority workflows (device_management, monitoring)")
    print(f"   3. Use HTTP Request nodes with extracted endpoint URLs")
    print(f"   4. Implement error handling for API authentication")
    print(f"   5. Test with sample payloads from endpoint documentation")
    
    if recommendations:
        print(f"\n📋 Recommended Workflow Implementation Order:")
        priority_order = ["high", "medium", "low"]
        for priority in priority_order:
            priority_items = [k for k, v in recommendations.items() if v.get('priority') == priority]
            if priority_items:
                print(f"   {priority.upper()} Priority: {', '.join(priority_items)}")
    
    # Show sample endpoints for immediate use
    if all_endpoints:
        print(f"\n🎯 Ready-to-Use Endpoint Examples:")
        method_samples = {}
        for endpoint in all_endpoints[:20]:  # First 20 endpoints
            method = endpoint.get('method', 'GET')
            if method not in method_samples:
                method_samples[method] = []
            if len(method_samples[method]) < 3:  # Max 3 per method
                method_samples[method].append(endpoint)
        
        for method, samples in method_samples.items():
            print(f"\n   {method} Examples:")
            for sample in samples:
                print(f"   {method}: {sample['url']}")
        
        print("\n✅ Ready for n8n workflow development!")

if __name__ == "__main__":
    main()
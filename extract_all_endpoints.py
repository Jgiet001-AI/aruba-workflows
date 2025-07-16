#!/usr/bin/env python3
"""
Complete HPE Aruba Postman Collection Endpoint Extractor
Extracts all HTTP methods from exported Postman collections
"""

import json
import os
import csv
from pathlib import Path
from collections import defaultdict, Counter

class PostmanEndpointExtractor:
    def __init__(self, collections_dir):
        self.collections_dir = Path(collections_dir)
        self.endpoints = []
        self.http_methods = Counter()
        self.api_categories = defaultdict(list)
        
    def extract_from_item(self, item, collection_name, folder_path=""):
        """Recursively extract endpoints from Postman items"""
        if 'request' in item:
            # This is a request item
            request = item['request']
            if isinstance(request, dict) and 'method' in request:
                method = request['method']
                url = self.parse_url(request.get('url', ''))
                
                endpoint = {
                    'collection': collection_name,
                    'folder': folder_path,
                    'name': item.get('name', 'Unnamed'),
                    'method': method,
                    'url': url,
                    'description': item.get('description', ''),
                    'headers': self.extract_headers(request),
                    'body': self.extract_body(request),
                    'auth': self.extract_auth(request)
                }
                
                self.endpoints.append(endpoint)
                self.http_methods[method] += 1
                
                # Categorize by URL pattern
                category = self.categorize_endpoint(url, method)
                self.api_categories[category].append(endpoint)
        
        # Process sub-items (folders)
        if 'item' in item:
            current_path = f"{folder_path}/{item.get('name', '')}" if folder_path else item.get('name', '')
            for sub_item in item['item']:
                self.extract_from_item(sub_item, collection_name, current_path)
    
    def parse_url(self, url_obj):
        """Parse Postman URL object to string"""
        if isinstance(url_obj, str):
            return url_obj
        elif isinstance(url_obj, dict):
            if 'raw' in url_obj:
                return url_obj['raw']
            elif 'host' in url_obj and 'path' in url_obj:
                host = '.'.join(url_obj['host']) if isinstance(url_obj['host'], list) else str(url_obj['host'])
                path = '/'.join(url_obj['path']) if isinstance(url_obj['path'], list) else str(url_obj['path'])
                protocol = url_obj.get('protocol', 'https')
                return f"{protocol}://{host}/{path}"
        return ""
    
    def extract_headers(self, request):
        """Extract headers from request"""
        headers = {}
        if 'header' in request:
            for header in request['header']:
                if isinstance(header, dict):
                    headers[header.get('key', '')] = header.get('value', '')
        return headers
    
    def extract_body(self, request):
        """Extract body information from request"""
        if 'body' in request:
            body = request['body']
            if isinstance(body, dict):
                return {
                    'mode': body.get('mode', ''),
                    'raw': body.get('raw', ''),
                    'formdata': body.get('formdata', [])
                }
        return {}
    
    def extract_auth(self, request):
        """Extract authentication information"""
        if 'auth' in request:
            auth = request['auth']
            if isinstance(auth, dict):
                return {
                    'type': auth.get('type', ''),
                    'details': auth
                }
        return {}
    
    def categorize_endpoint(self, url, method):
        """Categorize endpoint by URL pattern and method"""
        url_lower = url.lower()
        
        # Configuration endpoints
        if any(word in url_lower for word in ['config', 'template', 'setting']):
            return f"Configuration Management ({method})"
        
        # Device endpoints
        elif any(word in url_lower for word in ['device', 'switch', 'ap', 'appliance']):
            return f"Device Management ({method})"
        
        # Monitoring endpoints
        elif any(word in url_lower for word in ['monitor', 'stats', 'metric', 'health']):
            return f"Monitoring & Analytics ({method})"
        
        # Security endpoints
        elif any(word in url_lower for word in ['security', 'auth', 'user', 'role', 'policy']):
            return f"Security & Access ({method})"
        
        # Network endpoints
        elif any(word in url_lower for word in ['vlan', 'interface', 'port', 'network']):
            return f"Network Configuration ({method})"
        
        # Alert endpoints
        elif any(word in url_lower for word in ['alert', 'notification', 'event']):
            return f"Alerts & Events ({method})"
        
        # Firmware endpoints
        elif any(word in url_lower for word in ['firmware', 'upgrade', 'update']):
            return f"Firmware Management ({method})"
        
        # Backup endpoints
        elif any(word in url_lower for word in ['backup', 'restore', 'archive']):
            return f"Backup & Restore ({method})"
        
        else:
            return f"Other ({method})"
    
    def extract_all_collections(self):
        """Extract endpoints from all JSON files in collections directory"""
        json_files = list(self.collections_dir.glob("*.json"))
        
        if not json_files:
            print(f"No JSON files found in {self.collections_dir}")
            print("Please export your Postman collections as JSON files to this directory:")
            print(f"  {self.collections_dir}")
            print("\nTo export from Postman:")
            print("1. Click the three dots next to collection name")
            print("2. Select 'Export'")
            print("3. Choose 'Collection v2.1 (Recommended)'")
            print("4. Save to the exported-collections directory")
            return
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    collection_data = json.load(f)
                
                collection_name = collection_data.get('info', {}).get('name', json_file.stem)
                print(f"Processing collection: {collection_name}")
                
                if 'item' in collection_data:
                    for item in collection_data['item']:
                        self.extract_from_item(item, collection_name)
                        
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
    
    def generate_analysis_report(self, output_dir):
        """Generate comprehensive analysis report"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # 1. Complete endpoints JSON
        with open(output_dir / 'all_endpoints_complete.json', 'w') as f:
            json.dump(self.endpoints, f, indent=2)
        
        # 2. HTTP methods summary CSV
        with open(output_dir / 'http_methods_summary.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['HTTP Method', 'Count', 'Percentage'])
            total = sum(self.http_methods.values())
            for method, count in self.http_methods.most_common():
                percentage = (count / total) * 100 if total > 0 else 0
                writer.writerow([method, count, f"{percentage:.1f}%"])
        
        # 3. API categories JSON
        with open(output_dir / 'api_categories.json', 'w') as f:
            json.dump(dict(self.api_categories), f, indent=2)
        
        # 4. Collections summary CSV
        with open(output_dir / 'collections_summary.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Collection', 'Total Endpoints', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
            
            collection_stats = defaultdict(lambda: defaultdict(int))
            for endpoint in self.endpoints:
                collection_stats[endpoint['collection']]['total'] += 1
                collection_stats[endpoint['collection']][endpoint['method']] += 1
            
            for collection, stats in collection_stats.items():
                writer.writerow([
                    collection,
                    stats['total'],
                    stats.get('GET', 0),
                    stats.get('POST', 0),
                    stats.get('PUT', 0),
                    stats.get('PATCH', 0),
                    stats.get('DELETE', 0)
                ])
        
        # 5. n8n workflow patterns
        self.generate_n8n_patterns(output_dir)
        
        print(f"\nAnalysis complete! Generated {len(self.endpoints)} endpoints")
        print(f"Results saved to: {output_dir}")
    
    def generate_n8n_patterns(self, output_dir):
        """Generate n8n workflow pattern recommendations"""
        patterns = []
        
        # Monitoring workflows (GET endpoints)
        get_endpoints = [e for e in self.endpoints if e['method'] == 'GET']
        if get_endpoints:
            patterns.append({
                'name': 'Device Health Monitoring',
                'description': 'Scheduled workflow to monitor device health',
                'endpoints': [e['url'] for e in get_endpoints if 'health' in e['url'].lower() or 'monitor' in e['url'].lower()][:5],
                'trigger': 'Schedule (every 5 minutes)',
                'actions': ['Get device metrics', 'Check thresholds', 'Send alerts']
            })
        
        # Configuration workflows (POST/PUT endpoints)
        config_endpoints = [e for e in self.endpoints if e['method'] in ['POST', 'PUT'] and 'config' in e['url'].lower()]
        if config_endpoints:
            patterns.append({
                'name': 'Configuration Management',
                'description': 'Webhook-triggered configuration updates',
                'endpoints': [e['url'] for e in config_endpoints][:5],
                'trigger': 'Webhook',
                'actions': ['Validate config', 'Backup current', 'Apply changes', 'Verify success']
            })
        
        # Device management workflows
        device_endpoints = [e for e in self.endpoints if 'device' in e['url'].lower()]
        if device_endpoints:
            patterns.append({
                'name': 'Device Lifecycle Management',
                'description': 'Complete device provisioning and management',
                'endpoints': [e['url'] for e in device_endpoints][:5],
                'trigger': 'Manual or Webhook',
                'actions': ['Provision device', 'Configure settings', 'Monitor status', 'Decommission']
            })
        
        with open(output_dir / 'n8n_workflow_patterns.json', 'w') as f:
            json.dump(patterns, f, indent=2)

def main():
    """Main execution function"""
    base_dir = Path("/Users/jeangiet/Documents/Claude/aruba-workflows")
    collections_dir = base_dir / "exported-collections"
    output_dir = base_dir / "analysis-results"
    
    # Create directories if they don't exist
    collections_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    print("HPE Aruba Postman Collection Endpoint Extractor")
    print("=" * 50)
    
    extractor = PostmanEndpointExtractor(collections_dir)
    extractor.extract_all_collections()
    
    if extractor.endpoints:
        extractor.generate_analysis_report(output_dir)
        
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(f"Total endpoints extracted: {len(extractor.endpoints)}")
        print(f"HTTP method breakdown:")
        for method, count in extractor.http_methods.most_common():
            print(f"  {method}: {count}")
        
        print(f"\nAPI categories identified: {len(extractor.api_categories)}")
        for category in sorted(extractor.api_categories.keys()):
            print(f"  {category}: {len(extractor.api_categories[category])} endpoints")
        
        print(f"\nResults saved to: {output_dir}")
        
        # Generate quick start guide
        print("\n" + "=" * 50)
        print("NEXT STEPS FOR N8N WORKFLOWS")
        print("=" * 50)
        print("1. Review the generated analysis files")
        print("2. Check n8n_workflow_patterns.json for ready-to-use workflow ideas")
        print("3. Use the endpoint data to build HTTP Request nodes in n8n")
        print("4. Start with monitoring workflows using GET endpoints")
        print("5. Add configuration automation using POST/PUT endpoints")
        
    else:
        print("No endpoints found. Please export your Postman collections:")
        print(f"1. Export collections as JSON files to: {collections_dir}")
        print("2. Run this script again")
        print("\nCollections to export:")
        print("- AP provisioning")
        print("- Aruba Central AOS 10") 
        print("- Device-Onboarding-GLP")
        print("- Device-Onboarding")
        print("- EC Orchestrator")
        print("- HPE Aruba Networking")
        print("- New HPE Aruba Networking")

if __name__ == "__main__":
    main()
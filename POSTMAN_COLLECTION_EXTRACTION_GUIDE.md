# Complete HPE Aruba Postman Collection Extraction Guide

This guide provides multiple methods to extract ALL HTTP endpoints (GET, POST, PUT, PATCH, DELETE) from your HPE Aruba Postman collections for n8n workflow development.

## Collections to Extract

Based on your workspace screenshot, we need to extract:

1. **AP provisioning**
2. **Aruba Central AOS 10**
3. **Device-Onboarding-GLP**
4. **Device-Onboarding**
5. **EC Orchestrator**
6. **HPE Aruba Networking**
7. **New HPE Aruba Networking**

---

## Method 1: Manual Export from Postman (Immediate)

### Step 1: Export Collections
1. Open Postman application
2. For each collection:
   - Click the **three dots** next to collection name
   - Select **Export**
   - Choose **Collection v2.1 (Recommended)**
   - Save to `/Users/jeangiet/Documents/Claude/aruba-workflows/exported-collections/`

### Step 2: Run Extraction Script
```bash
cd /Users/jeangiet/Documents/Claude/aruba-workflows
python3 extract_all_endpoints.py
```

### Step 3: Review Results
- Complete endpoint mapping in `all_endpoints_analysis.json`
- HTTP method breakdown in `http_methods_summary.csv`
- n8n workflow recommendations in `n8n_workflow_patterns.md`

---

## Method 2: Postman API Access (Automated)

### Step 1: Get Postman API Key
1. Go to https://web.postman.co/settings/me/api-keys
2. Generate new API key
3. Copy the key

### Step 2: Configure Environment
```bash
export POSTMAN_API_KEY="your-api-key-here"
export WORKSPACE_ID="your-workspace-id"
```

### Step 3: Run Automated Extraction
```bash
cd /Users/jeangiet/Documents/Claude/aruba-workflows
node extract_via_api.js
```

---

## Method 3: Using postman-mcp Server (When Available)

Once your postman-mcp server is configured:

### Step 1: Test MCP Connection
```javascript
// Test if postman-mcp functions are available
await list_collections();
await get_collection({collection_id: "your-collection-id"});
```

### Step 2: Extract All Collections
```javascript
// Use MCP functions to extract all endpoints
const collections = await list_collections();
for (const collection of collections) {
  const data = await get_collection({collection_id: collection.id});
  // Process endpoints
}
```

---

## Extraction Scripts

### Complete Endpoint Extraction Script

```python
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
        
        print(f"Analysis complete! Generated {len(self.endpoints)} endpoints")
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
    collections_dir = "/Users/jeangiet/Documents/Claude/aruba-workflows/exported-collections"
    output_dir = "/Users/jeangiet/Documents/Claude/aruba-workflows/analysis-results"
    
    # Create directories if they don't exist
    Path(collections_dir).mkdir(exist_ok=True)
    Path(output_dir).mkdir(exist_ok=True)
    
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
    else:
        print("No endpoints found. Make sure you have exported Postman collections as JSON files")
        print(f"Place collection JSON files in: {collections_dir}")

if __name__ == "__main__":
    main()
```

### Save the Script
```bash
# Save the script
cat > /Users/jeangiet/Documents/Claude/aruba-workflows/extract_all_endpoints.py << 'EOF'
[Script content above]
EOF

# Make it executable
chmod +x /Users/jeangiet/Documents/Claude/aruba-workflows/extract_all_endpoints.py
```

---

## Expected Results

After running the extraction, you'll have:

### 1. Complete Endpoint Database
- `all_endpoints_complete.json` - Every endpoint with full details
- `http_methods_summary.csv` - Breakdown by HTTP method
- `collections_summary.csv` - Per-collection statistics

### 2. API Categorization
- Device Management (GET/POST/PUT/DELETE)
- Configuration Management (GET/POST/PUT/PATCH)
- Monitoring & Analytics (GET)
- Security & Access (GET/POST/PUT/DELETE)
- Network Configuration (GET/POST/PUT/DELETE)
- Alerts & Events (GET/POST)
- Firmware Management (GET/POST)
- Backup & Restore (GET/POST)

### 3. n8n Workflow Templates
Ready-to-use workflow patterns for:
- Device health monitoring
- Configuration management
- Alert processing
- Bulk operations
- Compliance checking

---

## Next Steps

1. **Export your 7 collections** from Postman as JSON
2. **Run the extraction script** to get complete endpoint mapping
3. **Review the analysis** to understand available operations
4. **Start building n8n workflows** using the documented endpoints

This comprehensive approach ensures you have complete coverage of all HTTP methods across all your HPE Aruba collections for building robust n8n automation workflows.
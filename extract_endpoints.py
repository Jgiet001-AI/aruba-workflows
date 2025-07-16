#!/usr/bin/env python3
import json
import re
from collections import defaultdict

def extract_requests(items, prefix=''):
    requests = []
    for item in items:
        if 'item' in item:
            # This is a folder, recurse
            folder_name = item.get('name', 'unnamed')
            requests.extend(extract_requests(item['item'], f'{prefix}{folder_name}/'))
        elif 'request' in item:
            # This is a request
            request = item['request']
            if isinstance(request, dict):
                method = request.get('method', 'UNKNOWN')
                name = item.get('name', 'unnamed')
                url = ''
                path = ''
                
                if 'url' in request:
                    if isinstance(request['url'], str):
                        url = request['url']
                        path = url.replace('{{base_url}}', '').split('?')[0]
                    elif isinstance(request['url'], dict):
                        if 'raw' in request['url']:
                            url = request['url']['raw']
                            path = url.replace('{{base_url}}', '').split('?')[0]
                        elif 'path' in request['url']:
                            # Handle path as array
                            if isinstance(request['url']['path'], list):
                                path = '/' + '/'.join(request['url']['path'])
                            else:
                                path = str(request['url']['path'])
                
                requests.append({
                    'folder': prefix.rstrip('/'),
                    'name': name,
                    'method': method,
                    'url': url,
                    'path': path,
                    'clean_path': re.sub(r':[^/]+', '{id}', path)  # Replace :param with {id}
                })
    return requests

def main():
    # Read the large collection file
    with open('/Users/jeangiet/Documents/GL-Ultimate/HPE Aruba Networking Central (Classic Central).postman_collection.json', 'r') as f:
        data = json.load(f)

    # Extract all requests
    all_requests = extract_requests(data.get('item', []))

    # Group by method and folder
    method_groups = defaultdict(list)
    folder_groups = defaultdict(list)

    for req in all_requests:
        method_groups[req['method']].append(req)
        folder_groups[req['folder']].append(req)

    # Create comprehensive endpoint mapping
    endpoint_mapping = {
        'collection_name': data.get('info', {}).get('name', 'Unknown Collection'),
        'total_requests': len(all_requests),
        'summary': {
            'GET': len(method_groups['GET']),
            'POST': len(method_groups['POST']),
            'PUT': len(method_groups['PUT']),
            'PATCH': len(method_groups['PATCH']),
            'DELETE': len(method_groups['DELETE'])
        },
        'endpoints_by_method': {},
        'endpoints_by_category': {},
        'unique_base_paths': set(),
        'api_categories': list(folder_groups.keys())
    }

    # Organize by method
    for method in sorted(method_groups.keys()):
        endpoint_mapping['endpoints_by_method'][method] = []
        for req in method_groups[method]:
            endpoint_info = {
                'name': req['name'],
                'path': req['path'],
                'clean_path': req['clean_path'],
                'category': req['folder'],
                'full_url': req['url']
            }
            endpoint_mapping['endpoints_by_method'][method].append(endpoint_info)
            
            # Collect base paths
            base_path = req['path'].split('/')[1] if req['path'].startswith('/') else req['path'].split('/')[0]
            endpoint_mapping['unique_base_paths'].add(base_path)

    # Convert set to list for JSON serialization
    endpoint_mapping['unique_base_paths'] = sorted(list(endpoint_mapping['unique_base_paths']))

    # Organize by category
    for folder in sorted(folder_groups.keys()):
        if folder:  # Skip empty folder names
            endpoint_mapping['endpoints_by_category'][folder] = {}
            folder_requests = folder_groups[folder]
            
            # Group by method within each category
            for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                method_requests = [r for r in folder_requests if r['method'] == method]
                if method_requests:
                    endpoint_mapping['endpoints_by_category'][folder][method] = []
                    for req in method_requests:
                        endpoint_mapping['endpoints_by_category'][folder][method].append({
                            'name': req['name'],
                            'path': req['path'],
                            'clean_path': req['clean_path']
                        })

    # Save the comprehensive mapping
    with open('/Users/jeangiet/Documents/Claude/aruba-workflows/aruba_central_complete_endpoint_mapping.json', 'w') as f:
        json.dump(endpoint_mapping, f, indent=2)

    print('✅ Created comprehensive endpoint mapping!')
    print(f'Total Requests: {endpoint_mapping["total_requests"]}')
    print(f'API Categories: {len(endpoint_mapping["api_categories"])}')
    print(f'Unique Base Paths: {len(endpoint_mapping["unique_base_paths"])}')
    print()
    print('Method Summary:')
    for method, count in endpoint_mapping['summary'].items():
        print(f'  {method}: {count} endpoints')
    print()
    print('Top 10 API Categories:')
    for i, category in enumerate(sorted(endpoint_mapping['api_categories'])[:10]):
        if category:
            total_in_category = len(folder_groups[category])
            print(f'  {i+1:2d}. {category}: {total_in_category} endpoints')
    print()
    print('Base API Paths:')
    for path in endpoint_mapping['unique_base_paths'][:20]:
        if path and path != '':
            print(f'  /{path}')

    # Create a summary for n8n workflow building
    print()
    print('=' * 80)
    print('N8N WORKFLOW BUILDING SUMMARY')
    print('=' * 80)
    
    # Group the most common patterns
    common_patterns = {
        'Device Management': ['monitoring', 'device', 'inventory', 'firmware'],
        'Configuration': ['configuration', 'template', 'wlan', 'group'],
        'Authentication': ['auth', 'oauth', 'token', 'login'],
        'Analytics & Reports': ['analytics', 'reports', 'audit', 'aiops'],
        'Network Operations': ['ap', 'switch', 'gateway', 'client']
    }
    
    print()
    print('Key Workflow Categories for n8n:')
    for category, keywords in common_patterns.items():
        matching_folders = [f for f in endpoint_mapping['api_categories'] 
                          if any(kw in f.lower() for kw in keywords)]
        if matching_folders:
            print(f'\n{category}:')
            for folder in matching_folders[:5]:  # Show top 5
                if folder:
                    count = len(folder_groups[folder])
                    print(f'  - {folder}: {count} endpoints')

if __name__ == '__main__':
    main()
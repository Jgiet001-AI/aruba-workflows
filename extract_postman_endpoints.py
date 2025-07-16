#!/usr/bin/env python3
"""
Postman Collection API Endpoint Extractor

This script extracts all API endpoints with their HTTP methods from Postman collections
and organizes them by collection for easy analysis.

Usage:
    python extract_postman_endpoints.py

Features:
- Searches for all Postman collection files in your Documents directory
- Extracts endpoints with HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Groups endpoints by collection
- Provides detailed analysis of each collection's API coverage
- Outputs results in multiple formats: JSON, CSV, and markdown
"""

import json
import os
import glob
import csv
from pathlib import Path
from typing import Dict, List, Set, Any
from urllib.parse import urlparse

class PostmanEndpointExtractor:
    def __init__(self):
        self.collections = {}
        self.all_endpoints = []
        
    def find_collection_files(self, search_path: str = None) -> List[str]:
        """Find all Postman collection files."""
        if search_path is None:
            search_path = str(Path.home() / "Documents")
        
        patterns = [
            "**/*.postman_collection.json",
            "**/*collection*.json"
        ]
        
        collection_files = []
        for pattern in patterns:
            files = glob.glob(os.path.join(search_path, pattern), recursive=True)
            collection_files.extend(files)
        
        # Remove duplicates and filter for actual Postman collections
        unique_files = list(set(collection_files))
        postman_files = []
        
        for file_path in unique_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Check if it's a valid Postman collection
                    if 'info' in data and 'item' in data:
                        postman_files.append(file_path)
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
                continue
                
        return postman_files
    
    def extract_endpoints_from_item(self, item: Dict[str, Any], collection_name: str) -> List[Dict[str, Any]]:
        """Recursively extract endpoints from collection items."""
        endpoints = []
        
        if 'request' in item:
            # This is a request item
            request = item['request']
            if isinstance(request, dict) and 'url' in request and 'method' in request:
                endpoint_info = self.parse_request(request, item.get('name', 'Unnamed'), collection_name)
                if endpoint_info:
                    endpoints.append(endpoint_info)
        
        # Check for nested items (folders)
        if 'item' in item:
            for sub_item in item['item']:
                endpoints.extend(self.extract_endpoints_from_item(sub_item, collection_name))
                
        return endpoints
    
    def parse_request(self, request: Dict[str, Any], request_name: str, collection_name: str) -> Dict[str, Any]:
        """Parse a single request to extract endpoint information."""
        try:
            method = request.get('method', 'GET').upper()
            url_info = request.get('url', {})
            
            # Handle different URL formats
            if isinstance(url_info, str):
                raw_url = url_info
                path_parts = []
            else:
                raw_url = url_info.get('raw', '')
                path_parts = url_info.get('path', [])
            
            # Clean URL and extract path
            clean_url = self.clean_url(raw_url)
            path = self.extract_path(raw_url, path_parts)
            
            # Extract query parameters
            query_params = []
            if isinstance(url_info, dict) and 'query' in url_info:
                for param in url_info['query']:
                    if isinstance(param, dict):
                        query_params.append({
                            'key': param.get('key', ''),
                            'value': param.get('value', ''),
                            'description': param.get('description', '')
                        })
            
            # Extract headers
            headers = []
            if 'header' in request:
                for header in request['header']:
                    if isinstance(header, dict):
                        headers.append({
                            'key': header.get('key', ''),
                            'value': header.get('value', ''),
                            'description': header.get('description', '')
                        })
            
            # Extract body information
            body_info = {}
            if 'body' in request:
                body = request['body']
                if isinstance(body, dict):
                    body_info = {
                        'mode': body.get('mode', ''),
                        'raw': body.get('raw', '') if body.get('mode') == 'raw' else '',
                        'form_data': body.get('formdata', []) if body.get('mode') == 'formdata' else []
                    }
            
            return {
                'collection': collection_name,
                'request_name': request_name,
                'method': method,
                'path': path,
                'raw_url': raw_url,
                'clean_url': clean_url,
                'query_params': query_params,
                'headers': headers,
                'body': body_info,
                'auth': request.get('auth', {})
            }
            
        except Exception as e:
            print(f"Error parsing request '{request_name}': {e}")
            return None
    
    def clean_url(self, raw_url: str) -> str:
        """Clean URL by removing variables and protocols."""
        if not raw_url:
            return ""
        
        # Remove common Postman variables
        clean = raw_url
        variables = ['{{base_url}}', '{{baseUrl}}', '{{url}}', '{{host}}']
        for var in variables:
            clean = clean.replace(var, '')
        
        # Remove protocol if present
        if clean.startswith(('http://', 'https://')):
            try:
                parsed = urlparse(clean)
                clean = parsed.path
                if parsed.query:
                    clean += f"?{parsed.query}"
            except:
                pass
        
        return clean.strip('/')
    
    def extract_path(self, raw_url: str, path_parts: List[str]) -> str:
        """Extract API path from URL."""
        if path_parts:
            return '/' + '/'.join(str(part) for part in path_parts)
        
        # Fallback to parsing raw URL
        clean_url = self.clean_url(raw_url)
        if '?' in clean_url:
            clean_url = clean_url.split('?')[0]
        
        if clean_url and not clean_url.startswith('/'):
            clean_url = '/' + clean_url
            
        return clean_url
    
    def process_collection(self, file_path: str) -> Dict[str, Any]:
        """Process a single Postman collection file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                collection_data = json.load(f)
            
            collection_name = collection_data.get('info', {}).get('name', os.path.basename(file_path))
            collection_info = {
                'name': collection_name,
                'file_path': file_path,
                'description': collection_data.get('info', {}).get('description', ''),
                'endpoints': []
            }
            
            # Extract endpoints from all items
            for item in collection_data.get('item', []):
                endpoints = self.extract_endpoints_from_item(item, collection_name)
                collection_info['endpoints'].extend(endpoints)
                self.all_endpoints.extend(endpoints)
            
            return collection_info
            
        except Exception as e:
            print(f"Error processing collection {file_path}: {e}")
            return None
    
    def analyze_collections(self) -> Dict[str, Any]:
        """Analyze all processed collections."""
        analysis = {
            'total_collections': len(self.collections),
            'total_endpoints': len(self.all_endpoints),
            'methods_summary': {},
            'collections_summary': [],
            'unique_paths': set(),
            'aruba_apis': []
        }
        
        # Count methods
        for endpoint in self.all_endpoints:
            method = endpoint['method']
            analysis['methods_summary'][method] = analysis['methods_summary'].get(method, 0) + 1
            analysis['unique_paths'].add(endpoint['path'])
        
        # Analyze each collection
        for collection_name, collection_info in self.collections.items():
            endpoints = collection_info['endpoints']
            methods = {}
            for endpoint in endpoints:
                method = endpoint['method']
                methods[method] = methods.get(method, 0) + 1
            
            summary = {
                'name': collection_name,
                'endpoint_count': len(endpoints),
                'methods': methods,
                'file_path': collection_info['file_path']
            }
            analysis['collections_summary'].append(summary)
            
            # Identify Aruba-related APIs
            if any(keyword in collection_name.lower() for keyword in ['aruba', 'central', 'aos', 'edgeconnect']):
                analysis['aruba_apis'].append({
                    'collection': collection_name,
                    'endpoints': len(endpoints),
                    'methods': methods
                })
        
        analysis['unique_paths'] = list(analysis['unique_paths'])
        return analysis
    
    def save_results(self, output_dir: str = None):
        """Save extraction results in multiple formats."""
        if output_dir is None:
            output_dir = "/Users/jeangiet/Documents/Claude/aruba-workflows"
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save detailed JSON
        detailed_data = {
            'collections': self.collections,
            'analysis': self.analyze_collections()
        }
        
        with open(os.path.join(output_dir, 'postman_collections_detailed.json'), 'w') as f:
            json.dump(detailed_data, f, indent=2, default=str)
        
        # Save endpoints CSV
        csv_file = os.path.join(output_dir, 'postman_endpoints.csv')
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if self.all_endpoints:
                writer = csv.DictWriter(f, fieldnames=[
                    'collection', 'request_name', 'method', 'path', 'raw_url'
                ])
                writer.writeheader()
                for endpoint in self.all_endpoints:
                    writer.writerow({
                        'collection': endpoint['collection'],
                        'request_name': endpoint['request_name'],
                        'method': endpoint['method'],
                        'path': endpoint['path'],
                        'raw_url': endpoint['raw_url']
                    })
        
        # Save markdown summary
        self.save_markdown_summary(output_dir)
        
        print(f"Results saved to {output_dir}")
        print(f"- Detailed JSON: postman_collections_detailed.json")
        print(f"- Endpoints CSV: postman_endpoints.csv")
        print(f"- Summary: postman_summary.md")
    
    def save_markdown_summary(self, output_dir: str):
        """Save a markdown summary of the analysis."""
        analysis = self.analyze_collections()
        
        md_content = f"""# Postman Collections Analysis Summary

## Overview
- **Total Collections**: {analysis['total_collections']}
- **Total API Endpoints**: {analysis['total_endpoints']}
- **Unique Paths**: {len(analysis['unique_paths'])}

## HTTP Methods Distribution
"""
        
        for method, count in sorted(analysis['methods_summary'].items()):
            md_content += f"- **{method}**: {count} endpoints\n"
        
        md_content += "\n## Collections Summary\n\n"
        
        for collection in analysis['collections_summary']:
            md_content += f"### {collection['name']}\n"
            md_content += f"- **Endpoints**: {collection['endpoint_count']}\n"
            md_content += f"- **File**: `{collection['file_path']}`\n"
            md_content += "- **Methods**:\n"
            for method, count in collection['methods'].items():
                md_content += f"  - {method}: {count}\n"
            md_content += "\n"
        
        if analysis['aruba_apis']:
            md_content += "## Aruba-Related APIs\n\n"
            for api in analysis['aruba_apis']:
                md_content += f"### {api['collection']}\n"
                md_content += f"- **Endpoints**: {api['endpoints']}\n"
                md_content += "- **Methods**:\n"
                for method, count in api['methods'].items():
                    md_content += f"  - {method}: {count}\n"
                md_content += "\n"
        
        md_content += "## All Unique API Paths\n\n"
        for path in sorted(analysis['unique_paths']):
            if path:  # Skip empty paths
                md_content += f"- `{path}`\n"
        
        with open(os.path.join(output_dir, 'postman_summary.md'), 'w') as f:
            f.write(md_content)
    
    def run_extraction(self, search_path: str = None):
        """Run the complete extraction process."""
        print("🔍 Searching for Postman collection files...")
        collection_files = self.find_collection_files(search_path)
        
        if not collection_files:
            print("❌ No Postman collection files found.")
            return
        
        print(f"📁 Found {len(collection_files)} collection file(s):")
        for file_path in collection_files:
            print(f"  - {file_path}")
        
        print("\n⚙️ Processing collections...")
        for file_path in collection_files:
            collection_info = self.process_collection(file_path)
            if collection_info:
                self.collections[collection_info['name']] = collection_info
                print(f"  ✅ Processed: {collection_info['name']} ({len(collection_info['endpoints'])} endpoints)")
            else:
                print(f"  ❌ Failed to process: {file_path}")
        
        if self.collections:
            print(f"\n📊 Analysis complete:")
            analysis = self.analyze_collections()
            print(f"  - Total collections: {analysis['total_collections']}")
            print(f"  - Total endpoints: {analysis['total_endpoints']}")
            print(f"  - HTTP methods: {', '.join(analysis['methods_summary'].keys())}")
            
            print("\n💾 Saving results...")
            self.save_results()
            print("✅ Extraction complete!")
        else:
            print("❌ No valid collections were processed.")

def main():
    """Main execution function."""
    print("🚀 Postman Collection API Endpoint Extractor")
    print("=" * 50)
    
    extractor = PostmanEndpointExtractor()
    extractor.run_extraction()

if __name__ == "__main__":
    main()
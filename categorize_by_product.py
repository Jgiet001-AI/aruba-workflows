#!/usr/bin/env python3
"""
Categorize HPE Aruba endpoints by product type for targeted n8n workflows
"""

import json
import re
from pathlib import Path
from collections import defaultdict

class ArubaProductCategorizer:
    def __init__(self, endpoints_file):
        self.endpoints_file = Path(endpoints_file)
        self.endpoints = []
        self.product_categories = defaultdict(list)
        self.load_endpoints()
        
    def load_endpoints(self):
        """Load endpoints from JSON file"""
        with open(self.endpoints_file, 'r') as f:
            self.endpoints = json.load(f)
        print(f"📋 Loaded {len(self.endpoints)} endpoints for categorization")
    
    def categorize_by_product(self):
        """Categorize endpoints by HPE Aruba product type"""
        for endpoint in self.endpoints:
            url = endpoint.get('url', '').lower()
            name = endpoint.get('name', '').lower()
            description = endpoint.get('description', '').lower()
            folder = endpoint.get('folder', '').lower()
            
            # Combined text for analysis
            combined_text = f"{url} {name} {description} {folder}"
            
            # Determine product category
            category = self.determine_product_category(combined_text, endpoint)
            self.product_categories[category].append(endpoint)
    
    def determine_product_category(self, text, endpoint):
        """Determine which Aruba product this endpoint belongs to"""
        
        # AOS-CX (Switches)
        if any(keyword in text for keyword in [
            'aos-cx', 'aoscx', 'switch', 'vlan', 'interface', 'port', 'stp', 'lacp',
            'ospf', 'bgp', 'acl', 'qos', 'lldp', 'mac-table', 'arp', 'routing',
            'trunk', 'access', 'spanning-tree', 'layer2', 'layer3', 'fabric'
        ]):
            return "AOS-CX Switches"
        
        # Access Points (APs)
        elif any(keyword in text for keyword in [
            'access-point', 'access_point', 'ap_', 'ap-', 'wireless', 'wifi', 'ssid',
            'radio', 'antenna', 'channel', 'mesh', 'beacon', 'wlan', 'airtime',
            'client', 'station', 'roaming', 'band', '2.4ghz', '5ghz', '6ghz',
            'provisioning', 'rf', 'spectrum'
        ]):
            return "Access Points (APs)"
        
        # EdgeConnect (SD-WAN)
        elif any(keyword in text for keyword in [
            'edgeconnect', 'edge-connect', 'sd-wan', 'sdwan', 'wan', 'orchestrator',
            'appliance', 'tunnel', 'overlay', 'underlay', 'mpls', 'internet',
            'path', 'sla', 'policy', 'traffic-steering', 'boost', 'silver-peak'
        ]):
            return "EdgeConnect (SD-WAN)"
        
        # UXI (User Experience Insight)
        elif any(keyword in text for keyword in [
            'uxi', 'user-experience', 'insight', 'sensor', 'test', 'synthetic',
            'probe', 'measurement', 'latency', 'jitter', 'packet-loss', 'throughput',
            'connectivity', 'network-test', 'application-test', 'web-test'
        ]):
            return "UXI (User Experience)"
        
        # ClearPass (NAC)
        elif any(keyword in text for keyword in [
            'clearpass', 'clear-pass', 'nac', 'radius', 'authentication', 'authorization',
            'guest', 'onboard', 'device-fingerprint', 'posture', 'compliance',
            'certificate', 'identity', 'access-control', '802.1x'
        ]):
            return "ClearPass (NAC)"
        
        # Central (Management Platform)
        elif any(keyword in text for keyword in [
            'central', 'aruba-central', 'cloud', 'management', 'dashboard', 'portal',
            'tenant', 'organization', 'site', 'group', 'template', 'firmware',
            'upgrade', 'monitoring', 'alert', 'notification', 'report', 'analytics'
        ]):
            return "Aruba Central (Platform)"
        
        # AirWave (Legacy Management)
        elif any(keyword in text for keyword in [
            'airwave', 'air-wave', 'amp', 'legacy-management', 'snmp', 'trap'
        ]):
            return "AirWave (Legacy)"
        
        # Mobility Conductor/Controllers
        elif any(keyword in text for keyword in [
            'conductor', 'controller', 'mobility', 'mc', 'mm', 'mobility-master',
            'md', 'mobility-controller', 'cluster', 'redundancy', 'master'
        ]):
            return "Mobility Controllers"
        
        # Security & Compliance
        elif any(keyword in text for keyword in [
            'security', 'threat', 'intrusion', 'firewall', 'vpn', 'encryption',
            'compliance', 'audit', 'vulnerability', 'malware', 'policy-enforcement'
        ]):
            return "Security & Compliance"
        
        # Network Analytics & AI
        elif any(keyword in text for keyword in [
            'ai', 'artificial-intelligence', 'machine-learning', 'ml', 'analytics',
            'insight', 'recommendation', 'anomaly', 'prediction', 'optimization',
            'netinsight', 'aiops'
        ]):
            return "Network Analytics & AI"
        
        # Location Services
        elif any(keyword in text for keyword in [
            'location', 'positioning', 'wayfinding', 'proximity', 'beacon',
            'ble', 'bluetooth', 'rtls', 'geofence', 'asset-tracking'
        ]):
            return "Location Services"
        
        # Cloud Services & APIs
        elif any(keyword in text for keyword in [
            'oauth', 'token', 'api-key', 'authentication', 'authorization',
            'webhook', 'callback', 'subscription', 'event', 'integration'
        ]):
            return "Cloud Services & APIs"
        
        # Device Onboarding & Provisioning
        elif any(keyword in text for keyword in [
            'onboard', 'provision', 'zero-touch', 'ztp', 'activation', 'enrollment',
            'bootstrap', 'deployment', 'staging', 'inventory'
        ]):
            return "Device Onboarding"
        
        # Monitoring & Troubleshooting
        elif any(keyword in text for keyword in [
            'monitoring', 'health', 'status', 'diagnostic', 'troubleshoot',
            'debug', 'log', 'trace', 'packet-capture', 'syslog', 'snmp'
        ]):
            return "Monitoring & Diagnostics"
        
        # Network Services (DHCP, DNS, etc.)
        elif any(keyword in text for keyword in [
            'dhcp', 'dns', 'ntp', 'syslog', 'tftp', 'ftp', 'http', 'https',
            'proxy', 'load-balancer', 'service'
        ]):
            return "Network Services"
        
        # Default fallback based on HTTP method and URL patterns
        else:
            # Try to categorize by URL structure
            if '/device' in text or '/switch' in text:
                return "AOS-CX Switches"
            elif '/ap' in text or '/access' in text:
                return "Access Points (APs)"
            elif '/edge' in text or '/wan' in text:
                return "EdgeConnect (SD-WAN)"
            elif '/uxi' in text or '/sensor' in text:
                return "UXI (User Experience)"
            elif '/central' in text or '/cloud' in text:
                return "Aruba Central (Platform)"
            else:
                return "General/Uncategorized"
    
    def analyze_configuration_endpoints(self):
        """Analyze configuration-specific endpoints by product"""
        config_categories = defaultdict(lambda: defaultdict(list))
        
        for category, endpoints in self.product_categories.items():
            for endpoint in endpoints:
                method = endpoint.get('method', '')
                url = endpoint.get('url', '').lower()
                name = endpoint.get('name', '').lower()
                
                # Configuration-related keywords
                if any(keyword in f"{url} {name}" for keyword in [
                    'config', 'template', 'setting', 'policy', 'rule', 'profile',
                    'parameter', 'option', 'preference', 'setup', 'configure'
                ]):
                    config_categories[category][method].append(endpoint)
        
        return config_categories
    
    def generate_product_summary(self, output_dir):
        """Generate comprehensive product categorization summary"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # 1. Complete product categorization
        with open(output_dir / 'endpoints_by_product.json', 'w') as f:
            json.dump(dict(self.product_categories), f, indent=2)
        
        # 2. Configuration-specific endpoints
        config_endpoints = self.analyze_configuration_endpoints()
        with open(output_dir / 'configuration_endpoints_by_product.json', 'w') as f:
            json.dump(dict(config_endpoints), f, indent=2)
        
        # 3. Product summary statistics
        summary_stats = {}
        for category, endpoints in self.product_categories.items():
            method_count = defaultdict(int)
            for endpoint in endpoints:
                method_count[endpoint.get('method', 'UNKNOWN')] += 1
            
            summary_stats[category] = {
                'total_endpoints': len(endpoints),
                'methods': dict(method_count),
                'configuration_endpoints': len([
                    e for e in endpoints 
                    if any(keyword in f"{e.get('url', '')} {e.get('name', '')}".lower() 
                          for keyword in ['config', 'template', 'setting', 'policy'])
                ])
            }
        
        with open(output_dir / 'product_summary_statistics.json', 'w') as f:
            json.dump(summary_stats, f, indent=2)
        
        # 4. Generate n8n workflow recommendations by product
        self.generate_workflow_recommendations(output_dir, config_endpoints)
        
        print(f"📊 Product categorization complete! Results saved to: {output_dir}")
    
    def generate_workflow_recommendations(self, output_dir, config_endpoints):
        """Generate n8n workflow recommendations for each product category"""
        recommendations = {}
        
        for category, methods in config_endpoints.items():
            total_config_endpoints = sum(len(endpoints) for endpoints in methods.values())
            
            if total_config_endpoints > 0:
                recommendations[category] = {
                    'workflow_name': f"{category.replace(' ', '_').lower()}_configuration_management",
                    'description': f"Configuration management workflow for {category}",
                    'total_config_endpoints': total_config_endpoints,
                    'available_operations': {
                        'GET': len(methods.get('GET', [])),
                        'POST': len(methods.get('POST', [])),
                        'PUT': len(methods.get('PUT', [])),
                        'PATCH': len(methods.get('PATCH', [])),
                        'DELETE': len(methods.get('DELETE', []))
                    },
                    'workflow_capabilities': self.get_workflow_capabilities(category, methods),
                    'sample_endpoints': self.get_sample_endpoints(methods),
                    'priority': self.calculate_priority(category, total_config_endpoints)
                }
        
        with open(output_dir / 'n8n_workflow_recommendations.json', 'w') as f:
            json.dump(recommendations, f, indent=2)
    
    def get_workflow_capabilities(self, category, methods):
        """Determine workflow capabilities based on available endpoints"""
        capabilities = []
        
        if methods.get('GET'):
            capabilities.append("Configuration Retrieval")
            capabilities.append("Status Monitoring")
        
        if methods.get('POST'):
            capabilities.append("Configuration Deployment")
            capabilities.append("Template Application")
        
        if methods.get('PUT'):
            capabilities.append("Configuration Updates")
            capabilities.append("Policy Changes")
        
        if methods.get('PATCH'):
            capabilities.append("Incremental Updates")
        
        if methods.get('DELETE'):
            capabilities.append("Configuration Cleanup")
            capabilities.append("Policy Removal")
        
        return capabilities
    
    def get_sample_endpoints(self, methods):
        """Get sample endpoints for each HTTP method"""
        samples = {}
        for method, endpoints in methods.items():
            if endpoints:
                samples[method] = [
                    {
                        'name': ep.get('name', 'Unnamed'),
                        'url': ep.get('url', ''),
                        'description': ep.get('description', '')
                    }
                    for ep in endpoints[:3]  # Top 3 examples
                ]
        return samples
    
    def calculate_priority(self, category, endpoint_count):
        """Calculate workflow priority based on product importance and endpoint count"""
        # High priority categories
        if any(keyword in category.lower() for keyword in ['aos-cx', 'access points', 'central']):
            if endpoint_count >= 10:
                return "HIGH"
            else:
                return "MEDIUM"
        
        # Medium priority categories
        elif any(keyword in category.lower() for keyword in ['edgeconnect', 'uxi', 'security']):
            if endpoint_count >= 5:
                return "MEDIUM"
            else:
                return "LOW"
        
        # Lower priority categories
        else:
            return "LOW" if endpoint_count >= 3 else "VERY_LOW"
    
    def print_categorization_summary(self):
        """Print categorization summary to console"""
        print("\n" + "="*80)
        print("📋 HPE ARUBA PRODUCT CATEGORIZATION SUMMARY")
        print("="*80)
        
        # Sort categories by endpoint count
        sorted_categories = sorted(
            self.product_categories.items(), 
            key=lambda x: len(x[1]), 
            reverse=True
        )
        
        total_endpoints = sum(len(endpoints) for endpoints in self.product_categories.values())
        
        for category, endpoints in sorted_categories:
            percentage = (len(endpoints) / total_endpoints) * 100
            
            # Count configuration endpoints
            config_count = len([
                e for e in endpoints 
                if any(keyword in f"{e.get('url', '')} {e.get('name', '')}".lower() 
                      for keyword in ['config', 'template', 'setting', 'policy'])
            ])
            
            # Count methods
            method_count = defaultdict(int)
            for endpoint in endpoints:
                method_count[endpoint.get('method', 'UNKNOWN')] += 1
            
            print(f"\n🎯 {category}")
            print(f"   Total Endpoints: {len(endpoints)} ({percentage:.1f}%)")
            print(f"   Configuration Endpoints: {config_count}")
            print(f"   HTTP Methods: {dict(method_count)}")
            
            # Show priority for configuration workflows
            if config_count > 0:
                priority = self.calculate_priority(category, config_count)
                print(f"   n8n Workflow Priority: {priority}")

def main():
    """Main execution function"""
    endpoints_file = "/Users/jeangiet/Documents/Claude/aruba-workflows/postman-api-results/all_aruba_endpoints.json"
    output_dir = "/Users/jeangiet/Documents/Claude/aruba-workflows/product-categorization"
    
    print("🚀 HPE Aruba Product Categorization for Configuration Management")
    print("="*70)
    
    categorizer = ArubaProductCategorizer(endpoints_file)
    categorizer.categorize_by_product()
    categorizer.generate_product_summary(output_dir)
    categorizer.print_categorization_summary()
    
    print(f"\n✅ Categorization complete! Check {output_dir} for detailed results")
    print("\n🔧 Ready to build product-specific configuration management workflows!")

if __name__ == "__main__":
    main()
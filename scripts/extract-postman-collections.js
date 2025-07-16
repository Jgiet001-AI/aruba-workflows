#!/usr/bin/env node
/**
 * Script to extract all Postman collections via Postman API
 * Usage: POSTMAN_API_KEY=your_key node extract-postman-collections.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const POSTMAN_API_KEY = process.env.POSTMAN_API_KEY;
const OUTPUT_DIR = '/Users/jeangiet/Documents/Claude/aruba-workflows/collections';

if (!POSTMAN_API_KEY) {
  console.error('Please set POSTMAN_API_KEY environment variable');
  process.exit(1);
}

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

function makeAPIRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.getpostman.com',
      path: path,
      method: 'GET',
      headers: {
        'X-API-Key': POSTMAN_API_KEY,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function extractAllCollections() {
  console.log('Fetching all collections...');
  
  try {
    // Get all collections
    const collectionsResponse = await makeAPIRequest('/collections');
    const collections = collectionsResponse.collections;

    console.log(`Found ${collections.length} collections`);

    // Filter for HPE Aruba collections
    const arubaCollections = collections.filter(collection => 
      collection.name.toLowerCase().includes('aruba') ||
      collection.name.toLowerCase().includes('hpe') ||
      collection.name.toLowerCase().includes('ap provisioning') ||
      collection.name.toLowerCase().includes('device-onboarding') ||
      collection.name.toLowerCase().includes('ec orchestrator')
    );

    console.log(`Found ${arubaCollections.length} Aruba-related collections:`);
    arubaCollections.forEach(c => console.log(`  - ${c.name}`));

    // Extract detailed information for each collection
    for (const collection of arubaCollections) {
      console.log(`\nExtracting details for: ${collection.name}`);
      
      try {
        const detailResponse = await makeAPIRequest(`/collections/${collection.uid}`);
        const collectionData = detailResponse.collection;

        // Save the collection
        const filename = `${collection.name.replace(/[^a-zA-Z0-9]/g, '_')}.json`;
        const filepath = path.join(OUTPUT_DIR, filename);
        fs.writeFileSync(filepath, JSON.stringify(collectionData, null, 2));
        
        console.log(`  Saved to: ${filepath}`);
        
        // Extract API mapping
        const apiMapping = extractAPIMapping(collectionData);
        const mappingFilename = `${collection.name.replace(/[^a-zA-Z0-9]/g, '_')}_mapping.json`;
        const mappingFilepath = path.join(OUTPUT_DIR, mappingFilename);
        fs.writeFileSync(mappingFilepath, JSON.stringify(apiMapping, null, 2));
        
        console.log(`  API mapping saved to: ${mappingFilepath}`);
        
      } catch (error) {
        console.error(`  Error extracting ${collection.name}:`, error.message);
      }
    }

    // Create comprehensive mapping
    console.log('\nCreating comprehensive API mapping...');
    const comprehensiveMapping = createComprehensiveMapping(OUTPUT_DIR);
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'comprehensive_aruba_api_mapping.json'),
      JSON.stringify(comprehensiveMapping, null, 2)
    );

  } catch (error) {
    console.error('Error:', error);
  }
}

function extractAPIMapping(collection) {
  const mapping = {
    name: collection.info.name,
    description: collection.info.description || '',
    endpoints: []
  };

  function processItem(item, folder = '') {
    if (item.item) {
      // This is a folder
      const folderName = folder ? `${folder}/${item.name}` : item.name;
      item.item.forEach(subItem => processItem(subItem, folderName));
    } else if (item.request) {
      // This is a request
      const endpoint = {
        name: item.name,
        method: item.request.method,
        url: item.request.url,
        folder: folder,
        description: item.request.description || '',
        headers: item.request.header || [],
        params: [],
        body: item.request.body || null
      };

      // Extract URL parameters
      if (item.request.url && item.request.url.variable) {
        endpoint.params = item.request.url.variable;
      }

      // Extract query parameters
      if (item.request.url && item.request.url.query) {
        endpoint.queryParams = item.request.url.query;
      }

      mapping.endpoints.push(endpoint);
    }
  }

  if (collection.item) {
    collection.item.forEach(item => processItem(item));
  }

  return mapping;
}

function createComprehensiveMapping(outputDir) {
  const files = fs.readdirSync(outputDir).filter(f => f.endsWith('_mapping.json'));
  const comprehensive = {
    generatedAt: new Date().toISOString(),
    totalCollections: files.length,
    collections: {},
    endpointsByMethod: {
      GET: [],
      POST: [],
      PUT: [],
      PATCH: [],
      DELETE: []
    },
    endpointsByCategory: {}
  };

  files.forEach(file => {
    const mapping = JSON.parse(fs.readFileSync(path.join(outputDir, file), 'utf8'));
    comprehensive.collections[mapping.name] = mapping;

    // Categorize endpoints
    mapping.endpoints.forEach(endpoint => {
      // By HTTP method
      if (comprehensive.endpointsByMethod[endpoint.method]) {
        comprehensive.endpointsByMethod[endpoint.method].push({
          collection: mapping.name,
          name: endpoint.name,
          url: endpoint.url,
          folder: endpoint.folder
        });
      }

      // By category (based on folder/endpoint name)
      const category = categorizeEndpoint(endpoint);
      if (!comprehensive.endpointsByCategory[category]) {
        comprehensive.endpointsByCategory[category] = [];
      }
      comprehensive.endpointsByCategory[category].push({
        collection: mapping.name,
        method: endpoint.method,
        name: endpoint.name,
        url: endpoint.url
      });
    });
  });

  return comprehensive;
}

function categorizeEndpoint(endpoint) {
  const name = endpoint.name.toLowerCase();
  const folder = (endpoint.folder || '').toLowerCase();
  const url = endpoint.url ? endpoint.url.toString().toLowerCase() : '';

  if (name.includes('device') || folder.includes('device') || url.includes('device')) {
    return 'Device Management';
  } else if (name.includes('config') || folder.includes('config') || url.includes('config')) {
    return 'Configuration';
  } else if (name.includes('monitor') || folder.includes('monitor') || url.includes('stats') || url.includes('health')) {
    return 'Monitoring';
  } else if (name.includes('auth') || folder.includes('auth') || url.includes('auth') || url.includes('login')) {
    return 'Authentication';
  } else if (name.includes('alert') || folder.includes('alert') || url.includes('alert')) {
    return 'Alerting';
  } else if (name.includes('vlan') || folder.includes('vlan') || url.includes('vlan')) {
    return 'Network Configuration';
  } else if (name.includes('user') || folder.includes('user') || url.includes('user')) {
    return 'User Management';
  } else if (name.includes('firmware') || folder.includes('firmware') || url.includes('firmware')) {
    return 'Firmware Management';
  } else if (name.includes('template') || folder.includes('template') || url.includes('template')) {
    return 'Templates';
  } else {
    return 'Other';
  }
}

// Run the extraction
extractAllCollections().catch(console.error);
"""
Netlify serverless function for template downloads.
Provides API endpoint for accessing scraped templates.
"""

import json
import os
from typing import Dict, Any


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Netlify function handler for template downloads.
    
    GET /api/templates - List all templates
    GET /api/templates?source=n8n - Filter by source
    GET /api/templates?limit=5 - Limit results
    """
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS request for CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Only allow GET requests
    if event.get('httpMethod') != 'GET':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse query parameters
        params = event.get('queryStringParameters') or {}
        source_filter = params.get('source', '').lower()
        limit = int(params.get('limit', 100))
        
        # Load templates data
        templates = load_templates()
        
        # Apply filters
        if source_filter:
            templates = [t for t in templates if t.get('source', '').lower() == source_filter]
        
        # Apply limit
        templates = templates[:limit]
        
        response_data = {
            'count': len(templates),
            'templates': templates,
            'sources': list(set(t.get('source', 'unknown') for t in templates))
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }


def load_templates() -> list:
    """Load templates from data files."""
    templates = []
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Try to load n8n templates
    try:
        n8n_path = os.path.join(data_dir, 'n8n_templates.json')
        if os.path.exists(n8n_path):
            with open(n8n_path, 'r') as f:
                data = json.load(f)
                templates.extend(data.get('templates', []))
    except Exception:
        pass
    
    # Try to load Zapier templates
    try:
        zapier_path = os.path.join(data_dir, 'zapier_templates.json')
        if os.path.exists(zapier_path):
            with open(zapier_path, 'r') as f:
                data = json.load(f)
                templates.extend(data.get('templates', []))
    except Exception:
        pass
    
    # If no templates found, return sample data
    if not templates:
        templates = [
            {
                'title': 'Sample Template',
                'description': 'This is a sample template',
                'source': 'n8n',
                'url': 'https://example.com'
            }
        ]
    
    return templates

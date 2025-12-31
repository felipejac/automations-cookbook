#!/usr/bin/env python3
"""
Master N8N Template Scraper - Build World's Biggest n8n Template Database

Scrapes n8n templates from multiple sources:
- Official n8n API
- GitHub repositories
- npm packages  
- Community integrations
"""

import requests
import json
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class N8NMasterScraper:
    def __init__(self):
        self.templates = {}
        self.sources_data = []
        
    def scrape_official_api(self):
        """Scrape from n8n official API"""
        logger.info("Scraping n8n official API...")
        try:
            response = requests.get('https://api.n8n.io/api/v1/templates', timeout=10)
            if response.status_code == 200:
                data = response.json()
                for template in data.get('data', []):
                    self.templates[template.get('id')] = {
                        'name': template.get('name'),
                        'description': template.get('description'),
                        'source': 'official',
                        'difficulty': template.get('difficulty')
                    }
                logger.info(f"Found {len(data.get('data', []))} official templates")
        except Exception as e:
            logger.error(f"Error: {e}")
    
    def scrape_github(self):
        """Scrape n8n repos from GitHub"""
        logger.info("Scraping GitHub...")
        try:
            headers = {'User-Agent': 'n8n-scraper'}
            params = {'q': 'n8n', 'sort': 'stars', 'per_page': 100}
            response = requests.get('https://api.github.com/search/repositories', params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for repo in data.get('items', []):
                    self.templates[f"gh_{repo['id']}"] = {
                        'name': repo['name'],
                        'description': repo.get('description'),
                        'source': 'github',
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count']
                    }
                logger.info(f"Found {len(data.get('items', []))} GitHub repos")
        except Exception as e:
            logger.error(f"GitHub scrape error: {e}")
    
    def scrape_npm(self):
        """Scrape n8n packages from npm"""
        logger.info("Scraping npm...")
        try:
            params = {'q': 'n8n', 'size': 200}
            response = requests.get('https://registry.npmjs.org/-/v1/search', params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for pkg in data.get('objects', []):
                    p = pkg['package']
                    self.templates[f"npm_{p['name']}"] = {
                        'name': p['name'],
                        'description': p.get('description'),
                        'source': 'npm',
                        'downloads': p.get('downloads')
                    }
                logger.info(f"Found {len(data.get('objects', []))} npm packages")
        except Exception as e:
            logger.error(f"NPM scrape error: {e}")
    
    def save_database(self):
        """Save all templates to database"""
        Path('data').mkdir(exist_ok=True)
        output = Path('data/n8n_templates_master.json')
        
        with open(output, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total': len(self.templates),
                'templates': self.templates
            }, f, indent=2)
        
        logger.info(f"Saved {len(self.templates)} templates to {output}")
    
    def run(self):
        """Execute full scraping workflow"""
        logger.info("=" * 60)
        logger.info("MASTER N8N TEMPLATE SCRAPER - WORLD'S BIGGEST DATABASE")
        logger.info("=" * 60)
        
        self.scrape_official_api()
        self.scrape_github()
        self.scrape_npm()
        self.save_database()
        
        logger.info(f"\nCOMPLETE: {len(self.templates)} total templates collected")
        logger.info("=" * 60)
        return self.templates

if __name__ == '__main__':
    scraper = N8NMasterScraper()
    templates = scraper.run()
    print(f"\nSUCCESS: {len(templates)} n8n templates scraped and saved!")

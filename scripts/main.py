#!/usr/bin/env python3
"""Automations Cookbook - N8N Integration Scraper & Tutorial Generator"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

class N8NIntegrationScraper:
    """Scrape n8n integration docs and generate tutorials"""
    
    def __init__(self):
        self.base_url = "https://docs.n8n.io"
        self.output_dir = Path("../data/integrations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def scrape_integrations(self):
        """Scrape available integrations from n8n docs"""
        try:
            # Fetch integration list from n8n
            response = requests.get(f"{self.base_url}/api/integrations")
            if response.status_code == 200:
                integrations = response.json()
                self.save_integrations(integrations)
                return integrations
        except Exception as e:
            print(f"Error scraping: {e}")
            return []
    
    def generate_tutorial(self, integration_name: str, source: str, target: str):
        """Generate tutorial content for an integration"""
        tutorial = {
            "title": f"How to integrate {source} with {target} using n8n",
            "generated_at": datetime.now().isoformat(),
            "sections": {
                "setup": self._generate_setup_section(source),
                "workflow": self._generate_workflow_section(source, target),
                "testing": self._generate_testing_section(),
                "troubleshooting": self._generate_troubleshooting_section()
            },
            "template": self._generate_json_template(source, target)
        }
        return tutorial
    
    def _generate_setup_section(self, service: str) -> dict:
        return {
            "title": f"Setting up {service}",
            "steps": [
                f"Create {service} account",
                f"Get {service} API credentials",
                f"Configure {service} connection in n8n"
            ]
        }
    
    def _generate_workflow_section(self, source: str, target: str) -> dict:
        return {
            "title": f"Creating {source} to {target} workflow",
            "steps": [
                f"Add {source} trigger node",
                f"Configure data mapping",
                f"Add {target} action node",
                f"Test workflow execution"
            ]
        }
    
    def _generate_testing_section(self) -> dict:
        return {
            "title": "Testing your integration",
            "steps": [
                "Execute workflow with test data",
                "Verify target system received data",
                "Check error logs if needed"
            ]
        }
    
    def _generate_troubleshooting_section(self) -> dict:
        return {
            "title": "Common issues and solutions",
            "issues": [
                "Authentication failures",
                "Data mapping errors",
                "Rate limiting",
                "Timeout issues"
            ]
        }
    
    def _generate_json_template(self, source: str, target: str) -> dict:
        return {
            "name": f"{source} -> {target}",
            "nodes": [
                {
                    "parameters": {},
                    "name": f"{source} Trigger",
                    "type": f"n8n-nodes-base.{source.lower()}",
                    "typeVersion": 1,
                    "position": [250, 300]
                },
                {
                    "parameters": {},
                    "name": f"{target} Action",
                    "type": f"n8n-nodes-base.{target.lower()}",
                    "typeVersion": 1,
                    "position": [500, 300]
                }
            ],
            "connections": {
                f"{source} Trigger": {
                    "main": [
                        [{"node": f"{target} Action", "branch": 0, "index": 0}]
                    ]
                }
            }
        }
    
    def save_integrations(self, integrations: list):
        """Save integrations data to JSON"""
        output_file = self.output_dir / "integrations.json"
        with open(output_file, 'w') as f:
            json.dump(integrations, f, indent=2)
        print(f"Saved {len(integrations)} integrations")

if __name__ == "__main__":
    scraper = N8NIntegrationScraper()
    # scraper.scrape_integrations()  # Enable when API available
    
    # Generate sample tutorials
    sample_integrations = [
        ("dropbox", "Dropbox", "HubSpot"),
        ("slack", "Slack", "Google Sheets"),
        ("stripe", "Stripe", "Shopify")
    ]
    
    for name, source, target in sample_integrations:
        tutorial = scraper.generate_tutorial(name, source, target)
        output_file = scraper.output_dir / f"{name}_tutorial.json"
        with open(output_file, 'w') as f:
            json.dump(tutorial, f, indent=2)
        print(f"Generated tutorial for {source} -> {target}")

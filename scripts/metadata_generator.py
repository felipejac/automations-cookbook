"""
YAML metadata generator for SEO optimization.
Generates SEO-friendly frontmatter for tutorials and templates.
"""

import yaml
from typing import Dict, List, Optional
from datetime import datetime
import os
import re

from .logger import get_logger
from .config import Config

logger = get_logger(__name__)


class MetadataGeneratorError(Exception):
    """Custom exception for metadata generation errors."""
    pass


class MetadataGenerator:
    """Generate YAML frontmatter metadata for SEO optimization."""
    
    def __init__(self):
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    def generate_metadata(self, tutorial: Dict) -> Dict:
        """
        Generate SEO metadata for a tutorial.
        
        Args:
            tutorial: Tutorial dictionary
            
        Returns:
            Metadata dictionary
        """
        try:
            title = tutorial.get('title', 'Untitled')
            source = tutorial.get('source', 'unknown')
            content = tutorial.get('content', '')
            
            logger.info(f"Generating metadata for: {title}")
            
            metadata = {
                'title': title,
                'description': self._generate_description(tutorial),
                'keywords': self._extract_keywords(tutorial),
                'author': 'Automations Cookbook',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'category': self._determine_category(source),
                'tags': self._generate_tags(tutorial),
                'source': source,
                'url': tutorial.get('template_url', ''),
                'seo': {
                    'og_title': title,
                    'og_description': self._generate_description(tutorial),
                    'og_type': 'article',
                    'twitter_card': 'summary_large_image'
                }
            }
            
            logger.info(f"Successfully generated metadata for: {title}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error generating metadata: {e}")
            raise MetadataGeneratorError(f"Metadata generation failed: {e}")
    
    def generate_batch_metadata(self, tutorials: List[Dict]) -> List[Dict]:
        """
        Generate metadata for multiple tutorials.
        
        Args:
            tutorials: List of tutorial dictionaries
            
        Returns:
            List of metadata dictionaries
        """
        logger.info(f"Generating metadata for {len(tutorials)} tutorials")
        metadata_list = []
        
        for idx, tutorial in enumerate(tutorials):
            try:
                metadata = self.generate_metadata(tutorial)
                metadata_list.append(metadata)
                logger.info(f"Generated metadata {idx + 1}/{len(tutorials)}")
            except Exception as e:
                logger.warning(f"Failed to generate metadata {idx + 1}: {e}")
        
        logger.info(f"Successfully generated {len(metadata_list)} metadata entries")
        return metadata_list
    
    def save_metadata_yaml(self, metadata: Dict, filename: str):
        """
        Save metadata as YAML file.
        
        Args:
            metadata: Metadata dictionary
            filename: Output filename
        """
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"Saved metadata to {filepath}")
        except IOError as e:
            logger.error(f"Failed to save metadata: {e}")
            raise MetadataGeneratorError(f"Failed to save metadata: {e}")
    
    def create_frontmatter(self, metadata: Dict, content: str) -> str:
        """
        Create a complete document with YAML frontmatter.
        
        Args:
            metadata: Metadata dictionary
            content: Document content
            
        Returns:
            Complete document with frontmatter
        """
        yaml_frontmatter = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)
        return f"---\n{yaml_frontmatter}---\n\n{content}"
    
    def _generate_description(self, tutorial: Dict) -> str:
        """Generate SEO description from tutorial."""
        description = tutorial.get('description', '')
        if description:
            # Truncate to ~160 characters for SEO
            if len(description) > 160:
                description = description[:157] + '...'
            return description
        
        # Extract from content if no description
        content = tutorial.get('content', '')
        if content:
            # Get first paragraph
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            if paragraphs:
                first_para = paragraphs[0]
                if len(first_para) > 160:
                    first_para = first_para[:157] + '...'
                return first_para
        
        return f"Learn how to set up and use {tutorial.get('title', 'this automation')}"
    
    def _extract_keywords(self, tutorial: Dict) -> List[str]:
        """Extract relevant keywords from tutorial."""
        keywords = set()
        
        # Add source as keyword
        source = tutorial.get('source', '')
        if source:
            keywords.add(source.lower())
        
        # Add common automation keywords
        keywords.update(['automation', 'workflow', 'integration'])
        
        # Extract from title
        title = tutorial.get('title', '')
        if title:
            # Split title and add meaningful words
            words = re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())
            keywords.update(words[:5])  # Limit to 5 words from title
        
        return sorted(list(keywords))[:10]  # Return top 10 keywords
    
    def _generate_tags(self, tutorial: Dict) -> List[str]:
        """Generate tags for tutorial."""
        tags = set()
        
        source = tutorial.get('source', '')
        if source:
            tags.add(source)
        
        # Add tags based on title keywords
        title = tutorial.get('title', '').lower()
        
        # Common integration tags
        integrations = ['slack', 'email', 'gmail', 'github', 'trello', 'asana', 
                       'salesforce', 'hubspot', 'mailchimp', 'dropbox', 'google']
        for integration in integrations:
            if integration in title:
                tags.add(integration)
        
        # Common action tags
        actions = ['notification', 'sync', 'backup', 'reminder', 'analytics']
        for action in actions:
            if action in title:
                tags.add(action)
        
        return sorted(list(tags))
    
    def _determine_category(self, source: str) -> str:
        """Determine category based on source."""
        category_map = {
            'n8n': 'n8n Workflows',
            'zapier': 'Zapier Integrations',
            'make': 'Make Scenarios',
            'integromat': 'Make Scenarios'
        }
        return category_map.get(source.lower(), 'Automation')


if __name__ == "__main__":
    # Example usage
    generator = MetadataGenerator()
    
    sample_tutorial = {
        'title': 'Slack to Email Notification',
        'description': 'Send email notifications when messages are posted in Slack',
        'source': 'zapier',
        'template_url': 'https://zapier.com/apps/slack/integrations/email',
        'content': 'This tutorial shows you how to set up automated email notifications...'
    }
    
    metadata = generator.generate_metadata(sample_tutorial)
    print(yaml.dump(metadata, default_flow_style=False))

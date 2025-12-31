"""
LLM-based tutorial generator using OpenAI API.
Generates tutorials from template data.
"""

import openai
from typing import Dict, List, Optional
import json
import os

from .logger import get_logger
from .config import Config

logger = get_logger(__name__)


class TutorialGeneratorError(Exception):
    """Custom exception for tutorial generation errors."""
    pass


class TutorialGenerator:
    """Generate tutorials using OpenAI's LLM."""
    
    def __init__(self):
        """Initialize the tutorial generator with OpenAI API key."""
        if not Config.OPENAI_API_KEY:
            logger.warning("OpenAI API key not set. Tutorial generation will fail.")
        else:
            openai.api_key = Config.OPENAI_API_KEY
        
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    def generate_tutorial(self, template: Dict) -> Optional[Dict]:
        """
        Generate a tutorial for a given template.
        
        Args:
            template: Template dictionary containing title, description, etc.
            
        Returns:
            Tutorial dictionary with sections and content
        """
        try:
            title = template.get('title', 'Untitled')
            description = template.get('description', '')
            source = template.get('source', 'unknown')
            
            logger.info(f"Generating tutorial for: {title}")
            
            prompt = self._create_prompt(template)
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical writer creating clear, concise tutorials for automation workflows."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=Config.LLM_MAX_TOKENS,
                temperature=Config.LLM_TEMPERATURE
            )
            
            tutorial_content = response.choices[0].message.content
            
            tutorial = {
                'title': title,
                'source': source,
                'template_url': template.get('url', ''),
                'content': tutorial_content,
                'sections': self._parse_sections(tutorial_content)
            }
            
            logger.info(f"Successfully generated tutorial for: {title}")
            return tutorial
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise TutorialGeneratorError(f"Failed to generate tutorial: {e}")
        except Exception as e:
            logger.error(f"Error generating tutorial: {e}")
            raise TutorialGeneratorError(f"Tutorial generation failed: {e}")
    
    def generate_batch_tutorials(self, templates: List[Dict]) -> List[Dict]:
        """
        Generate tutorials for multiple templates.
        
        Args:
            templates: List of template dictionaries
            
        Returns:
            List of tutorial dictionaries
        """
        logger.info(f"Generating tutorials for {len(templates)} templates")
        tutorials = []
        
        for idx, template in enumerate(templates):
            try:
                tutorial = self.generate_tutorial(template)
                if tutorial:
                    tutorials.append(tutorial)
                    logger.info(f"Generated tutorial {idx + 1}/{len(templates)}")
            except Exception as e:
                logger.warning(f"Failed to generate tutorial {idx + 1}: {e}")
        
        # Save results
        self._save_tutorials(tutorials)
        
        logger.info(f"Successfully generated {len(tutorials)} tutorials")
        return tutorials
    
    def _create_prompt(self, template: Dict) -> str:
        """Create a prompt for the LLM based on template data."""
        title = template.get('title', 'Untitled')
        description = template.get('description', 'No description available')
        source = template.get('source', 'unknown')
        
        prompt = f"""Create a comprehensive tutorial for the following {source} automation template:

Title: {title}
Description: {description}

Please structure the tutorial with the following sections:
1. Overview - Brief introduction to what this automation does
2. Prerequisites - What users need before setting up
3. Setup Steps - Step-by-step instructions
4. Configuration - How to configure the automation
5. Testing - How to test the automation
6. Troubleshooting - Common issues and solutions
7. Best Practices - Tips for optimization

Keep the tutorial clear, concise, and beginner-friendly."""
        
        return prompt
    
    def _parse_sections(self, content: str) -> List[Dict]:
        """
        Parse tutorial content into sections.
        
        Args:
            content: Tutorial content as string
            
        Returns:
            List of section dictionaries
        """
        sections = []
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            # Check if line is a section header (starts with number or ##)
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '##')):
                # Save previous section
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content).strip()
                    })
                # Start new section
                current_section = line.strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content).strip()
            })
        
        return sections
    
    def _save_tutorials(self, tutorials: List[Dict]):
        """Save generated tutorials to file."""
        filepath = os.path.join(Config.OUTPUT_DIR, 'generated_tutorials.json')
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'count': len(tutorials),
                    'tutorials': tutorials
                }, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(tutorials)} tutorials to {filepath}")
        except IOError as e:
            logger.error(f"Failed to save tutorials: {e}")
            raise TutorialGeneratorError(f"Failed to save tutorials: {e}")


if __name__ == "__main__":
    # Example usage
    generator = TutorialGenerator()
    
    # Sample template
    sample_template = {
        'title': 'Email to Slack Notification',
        'description': 'Automatically send Slack notifications when receiving important emails',
        'source': 'zapier',
        'url': 'https://zapier.com/apps/email/integrations/slack'
    }
    
    try:
        tutorial = generator.generate_tutorial(sample_template)
        print(f"Generated tutorial: {tutorial['title']}")
    except Exception as e:
        print(f"Error: {e}")

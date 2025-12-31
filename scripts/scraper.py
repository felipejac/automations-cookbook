"""
Web scraper for n8n and Zapier templates.
Includes error handling, logging, and rate limiting.
"""

import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from ratelimit import limits, sleep_and_retry
import json
import os

from .logger import get_logger
from .config import Config

logger = get_logger(__name__)


class TemplateScraperError(Exception):
    """Custom exception for scraper errors."""
    pass


class TemplateScraper:
    """Base class for template scraping with rate limiting and error handling."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': Config.USER_AGENT
        })
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(Config.CACHE_DIR, exist_ok=True)
    
    @sleep_and_retry
    @limits(calls=Config.RATE_LIMIT_CALLS, period=Config.RATE_LIMIT_PERIOD)
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """
        Make a rate-limited HTTP request with retry logic.
        
        Args:
            url: URL to request
            
        Returns:
            Response object or None on failure
        """
        for attempt in range(Config.RETRY_ATTEMPTS):
            try:
                logger.info(f"Requesting {url} (attempt {attempt + 1}/{Config.RETRY_ATTEMPTS})")
                response = self.session.get(url, timeout=Config.REQUEST_TIMEOUT)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < Config.RETRY_ATTEMPTS - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {Config.RETRY_ATTEMPTS} attempts")
                    return None
        return None
    
    def _parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content with BeautifulSoup."""
        return BeautifulSoup(html, 'lxml')
    
    def save_to_file(self, data: Dict, filename: str):
        """Save scraped data to JSON file."""
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved data to {filepath}")
        except IOError as e:
            logger.error(f"Failed to save data to {filepath}: {e}")
            raise TemplateScraperError(f"Failed to save data: {e}")


class N8nTemplateScraper(TemplateScraper):
    """Scraper for n8n workflow templates."""
    
    BASE_URL = "https://n8n.io/workflows"
    
    def scrape_templates(self, limit: int = 10) -> List[Dict]:
        """
        Scrape n8n templates from the official website.
        
        Args:
            limit: Maximum number of templates to scrape
            
        Returns:
            List of template dictionaries
        """
        logger.info(f"Starting n8n template scraping (limit: {limit})")
        templates = []
        
        try:
            response = self._make_request(self.BASE_URL)
            if not response:
                raise TemplateScraperError("Failed to fetch n8n templates page")
            
            soup = self._parse_html(response.text)
            
            # NOTE: The CSS selectors below are placeholders and need to be updated
            # based on the actual HTML structure of n8n.io/workflows
            # Inspect the page source to find the correct selectors
            template_elements = soup.find_all('div', class_='workflow-card', limit=limit)
            
            for idx, element in enumerate(template_elements):
                try:
                    template = self._extract_template_info(element)
                    if template:
                        templates.append(template)
                        logger.info(f"Extracted template {idx + 1}: {template.get('title', 'Untitled')}")
                except Exception as e:
                    logger.warning(f"Failed to extract template {idx + 1}: {e}")
            
            logger.info(f"Successfully scraped {len(templates)} n8n templates")
            
            # Save results
            self.save_to_file({
                'source': 'n8n',
                'count': len(templates),
                'templates': templates
            }, 'n8n_templates.json')
            
        except Exception as e:
            logger.error(f"Error during n8n scraping: {e}")
            raise TemplateScraperError(f"n8n scraping failed: {e}")
        
        return templates
    
    def _extract_template_info(self, element) -> Optional[Dict]:
        """Extract template information from HTML element."""
        try:
            # Placeholder implementation - update selectors based on actual site structure
            title = element.find('h3')
            description = element.find('p')
            link = element.find('a')
            
            return {
                'title': title.text.strip() if title else 'Untitled',
                'description': description.text.strip() if description else '',
                'url': link.get('href', '') if link else '',
                'source': 'n8n'
            }
        except Exception as e:
            logger.warning(f"Failed to parse template element: {e}")
            return None


class ZapierTemplateScraper(TemplateScraper):
    """Scraper for Zapier workflow templates."""
    
    BASE_URL = "https://zapier.com/apps"
    
    def scrape_templates(self, limit: int = 10) -> List[Dict]:
        """
        Scrape Zapier templates (Zaps).
        
        Args:
            limit: Maximum number of templates to scrape
            
        Returns:
            List of template dictionaries
        """
        logger.info(f"Starting Zapier template scraping (limit: {limit})")
        templates = []
        
        try:
            response = self._make_request(self.BASE_URL)
            if not response:
                raise TemplateScraperError("Failed to fetch Zapier templates page")
            
            soup = self._parse_html(response.text)
            
            # NOTE: The CSS selectors below are placeholders and need to be updated
            # based on the actual HTML structure of zapier.com/apps
            # Inspect the page source to find the correct selectors
            template_elements = soup.find_all('div', class_='zap-template', limit=limit)
            
            for idx, element in enumerate(template_elements):
                try:
                    template = self._extract_template_info(element)
                    if template:
                        templates.append(template)
                        logger.info(f"Extracted template {idx + 1}: {template.get('title', 'Untitled')}")
                except Exception as e:
                    logger.warning(f"Failed to extract template {idx + 1}: {e}")
            
            logger.info(f"Successfully scraped {len(templates)} Zapier templates")
            
            # Save results
            self.save_to_file({
                'source': 'zapier',
                'count': len(templates),
                'templates': templates
            }, 'zapier_templates.json')
            
        except Exception as e:
            logger.error(f"Error during Zapier scraping: {e}")
            raise TemplateScraperError(f"Zapier scraping failed: {e}")
        
        return templates
    
    def _extract_template_info(self, element) -> Optional[Dict]:
        """Extract template information from HTML element."""
        try:
            # Placeholder implementation - update selectors based on actual site structure
            title = element.find('h3')
            description = element.find('p')
            link = element.find('a')
            
            return {
                'title': title.text.strip() if title else 'Untitled',
                'description': description.text.strip() if description else '',
                'url': link.get('href', '') if link else '',
                'source': 'zapier'
            }
        except Exception as e:
            logger.warning(f"Failed to parse template element: {e}")
            return None


def scrape_all_templates(n8n_limit: int = 10, zapier_limit: int = 10) -> Dict:
    """
    Scrape templates from both n8n and Zapier.
    
    Args:
        n8n_limit: Number of n8n templates to scrape
        zapier_limit: Number of Zapier templates to scrape
        
    Returns:
        Dictionary with combined results
    """
    logger.info("Starting template scraping for all sources")
    results = {
        'n8n': [],
        'zapier': [],
        'total': 0
    }
    
    try:
        # Scrape n8n templates
        n8n_scraper = N8nTemplateScraper()
        results['n8n'] = n8n_scraper.scrape_templates(limit=n8n_limit)
    except Exception as e:
        logger.error(f"n8n scraping failed: {e}")
    
    try:
        # Scrape Zapier templates
        zapier_scraper = ZapierTemplateScraper()
        results['zapier'] = zapier_scraper.scrape_templates(limit=zapier_limit)
    except Exception as e:
        logger.error(f"Zapier scraping failed: {e}")
    
    results['total'] = len(results['n8n']) + len(results['zapier'])
    logger.info(f"Total templates scraped: {results['total']}")
    
    return results


if __name__ == "__main__":
    # Example usage
    results = scrape_all_templates(n8n_limit=5, zapier_limit=5)
    print(f"Scraped {results['total']} templates in total")

"""
Automation Framework Package
Provides tools for scraping, tutorial generation, and metadata creation.
"""

from .scraper import N8nTemplateScraper, ZapierTemplateScraper, scrape_all_templates
from .tutorial_generator import TutorialGenerator
from .metadata_generator import MetadataGenerator
from .logger import get_logger, setup_logger
from .config import Config

__version__ = '1.0.0'
__all__ = [
    'N8nTemplateScraper',
    'ZapierTemplateScraper',
    'scrape_all_templates',
    'TutorialGenerator',
    'MetadataGenerator',
    'get_logger',
    'setup_logger',
    'Config'
]

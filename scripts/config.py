"""
Configuration management for the automation framework.
Loads environment variables and provides configuration access.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for accessing environment variables."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Rate limiting settings
    RATE_LIMIT_CALLS = int(os.getenv('RATE_LIMIT_CALLS', '10'))
    RATE_LIMIT_PERIOD = int(os.getenv('RATE_LIMIT_PERIOD', '60'))  # seconds
    
    # Scraping settings
    USER_AGENT = os.getenv('USER_AGENT', 'AutomationsCookbook/1.0')
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))  # seconds
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '3'))
    
    # Output directories
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'data')
    CACHE_DIR = os.getenv('CACHE_DIR', 'cache')
    
    # LLM settings
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', '2000'))
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.7'))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required but not set")

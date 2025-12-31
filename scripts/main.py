"""
Main orchestration script for the automation framework.
Coordinates scraping, tutorial generation, and metadata creation.
"""

import argparse
import sys
from typing import Dict

from .scraper import scrape_all_templates
from .tutorial_generator import TutorialGenerator
from .metadata_generator import MetadataGenerator
from .logger import get_logger
from .config import Config

logger = get_logger(__name__)


def run_full_pipeline(n8n_limit: int = 10, zapier_limit: int = 10, generate_tutorials: bool = True):
    """
    Run the complete automation pipeline.
    
    Args:
        n8n_limit: Number of n8n templates to scrape
        zapier_limit: Number of Zapier templates to scrape
        generate_tutorials: Whether to generate tutorials with LLM
    """
    logger.info("=" * 60)
    logger.info("Starting Automation Framework Pipeline")
    logger.info("=" * 60)
    
    results = {
        'scraping': {},
        'tutorials': [],
        'metadata': [],
        'success': False
    }
    
    try:
        # Step 1: Scrape templates
        logger.info("Step 1: Scraping templates from n8n and Zapier")
        scraping_results = scrape_all_templates(n8n_limit=n8n_limit, zapier_limit=zapier_limit)
        results['scraping'] = scraping_results
        
        all_templates = scraping_results['n8n'] + scraping_results['zapier']
        logger.info(f"Total templates scraped: {len(all_templates)}")
        
        if not all_templates:
            logger.warning("No templates were scraped. Pipeline stopping.")
            return results
        
        # Step 2: Generate tutorials (optional)
        if generate_tutorials:
            logger.info("Step 2: Generating tutorials with LLM")
            try:
                Config.validate()  # Check if API key is set
                tutorial_gen = TutorialGenerator()
                tutorials = tutorial_gen.generate_batch_tutorials(all_templates)
                results['tutorials'] = tutorials
                logger.info(f"Generated {len(tutorials)} tutorials")
            except ValueError as e:
                logger.warning(f"Skipping tutorial generation: {e}")
                # Use templates as tutorials without LLM generation
                results['tutorials'] = all_templates
        else:
            logger.info("Skipping tutorial generation (disabled)")
            results['tutorials'] = all_templates
        
        # Step 3: Generate SEO metadata
        logger.info("Step 3: Generating SEO metadata")
        metadata_gen = MetadataGenerator()
        metadata_list = metadata_gen.generate_batch_metadata(results['tutorials'])
        results['metadata'] = metadata_list
        logger.info(f"Generated {len(metadata_list)} metadata entries")
        
        # Save combined metadata
        if metadata_list:
            metadata_gen.save_metadata_yaml(
                {'templates': metadata_list},
                'all_metadata.yaml'
            )
        
        results['success'] = True
        logger.info("Pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        results['success'] = False
    
    logger.info("=" * 60)
    logger.info("Pipeline Summary")
    logger.info("=" * 60)
    logger.info(f"Templates scraped: {results['scraping'].get('total', 0)}")
    logger.info(f"Tutorials generated: {len(results['tutorials'])}")
    logger.info(f"Metadata entries: {len(results['metadata'])}")
    logger.info(f"Status: {'SUCCESS' if results['success'] else 'FAILED'}")
    logger.info("=" * 60)
    
    return results


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description='Automation Framework - Scrape templates and generate content'
    )
    parser.add_argument(
        '--n8n-limit',
        type=int,
        default=10,
        help='Number of n8n templates to scrape (default: 10)'
    )
    parser.add_argument(
        '--zapier-limit',
        type=int,
        default=10,
        help='Number of Zapier templates to scrape (default: 10)'
    )
    parser.add_argument(
        '--no-tutorials',
        action='store_true',
        help='Skip LLM tutorial generation'
    )
    parser.add_argument(
        '--scrape-only',
        action='store_true',
        help='Only run scraping, skip tutorials and metadata'
    )
    
    args = parser.parse_args()
    
    if args.scrape_only:
        logger.info("Running scraper only")
        results = scrape_all_templates(
            n8n_limit=args.n8n_limit,
            zapier_limit=args.zapier_limit
        )
        print(f"Scraped {results['total']} templates")
    else:
        results = run_full_pipeline(
            n8n_limit=args.n8n_limit,
            zapier_limit=args.zapier_limit,
            generate_tutorials=not args.no_tutorials
        )
        
        if results['success']:
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()

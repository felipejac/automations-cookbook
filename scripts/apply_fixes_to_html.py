#!/usr/bin/env python3
"""
Apply Fixes to Integration Pages HTML

Removes:
- Vote button (Votar neste Template)
- Template em Desenvolvimento warning

Updates:
- Ver Todos os Templates button link (if needed)
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLFixer:
    def __init__(self, html_folder='integracoes-paginas'):
        self.html_folder = Path(html_folder)
        self.fixed_count = 0
        self.error_count = 0
        
    def fix_html_content(self, html_content):
        """Fix HTML by removing vote button and template em desenvolvimento"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove vote button (Votar neste Template)
            vote_buttons = soup.find_all('button')
            for button in vote_buttons:
                if button.get_text(strip=True) and 'Votar neste Template' in button.get_text():
                    button.decompose()
                    logger.info(f"  ✓ Removed vote button")
            
            # Remove template em desenvolvimento warning
            warnings = soup.find_all(['div', 'section'])
            for warning in warnings:
                if 'Template em Desenvolvimento' in str(warning):
                    warning.decompose()
                    logger.info(f"  ✓ Removed 'Template em Desenvolvimento' message")
            
            # Also try regex as backup
            html_str = str(soup)
            
            # Remove vote button pattern
            html_str = re.sub(
                r'<button[^>]*>\s*[🗳️◆]*\s*Votar neste Template\s*</button>',
                '',
                html_str,
                flags=re.IGNORECASE | re.DOTALL
            )
            
            # Remove template em desenvolvimento div
            html_str = re.sub(
                r'<div[^>]*>\s*⚠️.*?Template em Desenvolvimento.*?</div>',
                '',
                html_str,
                flags=re.IGNORECASE | re.DOTALL
            )
            
            html_str = re.sub(
                r'<div[^>]*>\s*⚠️.*?Esse template específico.*?</div>',
                '',
                html_str,
                flags=re.IGNORECASE | re.DOTALL
            )
            
            return html_str
            
        except Exception as e:
            logger.error(f"Error fixing HTML: {e}")
            self.error_count += 1
            return html_content
    
    def fix_files(self):
        """Fix all HTML files in the folder"""
        if not self.html_folder.exists():
            logger.warning(f"Folder {self.html_folder} does not exist")
            return
        
        html_files = list(self.html_folder.glob('*.html'))
        
        if not html_files:
            logger.info(f"No HTML files found in {self.html_folder}")
            return
        
        logger.info(f"Found {len(html_files)} HTML files to fix")
        
        for html_file in html_files:
            logger.info(f"\nFixing: {html_file.name}")
            
            try:
                # Read original content
                with open(html_file, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                # Apply fixes
                fixed_content = self.fix_html_content(original_content)
                
                # Write back if changed
                if fixed_content != original_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    self.fixed_count += 1
                    logger.info(f"  ✓ Fixed and saved")
                else:
                    logger.info(f"  ℹ No changes needed")
                    
            except Exception as e:
                logger.error(f"  ✗ Error processing {html_file.name}: {e}")
                self.error_count += 1
    
    def report(self):
        """Print summary report"""
        logger.info(f"\n{'='*60}")
        logger.info(f"HTML FIX SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"✓ Files fixed: {self.fixed_count}")
        logger.info(f"✗ Errors: {self.error_count}")
        logger.info(f"Completed at: {datetime.now().isoformat()}")
        logger.info(f"{'='*60}")

if __name__ == '__main__':
    fixer = HTMLFixer('integracoes-paginas')
    fixer.fix_files()
    fixer.report()

#!/usr/bin/env python3
"""
Fix integration pages by removing vote button and updating status message.
Run this script to process all HTML files in integracoes-paginas folder.
"""

import os
import re
from pathlib import Path

def fix_integration_page(html_content):
    """
    Fix integration page HTML:
    1. Remove the 'Votar neste Template' button
    2. Update 'Template em Desenvolvimento' message to show real status
    """
    
    # Remove the vote button button element
    # Pattern: <button ... onclick="voteTemplate()" ... >...</button>
    html_content = re.sub(
        r'<button[^>]*onclick="voteTemplate\(\)"[^>]*>.*?</button>\s*',
        '',
        html_content,
        flags=re.DOTALL
    )
    
    # Update the "Template em Desenvolvimento" warning message to success
    # Change from warning (yellow) to info (blue) or remove entirely
    html_content = re.sub(
        r'<div[^>]*class="[^"]*warning[^"]*"[^>]*>.*?Template em Desenvolvimento.*?</div>',
        '',
        html_content,
        flags=re.DOTALL
    )
    
    # Remove the alert/warning div completely
    html_content = re.sub(
        r'<div[^>]*class="[^"]*alert[^"]*"[^>]*>.*?</div>',
        '',
        html_content,
        flags=re.DOTALL
    )
    
    return html_content

def process_all_pages():
    """
    Process all HTML files in the integracoes-paginas folder
    """
    base_path = Path('integracoes-paginas')
    
    if not base_path.exists():
        print(f"Creating {base_path} folder...")
        base_path.mkdir(parents=True, exist_ok=True)
    
    html_files = list(base_path.glob('**/*.html'))
    
    if not html_files:
        print("No HTML files found in integracoes-paginas folder.")
        print("This script should be run in the root directory where integracoes-paginas exists.")
        return
    
    fixed_count = 0
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Apply fixes
            fixed_content = fix_integration_page(original_content)
            
            # Only write if content changed
            if fixed_content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✓ Fixed: {html_file}")
                fixed_count += 1
            else:
                print(f"- Skipped (no changes): {html_file}")
                
        except Exception as e:
            print(f"✗ Error processing {html_file}: {e}")
    
    print(f"\n✓ Fixed {fixed_count} pages")
    print("Ready to deploy!")

if __name__ == '__main__':
    print("Fixing integration pages...")
    print("Removing vote buttons and updating status messages...\n")
    process_all_pages()

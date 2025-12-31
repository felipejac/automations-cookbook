#!/bin/bash

# Build script for Automations Cookbook
# Fixes integration pages and rebuilds everything

echo "========================================"
echo "Building Automations Cookbook"
echo "========================================"

# Step 1: Apply fixes to integration pages
echo ""
echo "Step 1: Applying fixes to integration pages..."
if [ -f "scripts/apply_fixes_to_html.py" ]; then
    python3 scripts/apply_fixes_to_html.py
    echo "✓ HTML fixes applied"
else
    echo "⚠ apply_fixes_to_html.py not found"
fi

# Step 2: Generate/update integration pages  
echo ""
echo "Step 2: Ensuring all integration pages exist..."
if [ -f "scripts/generate_tutorials.py" ]; then
    python3 scripts/generate_tutorials.py
    echo "✓ Integration pages generated"
else
    echo "⚠ generate_tutorials.py not found"
fi

# Step 3: Copy pages to public folder if needed
echo ""
echo "Step 3: Preparing pages for deployment..."
if [ -d "integracoes-paginas" ] && [ -d "public" ]; then
    cp -r integracoes-paginas/*.html public/ 2>/dev/null || true
    echo "✓ Pages copied to public folder"
fi

echo ""
echo "========================================"
echo "Build complete! Ready for deployment."
echo "========================================"

exit 0

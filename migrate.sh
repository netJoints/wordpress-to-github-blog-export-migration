#!/bin/bash

# WordPress to GitHub Migration - Quick Start Script
# This script sets up the environment and runs the migration

echo "============================================"
echo "WordPress to GitHub Migration Tool"
echo "============================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -q requests beautifulsoup4 lxml html2text

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Get site URL
echo ""
echo "Please enter your WordPress site URL:"
echo "Example: https://netjoints.com"
read -p "URL: " SITE_URL

if [ -z "$SITE_URL" ]; then
    echo "❌ Site URL cannot be empty"
    exit 1
fi

# Get output directory (optional)
echo ""
echo "Enter output directory name (or press Enter for default 'blog_backup'):"
read -p "Directory: " OUTPUT_DIR

if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="blog_backup"
fi

# Run the migration
echo ""
echo "============================================"
echo "Starting migration from: $SITE_URL"
echo "Output directory: $OUTPUT_DIR"
echo "============================================"
echo ""

python3 wordpress_to_github.py "$SITE_URL" "$OUTPUT_DIR"

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "✓ Migration completed successfully!"
    echo "============================================"
    echo ""
    echo "Your blog backup is ready in: $OUTPUT_DIR/"
    echo ""
    echo "Next steps:"
    echo "  1. Review the files in $OUTPUT_DIR/"
    echo "  2. cd $OUTPUT_DIR"
    echo "  3. git init"
    echo "  4. git add ."
    echo "  5. git commit -m 'Initial blog backup'"
    echo "  6. Create a repo on GitHub and push"
    echo ""
else
    echo ""
    echo "❌ Migration failed. Please check the error messages above."
    exit 1
fi

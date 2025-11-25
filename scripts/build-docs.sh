#!/bin/bash

# Default values
config_file="mkdocs.yml"
serve_mode=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            config_file="$2"
            shift 2
            ;;
        serve)
            serve_mode=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [-f|--file <config_file>] [serve]"
            echo "  -f, --file    Specify MkDocs config file (default: mkdocs.yml)"
            echo "  serve         Serve documentation locally instead of building"
            echo "  -h, --help    Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

echo "Converting Jupyter notebooks to Markdown..."
python scripts/convert_notebooks.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to convert notebooks"
    exit 1
fi

# Create directories if they don't exist
mkdir -p docs/en
mkdir -p docs/fr
mkdir -p docs/en/pointclouds
mkdir -p docs/fr/pointclouds
mkdir -p docs/en/vertical-transformations
mkdir -p docs/fr/vertical-transformations

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if MkDocs is installed
if ! python -m mkdocs --version &> /dev/null; then
    echo "Error: MkDocs is not installed"
    echo "Please install MkDocs using: pip install mkdocs mkdocs-material mkdocs-static-i18n nbconvert"
    exit 1
fi

# Check if config file exists
if [ ! -f "$config_file" ]; then
    echo "Error: Config file '$config_file' not found"
    exit 1
fi

echo "Using config file: $config_file"

if [ "$serve_mode" = true ]; then
    echo "Serving documentation locally..."
    python -m mkdocs serve -f "$config_file"
else
    # Clean previous build
    if [ -d "site" ]; then
        echo "Cleaning previous build..."
        rm -rf site
    fi

    # Build the documentation
    echo "Building MkDocs documentation..."
    python -m mkdocs build -f "$config_file"

    if [ $? -eq 0 ]; then
        echo "Build completed successfully!"
        echo "Documentation is available in the 'site' directory"
        echo ""
        echo "To serve locally, run: mkdocs serve -f \"$config_file\""
    else
        echo "Build failed!"
        exit 1
    fi

    echo "Build complete!"
fi
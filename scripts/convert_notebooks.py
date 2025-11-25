#!/usr/bin/env python3
"""
Convert Jupyter notebooks to Markdown for MkDocs while preserving download links and cell outputs
"""

import os
import json
import nbformat
from nbconvert import MarkdownExporter
from pathlib import Path
import re

def fix_markdown_lists(markdown_content):
    """Fix markdown list formatting issues that can occur during nbconvert"""
    lines = markdown_content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Fix numbered lists that might be missing proper spacing
        if re.match(r'^\d+\.', line.strip()) and i > 0:
            prev_line = lines[i-1].strip()
            # Add blank line before numbered list if previous line isn't empty or part of list
            if prev_line and not re.match(r'^\d+\.', prev_line) and not prev_line.startswith('   '):
                fixed_lines.append('')
        
        # Fix bullet lists
        if re.match(r'^[\*\-\+]\s', line.strip()) and i > 0:
            prev_line = lines[i-1].strip()
            # Add blank line before bullet list if previous line isn't empty or part of list
            if prev_line and not re.match(r'^[\*\-\+]\s', prev_line) and not prev_line.startswith('   '):
                fixed_lines.append('')
        
        # Ensure proper indentation for nested lists
        if re.match(r'^[\*\-\+]\s', line):
            # Convert to proper markdown list format
            line = re.sub(r'^([\*\-\+])\s', r'* ', line)
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def get_language_strings(notebook_path):
    """Determine language strings based on notebook path"""
    if '_FR.ipynb' in notebook_path or '/fr/' in notebook_path:
        return {
            'download_button': '📓 Télécharger le notebook Jupyter',
            'github_button': '👁️ Voir sur GitHub',
            'colab_button': '🚀 Ouvrir dans Colab',
            'access_title': 'Accès au notebook',
            'preview_title': 'Aperçu statique',
            'preview_text': 'Ceci est un aperçu statique du notebook. Téléchargez le fichier notebook original pour exécuter le code de manière interactive.'
        }
    else:
        return {
            'download_button': '📓 Download Jupyter Notebook',
            'github_button': '👁️ View on GitHub', 
            'colab_button': '🚀 Open in Colab',
            'access_title': 'Notebook Access',
            'preview_title': 'Static Preview',
            'preview_text': 'This is a static preview of the notebook. Download the original notebook file to run the code interactively.'
        }

def convert_notebook_to_markdown(notebook_path, output_path, download_link, repo_base_url="https://github.com/NRCan/CanElevation/blob/main"):
    """Convert a Jupyter notebook to Markdown with download link and cell outputs"""
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Create markdown exporter with configuration to include outputs
    md_exporter = MarkdownExporter()
    
    # Configure the exporter to include outputs and images
    md_exporter.exclude_input_prompt = False
    md_exporter.exclude_output_prompt = False
    
    # Convert to markdown - this includes all outputs by default
    (body, resources) = md_exporter.from_notebook_node(nb)
    
    # Fix markdown list formatting issues
    # body = fix_markdown_lists(body)
    
    # Handle image outputs - save them to assets directory
    output_dir = os.path.dirname(output_path)
    assets_dir = os.path.join(output_dir, 'assets')
    
    if 'outputs' in resources:
        os.makedirs(assets_dir, exist_ok=True)
        
        # Save image files and update references in markdown
        for filename, data in resources['outputs'].items():
            asset_path = os.path.join(assets_dir, filename)
            with open(asset_path, 'wb') as f:
                f.write(data)
            
            # Update image references in markdown to use relative paths
            relative_asset_path = f"assets/{filename}"
            body = body.replace(f"![png]({filename})", f"![png]({relative_asset_path})")
            body = body.replace(f"![svg]({filename})", f"![svg]({relative_asset_path})")
            body = body.replace(f"![jpeg]({filename})", f"![jpeg]({relative_asset_path})")
    
    # Get language-specific strings
    lang_strings = get_language_strings(notebook_path)
    
    # Add download and view links at the top
    notebook_name = os.path.basename(notebook_path)
    github_url = f"{repo_base_url}/{notebook_path.replace(os.sep, '/')}"
    
#     download_section = f"""!!! info "{lang_strings['access_title']}"
#     [:material-download: {lang_strings['download_button']}]({download_link}){{ .md-button .md-button--primary }}
#     [:material-github: {lang_strings['github_button']}]({github_url}){{ .md-button }}
#     [:material-rocket-launch: {lang_strings['colab_button']}](https://colab.research.google.com/github/NRCan/CanElevation/blob/main/{notebook_path.replace(os.sep, '/')}){{ .md-button }}

    

# !!! warning "{lang_strings['preview_title']}"
#     {lang_strings['preview_text']}

# """
    
    download_section = f"""!!! info "{lang_strings['access_title']}"
    [{lang_strings['download_button']}]({download_link}){{ .md-button .md-button--primary }}
    
!!! warning "{lang_strings['preview_title']}"
    {lang_strings['preview_text']}

"""
    
    # Combine download links with content
    final_content = download_section + body
    
    # Write to output file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Converted {notebook_path} -> {output_path}")
    if 'outputs' in resources:
        print(f"  └── Saved {len(resources['outputs'])} image(s) to {assets_dir}")

def main():
    # Updated notebook conversions with new paths
    notebooks = [
        {
            'source': 'docs/en/pointclouds/DEM_from_COPC_lidar_EN.ipynb',
            'output': 'docs/en/pointclouds/dem-from-copc-lidar.md',
            'download': './DEM_from_COPC_lidar_EN.ipynb'  # Relative to the markdown file
        },
        {
            'source': 'docs/fr/pointclouds/DEM_from_COPC_lidar_FR.ipynb',
            'output': 'docs/fr/pointclouds/dem-from-copc-lidar.md',
            'download': './DEM_from_COPC_lidar_FR.ipynb'
        },
        {
            'source': 'docs/en/pointclouds/Get_Projects_Tiles_by_AOI_EN.ipynb',
            'output': 'docs/en/pointclouds/projects-tiles-by-aoi.md',
            'download': './Get_Projects_Tiles_by_AOI_EN.ipynb'
        },
        {
            'source': 'docs/fr/pointclouds/Get_Projects_Tiles_by_AOI_FR.ipynb',
            'output': 'docs/fr/pointclouds/projects-tiles-by-aoi.md',
            'download': './Get_Projects_Tiles_by_AOI_FR.ipynb'
        }
    ]
    
    for notebook in notebooks:
        if os.path.exists(notebook['source']):
            convert_notebook_to_markdown(
                notebook['source'], 
                notebook['output'], 
                notebook['download']
            )
        else:
            print(f"Warning: {notebook['source']} not found")

if __name__ == "__main__":
    main()
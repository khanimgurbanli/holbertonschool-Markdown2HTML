#!/usr/bin/python3
"""
markdown2html.py

Converts a Markdown file to HTML.

Usage:
    ./markdown2html.py <input_file.md> <output_file.html>

Requirements:
    - If the number of arguments is less than 2: print in STDERR
      Usage: ./markdown2html.py README.md README.html and exit 1
    - If the Markdown file doesn’t exist: print in STDERR
      Missing <filename> and exit 1
    - Otherwise, print nothing and exit 0
"""

import sys
import os
import markdown2

def convert_markdown_to_html(input_file, output_file):
    """
    Convert Markdown content from input file to HTML and save to output file.

    Args:
        input_file (str): Path to Markdown input file.
        output_file (str): Path to HTML output file.
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    
    # Read markdown content
    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(markdown_content)
    
    # Write HTML content to output file
    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
    
    # Print success message (optional)
    print(f"Successfully converted {input_file} to {output_file}")

    # Exit with status 0 (success)
    sys.exit(0)

if __name__ == "__main__":
    # Check number of arguments
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file.md> <output_file.html>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_markdown_to_html(input_file, output_file)

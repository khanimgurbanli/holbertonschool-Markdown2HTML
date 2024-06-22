#!/usr/bin/python3
'''
Converts a Markdown file to HTML.

Usage:
    ./markdown2html.py <input_file.md> <output_file.html>
'''

import sys
import os.path
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    """Converts Markdown content to HTML and writes it to an output file.

    Args:
        input_file (str): Path to Markdown input file.
        output_file (str): Path to HTML output file.
    """
    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    # Open input and output files
    with open(input_file, 'r', encoding='utf-8') as md_file, \
         open(output_file, 'w', encoding='utf-8') as html_file:

        # Initialize variables for list and paragraph tracking
        unordered_start = False
        ordered_start = False
        paragraph = False

        # Process each line in the Markdown file
        for line in md_file:
            # Replace Markdown syntax for bold and emphasis
            line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)

            # Replace MD5 hash syntax [[...]] with hash value
            md5_matches = re.findall(r'\[\[(.+?)\]\]', line)
            for match in md5_matches:
                line = line.replace(f'[[{match}]]', hashlib.md5(match.encode()).hexdigest())

            # Remove 'C' from double parentheses ((...))
            c_removed = re.sub(r'\(\((.+?)\)\)', lambda m: m.group(1).replace('C', '').replace('c', ''), line)

            # Determine if the line starts with headings or lists
            if line.startswith('#'):
                heading_level = len(line.split()[0])
                line = f'<h{heading_level}>{line.strip("# \n")}</h{heading_level}>\n'
            elif line.startswith('-'):
                if not unordered_start:
                    html_file.write('<ul>\n')
                    unordered_start = True
                line = f'<li>{line.strip("- \n")}</li>\n'
            elif line.startswith('*'):
                if not ordered_start:
                    html_file.write('<ol>\n')
                    ordered_start = True
                line = f'<li>{line.strip("* \n")}</li>\n'
            else:
                if not paragraph and line.strip():
                    html_file.write('<p>\n')
                    paragraph = True
                elif not line.strip():
                    html_file.write('<br/>\n')
                elif paragraph:
                    html_file.write('</p>\n')
                    paragraph = False

            # Write the processed line to the HTML file
            if line.strip():
                html_file.write(line)

        # Close any open lists or paragraphs
        if unordered_start:
            html_file.write('</ul>\n')
        if ordered_start:
            html_file.write('</ol>\n')
        if paragraph:
            html_file.write('</p>\n')

if __name__ == '__main__':
    # Check command-line arguments
    if len(sys.argv) != 3:
        print('Usage: ./markdown2html.py <input_file.md> <output_file.html>', file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Convert Markdown to HTML
    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)

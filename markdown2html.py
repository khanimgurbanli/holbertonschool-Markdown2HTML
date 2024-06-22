#!/usr/bin/python3
'''
Converts a Markdown file to HTML.

Usage:
    ./markdown2html.py README.md README.html
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
            # Replace Markdown syntax for bold (**...**) and emphasis (__...__)
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)

            # Replace MD5 hash syntax [[...]] with hash value
            line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)

            # Remove 'C' from double parentheses ((...))
            line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('C', '').replace('c', ''), line)

            length = len(line)
            headings = line.lstrip('#')
            heading_num = length - len(headings)
            unordered = line.lstrip('-')
            unordered_num = length - len(unordered)
            ordered = line.lstrip('*')
            ordered_num = length - len(ordered)

            # Handle headings, unordered lists, ordered lists
            if 1 <= heading_num <= 6:
                line = f'<h{heading_num}>{headings.strip()}</h{heading_num}>\n'

            if unordered_num:
                if not unordered_start:
                    html_file.write('<ul>\n')
                    unordered_start = True
                line = f'<li>{unordered.strip()}</li>\n'
            if unordered_start and not unordered_num:
                html_file.write('</ul>\n')
                unordered_start = False

            if ordered_num:
                if not ordered_start:
                    html_file.write('<ol>\n')
                    ordered_start = True
                line = f'<li>{ordered.strip()}</li>\n'
            if ordered_start and not ordered_num:
                html_file.write('</ol>\n')
                ordered_start = False

            if not (heading_num or unordered_start or ordered_start):
                if not paragraph and length > 1:
                    html_file.write('<p>\n')
                    paragraph = True
                elif length > 1:
                    html_file.write('<br/>\n')
                elif paragraph:
                    html_file.write('</p>\n')
                    paragraph = False

            if length > 1:
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
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Convert Markdown to HTML
    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)

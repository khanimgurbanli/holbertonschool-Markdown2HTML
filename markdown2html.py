import sys
import os
import markdown2

def convert_markdown_to_html(input_file, output_file):
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
    
    print(f"Successfully converted {input_file} to {output_file}")
    sys.exit(0)

if __name__ == "__main__":
    # Check number of arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file.md> <output_file.html>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_markdown_to_html(input_file, output_file)

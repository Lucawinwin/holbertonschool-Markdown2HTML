#!/usr/bin/env python3

import sys
import os
import re

def convert_markdown_to_html(markdown_content):
    """Convert markdown content to HTML"""
    html_content = markdown_content
    
    # Convert headers
    html_content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^##### (.*?)$', r'<h5>\1</h5>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^###### (.*?)$', r'<h6>\1</h6>', html_content, flags=re.MULTILINE)
    
    # Convert bold text
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_content)
    html_content = re.sub(r'__(.*?)__', r'<em>\1</em>', html_content)
    
    # Convert code blocks
    html_content = re.sub(r'`(.*?)`', r'<code>\1</code>', html_content)
    
    # Convert line breaks (double newlines to paragraph breaks)
    paragraphs = html_content.split('\n\n')
    html_paragraphs = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            # Check if it's already wrapped in HTML tags
            if not re.match(r'^\s*<[hH][1-6]>', paragraph):
                html_paragraphs.append(f'<p>{paragraph}</p>')
            else:
                html_paragraphs.append(paragraph)
    
    return '\n'.join(html_paragraphs)

def main():
    # Check number of arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Read markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to HTML
        html_content = convert_markdown_to_html(markdown_content)
        
        # Write HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Exit successfully (no output on success)
        sys.exit(0)
        
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()




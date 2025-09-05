#!/usr/bin/python3
"""
Markdown to HTML converter script
Converts a Markdown file to HTML format
"""

import sys
import os
import re


def parse_markdown_line(line):
    """Parse a single line of Markdown and convert to HTML"""
    line = line.rstrip('\n\r')
    
    # Handle headers
    if line.startswith('#'):
        level = 0
        for char in line:
            if char == '#':
                level += 1
            else:
                break
        if level <= 6 and line[level:level+1] == ' ':
            content = line[level+1:].strip()
            return f'<h{level}>{content}</h{level}>'
    
    # Handle unordered lists
    if line.startswith('- '):
        content = line[2:].strip()
        return f'<li>{content}</li>'
    
    # Handle ordered lists (basic implementation)
    if re.match(r'^\d+\. ', line):
        content = re.sub(r'^\d+\. ', '', line).strip()
        return f'<li>{content}</li>'
    
    # Handle paragraphs (non-empty lines that aren't special)
    if line.strip() and not line.startswith('#') and not line.startswith('- ') and not re.match(r'^\d+\. ', line):
        return f'<p>{line.strip()}</p>'
    
    # Empty lines
    if not line.strip():
        return ''
    
    return line


def convert_markdown_to_html(markdown_content):
    """Convert Markdown content to HTML"""
    lines = markdown_content.split('\n')
    html_lines = []
    in_ul_list = False
    in_ol_list = False
    
    for line in lines:
        html_line = parse_markdown_line(line)
        
        # Handle list management
        if html_line.startswith('<li>'):
            if line.startswith('- '):
                if not in_ul_list:
                    if in_ol_list:
                        html_lines.append('</ol>')
                        in_ol_list = False
                    html_lines.append('<ul>')
                    in_ul_list = True
            elif re.match(r'^\d+\. ', line):
                if not in_ol_list:
                    if in_ul_list:
                        html_lines.append('</ul>')
                        in_ul_list = False
                    html_lines.append('<ol>')
                    in_ol_list = True
            html_lines.append(html_line)
        else:
            # Close any open lists
            if in_ul_list:
                html_lines.append('</ul>')
                in_ul_list = False
            if in_ol_list:
                html_lines.append('</ol>')
                in_ol_list = False
            
            if html_line:  # Only add non-empty lines
                html_lines.append(html_line)
    
    # Close any remaining open lists
    if in_ul_list:
        html_lines.append('</ul>')
    if in_ol_list:
        html_lines.append('</ol>')
    
    return '\n'.join(html_lines)


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
        # Read the Markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to HTML
        html_content = convert_markdown_to_html(markdown_content)
        
        # Write the HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Exit successfully with no output
        sys.exit(0)
        
    except Exception as e:
        print(f"Error processing files: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
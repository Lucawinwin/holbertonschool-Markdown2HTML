#!/usr/bin/python3
import sys
import os
import re
import hashlib

def md5_replace(match):
    text = match.group(1)
    return hashlib.md5(text.encode()).hexdigest()

def remove_c(match):
    text = match.group(1)
    return re.sub(r'[cC]', '', text)

def convert_inline(text):
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Emphasis
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    # MD5
    text = re.sub(r'\[\[(.*?)\]\]', md5_replace, text)
    # Remove 'c' or 'C'
    text = re.sub(r'\(\((.*?)\)\)', remove_c, text)
    return text

def parse_markdown(lines):
    html_lines = []
    in_ul = False
    in_ol = False
    in_p = False

    for line in lines:
        line = line.rstrip('\n')

        # Headings
        heading_match = re.match(r'^(#{1,6}) (.*)', line)
        if heading_match:
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            if in_ol:
                html_lines.append('</ol>')
                in_ol = False
            if in_p:
                html_lines.append('</p>')
                in_p = False
            level = len(heading_match.group(1))
            content = convert_inline(heading_match.group(2))
            html_lines.append(f'<h{level}>{content}</h{level}>')
            continue

        # Unordered list
        ul_match = re.match(r'^- (.*)', line)
        if ul_match:
            if in_ol:
                html_lines.append('</ol>')
                in_ol = False
            if not in_ul:
                html_lines.append('<ul>')
                in_ul = True
            content = convert_inline(ul_match.group(1))
            html_lines.append(f'<li>{content}</li>')
            continue

        # Ordered list
        ol_match = re.match(r'^\* (.*)', line)
        if ol_match:
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            if not in_ol:
                html_lines.append('<ol>')
                in_ol = True
            content = convert_inline(ol_match.group(1))
            html_lines.append(f'<li>{content}</li>')
            continue

        # Paragraphs
        if line.strip() == "":
            if in_p:
                html_lines.append('</p>')
                in_p = False
            continue
        else:
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            if in_ol:
                html_lines.append('</ol>')
                in_ol = False
            if not in_p:
                html_lines.append('<p>')
                in_p = True
                content = convert_inline(line)
                html_lines.append(content)
            else:
                content = convert_inline(line)
                html_lines.append('<br/>' if content else '')
                html_lines.append(content)

    # Close any open tags
    if in_ul:
        html_lines.append('</ul>')
    if in_ol:
        html_lines.append('</ol>')
    if in_p:
        html_lines.append('</p>')

    return html_lines

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(md_file):
        sys.stderr.write(f"Missing {md_file}\n")
        sys.exit(1)

    with open(md_file, "r") as f:
        lines = f.readlines()

    html_lines = parse_markdown(lines)

    with open(html_file, "w") as f:
        f.write("\n".join(html_lines))

    sys.exit(0)

if __name__ == "__main__":
    main()

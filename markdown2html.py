#!/usr/bin/python3
"""
markdown2html module

A simple script that takes a Markdown file and converts it
to an HTML file. Currently, it only handles headings (# to ######).
"""
import sys
import os


def convert_markdown_to_html(input_file, output_file):
    """Convert Markdown headings into HTML headings"""
    with open(input_file, "r", encoding="utf-8") as f_in, \
            open(output_file, "w", encoding="utf-8") as f_out:

        for line in f_in:
            line = line.rstrip()  # remove trailing newline/spaces
            if line.startswith("#"):
                # Count heading level
                level = len(line.split(" ")[0])
                text = line[level:].strip()
                if 1 <= level <= 6:  # only levels 1 to 6 supported
                    f_out.write(f"<h{level}>{text}</h{level}>\n")
                else:
                    f_out.write(line + "\n")  # fallback (if invalid)
            else:
                # Non-heading lines are ignored (or could be plain text)
                pass


def main():
    """Main entry point of the script"""
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)


if __name__ == "__main__":
    main()

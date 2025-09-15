#!/usr/bin/python3
"""
markdown2html module

A simple script that takes a Markdown file and converts it
to an HTML file. Currently, it handles:
- Headings (# to ######)
- Unordered lists (- item)
"""
import sys
import os


def convert_markdown_to_html(input_file, output_file):
    """Convert Markdown headings and lists into HTML"""
    with open(input_file, "r", encoding="utf-8") as f_in, \
            open(output_file, "w", encoding="utf-8") as f_out:

        inside_list = False  # track if we're inside a <ul>

        for line in f_in:
            line = line.rstrip()  # remove trailing newline/spaces

            if line.startswith("#"):
                # Close list if we were in one
                if inside_list:
                    f_out.write("</ul>\n")
                    inside_list = False

                # Headings
                level = len(line.split(" ")[0])
                text = line[level:].strip()
                if 1 <= level <= 6:
                    f_out.write(f"<h{level}>{text}</h{level}>\n")

            elif line.startswith("- "):
                # Start list if not already inside one
                if not inside_list:
                    f_out.write("<ul>\n")
                    inside_list = True

                text = line[2:].strip()
                f_out.write(f"<li>{text}</li>\n")

            else:
                # If a blank or non-markdown line ends a list
                if inside_list:
                    f_out.write("</ul>\n")
                    inside_list = False

        # Close any unclosed list at EOF
        if inside_list:
            f_out.write("</ul>\n")


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

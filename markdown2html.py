#!/usr/bin/python3
"""
markdown2html module

A simple script that takes a Markdown file and converts it
to an HTML file. Currently, it handles:
- Headings (# to ######)
- Unordered lists (- item)
- Ordered lists (* item)
"""
import sys
import os


def convert_markdown_to_html(input_file, output_file):
    """Convert Markdown headings and lists into HTML"""
    with open(input_file, "r", encoding="utf-8") as f_in, \
            open(output_file, "w", encoding="utf-8") as f_out:

        inside_ul = False
        inside_ol = False

        for line in f_in:
            line = line.rstrip()

            if line.startswith("#"):
                # Close lists if any are open
                if inside_ul:
                    f_out.write("</ul>\n")
                    inside_ul = False
                if inside_ol:
                    f_out.write("</ol>\n")
                    inside_ol = False

                # Headings
                level = len(line.split(" ")[0])
                text = line[level:].strip()
                if 1 <= level <= 6:
                    f_out.write(f"<h{level}>{text}</h{level}>\n")

            elif line.startswith("- "):  # unordered list
                if inside_ol:  # close ol if switching
                    f_out.write("</ol>\n")
                    inside_ol = False
                if not inside_ul:
                    f_out.write("<ul>\n")
                    inside_ul = True
                text = line[2:].strip()
                f_out.write(f"<li>{text}</li>\n")

            elif line.startswith("* "):  # ordered list
                if inside_ul:  # close ul if switching
                    f_out.write("</ul>\n")
                    inside_ul = False
                if not inside_ol:
                    f_out.write("<ol>\n")
                    inside_ol = True
                text = line[2:].strip()
                f_out.write(f"<li>{text}</li>\n")

            else:
                # Close any open list if line doesn't belong to one
                if inside_ul:
                    f_out.write("</ul>\n")
                    inside_ul = False
                if inside_ol:
                    f_out.write("</ol>\n")
                    inside_ol = False

        # Close at EOF
        if inside_ul:
            f_out.write("</ul>\n")
        if inside_ol:
            f_out.write("</ol>\n")


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


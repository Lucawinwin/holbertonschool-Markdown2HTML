#!/usr/bin/python3
"""
markdown2html module

A simple script that takes a Markdown file and converts it
to an HTML file. For now, it only checks arguments and creates
the output file without actual conversion.

Usage:
    ./markdown2html.py INPUT.md OUTPUT.html
"""
import sys
import os


def main():
    """Main entry point of the script"""
    # Check number of arguments
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if input file exists
    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    # Create an empty output file (conversion to be added later)
    with open(output_file, "w", encoding="utf-8") as f:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()

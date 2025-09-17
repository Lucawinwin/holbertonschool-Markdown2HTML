#!/usr/bin/python3
"""
Markdown to HTML converter script.

This module converts Markdown files to HTML format.
"""

import sys
import os


def main():
    """
    Main function to handle command line arguments and file processing.
    
    Takes two arguments:
    - First argument: name of the Markdown file
    - Second argument: output file name
    
    Exit codes:
    - 0: Success
    - 1: Error (wrong arguments or missing file)
    """
    # Check if we have exactly 2 arguments (plus script name = 3 total)
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)
    
    # If we reach here, everything is OK
    # For now, just exit with success (future tasks will add conversion logic)
    sys.exit(0)


if __name__ == "__main__":
    main()

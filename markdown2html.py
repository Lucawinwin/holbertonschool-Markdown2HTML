#!/usr/bin/python3
"""
markdown2html module

Ce script convertit un fichier Markdown en fichier HTML.
Actuellement, il gère la syntaxe des titres (# à ######).
"""

import sys
import os


def convert_markdown_to_html(input_file, output_file):
    """
    Convertit un fichier Markdown en fichier HTML
    en gérant uniquement les titres (# à ######).
    """
    with open(input_file, "r", encoding="utf-8") as f_in, \
            open(output_file, "w", encoding="utf-8") as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                level = len(line.split(" ")[0])
                if 1 <= level <= 6:
                    content = line[level + 1:].strip()
                    f_out.write(f"<h{level}>{content}</h{level}>\n")
                else:
                    f_out.write(line + "\n")
            else:
                f_out.write(line + "\n")


def main():
    """Point d’entrée du script"""
    if len(sys.argv) < 3:
        sys.stderr.write(
            "Usage: ./markdown2html.py README.md README.html\n"
        )
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


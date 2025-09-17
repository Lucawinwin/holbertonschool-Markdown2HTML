#!/usr/bin/python3
"""
markdown2html module

Ce script convertit un fichier Markdown en fichier HTML.
Il gère :
- Les titres (# à ######)
- Les listes non ordonnées (- élément)
"""

import sys
import os


def convert_markdown_to_html(input_file, output_file):
    """
    Convertit un fichier Markdown en fichier HTML.
    Gère les titres et les listes non ordonnées.
    """
    inside_list = False

    with open(input_file, "r", encoding="utf-8") as f_in, \
            open(output_file, "w", encoding="utf-8") as f_out:

        for line in f_in:
            line = line.strip()
            if not line:
                if inside_list:
                    f_out.write("</ul>\n")
                    inside_list = False
                continue

            # Titres Markdown
            if line.startswith("#"):
                if inside_list:
                    f_out.write("</ul>\n")
                    inside_list = False
                level = len(line.split(" ")[0])
                if 1 <= level <= 6:
                    content = line[level + 1:].strip()
                    f_out.write(f"<h{level}>{content}</h{level}>\n")
                else:
                    f_out.write(line + "\n")

            # Listes non ordonnées
            elif line.startswith("- "):
                if not inside_list:
                    f_out.write("<ul>\n")
                    inside_list = True


#!/usr/bin/python3
"""
markdown2html module

Ce script convertit un fichier Markdown en fichier HTML.
Il gère :
- Les titres (# à ######)
- Les listes non ordonnées (- élément)
- Les listes ordonnées (* élément)
- Les paragraphes (séparés par des lignes vides)
- Le texte en gras (**...**)
- Le texte en italique (__...__)
- Syntaxes personnalisées :
    [[texte]] → MD5 minuscule
    ((texte)) → supprime toutes les lettres 'c' ou 'C'
"""

import sys
import os
import re
import hashlib


def apply_inline_formatting(text):
    """
    Applique les transformations de style inline :
    - **texte** → <b>texte</b>
    - __texte__ → <em>texte</em>
    - [[texte]] → MD5 minuscule
    - ((texte)) → supprime 'c' et 'C'
    """
    # Gras
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

    # Italique
    text = re.sub(r"__(.+?)__", r"<em>\1</em>", text)

    # MD5 [[texte]]
    def md5_repl(match):
        s = match.group(1)
        return hashlib.md5(s.encode("utf-8")).hexdigest()

    text = re.sub(r"\[\[(.+?)\]\]", md5_repl, text)

    # Supprimer 'c' ou 'C' ((texte))
    def remove_c(match):
        s = match.group(1)
        return re.sub(r"[cC]", "", s)

    text = re.sub(r"\(\((.+?)\)\)", remove_c, text)

    return text


def convert_markdown_to_html(input_file, output_file):
    """
    Convertit un fichier Markdown en fichier HTML.
    Gère titres, listes, paragraphes et inline styles.
    """
    inside_ul = False
    inside_ol = False
    inside_p = False

    with open(input_file, "r", encoding="utf-8") as f_in, \
            open(output_file, "w", encoding="utf-8") as f_out:

        for line in f_in:
            line = line.rstrip()

            # Ligne vide : ferme paragraphes et listes
            if not line.strip():
                if inside_ul:
                    f_out.write("</ul>\n")
                    inside_ul = False
                if inside_ol:
                    f_out.write("</ol>\n")
                    inside_ol = False
                if inside_p:
                    f_out.write("</p>\n")
                    inside_p = False
                continue

            # Titres
            if line.startswith("#"):
                if inside_ul:
                    f_out.write("</ul>\n")
                    inside_ul = False
                if inside_ol:
                    f_out.write("</ol>\n")
                    inside_ol = False
                if inside_p:
                    f_out.write("</p>\n")
                    inside_p = False

                level = len(line.split(" ")[0])
                if 1 <= level <= 6:
                    content = line[level + 1:].strip()
                    content = apply_inline_formatting(content)
                    f_out.write(f"<h{level}>{content}</h{level}>\n")
                else:
                    f_out.write(line + "\n")

            # Liste non ordonnée
            elif line.startswith("- "):
                if inside_ol:
                    f_out.write("</ol>\n")
                    inside_ol = False
                if inside_p:
                    f_out.write("</p>\n")
                    inside_p = False
                if not inside_ul:
                    f_out.write("<ul>\n")
                    inside_ul = True
                content = line[2:].strip()
                content = apply_inline_formatting(content)
                f_out.write(f"<li>{content}</li>\n")

            # Liste ordonnée
            elif line.startswith("* "):
                if inside_ul:
                    f_out.write("</ul>\n")
                    inside_ul = False
                if inside_p:
                    f_out.write("</p>\n")
                    inside_p = False
                if not inside_ol:
                    f_out.write("<ol>\n")
                    inside_ol = True
                content = line[2:].strip()
                content = apply_inline_formatting(content)
                f_out.write(f"<li>{content}</li>\n")

            # Paragraphe
            else:
                if inside_ul:
                    f_out.write("</ul>\n")
                    inside_ul = False
                if inside_ol:
                    f_out.write("</ol>\n")
                    inside_ol = False

                content = apply_inline_formatting(line.strip())

                if not inside_p:
                    f_out.write("<p>\n")
                    inside_p = True
                    f_out.write(content + "\n")
                else:
                    f_out.write("<br/>\n")
                    f_out.write(content + "\n")

        # Fermeture si fichier finit par une liste ou un paragraphe
        if inside_ul:
            f_out.write("</ul>\n")
        if inside_ol:
            f_out.write("</ol>\n")
        if inside_p:
            f_out.write("</p>\n")


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



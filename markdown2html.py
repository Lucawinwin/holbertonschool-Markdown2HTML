#!/usr/bin/python3
"""
markdown2html module

Ce script convertit un fichier Markdown en fichier HTML.
Pour l’instant, il ne fait que gérer les vérifications de base :
- nombre d’arguments
- existence du fichier Markdown d’entrée
"""

import sys
import os


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

    # Plus tard, on ajoutera la logique de conversion Markdown → HTML
    # Pour l’instant, on respecte juste les consignes
    sys.exit(0)


if __name__ == "__main__":
    main()

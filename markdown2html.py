#!/usr/bin/python3
"""
Markdown to HTML
"""

import sys
import os
import re
import hashlib


def convert_markdown(md_content):
    """
    Convert Markdown headings, lists, paragraphs, bold, emphasis,
    and custom syntax to HTML.
    """
    html_content = []
    in_ulist = False
    in_olist = False
    in_paragraph = False
    paragraph_lines = []
    
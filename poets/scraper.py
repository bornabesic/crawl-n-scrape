"""
Module containing user-written code for scraping the
web content.
"""

from typing import Tuple
import re

_TITLE_PATTERN = re.compile(r"<span style=\"font-weight:bold;font-size:16px;color:#3C605B;font-family:Times New Roman;\">([^<]*)<span style=\"color:#000000;\">.*</span></span>")
_POEM_PATTERN = re.compile(r"<div style=\"padding-left:14px;padding-top:20px;font-family:Arial;font-size:13px;\">([^<]*)</div>", flags=re.DOTALL)

def scrape(link: str, content: str) -> Tuple[str, str]:
    """
	Returns the file name (without an extension) and the
    extracted data from the given link and HTML content.
	"""

    # Title
    title_match = _TITLE_PATTERN.search(content)
    title = title_match.group(1).strip()
    
    # Poem
    poem_match = _POEM_PATTERN.search(content.replace("<br>", "\n"))
    poem = poem_match.group(1).strip()

    return title, poem

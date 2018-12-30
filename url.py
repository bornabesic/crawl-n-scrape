"""
Module that defines an interface for retrieving and handling
web documents.
"""

import re
from urllib.request import urlopen
from urllib.error import URLError
from typing import Tuple, Set

def get(url: str, timeout: int = 10) -> str:
    """
    Performs a GET request, decodes retrieved bytes using
    UTF-8 and returns the resulting string content.
    If an error has occurred during the request, None is
    returned.
    """

    try:
        return urlopen(url, timeout=timeout).read().decode(encoding="utf-8", errors="ignore")
    except (URLError, ValueError):
        return None

_HREF_PATTERN = re.compile("href=\"([^\"]*)\"")
def links_from_text_file(content: str) -> Set[str]:
    """
    Extracts links from a text file retrieved from the web
    independently of file's type (e.g. HTML or raw text).
    """

    # href links
    href_links = _HREF_PATTERN.findall(content)

    # TODO: http / https raw links occuring in the content
    # raw_links = ...

    links = href_links
    return set(links)

def content_and_links(url: str) -> Tuple[str, Set[str]]:
    """
    Return a content (text) and all containing links from a
    web document at a specified URL.
    """

    content = get(url)
    links = set()
    if content is not None:
        links = links_from_text_file(content)

    return content, links

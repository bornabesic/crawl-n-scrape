"""
Crawl 'n' Scrape category module.
"""

import re
from typing import Iterable

class Category:
    """
    Class that represents one of the categories
    in which the scraped data will be placed.
    """

    def __init__(self, name: str, regexes: Iterable[str], seed: Iterable[str]):
        self.name = name
        self.seed = list(seed)

        self.patterns = list()
        for regex in regexes:
            self.patterns.append(re.compile(regex))

    def __repr__(self):
        return f"Category({repr(self.patterns)}, {repr(self.seed)})"

    def matches(self, link: str) -> bool:
        """
        Check if the given link belongs to this category.
        """

        for pattern in self.patterns:
            if pattern.match(link) is not None:
                return True

        return False

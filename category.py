import re
from typing import Iterable

class Category:

    def __init__(self, name: str, regexes: Iterable[str], seed: Iterable[str]):
        self.name = name
        self.seed = list(seed)

        self.patterns = list()
        for regex in regexes:
            self.patterns.append(re.compile(regex))

    def __repr__(self):
        return f"Category({repr(self.patterns)}, {repr(self.seed)})"

    def matches(self, link: str) -> bool:
        for pattern in self.patterns:
            if pattern.match(link) is not None:
                return True
        return False

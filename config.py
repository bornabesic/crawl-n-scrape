"""
Crawl 'n' Scrape configuration module.
"""

import importlib
import os.path
from configparser import ConfigParser

from category import Category

# INI configuration file definition
_INI_FILENAME = "config.ini"

_SECTION_DEFAULT = "default"

_KEY_BASE_URL = "base_url"
_KEY_REGEX = "regex"
_KEY_SEED = "seed"

# Scraper module
_SCRAPER_MODULE_NAME = "scraper" # .py

_REQUIRED_METHODS = [
    "scrape"
]

class Config:
    """
    Class containing the configuration for crawling
    the web and scraping the content.
    """

    def __init__(self, directory):
        self.directory = directory.rstrip("/")

        # Check if the given directory exists
        if not os.path.exists(self.directory):
            raise FileNotFoundError("The specified directory does not exist.")

        # Read the INI configuration file
        cfg_parser = ConfigParser()
        cfg_parser.read(os.path.join(self.directory, _INI_FILENAME))

        if _SECTION_DEFAULT not in cfg_parser:
            raise RuntimeError("Default section not present in the INI file.")

        if _KEY_BASE_URL not in cfg_parser[_SECTION_DEFAULT]:
            raise RuntimeError("Base URL not present in the default section.")

        # Base URL
        self.base_url = cfg_parser[_SECTION_DEFAULT][_KEY_BASE_URL]

        # Categories
        category_names = cfg_parser.sections()
        category_names.remove(_SECTION_DEFAULT)

        self.categories = list()
        for category_name in category_names:
            has_regex = _KEY_REGEX in cfg_parser[category_name]
            has_seed = _KEY_SEED in cfg_parser[category_name]
            if not has_regex or not has_seed:
                raise RuntimeWarning(f"Category '{category_name}' is missing a regex or a seed.'")
            else:
                regexes = filter(None, cfg_parser[category_name][_KEY_REGEX].split("\n"))
                seed = filter(None, cfg_parser[category_name][_KEY_SEED].split("\n"))
                self.categories.append(Category(category_name, regexes, seed))

        # Read the parser module
        self.scraper = importlib.import_module(f"{self.directory}.{_SCRAPER_MODULE_NAME}")

        for method_name in _REQUIRED_METHODS:
            method_available = hasattr(self.scraper, method_name)
            if not method_available:
                raise RuntimeError("Scraper module does not contain all the required methods.")

    def __repr__(self):
        return f"Config({repr(self.directory)})"

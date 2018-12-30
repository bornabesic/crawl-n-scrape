"""
Crawl 'n' Scrape linker module.
"""

import os.path
import pickle
from typing import Iterable
from config import Config

import msg
import url

_STATE_FILENAME = "links.pkl"

class Linker:
    """
    Iterable class that handles links during the crawling.
    """

    def __init__(self, config: Config):
        self.config = config
        self.visited = set()
        self.to_be_visited = set()

        self.state_file_path = os.path.join(config.directory, _STATE_FILENAME)

        if os.path.exists(self.state_file_path): # there is a state file
            with open(self.state_file_path, "rb") as state_file:
                self.visited, self.to_be_visited = pickle.load(state_file)
                msg.info(f"Read state (visited: {len(self.visited)}, to be visited: {len(self.to_be_visited)})")
        else:
            msg.info("Initializing...")

            initial_set = set(["/"])
            for category in config.categories:
                initial_set.update(category.seed)

            # TODO: Add links from the sitemap
            # for sitemap_url in url.filter_valid_links(sitemap_urls, categories, base_url):
            # 	to_be_visited.add(sitemap_url)

            for link in initial_set:
                page_content, page_links = url.content_and_links(config.base_url + link)

                if page_content is None:
                    msg.warning(f"Unable to reach {link} (no internet connection?)")
                    continue

                self.add_links(page_links)

    def __iter__(self):
        return self

    def __next__(self):
        if self.empty():
            raise StopIteration

        link, category = self.to_be_visited.pop()
        self.visited.add(link)
        return link, category

    def _ensure_relative_link(self, link: str) -> str:
        return link.replace(self.config.base_url, "")

    def empty(self) -> bool:
        """
        Check if there are links left to be visited.
        """

        return not self.to_be_visited

    def add_links(self, links: Iterable[str]) -> None:
        """
        Call add_link() for each link from the given list of
        links.
        """

        for link in links:
            self.add_link(link)

    def add_link(self, link: str) -> None:
        """
        Add the given link to the links that will be visited,
        if the link matches any of the categories in the
        configuration.
        """

        relative_link = self._ensure_relative_link(link)

        # Check if the link matches any of the categories
        for category in self.config.categories:
            if category.matches(relative_link) and relative_link not in self.visited:
                self.to_be_visited.add((relative_link, category))
                break

    def save_state(self):
        """
        Save the visited links and the links that will be
        visited into a file.
        """

        # msg.info("Saving the state...")

        state = (self.visited, self.to_be_visited)
        with open(self.state_file_path, "wb") as state_file:
            pickle.dump(state, state_file)

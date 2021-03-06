import unittest
from urllib.error import URLError

from .context import url

_INTERNET_AVAILABLE = bool(url.get("https://google.com"))

class TestsURL(unittest.TestCase):

	def test_get(self):

		if _INTERNET_AVAILABLE:
			self.assertIsNotNone(url.get("https://www.kaggle.com/"))

		self.assertIsNone(url.get("http://fail"))
		self.assertIsNone(url.get("not even a url"))

	def test_content_and_links(self):

		expected_links = {
			"/~knuth/diamondsigns/style.css",
			"faq.html#asian",
			"taocp.html",
			"http://www.stanford.edu/",
			"faq.html",
			"iaq.html",
			"news.html",
			"musings.html",
			"books.html",
			"cm.html",
			"help.html",
			"diamondsigns/diam.html",
			"preprints.html",
			"vita.html",
			"organ.html",
			"fant.html",
			"graphics.html",
			"programs.html",
			"address.html",
			"news03.html#videos",
			"experiments.html",
			"http://www-cs.stanford.edu/",
			"https://validator.w3.org/check?uri=referer"
		}

		if _INTERNET_AVAILABLE:
			content, links = url.content_and_links("https://www-cs-faculty.stanford.edu/~knuth/")
			self.assertSetEqual(links, expected_links)

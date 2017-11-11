import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import unittest
import url
import robots

class TestsCNS(unittest.TestCase):
	knuth_links = {
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
		"http://validator.w3.org/check?uri=referer"
	}

	def test_ensure_relative_path(self):
		expected = "/3/library/unittest.html"
		full_url = "https://docs.python.org/3/library/unittest.html"
		base_url = "https://docs.python.org"
		self.assertEqual(expected, url.ensure_relative_path(full_url, base_url))

		expected = "/bornabesic/crawl-n-scrape"
		full_url = "https://github.com/bornabesic/crawl-n-scrape"
		base_url = "https://github.com"
		self.assertEqual(expected, url.ensure_relative_path(full_url, base_url))

	def test_links_from_html(self):
		expected_links = TestsCNS.knuth_links
		html_path = os.path.join(current_dir, "don_knuths_home_page.html")
		with open(html_path, "r", encoding = "utf-8") as f:
			html = f.read()
		self.assertEqual(url.links_from_html(html), expected_links)

	def test_filter_valid_links(self):
		links = TestsCNS.knuth_links
		categories = [{"regex": ".*\.html$"}]  # links that end with .html
		base_url = "http://www-cs-faculty.stanford.edu/~knuth/"
		valid_links = url.filter_valid_links(links, categories, base_url)
		expected_links = {
			"preprints.html",
			"vita.html",
			"organ.html",
			"fant.html",
			"graphics.html",
			"programs.html",
			"address.html",
			"experiments.html",
			"taocp.html",
			"faq.html",
			"iaq.html",
			"news.html",
			"musings.html",
			"books.html",
			"cm.html",
			"help.html",
			"diamondsigns/diam.html"
		}
		self.assertEqual(expected_links, valid_links)

		categories = [{"regex": ".*"}]  # all links
		valid_links = url.filter_valid_links(links, categories, base_url)
		self.assertEqual(links, valid_links)

	def test_parse_robots_txt(self):
		expected_dict = {
			"disallow":
			[
				"/users/.*",
				"/accounts/.*",
				"/forms/.*",
				"/facebook/.*",
				"/ankete/.*",
				"/ankete-rezultat/.*",
				"/pretraga/.*",
				"/analytics/.*",
				"/poruke/.*"
			],
			"crawl-delay": None,
			"sitemaps": list()
		}
		robots_path = os.path.join(current_dir, "vecernji_robots.txt")
		with open(robots_path, "r", encoding = "utf-8") as f:
			robots_txt = f.read()

		self.assertEqual(expected_dict, robots.parse_robots_txt(robots_txt))


if __name__ == '__main__':
	unittest.main()

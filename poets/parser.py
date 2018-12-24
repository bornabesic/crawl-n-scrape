from html.parser import HTMLParser
import re

class WebpageParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.reset_all_variables()

	def handle_starttag(self, tag, attrs):
		if tag=="div" and ("style", "padding-left:14px;padding-top:20px;font-family:Arial;font-size:13px;") in attrs:
			self.stack+=1
		elif tag=="br" and self.stack>=1:
			self.article+="\n"

	def handle_endtag(self, tag):
		if tag=="div" and self.stack>=1:
			self.stack-=1

	def handle_data(self, data):
		if self.stack>=1:
			self.article+=data

	def reset_all_variables(self):
		self.stack=0
		self.article=""

	def retrieve_data(self):
		text = str(self.article)
		final_text = re.sub(' +',' ', text).strip().strip("\n")
		return final_text

	def name_and_category_from_link(self, link):
		tokens = link.split("/")
		name = tokens[-1]
		category = tokens[2]

		return name, category

_webpage_parser = WebpageParser()


""" REQUIRED METHODS """

def parse(link: str, html: str) -> (str, str):
	"""
	Returns the file name and the extracted data from
	the given link and HTML content.
	"""
	_webpage_parser.feed(html)
	data = _webpage_parser.retrieve_data()
	_webpage_parser.reset_all_variables()
	name, category = _webpage_parser.name_and_category_from_link(link)
	return name, data

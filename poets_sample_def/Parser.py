from html.parser import HTMLParser
import re

class Parser(HTMLParser):

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
		# /poets/william_shakespeare/poems/1320
		tokens = link.split("/")
		name = tokens[-1]
		category = tokens[2]

		return name, category

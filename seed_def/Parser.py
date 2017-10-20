from html.parser import HTMLParser

class Parser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.reset_all_variables()

	def handle_starttag(self, tag, attrs):
		# TODO handle start tag from html
		pass

	def handle_endtag(self, tag):
		# TODO handle end tag from html
		pass

	def handle_data(self, data):
		# TODO handle data from html
		pass

	def reset_all_variables(self):
		# TODO variables initialization
		# e.g. self.article="", used to accumulate text
		pass

	def retrieve_data(self):
		# used to retreive scraped data from web page
		# called just after 'feed' method

		# TODO data processing if necessary

		return None

	def name_and_category_from_link(self, link):
		# TODO return category from link

		name = None
		category = None
		return name, category

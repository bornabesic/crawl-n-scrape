#!/usr/bin/python3

import url
import robots
import os
import os.path
import time
import argparse
import json
import sys
import pickle
import gzip
import platform
import msg

args_parser = argparse.ArgumentParser(
	formatter_class = argparse.ArgumentDefaultsHelpFormatter
)

args_parser.add_argument(
	"definition_dir",
	type = str,
	help = "Name of the directory containing def.json and Parser.py"
)

args_parser.add_argument(
	"--sitemap",
	action = "store_true",
	default = False,
	help = "Extract links by parsing the sitemap"
)

args_parser.add_argument(
	"--time_delay",
	type = float,
	default = 3,
	help = "Time delay (in seconds) between each web page access"
)

args_parser.add_argument(
	"--file_format",
	type = str,
	default = "txt",
	help = "Scraped data file format"
)

args = args_parser.parse_args()
args.definition_dir = args.definition_dir.rstrip("/")
if not os.path.exists(args.definition_dir):
	msg.error("The specified definition directory does not exist.")
	sys.exit(1)

required_methods = ["parse", "name_and_category_from_link"]
parser = __import__("{}.parser".format(args.definition_dir), fromlist = required_methods)

all_methods_available = True
for method_name in required_methods:
    method_available = hasattr(parser, method_name)
    if not method_available:
        msg.error("Method '{}' is missing from the parser.py".format(method_name))
        all_methods_available = False

if not all_methods_available: sys.exit(1)

with open(os.path.join(args.definition_dir, "def.json"), "r", encoding = "utf-8") as def_file:
    definition = json.load(def_file)

base_url = definition["base_url"].rstrip("/")
categories = definition["categories"]

# --------------------- INITIALIZATION---------------------

system = platform.system()
release = platform.release()
print("Crawl 'n' Scrape - {} {}".format(system, release))

def filter_valid_links(links, categories, base_url):
	relative_links = set(map(lambda link: url.ensure_relative_path(link, base_url), links))
	filtered_links = set()

	for category in categories:
		rtype = type(category["regex"])
		if rtype is str: # single regex
			filtered_links.update(url.regex_filter(category["regex"], relative_links))
		elif rtype is list: # multiple regexes
			for regex in category["regex"]:
				filtered_links.update(url.regex_filter(regex, relative_links))

	return filtered_links

time_delay = args.time_delay
sitemap_urls = list()

# read robots.txt
rbts = robots.read_robots_txt(base_url)
if rbts:
	if rbts["crawl-delay"]:
		time_delay = max(rbts["crawl-delay"], args.time_delay)
		msg.info("robots.txt - Time delay: {} s".format(time_delay))

	if args.sitemap and len(rbts["sitemaps"]) > 0:
		for sitemap in rbts["sitemaps"]:
			msg.info("robots.txt - Sitemap: {}".format(sitemap))
			local_sitemap_urls = robots.read_sitemap(sitemap, base_url)
			if len(local_sitemap_urls)>0:
				sitemap_urls.extend(local_sitemap_urls)
				msg.info("robots.txt - Extracted {} links from the sitemap".format(len(local_sitemap_urls)))

# read visited links file
visited = set()
to_be_visited = set()

state_file_path = os.path.join(args.definition_dir, "state.cns")

if os.path.isfile(state_file_path): # there is a state file
	with gzip.open(state_file_path, "rb") as state_file:
		visited, to_be_visited = pickle.load(state_file)
		msg.info("Read state (visited: {}, to be visited: {})".format(len(visited), len(to_be_visited)))
else:
	msg.info("Initializing...")
	initial_set = set()
	initial_set.add("/")

	# add links from the sitemap
	for sitemap_url in filter_valid_links(sitemap_urls, categories, base_url):
		to_be_visited.add(sitemap_url)

	# prepare categories
	for category in categories:
		try:
			os.mkdir(os.path.join(args.definition_dir, category["name"]))
		except FileExistsError:
			pass

		initial_set.update(category["seed"])

	for link in initial_set:
		page_content, page_links = url.gather_links(base_url+link)
		if page_content is None:
			msg.warning("Unable to reach {} (no internet connection?)".format(link))
			continue
		valid_links = filter_valid_links(page_links, categories, base_url)
		to_be_visited.update(valid_links)

	del initial_set

# --------------------- CRAWL AND SCRAPE ---------------------

category_names = set(map(lambda category: category["name"], categories))
try:
	while len(to_be_visited) > 0:
	    link = to_be_visited.pop()
	    if link in visited: continue

	    name, category = parser.name_and_category_from_link(link)
	    if category not in category_names:
	        msg.warning("Category '{}' is not specified in the def.json but 'name_and_category_from_link' returned it. Skipping...".format(category))
	        continue

	    filename = 	os.path.join(args.definition_dir, category, "{}.{}".format(name, args.file_format))

	    visited.add(link)

	    time.sleep(time_delay)

	    page_content, page_links = url.gather_links(base_url+link)
	    if page_content is None:
	        msg.warning("Unable to reach {} (no internet connection?)".format(link))
	        continue

	    msg.info("Visited {}".format(link))

	    valid_links = filter_valid_links(page_links, categories, base_url)
	    to_be_visited.update(valid_links)

	    if os.path.isfile(filename): continue # file already exists

	    data = parser.parse(page_content)
	    with open(filename, "wt", encoding = "utf-8") as f:
	        f.write(data)

	msg.info("There are no more links to be visited. Program will now exit.")
except KeyboardInterrupt: # Ctrl + C
	pass
except Exception as e:
	msg.error(str(e))

msg.info("Saving the state...")

state = (visited, to_be_visited)
with gzip.open(state_file_path, "wb") as state_file:
	pickle.dump(state, state_file)

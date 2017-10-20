#!/usr/bin/python3

import url
import robots
import os
import os.path
import random
import time
import argparse
import json

parser = argparse.ArgumentParser(
	formatter_class = argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
	"--sitemap",
	action = "store_true",
	help = "Extract links by parsing the sitemap"
)

parser.add_argument(
	"--time_delay",
	type = float,
	default = 3,
	help = "Time delay (in seconds) between each web page access"
)

parser.add_argument(
	"definition_dir",
	type = str,
	help = "Name of the directory containing def.json and Parser.py"
)

args = parser.parse_args()
args.definition_dir = args.definition_dir.rstrip("/")

module = __import__(args.definition_dir+".Parser")
Parser = getattr(module, "Parser")
parser = Parser.Parser()

with open(os.path.join(args.definition_dir, "def.json"), "r", encoding = "utf-8") as def_file:
    definition = json.load(def_file)

base_url = definition["base_url"].rstrip("/")
categories = definition["categories"]

# --------------------- INITIALIZATION---------------------

def filter_valid_links(links, categories, base_url):
	relative_links = set()
	for link in links:
		relative_links.add(url.ensure_relative_path(link, base_url))

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
		print("[robots.txt] Time delay: {} s".format(time_delay))

	if args.sitemap and len(rbts["sitemaps"]) > 0:
		for sitemap in rbts["sitemaps"]:
			print("[robots.txt] Sitemap: {}".format(sitemap))
			local_sitemap_urls = robots.read_sitemap(sitemap, base_url)
			if len(local_sitemap_urls)>0:
				sitemap_urls.extend(local_sitemap_urls)
				print("[robots.txt] Extracted {} links from the sitemap".format(len(local_sitemap_urls)))

# read visited links file
visited = set()
visited_file_path = os.path.join(args.definition_dir, "visited.txt")
if os.path.isfile(visited_file_path):
	with open(visited_file_path, "r", encoding="utf-8") as visited_file:
		visited.update([l for l in visited_file.read().split("\n") if l.strip()!=""])
		print("Read {} visited links from definition directory.".format(len(visited)))

to_be_visited = []
initial_set = set()
initial_set.add("/")

# add links from the sitemap
for sitemap_url in filter_valid_links(sitemap_urls, categories, base_url):
	if sitemap_url not in to_be_visited:
		to_be_visited.append(sitemap_url)

# prepare categories
for category in categories:
    try:
        os.mkdir(os.path.join(args.definition_dir, category["name"]))
    except FileExistsError:
        pass

    initial_set.update(category["seed"])

for link in initial_set:
    page_content, page_links = url.gather_links(base_url+link)

    valid_links = filter_valid_links(page_links, categories, base_url)

    for valid_link in valid_links:
        if valid_link not in to_be_visited:
            to_be_visited.append(valid_link)

random.shuffle(to_be_visited)

# --------------------- CRAWL AND SCRAPE ---------------------

try:
	while len(to_be_visited) > 0:
	    link = to_be_visited.pop(0)
	    name, category = parser.name_and_category_from_link(link)

	    filename = 	os.path.join(args.definition_dir, category, name+".txt")

	    if link in visited:
	        continue

	    visited.add(link)

	    page_content, page_links = url.gather_links(base_url+link)

	    valid_links = filter_valid_links(page_links, categories, base_url)

	    for valid_link in valid_links:
	        if not valid_link in to_be_visited:
	            to_be_visited.append(valid_link)

	    time.sleep(time_delay)

	    if os.path.isfile(filename):
	        continue

	    if page_content:
	        data = url.extract_data(page_content, parser)

	        with open(filename, "wt", encoding = "utf-8") as f:
	            print(link)
	            f.write(data)
except KeyboardInterrupt:
	pass

print("Saving visited links...")
with open(visited_file_path, "w", encoding = "utf-8") as visited_file:
	for visited_link in visited:
		print(visited_link, file = visited_file)

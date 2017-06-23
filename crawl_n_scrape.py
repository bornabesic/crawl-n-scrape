#!/usr/bin/python3

import url
from LinkGatherer import LinkGatherer
import os
import os.path
import random
import time
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument(
	"definition_dir",
	type=str,
	help="Name of directory containing def.json and Parser.py"
)

parser.add_argument(
	"time_delay",
	type=float,
	help="Time delay (in seconds) between each web page access"
)

# TODO implement: read robots.txt

args = parser.parse_args()
args.definition_dir=args.definition_dir.strip("/")

module = __import__(args.definition_dir+".Parser")
Parser = getattr(module, "Parser")
parser = Parser.Parser()


with open(os.path.join(args.definition_dir, "def.json"), "r", encoding="utf-8") as def_file:
    definition = json.load(def_file)


base_url = definition["base_url"]
categories = definition["categories"]

# --------------------- INITIALIZATION---------------------

visited=set()
visited_file_path = os.path.join(args.definition_dir, "visited.txt")
if os.path.isfile(visited_file_path):
	with open(visited_file_path, "r", encoding="utf-8") as visited_file:
		visited.update([l for l in visited_file.read().split("\n") if l.strip()!=""])
		print("Read {} visited links from definition directory.".format(len(visited)))

to_be_visited = []
initial_set=set()
initial_set.add("/")

for category in categories:
    try:
        os.mkdir(os.path.join(args.definition_dir, category["name"]))
    except FileExistsError:
        pass

    initial_set.update(category["seed"])
gatherer = LinkGatherer()

for link in initial_set:
    page_content, page_links = gatherer.gather(base_url+link)

    new_links = set()
    for new_link in page_links:
        relative_link = url.ensure_relative_path(new_link, base_url)
        new_links.add(relative_link)

    new_links_filtered=set()
    for category in categories:
        rtype = type(category["regex"])
        if rtype is str: # single regex
        	new_links_filtered.update(url.regex_filter(category["regex"], new_links))
        elif rtype is list: # multiple regexes
            for regex in category["regex"]:
                new_links_filtered.update(url.regex_filter(regex, new_links))

    for valid_link in new_links_filtered:
        if valid_link not in to_be_visited:
            to_be_visited.append(valid_link)

random.shuffle(to_be_visited)

# --------------------- CRAWL AND SCRAPE ---------------------

try:
	while len(to_be_visited)>0:
	    link = to_be_visited.pop(0)
	    name, category = parser.name_and_category_from_link(link)

	    filename = 	os.path.join(args.definition_dir, category, name+".txt")

	    if link in visited:
	        continue

	    visited.add(link)

	    page_content, page_links = gatherer.gather(base_url+link)

	    new_links = set()
	    for new_link in page_links:
	        relative_link = url.ensure_relative_path(new_link, base_url)
	        new_links.add(relative_link)

	    new_links_filtered=set()
	    for category in categories:
	        rtype = type(category["regex"])
	        if rtype is str: # single regex
	    	    new_links_filtered.update(url.regex_filter(category["regex"], new_links))
	        elif rtype is list: # multiple regexes
	            for regex in category["regex"]:
	                new_links_filtered.update(url.regex_filter(regex, new_links))

	    for valid_link in new_links_filtered:
	        if not valid_link in to_be_visited:
	            to_be_visited.append(valid_link)

	    time.sleep(args.time_delay)

	    if os.path.isfile(filename):
	        continue

	    if page_content:
	        data = url.extract_data(page_content, parser)

	        with open(filename, "wt", encoding="utf-8") as f:
	            print(link)
	            f.write(data)
except KeyboardInterrupt:
	pass

print("Saving visited links...")
with open(visited_file_path, "w", encoding="utf-8") as visited_file:
	for visited_link in visited:
		print(visited_link, file=visited_file)

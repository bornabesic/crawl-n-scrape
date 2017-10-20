import re
from urllib.request import urlopen
import urllib.error

def get(url):
    try:
        return urlopen(url).read().decode(encoding="utf-8", errors="ignore")
    except urllib.error.URLError:
        return None
    except UnicodeEncodeError:
        print("UNICODE ERROR: " + url)

def ensure_relative_path(link, base):
    return link.replace(base, "")

def regex_filter(regex, links):
    pattern = re.compile(regex)
    filtered=set()
    for link in links:
        if pattern.match(link)==None:
            continue
        filtered.add(link)

    return filtered

def extract_data(page, parser):
    parser.feed(page)
    data = parser.retrieve_data()
    parser.reset_all_variables()
    return data

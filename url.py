import re
from urllib.request import urlopen
import urllib.error

def get(url, timeout = 10):
    try:
        return urlopen(url, timeout = timeout).read().decode(encoding="utf-8", errors="ignore")
    except KeyboardInterrupt:
        raise
    except:
        return None

def ensure_relative_path(link, base):
    return link.replace(base, "")

def regex_filter(regex, links):
    pattern = re.compile(regex)
    filtered = set()
    for link in links:
        if pattern.match(link)==None:
            continue
        filtered.add(link)

    return filtered

_URL_PATTERN = re.compile("href=\"([^\"]*)\"")
def content_and_links(url):
    html = get(url)
    if html is None:
        links = set()
    else:
        links = links_from_html(html)
    return html, links

def links_from_html(html):
    links = _URL_PATTERN.findall(html)
    return set(links)

def filter_valid_links(links, categories, base_url):
    relative_links = set(map(lambda link: ensure_relative_path(link, base_url), links))
    filtered_links = set()

    for category in categories:
        rtype = type(category["regex"])
        if rtype is str: # single regex
            filtered_links.update(regex_filter(category["regex"], relative_links))
        elif rtype is list: # multiple regexes
            for regex in category["regex"]:
                filtered_links.update(regex_filter(regex, relative_links))

    return filtered_links

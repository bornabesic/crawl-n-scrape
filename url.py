import re
from urllib.request import urlopen

def get(url, timeout = 10):
    try:
        return urlopen(url, timeout = timeout).read().decode(encoding="utf-8", errors="ignore")
    except KeyboardInterrupt:
        raise
    except:
        return None

_URL_PATTERN = re.compile("href=\"([^\"]*)\"")
def links_from_html(html):
    links = _URL_PATTERN.findall(html)
    return set(links)

def content_and_links(url):
    html = get(url)
    if html is None:
        links = set()
    else:
        links = links_from_html(html)
    return html, links

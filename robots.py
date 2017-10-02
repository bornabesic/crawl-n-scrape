from url import get
import re

_directive_regex = re.compile(r"(.+?): (.+?)")


def read_robots_txt(base_url):
    robots = get("{}/robots.txt".format(base_url))
    if not robots: return None

    directives = robots.split("\n")

    robots_dict = {
        "disallow": list(),
        "crawl-delay": None,
        "sitemaps": list()
    }

    parse = False
    for d in directives:
        match = _directive_regex.fullmatch(d)
        if not match:
            parse = False
            continue

        dkey, dval = match.group(1).lower(), match.group(2)
        if (dkey, dval) == ("user-agent", "*"):
            parse = True
            continue
        elif dkey == "sitemap":
            robots_dict["sitemaps"].append(dval)

        if not parse: continue

        if dkey == "disallow":
            py_regex_val = dval.replace(".", "\\.").replace("*", ".*")
            if not py_regex_val.endswith("$"): py_regex_val += ".*"
            robots_dict["disallow"].append(py_regex_val)

        elif dkey == "crawl-delay": robots_dict["crawl-delay"] = dval
            
    return robots_dict

_url_entry_regex = re.compile(r"<url>.*?<loc>(.+?)</loc>.*?</url>", flags = re.DOTALL)
_sitemap_entry_regex = re.compile(r"<sitemap>.*?<loc>(.+?)</loc>.*?</sitemap>", flags = re.DOTALL)
def read_sitemap(sitemap_url, base_url = None): # if base_url is specified, the fallback is /sitemap.xml
    visited_sitemaps = set()
    sitemaps = set([sitemap_url])
    urls = set()

    while len(sitemaps)>0:
        item = sitemaps.pop()
        if item in visited_sitemaps: continue
        visited_sitemaps.add(item)

        sitemap = get(item)
        if not sitemap: continue

        local_urls = _url_entry_regex.findall(sitemap)
        local_sitemaps = _sitemap_entry_regex.findall(sitemap)

        urls.update(local_urls)
        sitemaps.update(local_sitemaps)

    if len(urls) == 0 and base_url:
        sitemap_url = "{}/sitemap.xml".format(base_url)
        print("Fallback: trying {}".format(sitemap_url))
        urls = read_sitemap(sitemap_url)

    return urls





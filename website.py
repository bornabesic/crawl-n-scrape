import re

import msg
from url import get

_DIRECTIVE_REGEX = re.compile(r"(.+?): (.+?)")
_URL_ENTRY_REGEX = re.compile(
    r"<url>.*?<loc>(.+?)</loc>.*?</url>",
    flags=re.DOTALL
)
_SITEMAP_ENTRY_REGEX = re.compile(
    r"<sitemap>.*?<loc>(.+?)</loc>.*?</sitemap>",
    flags=re.DOTALL
)

class Website:

    def __init__(self, base_url, time_delay=0, use_sitemap=False):
        self.base_url = base_url.rstrip("/")
        self.time_delay = time_delay
        self.sitemap_urls = list()

        # Read robots.txt
        robots_txt = Website.read_robots_txt(self.base_url)
        robots = Website.parse_robots_txt(robots_txt)
        if robots:
            if robots["crawl-delay"]:
                self.time_delay = max(robots["crawl-delay"], self.time_delay)
                msg.info(f"robots.txt - Time delay: {self.time_delay} s")

            # Read sitemap
            if use_sitemap and robots["sitemaps"]:
                for sitemap in robots["sitemaps"]:
                    msg.info(f"robots.txt - Sitemap: {sitemap}")
                    local_sitemap_urls = Website.read_sitemap(sitemap, base_url)
                    if local_sitemap_urls:
                        self.sitemap_urls.extend(local_sitemap_urls)
                        msg.info(f"robots.txt - Extracted {len(local_sitemap_urls)} links from the sitemap")

    @staticmethod
    def read_robots_txt(base_url):
        robots_txt = get(f"{base_url}/robots.txt")
        return robots_txt

    @staticmethod
    def parse_robots_txt(robots_txt):
        directives = robots_txt.split("\n")

        robots_dict = {
            "disallow": list(),
            "crawl-delay": None,
            "sitemaps": list()
        }

        parse = False
        for d in directives:
            match = _DIRECTIVE_REGEX.fullmatch(d)
            if not match:
                parse = False
                continue

            dkey, dval = match.group(1).lower(), match.group(2)
            if (dkey, dval) == ("user-agent", "*"):
                parse = True
                continue
            elif dkey == "sitemap":
                robots_dict["sitemaps"].append(dval)

            if not parse:
                continue

            if dkey == "disallow":
                py_regex_val = dval.replace(".", "\\.").replace("*", ".*")
                if not py_regex_val.endswith("$"):
                    py_regex_val += ".*"
                robots_dict["disallow"].append(py_regex_val)

            elif dkey == "crawl-delay":
                try:
                    robots_dict["crawl-delay"] = int(dval)
                except ValueError:
                    pass
                
        return robots_dict

    @staticmethod
    def read_sitemap(sitemap_url, base_url=None): # if base_url is specified, the fallback is /sitemap.xml
        visited_sitemaps = set()
        sitemaps = set([sitemap_url])
        urls = set()

        while sitemaps:
            item = sitemaps.pop()
            if item in visited_sitemaps:
                continue

            visited_sitemaps.add(item)

            sitemap = get(item)
            if not sitemap:
                continue

            local_urls = _URL_ENTRY_REGEX.findall(sitemap)
            local_sitemaps = _SITEMAP_ENTRY_REGEX.findall(sitemap)

            urls.update(local_urls)
            sitemaps.update(local_sitemaps)

        if urls and base_url:
            sitemap_url = f"{base_url}/sitemap.xml"
            print(f"Fallback: trying {sitemap_url}")
            urls = Website.read_sitemap(sitemap_url)

        return urls

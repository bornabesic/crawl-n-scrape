import url
import re

class LinkGatherer:

    url_pattern = re.compile("href=\"([^\"]*)\"")

    def gather(self, web_url):
        web_page = url.get(web_url)
        if web_page==None:
            return None, set()

        links = LinkGatherer.url_pattern.findall(web_page)
        return web_page, set(links)

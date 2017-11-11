# Crawl 'n' Scrape
[![Build Status](https://travis-ci.org/bornabesic/crawl-n-scrape.svg?branch=travis-ci)](https://travis-ci.org/bornabesic/crawl-n-scrape)
```
usage: crawl_n_scrape.py [-h] [--sitemap] [--time_delay TIME_DELAY]
                         [--file_format FILE_FORMAT]
                         definition_dir

positional arguments:
  definition_dir        Name of the directory containing def.json and
                        parser.py

optional arguments:
  -h, --help            show this help message and exit
  --sitemap             Extract links by parsing the sitemap (default: False)
  --time_delay TIME_DELAY
                        Time delay (in seconds) between each web page access
                        (default: 3)
  --file_format FILE_FORMAT
                        Scraped data file format (default: txt)
  ```

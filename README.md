# Crawl 'n' Scrape
[![Build Status](https://travis-ci.org/bornabesic/crawl-n-scrape.svg?branch=travis-ci)](https://travis-ci.org/bornabesic/crawl-n-scrape)

## Python

Version required: >= __3.6__

## Features
- No dependencies! (only [The Python Standard Library](https://docs.python.org/3.6/library/index.html))
- Regex-based web crawling
- User-written scraping code
- Scraped data divided into categories

## Usage

```
crawl_n_scrape.py [-h] [--sitemap] [--time_delay TIME_DELAY]
                         [--file_format FILE_FORMAT]
                         definition_dir

positional arguments:
  definition_dir        Name of the directory containing config.ini and
                        scraper.py

optional arguments:
  -h, --help            show this help message and exit
  --sitemap             Extract links by parsing the sitemap (default: False)
  --time_delay TIME_DELAY
                        Time delay (in seconds) between each web page access
                        (default: 3)
  --file_format FILE_FORMAT
                        Scraped data file format (default: txt)
  ```

## TODO

- Measure the elapsed time
- Add a list field to the definition, containing regexes of URLs from which only the links (no content) should be extracted
- Fix colorized text in terminal on Windows
- Add Wiki
- Write more unit tests

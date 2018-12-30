import argparse
import os
import os.path
import platform
import sys
import time
import traceback

import msg
import url
from config import Config
from linker import Linker
from website import Website


def parse_cli_args():

    args_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    args_parser.add_argument(
        "definition_dir",
        type=str,
        help="Name of the directory containing config.ini and scraper.py"
    )

    args_parser.add_argument(
        "--sitemap",
        action="store_true",
        default=False,
        help="Extract links by parsing the sitemap"
    )

    args_parser.add_argument(
        "--time_delay",
        type=float,
        default=3,
        help="Time delay (in seconds) between each web page access"
    )

    args_parser.add_argument(
        "--file_format",
        type=str,
        default="txt",
        help="Scraped data file format"
    )

    return args_parser.parse_args()

def main():

    # Info
    system = platform.system()
    release = platform.release()
    print("Crawl 'n' Scrape - {} {}".format(system, release))

    # Parse the CLI arguments
    args = parse_cli_args()

    # Read the configuration
    try:
        config = Config(args.definition_dir)
    except Exception as error:
        msg.error(traceback.format_exc())
        sys.exit(1)

    # --------------------- INITIALIZATION ---------------------
    # Create a directory for each category
    for category in config.categories:
        os.makedirs(os.path.join(config.directory, category.name), exist_ok=True)

    # Read robots.txt and sitemap
    website = Website(config.base_url, args.time_delay, args.sitemap)

    # Linker
    linker = Linker(config)

    # --------------------- CRAWL AND SCRAPE ---------------------
    try:
        for link, category in linker:
            # Obey the time delay
            time.sleep(website.time_delay)

            # Retrieve the content from the web
            content, links = url.content_and_links(config.base_url + link)
            if content is None:
                msg.warning(f"Unable to reach {link} (no internet connection?)")
                continue

            msg.info("Visited {}".format(link))

            # Update the linker
            linker.add_links(links)

            # Parse the content
            filename, data = config.scraper.scrape(link, content)

            # Save the file
            file_path = os.path.join(
                config.directory,
                category.name,
                f"{filename}.{args.file_format}"
            )
            if os.path.exists(file_path): # File already exists
                continue

            with open(file_path, "wt", encoding="utf-8") as f:
                f.write(data)

            # Save the linker's state
            linker.save_state()

    except KeyboardInterrupt: # Ctrl + C
        pass
    except Exception as e:
        msg.error(traceback.format_exc())

if __name__ == "__main__":
    main()

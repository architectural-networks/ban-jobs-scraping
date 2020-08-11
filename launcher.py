import sys
import json

from scraper.crawl import crawl


def scrape(event=None, context=None):
    if context is None:
        context = {}
    if event is None:
        event = {}
    crawl(**event)


if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)
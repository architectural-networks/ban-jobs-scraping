import sys
import imp
import os
import logging
from urllib.parse import urlparse

from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from crochet import setup, wait_for
setup()

# Need to "mock" sqlite for the process to not crash in AWS Lambda / Amazon Linux
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")

logging.getLogger().handlers = [] # Necessary to manage the Log Level of Scrapy in AWS Lambda


def is_in_aws():
    return os.getenv('AWS_EXECUTION_ENV') is not None

@wait_for(10)
def crawl(settings=None, spider_name="baunetz", spider_kwargs=None):
    if spider_kwargs is None:
        spider_kwargs = {}
    if settings is None:
        settings = {}
    project_settings = get_project_settings()
    spider_loader = SpiderLoader(project_settings)

    spider_cls = spider_loader.load(spider_name)

    try:
        spider_key = urlparse(spider_kwargs.get("start_urls")[0]).hostname if spider_kwargs.get(
            "start_urls") else urlparse(spider_cls.start_urls[0]).hostname
    except Exception:
        logging.exception("Spider or kwargs need start_urls.")

    # proxies_filename = 'proxies.txt'
    if is_in_aws():
        # Lambda can only write to the /tmp folder.
        # settings['ROTATING_PROXY_LIST_PATH'] = "/tmp/"+proxies_filename
        settings['HTTPCACHE_DIR'] = "/tmp/httpcache"

    # else:
    #     settings['ROTATING_PROXY_LIST_PATH'] = data_path(proxies_filename)
    #     feed_uri = "file://{}/%(name)s-{}-%(time)s.json".format(
    #         os.path.join(os.getcwd(), "feed"),
    #         spider_key,
    #     )

    # process = CrawlerProcess({**project_settings, **settings})
    # process.crawl(spider_cls, **spider_kwargs)
    # process.start()

    crawler = CrawlerRunner({**project_settings, **settings})
    d = crawler.crawl(spider_cls, **spider_kwargs)
    return d
    # d.addCallback(lambda _: reactor.stop())
    # reactor.run()

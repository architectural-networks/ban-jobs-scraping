import scrapy
from datetime import datetime
from scrapy.shell import inspect_response
from scraper.items import JobsItem
from scraper.models import Session, Job
from dotenv import load_dotenv
from scraper.utils import get_scraped_ids

load_dotenv()
import logging

logging.basicConfig(level=logging.DEBUG)

class BaunetzSpider(scrapy.Spider):
    name = 'baunetz'
    allowed_domains = ['baunetz.de']
    start_urls = ['https://www.baunetz.de/stellenmarkt/index.html?s_text=&s_ort=Berlin']

    def parse(self, response):
        # debug
        # inspect_response(response, self)
        existingIds = get_scraped_ids('baunetz')
        jobsList = response.css('div.jobs-liste-eintrag')
        for job in jobsList:
            job_id = job.css('div.job-nr::text').get().replace('#', '')
            if job_id in existingIds:
                continue
            date = datetime.fromtimestamp(int(job.css('p.jobs-liste-eintrag-datum::attr(data-timestamp)').get()))
            title = job.css('p.jobs-liste-eintrag-titel::text').get()
            subtitle = job.css('div.jobs-liste-eintrag-tag::text').get()
            company = job.css('p.jobs-liste-eintrag-untertitel::text').get()
            url = job.css('div.jobs-liste-eintrag-info a::attr(href)').get().split('?')[0]

            item = JobsItem(
                site="baunetz",
                date=date,
                url=url,
                title=title,
                subtitle=subtitle,
                company=company,
                job_id=job_id,

            )
            yield item
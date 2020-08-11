import scrapy
from scrapy.shell import inspect_response
from scraper.items import JobsItem
from scraper.utils import get_scraped_ids
from datetime import datetime


class GermanarchitectsSpider(scrapy.Spider):
    name = 'germanarchitects'
    allowed_domains = ['german-architects.com']
    start_urls = ['https://www.german-architects.com/de/stellenanzeigen?country_id=9&preserve=1']

    def parse(self, response):
        # debug
        # inspect_response(response, self)
        existing_ids = get_scraped_ids(self.name)
        jobs = response.css('ul.list-unstyled > li')
        for job in jobs:
            city = job.xpath('.//address/text()').get()
            job_id = job.xpath('.//dt/a/@href').get()
            if (city is None) or ('Berlin' not in city) or (job_id in existing_ids):
                continue

            date_str = job.xpath('.//time/@datetime').get()
            date = datetime.strptime(date_str, '%d.%m.%y, %H:%M')

            title = job.xpath('.//dt/a/text()').get()
            company = job.xpath('.//dd/a/text()').get()
            url = 'https://www.german-architects.com' + job_id

            subtitle = ""
            item = JobsItem(
                site=self.name,
                date=date,
                url=url,
                title=title,
                subtitle=subtitle,
                company=company,
                job_id=job_id,

            )
            yield item

        pass

import scrapy
from scrapy.shell import inspect_response
from scraper.items import JobsItem
from scraper.utils import get_scraped_ids
from datetime import datetime

class DezeenSpider(scrapy.Spider):
    name = 'dezeen'
    allowed_domains = ['dezeenjobs.com']
    start_urls = ['https://www.dezeenjobs.com/location/berlin/']

    def parse(self, response):
        # debug
        # inspect_response(response, self)
        existing_ids = get_scraped_ids('dezeen')
        jobs = response.css(".job_listing")

        for job in jobs:
            url = job.css("a::attr(href)").get()

            job_id = url.split('/')[-2].split("-")[-1]
            if job_id in existing_ids:
                continue

            date_str = job.xpath(".//time/text()").get()
            date = datetime. strptime(date_str, '%d %B %Y')
            title = job.xpath('.//h1/a[1]/text()').get().strip()
            company = job.xpath('.//h1/a[2]/text()').get().replace('at', '').strip()
            subtitle = job.css('section.job-list-blurb > p::text').get().strip()

            image_url = job.css('img.company_logo::attr(src)').get()

            item = JobsItem(
                site="dezeen",
                date=date,
                url=url,
                title=title,
                subtitle=subtitle,
                company=company,
                job_id=job_id,
                image_url=image_url
            )
            yield item

        pass


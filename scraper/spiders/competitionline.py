import scrapy
from scrapy.shell import inspect_response
from scraper.items import JobsItem
from dotenv import load_dotenv
from scraper.utils import get_scraped_ids
import json

load_dotenv()
import logging

logging.basicConfig(level=logging.DEBUG)


class CompetitionlineSpider(scrapy.Spider):
    name = 'competitionline'
    allowed_domains = ['competitionline.com']
    start_urls = ['https://www.competitionline.com/api/jobs?ra=20&co=Deutschland&ci=Berlin&lat=52.51605&lon=13.37691']

    def parse(self, response):
        # debug
        # inspect_response(response, self)
        json_response = json.loads(response.body)
        jobs = json_response['hits']
        existingIds = get_scraped_ids('competitionline')

        for job in jobs:
            job_id = str(job['id'])
            if (job_id in existingIds) or (job['city'] != 'Berlin'):
                continue

            date = job['publication_date']
            title = job['title']
            subtitle = ""
            company = job['company_name']
            url = 'https://www.competitionline.com/de/jobs/' + job_id
            image_url = None
            if 'company_image' in job:
                image_url = "https://competitionline-images.imgix.net/" + job['company_image']

            item = JobsItem(
                site=self.name,
                date=date,
                url=url,
                title=title,
                subtitle=subtitle,
                company=company,
                job_id=job_id,
                image_url=image_url
            )
            yield item

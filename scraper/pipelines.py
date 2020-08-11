# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from datetime import datetime
import os
from scraper.models import Session, Job, ScrapingSession
from dotenv import load_dotenv
from slack import WebClient
from slack.errors import SlackApiError

load_dotenv()
import logging

logging.basicConfig(level=logging.DEBUG)






class JobPipeline(object):
    def open_spider(self, spider):
        slack_token = os.environ["SLACK_API_TOKEN"]
        self.client = WebClient(token=slack_token)
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):

        item['slack'] = self.send_slack_message(item)

        job = Job(**item)
        self.session.add(job)
        self.session.commit()
        return item

    def send_slack_message(self, item):
        # prepare message
        text = item['title'] + '\n@ ' + item['company'] + '\n' + ':point_right: ' + item['url']
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            },
            {
                "type": "divider"
            }
        ]

        try:
            response = self.client.chat_postMessage(
                channel="testing",
                blocks=blocks,
                # icon_url='https://res.cloudinary.com/architecturalnetworks/image/upload/c_scale,w_200/v1596867074/ban/slack_jobs_bot_image_wmohy3.png'
            )
            return True
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response[
                "error"]  # str like 'invalid_auth', 'channel_not_found'
            return False
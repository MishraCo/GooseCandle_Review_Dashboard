# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import os
import logging

class BbwcandlesScrapePipeline:
    pass
    '''
    def process_item(self, item, spider):
        return item
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter

from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.files import GCSFilesStore
import json
from google.cloud import storage
from scrapy import signals

class GCSFilesStoreJSON:
    def __init__(self, uri=None):
        if uri is None:
            uri = 'gs://sephorascrapping/GoosecreekCandles'
        #credentials_file = r'E:\Documents\GitHub_Repositories\Sephora\luminous-figure-419717-17cf4bd05e09.json'
        credentials_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
        
        with open(credentials_file, 'r') as file:
            credentials_dict = json.load(file)
            self.client = storage.Client.from_service_account_info(credentials_dict)
        
        self.bucket_name, _ = uri[5:].split('/', 1)
        self.bucket = self.client.get_bucket('sephorascrapping')
       
    def upload_to_bucket(self, blob_name, file_path):
        try:
            blob = self.bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
            print(f"File {file_path} uploaded to {blob_name} in bucket {self.bucket_name}.")
            return True
        except Exception as e:
            print(e)
            return False


class GCSFilePipeline:
    def __init__(self, local_file_path):
        self.local_file_path = local_file_path

    @classmethod
    def from_crawler(cls, crawler):
        # Access the FEED_URI from the spider's settings
        logging.info(f"FEED_URI set to: {crawler.settings.get('FEED_URI')}")
        local_file_path = crawler.settings.get('FEED_URI')
        pipeline = cls(local_file_path)
        #logging.info(f"FEED_URI set to: {crawler.settings.get('FEED_URI')}")
        crawler.signals.connect(pipeline.close_spider, signal=signals.spider_closed)
        return pipeline

    def close_spider(self, spider):
        if self.local_file_path:
            # The bucket URI is specified here, and you might want to configure it too
            store = GCSFilesStoreJSON('gs://sephorascrapping/')
            blob_name = f"GoosecreekCandles/{os.path.basename(self.local_file_path)}"
            success = store.upload_to_bucket(blob_name=blob_name, file_path=self.local_file_path)
            if success:
                spider.logger.info(f"Successfully uploaded {self.local_file_path} to GCS.")
            else:
                spider.logger.error(f"Failed to upload {self.local_file_path} to GCS.")
        else:
            spider.logger.error("No local file path found for uploading to GCS.")
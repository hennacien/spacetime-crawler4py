from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.unique_urls = set() # added this, will store the unique URLs for answering the questions
        self.largest_page = "" # set to page with most amount of words
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        count = 0 # total links
        while True:
            tbd_url = self.frontier.get_tbd_url()
            
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                print(f"SCRAPED URL: {scraped_url}")
                self.frontier.add_url(scraped_url)
                count += 1
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
        print(f'TOTAL LINKS {len(self.frontier.unique_urls)}')

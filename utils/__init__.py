import os
import logging
from hashlib import sha256
from urllib.parse import urlparse

def get_logger(name, filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    fh = logging.FileHandler(f"Logs/{filename if filename else name}.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
       "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def get_urlhash(url):
    parsed = urlparse(url)
    # everything other than scheme.
    return f"{parsed.netloc}/{parsed.path}/{parsed.params}/{parsed.query}/{parsed.fragment}"

def get_url_no_fragment(url): # added this so we can find the unique URLs without fragment
    parsed = urlparse(url)
    # everything other than fragment.
    return  f"{parsed.scheme}://{parsed.netloc}/{parsed.path}/{parsed.params}/{parsed.query}"

def normalize(url):
    if url.endswith("/"):
        return url.rstrip("/")
    return url

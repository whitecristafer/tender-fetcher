import logging
from logging.handlers import RotatingFileHandler

def setup_logging(logfile="tender_fetcher.log"):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    fh = RotatingFileHandler(logfile, maxBytes=1000000, backupCount=3)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
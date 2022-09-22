import json
import logging
import os
import time
from utilities import logger
from datetime import datetime

# logLevel = os.getenv("logLevel", "INFO")
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# chformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(chformatter)
# logger = logging.getLogger()
# logger.setLevel(getattr(logging, logLevel))
# logger.addHandler(ch)


class Utils(object):
    def __init__(self, **kwargs):
        # self.AWS = AWS(**kwargs)
        self.logger = logger
        pass

    def get_ts(self):
        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        return st
